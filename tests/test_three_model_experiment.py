import unittest
from engine.three_model_experiment import calibrate,fit_calibration,fit_models


class CalibrationTests(unittest.TestCase):
    def test_identity_and_monotonicity(self):
        for p in (.001,.03,.2,.8,.999):
            self.assertAlmostEqual(calibrate(dict(intercept=0,slope=1),p),p)
        artifact=fit_calibration([.01,.02,.03,.1,.2],[0,0,0,1,1])
        ps=[calibrate(artifact,p) for p in (.001,.01,.1,.9,.999)]
        self.assertEqual(ps,sorted(ps))
        self.assertTrue(all(0<p<1 for p in ps))

    def test_requires_two_classes_and_matching_lengths(self):
        for ps,ys in (([],[]),([.1],[0]),([.1,.2],[0,0]),([.1],[0,1])):
            with self.assertRaises(ValueError):fit_calibration(ps,ys)

    def test_correction_direction_and_repeatability(self):
        ps=[.01]*20;ys=[0]*18+[1]*2
        a=fit_calibration(ps,ys)
        self.assertGreater(calibrate(a,.01),.01)
        self.assertEqual(a,fit_calibration(ps,ys))

    def test_training_overlap_rejected_before_fit(self):
        row=dict(bill_id='116-hr1')
        with self.assertRaises(AssertionError):fit_models([row],[row],[row])

    def test_extra_training_rows_rejected_before_fit(self):
        with self.assertRaises(AssertionError):
            fit_models([dict(bill_id='116-hr1'),dict(bill_id='118-hr1')],[dict(bill_id='116-hr1')],[])


if __name__=='__main__':unittest.main()
