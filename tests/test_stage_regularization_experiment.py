import unittest
from scripts.stage_regularization_experiment import encode, CONFIGS


class StageExperimentTests(unittest.TestCase):
    def test_reference_encoding_and_other_features_preserved(self):
        for stage in range(4):
            x=[stage/4,.2,.1,.3,1,.1]
            encoded=encode(x,'categorical')
            self.assertEqual(encoded[:3],[float(stage==v) for v in (1,2,3)])
            self.assertEqual(encoded[3:],x[1:])
            self.assertEqual(encode(x,'linear'),x)

    def test_resolved_or_unknown_stage_rejected(self):
        for stage in (1.,-.25,.3):
            with self.assertRaises(ValueError):encode([stage,0,0,0,0,0],'categorical')
        with self.assertRaises(ValueError):encode([0]*6,'unknown')

    def test_exactly_one_configuration_factor_changes(self):
        control=CONFIGS['control']
        for name in ['weaker_l2','categorical_stage']:
            self.assertEqual(sum(a!=b for a,b in zip(control,CONFIGS[name])),1)
