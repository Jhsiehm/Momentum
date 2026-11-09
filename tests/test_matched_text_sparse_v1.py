import unittest
from types import SimpleNamespace
from unittest.mock import patch

import numpy as np
from scipy import sparse
from scipy.special import expit

from scripts import matched_text_sparse_v1 as m


class SparseSolverTests(unittest.TestCase):
    def setUp(self):
        self.X = sparse.csr_matrix([[-2., 0.], [-1., 1.], [0., -1.], [1., 1.], [2., 0.], [3., -1.]])
        self.y = np.array([0, 0, 1, 0, 1, 1])

    def test_finite_difference(self):
        theta = np.array([.2, -.3, .5])
        value, gradient = m.objective_gradient(theta, self.X, self.y)
        numerical = []
        for i in range(3):
            delta = np.zeros(3); delta[i] = 1e-5
            numerical.append((m.objective_gradient(theta + delta, self.X, self.y)[0] - m.objective_gradient(theta - delta, self.X, self.y)[0]) / 2e-5)
        np.testing.assert_allclose(gradient, numerical, atol=1e-9, rtol=1e-8)
        self.assertGreater(value, 0)

    def test_independent_scalar_gradient_descent(self):
        rows = [[-2., 0.], [-1., 1.], [0., -1.], [1., 1.], [2., 0.], [3., -1.]]
        theta = np.zeros(3)
        for _ in range(15000):
            grad = [0., .05 * theta[1], .05 * theta[2]]
            for row, label in zip(rows, self.y):
                residual = expit(theta[0] + sum(a*b for a,b in zip(row, theta[1:]))) - label
                grad[0] += residual / 6
                for j in range(2):
                    grad[j+1] += residual * row[j] / 6
            theta -= .1 * np.array(grad)
        result = m.fit(self.X, self.y)
        self.assertTrue(result['accepted'])
        np.testing.assert_allclose(result['parameters'], theta, atol=2e-5, rtol=0)
        self.assertEqual(result, m.fit(self.X, self.y))

    def test_intercept_only_and_unpenalized(self):
        X = sparse.csr_matrix((4, 0))
        result = m.fit(X, [0, 1, 1, 1])
        self.assertTrue(result['accepted'])
        self.assertAlmostEqual(result['parameters'][0], np.log(3), places=5)
        value, gradient = m.objective_gradient([1000], X, [0, 1, 1, 1])
        self.assertEqual(value, 250)
        self.assertEqual(gradient[0], .25)

    def test_extreme_logits_and_no_dense_conversion(self):
        with patch.object(sparse.csr_matrix, 'toarray', side_effect=AssertionError('densified')), patch.object(sparse.csr_matrix, 'todense', side_effect=AssertionError('densified')):
            value, grad = m.objective_gradient([0, 1000, -1000], self.X, self.y)
            self.assertTrue(np.isfinite(value))
            self.assertTrue(np.all(np.isfinite(grad)))
            self.assertTrue(m.fit(self.X, self.y)['accepted'])

    def test_invalid_inputs(self):
        for y in ([True,False,True,False,True,False], [0]*6, [0,1], [0,0,1,0,1,np.nan], [0,0,1,0,1,2], ['0','0','1','0','1','1'], [[0,0,1,0,1,1]]):
            with self.subTest(y=y), self.assertRaises(ValueError):
                m.fit(self.X, y)
        for X in (np.zeros((6,2)), sparse.csr_matrix((0,2)), sparse.csr_matrix([[np.inf],[1]]), sparse.csr_matrix([[1j],[0j]])):
            with self.subTest(X=X), self.assertRaises(ValueError):
                m.fit(X, self.y)
        for theta in ([0,1], [0,1,np.inf], [True,False,True], [[0,1,2]]):
            with self.assertRaises(ValueError): m.objective_gradient(theta,self.X,self.y)

    def test_failure_is_not_retried_or_promoted(self):
        def fake(success, theta):
            return SimpleNamespace(x=np.array(theta),success=success,status=1,message='synthetic failure',nit=2,nfev=3,njev=3)
        for success, theta in [(False,[0,0,0]),(True,[0,0,0]),(True,[np.nan,0,0])]:
            with patch.object(m,'minimize',return_value=fake(success,theta)) as solver:
                result=m.fit(self.X,self.y)
                self.assertFalse(result['accepted'])
                self.assertEqual(result['status'],'nonconverged')
                self.assertEqual(result['attempts'],1)
                solver.assert_called_once()
                self.assertEqual(solver.call_args.kwargs['options'],m.SOLVER_OPTIONS)
                self.assertIsNone(solver.call_args.kwargs['bounds'])

    def test_duplicate_entries_and_input_not_mutated(self):
        X=sparse.csr_matrix((np.array([1.,1.,-1.]),np.array([0,0,0]),np.array([0,2,3])),shape=(2,1))
        saved=X.data.copy()
        value, grad=m.objective_gradient([.2,.3],X,[1,0])
        expected=m.objective_gradient([.2,.3],sparse.csr_matrix([[2.],[-1.]]),[1,0])
        self.assertEqual(value,expected[0]); np.testing.assert_array_equal(grad,expected[1])
        np.testing.assert_array_equal(saved,X.data)


class StructuredScalingTests(unittest.TestCase):
    def test_training_only_scaling_and_unchanged_text(self):
        training=np.array([[0,1,2,3,4,5],[2,1,4,3,8,5]],dtype=float)
        scaler=m.fit_structured_scaler(training)
        self.assertEqual(scaler['scales'],[1.,.1,1.,.1,2.,.1])
        heldout=np.array([[101,1,3,3,6,5]],dtype=float)
        text=sparse.csr_matrix([[.6,0,.8]])
        before=dict(scaler)
        joined=m.combine_features(heldout,scaler,text)
        np.testing.assert_array_equal(joined[:,:6].toarray(),[[100,0,0,0,0,0]])
        np.testing.assert_array_equal(joined[:,6:].toarray(),text.toarray())
        self.assertEqual(scaler,before)
        self.assertEqual(m.combine_features(training,scaler,sparse.csr_matrix((2,10000))).shape,(2,10006))

    def test_bad_scaling_and_text(self):
        for values in (np.ones((2,5)),np.ones((0,6)),np.full((2,6),np.nan),np.ones((2,6),dtype=bool)):
            with self.assertRaises(ValueError): m.fit_structured_scaler(values)
        training=np.ones((2,6)); scaler=m.fit_structured_scaler(training)
        for text in (sparse.csr_matrix([[2.],[0]]),sparse.csr_matrix([[-1.],[0]]),sparse.csr_matrix([[1.]])):
            with self.assertRaises(ValueError): m.combine_features(training,scaler,text)
        for bad in ({},dict(scaler,scales=[0]*6),dict(scaler,means=[0]),dict(scaler,version='other')):
            with self.assertRaises(ValueError): m.transform_structured(training,bad)


if __name__ == '__main__':
    unittest.main()
