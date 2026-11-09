"""Independent synthetic adversarial checks; no legislative data/outcomes."""
import copy
import math
import unittest
from unittest.mock import patch
from types import SimpleNamespace

import numpy as np
from scipy.sparse import csr_matrix

from engine.paper_evaluation import seal
from scripts.bill_context_design_text_v2 import render
from scripts.bill_structural_input_v1 import build
from scripts.matched_text_preprocessing_v1 import CoreTfidf, VERSION, prepare_document
from scripts import matched_text_sparse_v1 as solver


def prepared(tokens):
    return dict(version=VERSION, token_segments=[dict(tokens=tokens)])


def document(body, form_extra=''):
    raw = ('<bill><form><congress>113th CONGRESS</congress><legis-num>H. R. 1</legis-num>'
           + form_extra + '</form><legis-body>' + body + '</legis-body></bill>').encode()
    view = render(raw, '113-hr1')
    view_hash = seal(view)['hash']
    sidecar = build(raw, '113-hr1', view, view_hash)
    return prepare_document(raw, '113-hr1', view, view_hash, sidecar)


class IndependentTextTests(unittest.TestCase):
    def test_substantive_language_and_statute_citation_survive(self):
        result = document('<text>May not repeal 42 U.S.C. 1983. H. R. 99 requires reporting. '
                          'H. R. 1 amends the law. Approved means an approved application.</text>',
                          '<official-title>A prohibition on payment</official-title>'
                          '<action>Passed House</action>')
        tokens = [t for s in result['token_segments'] for t in s['tokens']]
        for word in ('not', 'may', 'repeal', '42', '1983', '99', 'requires', 'approved', 'prohibition'):
            self.assertIn(word, tokens)
        self.assertNotIn('passed', tokens)
        self.assertNotIn('house', tokens)
        self.assertNotIn('1', tokens)
        self.assertIn('H. R. 1', result['text'])

    def test_mask_and_cell_boundaries_cannot_create_bigrams(self):
        result = document('<text>before H. R. 1 after</text>'
                          '<table><row><entry>alpha</entry><entry>beta</entry></row></table>')
        bigrams = [pair for s in result['token_segments'] for pair in zip(s['tokens'], s['tokens'][1:])]
        self.assertNotIn(('before', 'after'), bigrams)
        self.assertNotIn(('alpha', 'beta'), bigrams)

    def test_unicode_mapping_is_original_segment_not_normalized_offsets(self):
        result = document('<text>🐈 Cafe\u0301 İ NOT</text>')
        self.assertFalse(result['token_offsets_available'])
        self.assertIn('Cafe\u0301', result['text'])
        for segment in result['token_segments']:
            self.assertEqual(segment['text'], result['text'][segment['start']:segment['end']])
        self.assertIn('café', [t for s in result['token_segments'] for t in s['tokens']])

    def test_core_idf_is_frozen_and_document_frequency_not_term_frequency(self):
        core = [prepared(['ubiquitous', 'alpha', 'alpha', 'beta']) for _ in range(5)]
        core.append(prepared(['ubiquitous', 'rare']))
        fitted = CoreTfidf().fit(core, [str(i) for i in range(6)], ['core'] * 6)
        before = copy.deepcopy(fitted.manifest())
        self.assertNotIn(('ubiquitous',), fitted.terms_)
        self.assertNotIn(('rare',), fitted.terms_)
        self.assertIn(('alpha',), fitted.terms_)
        np.testing.assert_allclose(fitted.idf_, [math.log(7 / 6) + 1] * len(fitted.terms_))
        empty = fitted.transform([prepared(['evaluationexclusive'])])
        self.assertEqual(empty.nnz, 0)
        fitted.transform([prepared(['alpha'] * 1000 + ['evaluationexclusive'])])
        self.assertEqual(before, fitted.manifest())
        with self.assertRaises(ValueError):
            fitted.fit(core, [str(i) for i in range(6)], ['core'] * 6)

    def test_membership_roles_and_empty_vocabulary_fail_closed(self):
        docs = [prepared(['alpha']) for _ in range(6)]
        for roles in (['core'] * 5 + ['calibration'], ['core'] * 5 + ['evaluation']):
            with self.assertRaises(ValueError):
                CoreTfidf().fit(docs, list('abcdef'), roles)
        with self.assertRaises(ValueError):
            CoreTfidf().fit(docs, list('abcdef'), ['core'] * 6)

    def test_core_order_does_not_change_columns_or_idf(self):
        docs = [prepared(['zeta', 'alpha']) for _ in range(5)] + [prepared(['other'])]
        a = CoreTfidf().fit(docs, list('abcdef'), ['core'] * 6)
        b = CoreTfidf().fit(docs[::-1], list('fedcba'), ['core'] * 6)
        self.assertEqual(a.terms_, b.terms_)
        np.testing.assert_array_equal(a.idf_, b.idf_)
        np.testing.assert_array_equal(a.transform(docs).data, b.transform(docs).data)

    def test_fraction_boundaries_preserve_context_without_false_numeric_join(self):
        result = document('<text>4<fraction>1/2</fraction> hours; NW<fraction>1/4</fraction> sec.</text>')
        tokens = [t for segment in result['token_segments'] for t in segment['tokens']]
        self.assertIn('41/2 hours', result['text'])
        self.assertIn('NW1/4 sec.', result['text'])
        self.assertNotIn('41', tokens)
        self.assertNotIn('nw1', tokens)
        for word in ('4', '1', '2', 'hours', 'nw', 'sec'):
            self.assertIn(word, tokens)


class IndependentSolverTests(unittest.TestCase):
    def test_finite_difference_and_unpenalized_intercept(self):
        X = csr_matrix([[0., 1.], [1., -1.], [2., 0.], [-1., 2.]])
        y = np.array([0., 1., 1., 0.])
        theta = np.array([.7, -.2, .4])
        value, gradient = solver.objective_gradient(theta, X, y)
        numerical = []
        for j in range(3):
            delta = np.zeros(3)
            delta[j] = 1e-6
            numerical.append((solver.objective_gradient(theta + delta, X, y)[0]
                              - solver.objective_gradient(theta - delta, X, y)[0]) / 2e-6)
        np.testing.assert_allclose(gradient, numerical, atol=1e-9, rtol=0)
        logits = X @ theta[1:] + theta[0]
        direct = sum(math.log1p(math.exp(float(z))) - label * z for z, label in zip(logits, y)) / 4
        self.assertAlmostEqual(value - direct, .025 * sum(theta[1:] ** 2), places=14)
        self.assertAlmostEqual(gradient[0], sum(1 / (1 + math.exp(-float(z))) - label
                                               for z, label in zip(logits, y)) / 4, places=14)

    def test_success_flag_cannot_replace_gradient_gate(self):
        fake = SimpleNamespace(x=np.array([0., 0.]), success=True, status=0,
                               message='fabricated success', nit=0, nfev=1, njev=1)
        with patch.object(solver, 'minimize', return_value=fake):
            result = solver.fit(csr_matrix([[0.], [0.], [0.], [1.]]), [0, 0, 0, 1])
        self.assertTrue(result['optimizer_success'])
        self.assertFalse(result['accepted'])
        self.assertGreater(result['gradient_infinity_norm'], 1e-6)

    def test_sparse_fit_never_calls_toarray(self):
        X = csr_matrix(([1., -1., 2., -2.], ([0, 1, 2, 3], [0, 1000, 2000, 3000])),
                       shape=(4, 10001))
        with patch.object(csr_matrix, 'toarray', side_effect=AssertionError('Densification')):
            result = solver.fit(X, [1, 0, 1, 0])
        self.assertTrue(result['accepted'])
        self.assertEqual(result['columns'], 10001)

    def test_low_dimensional_independent_gradient_descent_equivalence(self):
        dense = np.array([[-2., 1.], [-1., 0.], [0., -1.], [1., 0.], [2., 1.], [1., -2.]])
        y = np.array([0., 0., 1., 0., 1., 1.])
        result = solver.fit(csr_matrix(dense), y)
        theta = np.zeros(3)
        for _ in range(20000):
            z = dense @ theta[1:] + theta[0]
            residual = 1 / (1 + np.exp(-z)) - y
            gradient = np.r_[residual.mean(), dense.T @ residual / len(y) + .05 * theta[1:]]
            if max(abs(gradient)) <= 1e-9:
                break
            theta -= .12 * gradient
        self.assertLessEqual(max(abs(gradient)), 1e-9)
        self.assertTrue(result['accepted'])
        np.testing.assert_allclose(result['parameters'], theta, atol=3e-5, rtol=0)
        self.assertAlmostEqual(result['objective'], solver.objective_gradient(theta, csr_matrix(dense), y)[0], places=10)

    def test_invalid_labels_and_unscaled_text_rejected(self):
        for labels in ([1, 1], [0, 2], [False, True], [0, float('nan')]):
            with self.assertRaises(ValueError):
                solver.fit(csr_matrix([[0.], [1.]]), labels)
        core = np.zeros((2, 6))
        scaler = solver.fit_structured_scaler(core)
        with self.assertRaises(ValueError):
            solver.combine_features(core, scaler, csr_matrix([[2.], [1.]]))


if __name__ == '__main__':
    unittest.main()
