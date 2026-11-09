import copy
import unittest

from engine.paper_evaluation import seal
from scripts.bill_context_design_text_v2 import render
from scripts.bill_structural_input_v1 import build
from scripts.mechanism_design_extractor_v5 import extract as baseline
from scripts.mechanism_structural_extractor_v1 import extract


class StructuralExtractorTests(unittest.TestCase):
    def fixture(self, body):
        raw = ('<bill><form><congress>113th CONGRESS</congress><legis-num>H. R. 1</legis-num>'
               '</form><legis-body><section><text>' + body + '</text></section></legis-body></bill>').encode()
        view = render(raw, '113-hr1')
        digest = seal(view)['hash']
        sidecar = build(raw, '113-hr1', view, digest)
        view['view_hash'] = digest
        return view, sidecar

    def test_cross_cell_actual_match_preserved_and_flagged(self):
        view, sidecar = self.fixture('<table><row><entry>shall </entry><entry>not</entry></row></table>')
        result = extract(view, sidecar)
        matches = [d for d in result['boundary_decisions'] if d['quote'] == 'shall not']
        self.assertTrue(matches, 'Fixture must actually produce a cross-cell lexical hit')
        self.assertTrue(all(d['decision'] == 'flag_cell_boundary' for d in matches))
        self.assertTrue(all(len(d['boundary_evidence']) == 2 for d in matches))
        self.assertEqual(result['raw_output'], baseline(view))
        self.assertEqual(result['full_context_text'], view['text'])
        self.assertEqual(len(result['usable_hits']) + result['counts']['flagged_hits'], result['counts']['raw_hits'])

    def test_same_cell_endpoint_touch_retains(self):
        view, sidecar = self.fixture('<table><row><entry>shall not</entry><entry>shall</entry></row></table>')
        result = extract(view, sidecar)
        self.assertTrue(result['boundary_decisions'])
        self.assertTrue(all(d['decision'] == 'retain' for d in result['boundary_decisions']))
        self.assertTrue(all(d['containing_cell_paths'] for d in result['boundary_decisions']))

    def test_nested_cell_boundary_is_not_masked_by_outer(self):
        view, sidecar = self.fixture('<table><row><entry>shall <table><row><entry>not</entry></row></table></entry></row></table>')
        result = extract(view, sidecar)
        match = next(d for d in result['boundary_decisions'] if d['quote'] == 'shall not')
        self.assertTrue(match['containing_cell_paths'])
        self.assertEqual(match['decision'], 'flag_cell_boundary')

    def test_empty_and_orphan_cells_conservatively_flag(self):
        for content in ('shall <entry/>not', '<entry>shall </entry><entry/>not'):
            view, sidecar = self.fixture(content)
            result = extract(view, sidecar)
            match = next(d for d in result['boundary_decisions'] if d['quote'] == 'shall not')
            self.assertEqual(match['decision'], 'flag_cell_boundary')
            self.assertTrue(all(e['table_path'] is None for e in match['boundary_evidence']))

    def test_unicode_fraction_context_unchanged(self):
        view, sidecar = self.fixture('🐈 café shall report after 4<fraction>1/2</fraction> hours. NW<fraction>1/4</fraction> sec.21')
        before = copy.deepcopy((view, sidecar))
        result = extract(view, sidecar)
        self.assertEqual(before, (view, sidecar))
        self.assertIn('41/2 hours', result['full_context_text'])
        self.assertIn('NW1/4', result['full_context_text'])
        self.assertEqual(result['counts']['flagged_hits'], 0)
        fraction_refs = [f for d in result['boundary_decisions'] for f in d['fraction_context']]
        self.assertEqual({f['text'] for f in fraction_refs}, {'1/2', '1/4'})
        for d in result['boundary_decisions']:
            self.assertEqual(d['quote'], view['text'][d['identity']['start']:d['identity']['end']])
        self.assertEqual(result, extract(view, sidecar))

    def test_forged_binding_and_projections_rejected(self):
        view, sidecar = self.fixture('<table><row><entry>shall not</entry></row></table><fraction>1/2</fraction>')
        mutations = [lambda s: s['source'].update(view_hash='0' * 64),
                     lambda s: s.update(text=s['text'] + 'x'),
                     lambda s: s.update(tables=[]),
                     lambda s: s['tables'][0]['cells'][0].update(start=0),
                     lambda s: s.update(fractions=[]),
                     lambda s: s['fractions'][0].update(context_text='fake'),
                     lambda s: s['nodes'].append(copy.deepcopy(s['nodes'][-1])),
                     lambda s: s['nodes'][0].update(children_paths=[]),
                     lambda s: s.update(segments=[]),
                     lambda s: s.update(offset_unit='bytes')]
        for mutation in mutations:
            forged = copy.deepcopy(sidecar)
            mutation(forged)
            with self.assertRaises(ValueError):
                extract(view, forged)
        forged = copy.deepcopy(view)
        forged['text'] += 'X'
        with self.assertRaises(ValueError):
            extract(forged, sidecar)

    def test_non_table_context_baseline_exact_and_all_retained(self):
        view, sidecar = self.fixture('The Secretary shall submit a report within 10 days. No person may interfere.')
        result = extract(view, sidecar)
        self.assertEqual(result['raw_output'], baseline(view))
        self.assertGreater(result['counts']['raw_hits'], 0)
        self.assertEqual(result['counts']['flagged_hits'], 0)
        self.assertEqual(result['sidecar_hash'], seal(sidecar)['hash'])


if __name__ == '__main__':
    unittest.main()
