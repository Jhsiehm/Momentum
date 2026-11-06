import unittest
from engine.learning import _fit
from engine.model import predict
try:
    import numpy
except ImportError:
    numpy=None
if numpy is not None:
    from scripts.convergence_experiment import fit_converged


@unittest.skipIf(numpy is None, 'Optional research dependency NumPy is not installed')
class ConvergenceTests(unittest.TestCase):
    def rows(self):
        return [dict(x=[i/40,int(i%2)],y=int(i%7==0)) for i in range(40)]

    def test_300_step_scalar_equivalence(self):
        rows=self.rows();scalar=_fit(rows,.05)
        vector,diagnostics,snapshot=fit_converged(rows,.05,cap=300)
        for r in rows:self.assertAlmostEqual(predict(scalar,r['x']),predict(snapshot,r['x']),places=13)
        self.assertEqual(vector,snapshot)
        self.assertFalse(diagnostics['converged'])

    def test_training_gradient_stopping(self):
        _,diagnostics,_=fit_converged(self.rows(),.2)
        self.assertTrue(diagnostics['converged'])
        self.assertLessEqual(diagnostics['max_absolute_gradient'],1e-6)
        self.assertGreaterEqual(diagnostics['iterations'],300)

    def test_iteration_cap_does_not_claim_convergence(self):
        _,diagnostics,_=fit_converged(self.rows(),.05,tolerance=1e-20,cap=301)
        self.assertEqual(diagnostics['iterations'],301)
        self.assertFalse(diagnostics['converged'])
