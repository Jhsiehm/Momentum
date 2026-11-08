import unittest
from scripts.mechanism_corrections_audit import validate_changes


class CorrectionTests(unittest.TestCase):
    def setUp(self):
        self.original = {'records': [{'bill_id': '113-s1', 'value': 'uncertain'}, {'bill_id': '113-s2', 'value': 'absent'}]}
        self.corrected = {'records': [{'bill_id': '113-s1', 'value': 'present'}, {'bill_id': '113-s2', 'value': 'absent'}]}
        self.expected = {'peer:agent_b:113-s1:0': '113-s1'}
        self.changes = [{'bill_id': '113-s1', 'description': 'Apply supported scope correction.', 'source_finding_ids': list(self.expected)}]

    def test_bound_correction_and_retained_uncertainty(self):
        self.assertEqual(validate_changes(self.original, self.corrected, self.changes, self.expected), 1)
        self.assertEqual(validate_changes(self.original, self.original, self.changes, self.expected), 0)

    def test_missing_duplicate_or_wrong_reference_rejected(self):
        for changes in ([], self.changes*2, [dict(self.changes[0], bill_id='113-s2')]):
            with self.assertRaises(ValueError): validate_changes(self.original, self.corrected, changes, self.expected)

    def test_undocumented_change_or_population_rejected(self):
        self.corrected['records'][1]['value'] = 'present'
        with self.assertRaisesRegex(ValueError, 'Undocumented'): validate_changes(self.original, self.corrected, self.changes, self.expected)
        self.corrected['records'].pop()
        with self.assertRaisesRegex(ValueError, 'population'): validate_changes(self.original, self.corrected, self.changes, self.expected)


if __name__ == '__main__': unittest.main()
