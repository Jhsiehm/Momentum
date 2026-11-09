import copy
import unittest
from scripts.mechanism_design_extractor_v4 import extract as v4
from scripts.mechanism_design_extractor_v5 import extract, RULES
from scripts.mechanism_validity_guard import validate_output
from tests.test_mechanism_design_extractor import view, clause


def additions(result):
    ids = {r['rule_id'] for r in RULES}
    return [h for c in result['candidates'] for h in c['hits'] if ids.intersection(h.get('rule_ids', []))]


class V5SubjectTests(unittest.TestCase):
    def test_subject_families_and_unseen_variations(self):
        cases = (
            'No franchise authority shall renew the license.',
            'No local franchise authorities may renew licenses.',
            'No information concerning any applicant acquired from the records may be disclosed.',
            'No information obtained from a confidential source shall be disclosed.',
            'No evidence derived therefrom may be admitted.',
            'No evidence derived from private messages shall be admitted.',
            'No rate of pay fixed under this subsection may exceed the ceiling.',
            'No rate of pay fixed pursuant to the revised schedule shall exceed the ceiling.',
            'No new permanent or temporary roads or other motorized vehicle routes shall be constructed.',
            'No temporary roads and vehicle routes may be built.',
        )
        for sentence in cases:
            with self.subTest(sentence=sentence):
                source = view(clause(sentence)); output = extract(source)
                self.assertTrue(additions(output))
                validate_output(source, output)
                self.assertEqual(output['proposals'], [])
                self.assertTrue(all(a['status'] == 'abstain' for a in output['assessments'].values()))

    def test_clause_bridges_and_negated_modals_rejected(self):
        cases = (
            'Services come at no cost to the Government wherever feasible and may continue.',
            'There shall be no limit to the number of terms an individual may serve.',
            'No information concerning costs is available and applicants may proceed.',
            'No information obtained from records exists. The applicant may proceed.',
            'No evidence derived from records exists; the agency may proceed.',
            'No rate of pay fixed under this section is available, but staff may proceed.',
            'No franchise authority shall not renew the license.',
            'No information concerning applicants may not be disclosed.',
            'No new roads or staff may use the facility.',
            'No evidence derived therefrom and the clerk may proceed.',
        )
        for sentence in cases:
            with self.subTest(sentence=sentence):
                self.assertFalse(additions(extract(view(clause(sentence)))))

    def test_bounds_and_structural_bridges(self):
        bodies = (
            '<section><text>No franchise authority</text><text>shall renew.</text></section>',
            '<section><header>No evidence derived therefrom may</header><text>Read this heading.</text></section>',
            '<section><text>No information concerning<paragraph><text>records may be used.</text></paragraph></text></section>',
        )
        for body in bodies:
            self.assertFalse(additions(extract(view(body))))
        for subject in ('No information concerning ', 'No evidence derived from '):
            self.assertFalse(additions(extract(view(clause(subject + 'word ' * 25 + 'may be disclosed.')))))
        self.assertFalse(additions(extract(view(clause('No rate of pay fixed under ' + 'word ' * 13 + 'shall exceed the cap.')))))

    def test_inline_and_unicode_duplicates_source_offsets(self):
        source = view('<section><text>No evidence derived from <em>café</em> records may be used.</text>'
                      '<text>No evidence derived from café records may be used.</text></section>')
        result = extract(source)
        self.assertEqual(len(additions(result)), 2)
        self.assertEqual(len({h['start'] for h in additions(result)}), 2)
        validate_output(source, result)

    def test_legacy_preservation_quarantine_determinism(self):
        source = view(clause('No person may not act. There are appropriated no funds. No franchise authority shall renew.'))
        saved = copy.deepcopy(source); baseline = v4(source); result = extract(source)
        keys = lambda r: {(c['mechanism'], h['start'], h['end']) for c in r['candidates'] for h in c['hits']}
        self.assertLessEqual(keys(baseline), keys(result))
        self.assertEqual(result['legacy_proposals'], baseline['legacy_proposals'])
        self.assertEqual(result['excluded_v3_rule_matches'], baseline['excluded_v3_rule_matches'])
        self.assertEqual(result['proposals'], [])
        self.assertEqual(result['accepted_v2_labels_created'], 0)
        self.assertEqual(source, saved)
        self.assertEqual(result, extract(source))
        validate_output(source, result)


if __name__ == '__main__':
    unittest.main()
