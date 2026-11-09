import copy
import unittest
from scripts.mechanism_design_extractor_v4 import extract
from scripts.mechanism_context_filter_v2 import classify as previous
from scripts.mechanism_context_filter_v3 import classify
from tests.test_mechanism_design_extractor import view


def chain(local='in clause (ii), as redesignated, ', root='Section 2705 of title 18, United States Code, is amended—', middle='in subsection (a)—', quote=False):
    inner = '<paragraph><text>' + middle + '</text><subparagraph><text>in paragraph (4), as redesignated,—</text><clause><text>in subparagraph (B)—</text><subclause><text>' + local + 'by striking annual report and inserting monthly report.</text></subclause></clause></subparagraph></paragraph>'
    if quote:
        inner = '<quoted-block>' + inner + '</quoted-block>'
    return '<section><text>' + root + '</text>' + inner + '</section>'


def run(body):
    v = view(body); output = extract(v)
    result = classify(v, output)
    ds = [d for d in result['decisions'] if d['mechanism'] == 'deadline' and d['quote'] == 'annual report']
    return v, output, result, ds[0]


class QualifiedAmendmentTests(unittest.TestCase):
    def test_qualified_chain_restores_flag(self):
        for local in ('in clause (ii), as redesignated, ', 'in clause (v), as redesignated, ',
                      'in paragraph (2), in the matter preceding subparagraph (A), '):
            v, output, result, d = run(chain(local))
            self.assertEqual(d['status'], 'flagged')
            self.assertEqual(d['previous_status'], 'retain')
            self.assertEqual(d['deletion_provenance'], 'qualified_structural_affirmative_amendment_source')
            self.assertFalse(result['semantic_accuracy_verified'])
            self.assertFalse(result['human_certified'])

    def test_no_ancestor_or_narrative_or_negation(self):
        for root in ('The manual describes amendments—', 'Section 2 is not amended—',
                     'If approved, Section 2 is amended—', 'Section 2 is amended only if approved—',
                     'Section 2 is amended. The manual describes the following—'):
            self.assertEqual(run(chain(root=root))[3]['status'], 'retain')

    def test_middle_must_be_scope_not_insertion_or_narrative(self):
        for middle in ('by inserting the following—', 'by adding the following—',
                       'The manual describes changes—', 'in subsection (a), unless approved—',
                       'in subsection (a), not as redesignated—'):
            self.assertEqual(run(chain(middle=middle))[3]['status'], 'retain')

    def test_local_prefix_requires_full_scope_grammar(self):
        for local in ('The manual describes in clause (ii), ', 'in clause (ii), if approved, ',
                      'in clause (ii), not as redesignated, ', 'in clause (ii), by inserting ',
                      'in clause (ii). ', 'in clause (ii), as proposed, '):
            self.assertEqual(run(chain(local))[3]['status'], 'retain')

    def test_quoted_boundary_cannot_inherit(self):
        self.assertEqual(run(chain(quote=True))[3]['status'], 'retain')

    def test_new_operand_not_flagged(self):
        v, output, result, d = run(chain().replace('monthly report', 'annual report'))
        ds = [x for x in result['decisions'] if x['mechanism'] == 'deadline' and x['quote'] == 'annual report']
        self.assertEqual([x['status'] for x in ds], ['flagged', 'retain'])

    def test_unchanged_inputs_exact_evidence_deterministic_all_hits_preserved(self):
        v, output, result, d = run(chain()); before = copy.deepcopy((v, output))
        self.assertEqual(classify(v, output), result)
        self.assertEqual((v, output), before)
        self.assertEqual(len(result['decisions']), len(previous(v, output)['decisions']))
        for decision in result['decisions']:
            for key in ('evidence', 'previous_evidence', 'legacy_evidence'):
                for item in decision[key]:
                    self.assertEqual(item['quote'], v['text'][item['start']:item['end']])

    def test_simple_affirmative_and_negated_behavior_preserved(self):
        for prefix in ('Section 2 is amended ', 'Section 2 is not amended '):
            v, output, result, _ = run('<section><text>' + prefix + 'by striking annual report and inserting monthly report.</text></section>')
            old = previous(v, output)
            self.assertEqual([(d['status'], d['reasons']) for d in old['decisions']], [(d['status'], d['reasons']) for d in result['decisions']])

if __name__ == '__main__':
    unittest.main()
