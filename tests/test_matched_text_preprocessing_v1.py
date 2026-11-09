import copy
import math
import unittest

import numpy as np
from scipy.sparse import isspmatrix_csr
from engine.paper_evaluation import seal
from scripts.bill_context_design_text_v2 import render
from scripts.bill_structural_input_v1 import build
from scripts.matched_text_preprocessing_v1 import VERSION, CoreTfidf, prepare_document


def doc(tokens):
    return dict(version=VERSION, token_segments=[dict(tokens=tokens)])


class TextPreprocessingTests(unittest.TestCase):
    def prepare(self, body, extra='', bill_id='113-hr1', number='H. R. 1'):
        raw = (f'<bill><form><congress>113th CONGRESS</congress><legis-num>{number}</legis-num>'
               f'<official-title>Protect public waters</official-title></form>{extra}'
               f'<legis-body>{body}</legis-body></bill>').encode()
        view = render(raw, bill_id)
        h = seal(view)['hash']
        sidecar = build(raw, bill_id, view, h)
        before = copy.deepcopy((view, sidecar))
        result = prepare_document(raw, bill_id, view, h, sidecar)
        self.assertEqual(before, (view, sidecar))
        return result

    def test_nfc_negation_unicode_and_source_bounds(self):
        result = self.prepare('<text>NO cafe&#769; shall not 🐈 Straße 2026</text>')
        words = [t for s in result['token_segments'] for t in s['tokens']]
        self.assertIn('café', words)
        self.assertIn('not', words)
        self.assertIn('no', words)
        self.assertIn('straße', words)
        self.assertNotIn('113th', words)
        self.assertIn('protect', words)
        for s in result['token_segments']:
            self.assertEqual(result['text'][s['start']:s['end']], s['text'])
        self.assertFalse(result['token_offsets_available'])

    def test_exact_identity_and_substantive_status_preserved(self):
        result = self.prepare('<text>H.R. 1 enacted H.R. 10 42 U.S.C. 1 Public Law 113-1</text>', '<action>Passed House</action>')
        words = [t for s in result['token_segments'] for t in s['tokens']]
        self.assertIn('enacted', words)
        self.assertNotIn('passed', words)
        self.assertIn('10', words)
        self.assertIn('42', words)
        self.assertIn('public', words)
        self.assertEqual(sum(m['reason'] == 'focal_identity' for m in result['masks']), 2)

    def test_senate_identifier_not_us_reference(self):
        result = self.prepare('<text>S. 1 U.S. 1 S. 10</text>', bill_id='113-s1', number='S. 1')
        matches = [result['text'][m['start']:m['end']] for m in result['masks'] if m['reason'] == 'focal_identity']
        self.assertEqual(matches, ['S. 1', 'S. 1'])

    def test_block_cell_mask_boundaries_and_inline_continuity(self):
        result = self.prepare('<text>before H.R. 1 after</text><table><row><entry>alpha</entry><entry>beta</entry></row></table><text>no <em>new</em> tax</text>')
        segments = [s['tokens'] for s in result['token_segments']]
        self.assertIn(['before'], segments)
        self.assertIn(['after'], segments)
        self.assertIn(['alpha'], segments)
        self.assertIn(['beta'], segments)
        self.assertIn(['no', 'new', 'tax'], segments)

    def test_fraction_boundaries_preserve_literal_tokens_without_numeric_guess(self):
        result = self.prepare('<text>4<fraction>1/2</fraction> hours NW<fraction>1/4</fraction> sec. 21</text>')
        words = [t for s in result['token_segments'] for t in s['tokens']]
        self.assertIn('41/2 hours NW1/4', result['text'])
        self.assertIn('4', words)
        self.assertIn('nw', words)
        self.assertNotIn('41', words)
        self.assertNotIn('nw1', words)
        self.assertIn(['1', '2'], [s['tokens'] for s in result['token_segments']])

    def test_ambiguous_administrative_tag_rejected(self):
        with self.assertRaisesRegex(ValueError, 'ambiguous'):
            self.prepare('<text>A<action>may pass</action>B</text>')

    def test_sidecar_tamper_rejected(self):
        raw = b'<bill><form><congress>113th CONGRESS</congress><legis-num>H.R. 1</legis-num></form><legis-body>A</legis-body></bill>'
        view = render(raw, '113-hr1'); h = seal(view)['hash']
        sidecar = build(raw, '113-hr1', view, h); sidecar['text'] += '!'
        with self.assertRaises(ValueError):
            prepare_document(raw, '113-hr1', view, h, sidecar)

    def core(self):
        return [doc(['common', 'alpha', 'alpha', 'beta']) for _ in range(5)] + [doc(['common', 'rare'])]

    def test_idf_tf_l2_and_df_filters(self):
        core = self.core()
        model = CoreTfidf().fit(core, list('abcdef'), ['core'] * 6)
        self.assertNotIn(('common',), model.terms_)
        self.assertNotIn(('rare',), model.terms_)
        self.assertTrue(np.allclose(model.idf_, math.log(7/6) + 1))
        matrix = model.transform(core)
        self.assertTrue(isspmatrix_csr(matrix))
        self.assertEqual(matrix.dtype, np.float64)
        self.assertTrue(np.allclose(matrix.multiply(matrix).sum(axis=1).A1, [1]*5 + [0]))
        row = matrix.toarray()[0]
        self.assertAlmostEqual(row[model.terms_.index(('alpha',))], 2 * row[model.terms_.index(('beta',))])

    def test_eval_cannot_refit_or_mutate_idf(self):
        model = CoreTfidf().fit(self.core(), list('abcdef'), ['core']*6)
        before = copy.deepcopy(model.manifest())
        self.assertEqual(model.transform([doc(['unseen'])]).nnz, 0)
        self.assertEqual(before, model.manifest())
        with self.assertRaises(ValueError):
            model.fit(self.core(), list('abcdef'), ['core']*6)
        with self.assertRaises(ValueError):
            CoreTfidf().fit(self.core(), list('abcdef'), ['core']*5+['evaluation'])
        with self.assertRaises(TypeError):
            CoreTfidf().fit(self.core(), list('abcdef'), ['core']*6, labels=[0]*6)

    def test_membership_empty_vocabulary_and_determinism(self):
        with self.assertRaises(ValueError):
            CoreTfidf().fit(self.core(), ['a']*6, ['core']*6)
        with self.assertRaises(ValueError):
            CoreTfidf().fit([doc(['same'])]*6, list('abcdef'), ['core']*6)
        a = CoreTfidf().fit(self.core(), list('abcdef'), ['core']*6)
        b = CoreTfidf().fit(self.core(), list('abcdef'), ['core']*6)
        self.assertEqual(a.manifest(), b.manifest())
        self.assertEqual(a.terms_, tuple(sorted(a.terms_)))
        self.assertEqual(a.transform(self.core()).toarray().tolist(), b.transform(self.core()).toarray().tolist())

    def test_cap_ranking_ties_and_no_boundary_bigrams(self):
        tokens = [f'w{i:05}' for i in range(10001)]
        # One token per segment prevents bigrams from changing cap ranking.
        many = dict(version=VERSION, token_segments=[dict(tokens=[t]) for t in tokens])
        model = CoreTfidf().fit([many]*5 + [doc(['outsider'])], list('abcdef'), ['core']*6)
        self.assertEqual(len(model.terms_), 10000)
        self.assertNotIn(('w10000',), model.terms_)
        self.assertTrue(all(len(t) == 1 for t in model.terms_))


if __name__ == '__main__':
    unittest.main()
