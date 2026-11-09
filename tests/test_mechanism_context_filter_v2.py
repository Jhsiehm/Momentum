import copy
import unittest
from scripts.mechanism_design_extractor_v4 import extract
from scripts.mechanism_context_filter import classify as old_filter
from scripts.mechanism_context_filter_v2 import classify
from tests.test_mechanism_design_extractor import view, clause


def annual(body):
    v = view(body); out = extract(v); result = classify(v, out)
    return v, out, result, [d for d in result['decisions'] if d['mechanism'] == 'deadline' and d['quote'] == 'annual report']


class AffirmativeProvenanceTests(unittest.TestCase):
    def test_proven_negated_narrative_deletion_falseflags_retained(self):
        for sentence in ('Section 2 is not amended by striking “annual report” and inserting “monthly report”.',
                         'The manual describes amendments by striking “annual report” and inserting “monthly report”.',
                         'If approved, Section 2 is amended by striking “annual report”.'):
            v, out, result, ds = annual(clause(sentence))
            self.assertTrue(any(d['status'] == 'flagged' for d in old_filter(v, out)['decisions'] if d['mechanism'] == 'deadline'))
            self.assertEqual(ds[0]['status'], 'retain')
            self.assertEqual(ds[0]['legacy_status'], 'flagged')
            self.assertEqual(ds[0]['deletion_provenance'], 'not_established')

    def test_positive_amendment_old_operand_flagged_new_operand_retained(self):
        _, _, _, ds = annual(clause('Section 2 is amended by striking “annual report” and inserting “annual report”.'))
        self.assertEqual([d['status'] for d in ds], ['flagged', 'retain'])
        self.assertEqual(ds[0]['deletion_provenance'], 'affirmative_amendment_source')

    def test_standalone_instruction_inherits_structural_affirmative_leadin(self):
        body = '<section><text>Section 2 of the Act is amended—</text><paragraph><text>by striking annual report and inserting monthly report.</text></paragraph></section>'
        _, _, _, ds = annual(body)
        self.assertEqual(ds[0]['status'], 'flagged')
        for prefix in ('Section 2 of the Act is not amended—', 'The manual discusses changes—'):
            _, _, _, ds = annual(body.replace('Section 2 of the Act is amended—', prefix))
            self.assertEqual(ds[0]['status'], 'retain')

    def test_quoted_block_positive_and_narrative_directives(self):
        for prefix, status in (('Section 2 is amended by striking the following:', 'flagged'),
                               ('The report describes amendments by striking the following:', 'retain'),
                               ('Section 2 is not amended by striking the following:', 'retain'),
                               ('Section 2 is amended by striking paragraph (1) and inserting the following:', 'retain')):
            body = '<section><text>' + prefix + '</text><quoted-block><section><text>The annual report shall be public.</text></section></quoted-block></section>'
            _, _, _, ds = annual(body)
            self.assertEqual(ds[0]['status'], status)

    def test_exact_evidence_and_no_mutation_or_hit_loss(self):
        v, out, result, _ = annual(clause('Section 2 is amended by striking “annual report” and inserting “annual report”.'))
        before = copy.deepcopy(out)
        self.assertEqual(result, classify(v, out));self.assertEqual(out, before)
        self.assertEqual(len(result['decisions']), sum(len(c['hits']) for c in out['candidates']))
        for d in result['decisions']:
            for e in d['evidence'] + d['legacy_evidence']:
                self.assertEqual(e['quote'], v['text'][e['start']:e['end']])
        self.assertFalse(result['semantic_accuracy_verified'])
        self.assertFalse(result['human_certified'])


if __name__ == '__main__': unittest.main()
