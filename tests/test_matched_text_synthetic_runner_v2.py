"""Serialization regression for the separately registered successor runner."""
import json
import unittest
import numpy as np
from engine.paper_evaluation import seal, unseal
from scripts.run_matched_text_synthetic_v2 import serializable_checks


class SyntheticRunnerSerializationTests(unittest.TestCase):
    def test_numpy_boolean_verdicts_seal_without_changing_truth_values(self):
        original = {'pass': np.bool_(True), 'fail': np.bool_(False), 'native': True}
        converted = serializable_checks(original)
        self.assertEqual(converted, {'pass': True, 'fail': False, 'native': True})
        self.assertTrue(all(type(value) is bool for value in converted.values()))
        self.assertIsInstance(original['pass'], np.bool_)
        result = dict(checks=converted, all_passed=all(converted.values()))
        self.assertEqual(unseal(seal(result)), json.loads(json.dumps(result, allow_nan=False)))
        self.assertFalse(result['all_passed'])

    def test_nonboolean_results_cannot_be_coerced_to_passes(self):
        for invalid in (1, 0, 'False', '', [], None, np.nan, np.float64(1.0)):
            with self.subTest(invalid=repr(invalid)), self.assertRaises(ValueError):
                serializable_checks({'bad': invalid})


if __name__ == '__main__':
    unittest.main()
