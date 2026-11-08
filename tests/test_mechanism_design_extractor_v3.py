"""Frozen-baseline invariants and bounded synthetic vocabulary examples."""
import copy
from concurrent.futures import ThreadPoolExecutor
import hashlib
from pathlib import Path
import unittest

from scripts.mechanism_design_extractor_v2 import extract as v2
from scripts.mechanism_design_extractor_v3 import extract, RULES, DEPENDENCY_SHA256
from scripts.run_mechanism_context_v2 import check_context
from tests.test_mechanism_design_extractor import view, clause


EXAMPLES = {
    'issue_statement': 'The official shall issue a detailed statement about impacts.',
    'furnish_information': 'The agency shall furnish such information to the board.',
    'display_website': 'Carriers shall prominently display on the website the amount of space.',
    'advise_in_writing': 'The Secretary shall advise the applicant in writing of reasons.',
    'provide_records': 'The clerk shall provide to the board the relevant records.',
    'file_document': 'The Secretary shall file a map and legal description.',
    'demonstrate_match': 'The applicant shall demonstrate that 50 percent of funds are matched.',
    'information_available': 'Information in the database shall be available to officers.',
    'annual_report': 'The recipient shall submit an annual report.',
    'annual_basis': 'The Director shall submit on an annual basis a report.',
    'semiannual_action': 'The entity shall conduct meetings open to the public semiannually.',
    'frequency_action': 'Payments shall be made not less frequently than 2 times a year.',
    'event_date_action': 'The hospital provides to the patient, on the date on which services occur, notice.',
    'evaluation_year_window': 'During the second and fifth years of operation, an evaluation shall be undertaken.',
    'election_relative': 'Two-thirds is broadcast during the 2 months immediately preceding election day.',
    'negative_subject_modal': 'No local administrator shall issue an order.',
    'maximum_award': 'The maximum amount of a voucher shall be $100.',
    'not_greater_than': 'The standard shall be not greater than the listed maximum.',
    'only_permission': 'The official may only act with written approval.',
    'supplement_not_supplant': 'Funds shall supplement, and not supplant, existing resources.',
    'ineligible_funding': 'The entity shall be ineligible to receive additional funding until approval.',
    'none_amounts': 'None of the amounts made available may be obligated for this purpose.',
    'land_withdrawal': 'All Federal land within the area is withdrawn from disposal.',
    'right_or_option': 'The applicant shall have the option to decline.',
    'retain_right': 'The Tribe shall retain any right to water.',
    'jurisdiction_savings': 'Nothing in this Act affects the jurisdiction of the State.',
    'appropriate_discretion': 'Access is allowed to the extent the Secretary determines appropriate.',
    'authorities': 'All authorities of this title shall terminate.',
    'not_unauthorized': 'The following shall not constitute the unauthorized use of gravel.',
    'deemed_approval': 'The product is deemed to be subject to an application for which approval is in effect.',
    'calendar_designation': 'March 5 is Public Service Day.',
    'boundary_exclusion': 'The boundary of the conservation area is modified to exclude 10 acres.',
    'reimplement_initiative': 'The Director shall reimplement the national public safety initiative.',
}


class ExpandedLocatorTests(unittest.TestCase):
    def test_manifest_unique_bounded_examples_and_source_binding(self):
        self.assertEqual(set(EXAMPLES), {r['rule_id'] for r in RULES})
        self.assertEqual(len(RULES), len({r['rule_id'] for r in RULES}))
        for rule in RULES:
            with self.subTest(rule=rule['rule_id']):
                source = view(clause(EXAMPLES[rule['rule_id']]))
                output = extract(source)
                found = [(c, h) for c in output['candidates'] for h in c['hits'] if rule['rule_id'] in h.get('rule_ids', [])]
                self.assertTrue(found)
                for candidate, hit in found:
                    self.assertEqual(candidate['mechanism'], rule['mechanism'])
                    self.assertEqual(hit['quote'], source['text'][hit['start']:hit['end']])
                    self.assertFalse(hit['semantic_governance_verified'])
                check_context(output, source)

    def test_baseline_candidate_hit_and_proposal_fields_preserved(self):
        source = view(''.join(clause(s) for s in EXAMPLES.values()))
        original = copy.deepcopy(source)
        baseline = v2(source)
        output = extract(source)
        self.assertEqual(source, original)
        self.assertEqual(baseline, v2(source))
        byid = {c['candidate_id']: c for c in output['candidates']}
        for candidate in baseline['candidates']:
            expanded = byid[candidate['candidate_id']]
            self.assertEqual({k:v for k,v in candidate.items() if k != 'hits'},
                             {k:v for k,v in expanded.items() if k != 'hits'})
            hitmap = {(h['start'], h['end']):h for h in expanded['hits']}
            for hit in candidate['hits']:
                new = hitmap[(hit['start'], hit['end'])]
                self.assertEqual(hit, {k:v for k,v in new.items() if k != 'rule_ids'})
        for key in ('proposals', 'suppressed_proposals', 'coverage', 'human_certified',
                    'historical_feature_eligible', 'trained_model', 'accepted_v2_labels_created'):
            self.assertEqual(output[key], baseline[key])
        for mechanism, assessment in output['assessments'].items():
            self.assertEqual(assessment['status'], 'abstain')
            self.assertEqual(assessment['candidate_count'], sum(c['mechanism'] == mechanism for c in output['candidates']))

    def test_no_duplicate_hits_and_repeat_concurrent_determinism(self):
        source = view(clause('The Director shall submit an annual report and shall have the option to decline.') * 2)
        expected = extract(source)
        for candidate in expected['candidates']:
            ids = [(h['start'], h['end']) for h in candidate['hits']]
            self.assertEqual(len(ids), len(set(ids)))
            for hit in candidate['hits']:
                self.assertEqual(len(hit.get('rule_ids', [])), len(set(hit.get('rule_ids', []))))
        with ThreadPoolExecutor(max_workers=4) as pool:
            outputs = list(pool.map(extract, [source] * 8))
        self.assertTrue(all(output == expected for output in outputs))

    def test_new_hit_parent_context_not_sibling_or_operative_claim(self):
        source = view('<section><text>Nothing in this Act requires—</text>'
                      '<paragraph><text>furnish such information to the committee.</text></paragraph>'
                      '<paragraph><text>File a map.</text></paragraph></section>')
        output = extract(source)
        pool = {s['span_id']:s for s in output['structural_spans']}
        hit = next(h for c in output['candidates'] for h in c['hits'] if 'furnish_information' in h.get('rule_ids', []))
        quotes = [pool[r['span_id']]['quote'] for r in hit['structural_context']]
        self.assertIn('Nothing in this Act requires—', quotes)
        self.assertNotIn('File a map.', quotes)
        self.assertFalse(output['proposals'])
        self.assertFalse(hit['semantic_governance_verified'])
        check_context(output, source)

    def test_bounded_patterns_do_not_cross_sentence_or_arbitrary_distance(self):
        for sentence in ('No agencies exist. Other officials may act.',
                         'The clerk shall file a cabinet.',
                         'The worker receives an annual salary.',
                         'The clerk shall provide ' + 'x ' * 200 + 'records.',
                         'The entity will furnish furniture.'):
            source = view(clause(sentence))
            output = extract(source)
            self.assertFalse([h for c in output['candidates'] for h in c['hits'] if h.get('rule_ids')])

    def test_dependency_hashes_match_frozen_modules(self):
        root = Path(__file__).resolve().parents[1]
        for path, expected in DEPENDENCY_SHA256.items():
            self.assertEqual(hashlib.sha256((root/path).read_bytes()).hexdigest(), expected)


if __name__ == '__main__':
    unittest.main()
