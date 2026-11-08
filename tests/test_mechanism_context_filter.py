"""Context triage contrasts and source/hit preservation; no accuracy claims."""
import copy
from concurrent.futures import ThreadPoolExecutor
import unittest

from scripts.mechanism_context_filter import classify
from scripts.mechanism_design_extractor_v3 import extract
from tests.test_mechanism_design_extractor import view, clause


def annual_decisions(body):
    source = view(body)
    expanded = extract(source)
    result = classify(source, expanded)
    return source, expanded, result, [d for d in result['decisions'] if d['mechanism'] == 'deadline' and d['quote'].lower() == 'annual report']


class ContextFilterTests(unittest.TestCase):
    def test_complete_hit_preservation_no_mutation_and_concurrent_determinism(self):
        source, expanded, result, _ = annual_decisions(clause('There is an annual report.', 'Findings') + clause('The Secretary shall submit an annual report.'))
        original_view, original_output = copy.deepcopy(source), copy.deepcopy(expanded)
        expected = {(c['mechanism'], h['start'], h['end']) for c in expanded['candidates'] for h in c['hits']}
        self.assertEqual({(d['mechanism'], d['start'], d['end']) for d in result['decisions']}, expected)
        self.assertEqual(len(result['decisions']), len(expected))
        with ThreadPoolExecutor(max_workers=4) as pool:
            results = list(pool.map(lambda _: classify(source, expanded), range(8)))
        self.assertTrue(all(r == result for r in results))
        self.assertEqual(source, original_view)
        self.assertEqual(expanded, original_output)
        for key in ('human_certified', 'historical_feature_eligible', 'semantic_accuracy_verified', 'trained_model'):
            self.assertIs(result[key], False)
        self.assertEqual(result['accepted_labels'], 0)
        self.assertTrue(result['design_review_exposure'])

    def test_every_evidence_span_is_exact_and_duplicate_unicode_occurrences_distinct(self):
        source, _, result, selected = annual_decisions(clause('Café 🌱 annual report.', 'Findings') + clause('Café 🌱 annual report.'))
        self.assertEqual([d['status'] for d in selected], ['flagged', 'retain'])
        self.assertNotEqual(selected[0]['start'], selected[1]['start'])
        for decision in result['decisions']:
            self.assertEqual(decision['quote'], source['text'][decision['start']:decision['end']])
            for e in decision['evidence']:
                self.assertEqual(e['quote'], source['text'][e['start']:e['end']])

    def test_findings_and_sense_do_not_escape_ancestor(self):
        body = ('<section><subsection><header>Sense of Congress</header><text>An annual report should be issued.</text></subsection>'
                '<subsection><header>Required action</header><text>The Secretary shall submit an annual report.</text></subsection></section>')
        _, _, _, selected = annual_decisions(body)
        self.assertEqual([d['status'] for d in selected], ['flagged', 'retain'])
        self.assertIn('findings_or_sense_context', selected[0]['reasons'])

    def test_inline_striking_replacement_not_global_and_layout_whitespace_supported(self):
        body = clause('Section 2 is amended by striking annual\n\treport and inserting monthly report.') + clause('The Director shall submit an annual report.')
        _, _, _, selected = annual_decisions(body)
        first = [d for d in classify(view(body), extract(view(body)))['decisions'] if d['mechanism'] == 'deadline' and 'annual' in d['quote'].lower()]
        self.assertEqual([d['status'] for d in first], ['flagged', 'retain'])
        self.assertIn('struck_replacement_operand', first[0]['reasons'])
        _, _, _, selected = annual_decisions(clause('Section 2 is amended by striking “annual report” and inserting “annual report”.'))
        self.assertEqual([d['status'] for d in selected], ['flagged', 'retain'])

    def test_ambiguous_or_unbounded_deletion_is_retained(self):
        examples = (
            'Section 2 is amended by striking annual report.',
            'The words annual report appear here. A later clause is amended by striking text and inserting other text.',
            'Section 2 is amended by striking “annual report with “nested words” inside”.',
            'Section 2 is amended by striking annual report; and inserting another report.',
            'Section 2 is amended by striking ' + 'x ' * 800 + 'annual report and inserting new text.',
        )
        for example in examples:
            with self.subTest(example=example[:80]):
                _, _, _, selected = annual_decisions(clause(example))
                self.assertTrue(selected)
                self.assertTrue(all(d['status'] == 'retain' for d in selected))

    def test_quoted_block_nearest_sibling_and_inserted_block_are_not_borrowed(self):
        for directive in ('Section 2 is amended by inserting the following:',
                          'Section 2 is amended by striking paragraph (1) and inserting the following:'):
            body = '<section><text>' + directive + '</text><quoted-block><section><text>The annual report shall be public.</text></section></quoted-block></section>'
            _, _, _, selected = annual_decisions(body)
            self.assertEqual(selected[0]['status'], 'retain')
        body = ('<section><text>Section 2 is amended by striking the following:</text>'
                '<paragraph><text>A separate instruction intervenes.</text></paragraph>'
                '<quoted-block><section><text>The annual report shall be public.</text></section></quoted-block></section>')
        _, _, _, selected = annual_decisions(body)
        self.assertEqual(selected[0]['status'], 'retain')

    def test_descriptive_project_content_retained_without_approval(self):
        _, _, result, selected = annual_decisions(clause('An optional project may include an annual report or an information display.'))
        self.assertEqual(selected[0]['status'], 'retain')
        self.assertEqual(selected[0]['reasons'], ['no_narrow_context_flag'])
        self.assertIn('not approved', result['interpretation'])

    def test_missing_body_boundary_does_not_claim_outside(self):
        source = view(clause('An annual report is expected.'))
        source['spans'] = [s for s in source['spans'] if s['tag'] != 'legis-body']
        result = classify(source, extract(source))
        self.assertTrue(all('outside_legis_body' not in d['reasons'] for d in result['decisions']))

    def test_wrong_input_binding_and_duplicate_hits_fail_closed(self):
        source = view(clause('The Secretary shall submit an annual report.'))
        expanded = extract(source)
        for key, value in (('bill_id', '999-hr1'), ('input_text_sha256', 'bad'), ('source_view_hash', 'b' * 64)):
            broken = copy.deepcopy(expanded)
            broken[key] = value
            with self.assertRaises(ValueError):
                classify(source, broken)
        broken = copy.deepcopy(expanded)
        broken['candidates'][0]['hits'].append(copy.deepcopy(broken['candidates'][0]['hits'][0]))
        with self.assertRaisesRegex(ValueError, 'Duplicate'):
            classify(source, broken)
        broken = copy.deepcopy(expanded)
        broken['candidates'][0]['hits'][0]['quote'] = 'not the source'
        with self.assertRaisesRegex(ValueError, 'source hit'):
            classify(source, broken)


if __name__ == '__main__':
    unittest.main()
