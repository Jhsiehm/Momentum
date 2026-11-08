"""Hierarchy and exact-source tests; no semantic or quality-set evaluation."""
import copy
import unittest

from scripts.mechanism_design_extractor import extract as v1
from scripts.mechanism_design_extractor_v2 import extract
from tests.test_mechanism_design_extractor import view, clause


def hit_context(result, quote, occurrence=0):
    hits = [h for c in result['candidates'] for h in c['hits'] if h['quote'] == quote]
    # The same trigger can occur in multiple mechanisms. Group by location.
    locations = sorted({h['start'] for h in hits})
    hit = next(h for h in hits if h['start'] == locations[occurrence])
    pool = {s['span_id']: s for s in result['structural_spans']}
    return hit, [(r, pool[r['span_id']]) for r in hit['structural_context']]


class StructuralExtractorTests(unittest.TestCase):
    def test_malformed_paths_fail_before_frozen_v1_ancestor_walk(self):
        for path in ('section[1]', '', '/', '//section[1]', '/section[1]/',
                     '/section', '/section[0]', '/section[1]/text'):
            source = view(clause('Submit a report.'))
            source['spans'][0]['path'] = path
            with self.assertRaisesRegex(ValueError, 'hierarchy path'):
                extract(source)

    def test_v1_unchanged_and_additive_output(self):
        source = view(clause('There are appropriated $100 for the program.') + clause('No person may submit a report.'))
        original = copy.deepcopy(source)
        expected = v1(source)
        result = extract(source)
        self.assertEqual(source, original)
        self.assertEqual(v1(source), expected)
        self.assertEqual(result, extract(source))
        stripped = copy.deepcopy(result)
        for c in stripped['candidates']:
            for h in c['hits']:
                for key in ('structural_context', 'structural_boundaries', 'structural_context_status', 'semantic_governance_verified'):
                    h.pop(key)
        for key in ('base_extractor_version', 'structural_context_schema', 'structural_spans', 'structural_context_interpretation'):
            stripped.pop(key)
        stripped['schema'] = expected['schema']
        stripped['extractor_version'] = expected['extractor_version']
        self.assertEqual(stripped, expected)
        self.assertTrue(all(a['status'] == 'abstain' for a in result['assessments'].values()))

    def test_parent_negation_retained_without_sibling_or_following_scope(self):
        source = view('<section><header>Conditions</header><text>Nothing in this Act requires—</text>'
                      '<paragraph><text>Establish a program.</text></paragraph>'
                      '<paragraph><header>Communication</header><text>Submit a report.</text></paragraph>'
                      '<text>Except when the Secretary determines otherwise.</text></section>')
        result = extract(source)
        hit, refs = hit_context(result, 'report')
        texts = [s['quote'] for _, s in refs]
        self.assertIn('Nothing in this Act requires—', texts)
        self.assertIn('Submit a report.', texts)
        self.assertIn('Conditions', texts)
        self.assertIn('Communication', texts)
        self.assertNotIn('Establish a program.', texts)
        self.assertNotIn('Except when the Secretary determines otherwise.', texts)
        self.assertFalse(hit['semantic_governance_verified'])
        candidate = next(c for c in result['candidates'] if c['mechanism'] == 'reporting')
        self.assertIn('Except when', candidate['quote'])
        self.assertEqual(result['proposals'], [])

    def test_quoted_struck_text_keeps_boundary_and_amendment_context(self):
        source = view('<section><text>Section 2 is amended by striking the following:</text>'
                      '<quoted-block><section><header>Old rule</header><text>No person may report.</text>'
                      '</section></quoted-block></section>')
        result = extract(source)
        hit, refs = hit_context(result, 'report')
        self.assertIn('Section 2 is amended by striking the following:', [s['quote'] for _, s in refs])
        self.assertEqual(len(hit['structural_boundaries']), 1)
        pool = {s['span_id']: s for s in result['structural_spans']}
        boundary = pool[hit['structural_boundaries'][0]['span_id']]
        self.assertEqual(boundary['tag'], 'quoted-block')
        self.assertIn('No person may report.', boundary['quote'])
        self.assertFalse(result['proposals'])

    def test_exact_unicode_duplicates_and_deduplicated_pool(self):
        source = view(clause('The Secretary shall submit a report about café 🌱.') * 2)
        result = extract(source)
        pool = result['structural_spans']
        self.assertEqual(len(pool), len({s['path'] for s in pool}))
        self.assertEqual(len(pool), len({s['span_id'] for s in pool}))
        for s in pool:
            self.assertEqual(s['quote'], source['text'][s['start']:s['end']])
        h1, c1 = hit_context(result, 'report', 0)
        h2, c2 = hit_context(result, 'report', 1)
        self.assertNotEqual(h1['start'], h2['start'])
        self.assertTrue(set(s['path'] for _, s in c1).isdisjoint(s['path'] for _, s in c2))
        self.assertLess(len(pool), sum(len(h['structural_context']) for c in result['candidates'] for h in c['hits']))

    def test_header_hit_does_not_gain_following_text_or_sibling_header(self):
        source = view('<section><header>Report</header><text>The Secretary shall submit data.</text>'
                      '<paragraph><header>Other</header><text>Report findings.</text></paragraph></section>')
        result = extract(source)
        hit, refs = hit_context(result, 'Report', 0)
        self.assertEqual([(r['relation'], s['quote']) for r, s in refs], [('containing_header', 'Report')])
        self.assertFalse(hit['semantic_governance_verified'])

    def test_every_ancestor_relation_has_exact_hierarchy_and_precedes_branch(self):
        source = view('<section><header>Scope</header><text>The Secretary shall—</text>'
                      '<subsection><text>Unless an exception applies—</text>'
                      '<paragraph><text>Submit a report.</text></paragraph></subsection></section>')
        result = extract(source)
        _, refs = hit_context(result, 'report')
        containing = next(s for r, s in refs if r['relation'] == 'containing_text')
        for r, s in refs:
            if r['relation'].startswith('ancestor_'):
                self.assertEqual(s['path'].rsplit('/', 1)[0], r['ancestor_path'])
                self.assertTrue(containing['path'].startswith(r['ancestor_path'] + '/'))
                self.assertLessEqual(s['end'], containing['start'])
        self.assertIn('Unless an exception applies—', [s['quote'] for _, s in refs])

    def test_renderer_omitted_intermediate_nodes_keep_true_ancestry(self):
        source = view('<section><text>The Secretary shall—</text><wrapper>'
                      '<paragraph><text>Submit a report.</text></paragraph></wrapper>'
                      '<text>Later exception.</text></section>')
        result = extract(source)
        _, refs = hit_context(result, 'report')
        self.assertIn('The Secretary shall—', [s['quote'] for _, s in refs])
        self.assertNotIn('Later exception.', [s['quote'] for _, s in refs])

    def test_hit_without_text_header_boundary_is_explicitly_unclassified(self):
        source = view('<section><table>report</table></section>')
        result = extract(source)
        hit, refs = hit_context(result, 'report')
        self.assertEqual(hit['structural_context_status'], 'container_only')
        self.assertEqual(refs, [])
        self.assertEqual(result['proposals'], [])


if __name__ == '__main__':
    unittest.main()
