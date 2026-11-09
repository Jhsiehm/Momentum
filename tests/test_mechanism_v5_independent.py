"""Independent synthetic regression probes; no quality cases or effect labels."""
import copy
import unittest
from scripts.mechanism_design_extractor_v4 import extract as baseline
from scripts.mechanism_design_extractor_v5 import extract, RULES
from scripts.mechanism_context_filter_v3 import classify
from scripts.mechanism_validity_guard import validate_output
from tests.test_mechanism_design_extractor import view, clause

RULE_IDS = {r['rule_id'] for r in RULES}

def added_rules(result):
    return [h for c in result['candidates'] for h in c['hits'] if RULE_IDS.intersection(h.get('rule_ids', []))]

def old_operand(body):
    source = view(body)
    result = classify(source, extract(source))
    return [d for d in result['decisions'] if d['mechanism'] == 'deadline' and d['quote'] == 'annual report'][0]

class IndependentV5Probes(unittest.TestCase):
    def test_conjunction_sentence_and_negation_barriers(self):
        for sentence in (
            'No information concerning funding and applicants may apply.',
            'No information concerning funding. Applicants may apply.',
            'No information concerning funding; applicants may apply.',
            'No evidence derived from cost estimates but applicants may apply.',
            'No rate of pay fixed under law or workers may protest.',
            'No new permanent or temporary roads may not be built.',
            'No franchise authority shall not regulate charges.',
            'No cost to the Government wherever feasible and may be waived.',
        ):
            with self.subTest(sentence=sentence):
                self.assertEqual(added_rules(extract(view(clause(sentence)))), [])

    def test_all_rule_families_are_guarded_locators_not_decisions(self):
        for sentence in (
            'No local franchise authority may regulate charges.',
            'No information concerning a claimant obtained under this Act may be disclosed.',
            'No evidence derived therefrom shall be admitted.',
            'No rate of pay fixed pursuant to this section may exceed the limit.',
            'No permanent or temporary roads or other motorized vehicle routes may be built.',
        ):
            with self.subTest(sentence=sentence):
                source = view(clause(sentence)); before = copy.deepcopy(source)
                previous = baseline(source); output = extract(source)
                self.assertTrue(added_rules(output))
                old = {(c['mechanism'], h['start'], h['end']) for c in previous['candidates'] for h in c['hits']}
                new = {(c['mechanism'], h['start'], h['end']) for c in output['candidates'] for h in c['hits']}
                self.assertLessEqual(old, new)
                self.assertEqual(output['legacy_proposals'], previous['legacy_proposals'])
                self.assertEqual(output['proposals'], [])
                self.assertEqual(source, before)
                validate_output(source, output)

    def test_no_cross_leaf_reconstruction_even_in_nested_wrappers(self):
        for body in (
            '<section><text>No local franchise authority</text><paragraph><text>may regulate charges.</text></paragraph></section>',
            '<section><text>No information concerning funding</text><text>may be disclosed.</text></section>',
            '<section><text>No evidence derived<paragraph><text>therefrom may be admitted.</text></paragraph></text></section>',
        ):
            self.assertEqual(added_rules(extract(view(body))), [])

    def test_qualified_ancestor_chain_requires_affirmative_authority(self):
        template = '<section><text>{}</text><paragraph><text>in subsection (a),</text><subparagraph><text>in paragraph (2), by striking “annual report” and inserting “monthly report”.</text></subparagraph></paragraph></section>'
        self.assertEqual(old_operand(template.format('Section 2 is amended—'))['status'], 'flagged')
        for lead in ('Section 2 is not amended—', 'The report says Section 2 is amended—',
                     'Section 2 is amended if funding is available—', 'Section 2 is amended by adding—'):
            with self.subTest(lead=lead):
                self.assertEqual(old_operand(template.format(lead))['status'], 'retain')

    def test_quoted_and_intervening_narrative_barriers(self):
        for barrier in ('<text>The following is a historical example.</text>',
                        '<text>Section 3 is not amended—</text>', '<text>by inserting the following:</text>'):
            body = '<section><text>Section 2 is amended—</text><paragraph>' + barrier + '<subparagraph><text>in paragraph (2), by striking “annual report” and inserting “monthly report”.</text></subparagraph></paragraph></section>'
            self.assertEqual(old_operand(body)['status'], 'retain')
        body = '<section><text>Section 2 is amended—</text><quoted-block><paragraph><text>in paragraph (2), by striking “annual report” and inserting “monthly report”.</text></paragraph></quoted-block></section>'
        self.assertEqual(old_operand(body)['status'], 'retain')

if __name__ == '__main__': unittest.main()
