import unittest
from scripts.training_source_class_readiness import summarize


class ClassReadinessTests(unittest.TestCase):
    def test_missing_sources_do_not_supply_positive_counts(self):
        memberships = {'117': {'core_ids': ['a','b'], 'calibration_ids': ['c','d']}}
        labels = {'a': 0, 'b': 1, 'c': 0, 'd': 1}
        result = summarize(memberships, labels, {'a','b','c'})['117']
        self.assertEqual(result['core'], dict(n=2, recorded_positive=1, both_classes=True))
        self.assertEqual(result['calibration'], dict(n=1, recorded_positive=0, both_classes=False))

    def test_overlap_and_invalid_labels_rejected(self):
        with self.assertRaisesRegex(ValueError, 'Overlapping'):
            summarize({'117': {'core_ids':['a'], 'calibration_ids':['a']}}, {'a': 1}, {'a'})
        for labels in ({}, {'a': -1}, {'a': True}):
            with self.assertRaisesRegex(ValueError, 'outcome'):
                summarize({'117': {'core_ids':['a'], 'calibration_ids':[]}}, labels, {'a'})


if __name__ == '__main__': unittest.main()
