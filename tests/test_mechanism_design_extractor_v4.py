import copy
import hashlib
import unittest
from scripts.mechanism_design_extractor_v2 import extract as v2
from scripts.mechanism_design_extractor_v3 import extract as v3
from scripts.mechanism_design_extractor_v4 import extract
from scripts.run_mechanism_context_v2 import check_context
from tests.test_mechanism_design_extractor import view, clause


def new_rule_hits(output, rule):
    return [h for c in output['candidates'] for h in c['hits'] if rule in h.get('rule_ids', [])]


class V4ScopeTests(unittest.TestCase):
    def test_no_cost_clause_is_not_negative_subject(self):
        source = view(clause('Services are provided at no cost to the public and may be used freely.'))
        self.assertTrue(new_rule_hits(v3(source), 'negative_subject_modal'))
        result = extract(source)
        self.assertFalse(new_rule_hits(result, 'negative_subject_modal'))
        self.assertTrue(any(e['reason'] == 'negative_subject_pattern_rejected' for e in result['excluded_v3_rule_matches']))
        for sentence in ('No applicant may receive aid.', 'No governmental entity shall obtain records.',
                         'No individual whose employment is funded under this Act may replace a worker.'):
            self.assertTrue(new_rule_hits(extract(view(clause(sentence))), 'negative_subject_modal'))

    def test_new_rules_do_not_bridge_separate_texts_or_paragraphs(self):
        for body, rule in (
            ('<section><text>No applicant</text><text>may receive aid.</text></section>', 'negative_subject_modal'),
            ('<section><paragraph><text>No applicant</text></paragraph><paragraph><text>may receive aid.</text></paragraph></section>', 'negative_subject_modal'),
            ('<section><text>The clerk shall provide</text><paragraph><text>records.</text></paragraph></section>', 'provide_records')):
            source = view(body)
            self.assertTrue(new_rule_hits(v3(source), rule))
            self.assertFalse(new_rule_hits(extract(source), rule))

    def test_inline_formatting_and_layout_inside_leaf_preserved(self):
        source = view('<section><text>No <em>applicant</em> may receive aid. The clerk shall provide\n\t records.</text></section>')
        output = extract(source)
        self.assertTrue(new_rule_hits(output, 'negative_subject_modal'))
        self.assertTrue(new_rule_hits(output, 'provide_records'))
        check_context(output, source)

    def test_parent_text_with_child_block_not_used_as_expansion_leaf(self):
        source = view('<section><text>No applicant<paragraph><text>may receive aid.</text></paragraph></text></section>')
        output = extract(source)
        self.assertFalse(new_rule_hits(output, 'negative_subject_modal'))
        self.assertTrue(any(e['reason'] == 'not_within_complete_leaf_text' for e in output['excluded_v3_rule_matches']))

    def test_all_legacy_suggestions_quarantined_including_proven_overclaims(self):
        for sentence in ('No person may not submit a report.', 'There are appropriated no funds for the program.',
                         'There are appropriated $100 for the program.'):
            source = view(clause(sentence)); baseline = v2(source); output = extract(source)
            self.assertTrue(baseline['proposals'])
            self.assertEqual(output['proposals'], [])
            self.assertEqual([p['proposal'] for p in output['legacy_proposals']], baseline['proposals'])
            self.assertEqual(output['accepted_v2_labels_created'], 0)

    def test_legacy_hits_retained_but_not_claimed_boundary_fixed(self):
        source = view('<section><text>No person</text><paragraph><text>may not act.</text></paragraph></section>')
        before = copy.deepcopy(source); baseline = v2(source); output = extract(source)
        old = {(c['mechanism'], h['start'], h['end']) for c in baseline['candidates'] for h in c['hits']}
        new = {(c['mechanism'], h['start'], h['end']) for c in output['candidates'] for h in c['hits']}
        self.assertTrue(old <= new)
        self.assertEqual(source, before)
        self.assertEqual(output, extract(source))
        self.assertIn('not fixed', output['legacy_locator_scope_warning'])
        self.assertTrue(all(a['status'] == 'abstain' for a in output['assessments'].values()))

    def test_hash_valid_overlapping_siblings_fail_closed(self):
        source = view(clause('The clerk shall provide records.'))
        node = next(s for s in source['spans'] if s['tag'] == 'text')
        other = dict(node, path=node['path'].replace('text[1]', 'text[2]'))
        source['spans'].append(other)
        with self.assertRaisesRegex(ValueError, 'Overlapping unrelated'):
            extract(source)

    def test_heading_expansion_excluded_without_erasing_legacy(self):
        source = view('<section><header>Annual report</header><text>The clerk shall submit an annual report.</text></section>')
        output = extract(source)
        hits = new_rule_hits(output, 'annual_report')
        self.assertEqual(len(hits), 1)
        self.assertEqual(hits[0]['expansion_scope'], 'complete_leaf_text')
        self.assertTrue(any(e['rule_id'] == 'annual_report' for e in output['excluded_v3_rule_matches']))


if __name__ == '__main__': unittest.main()
