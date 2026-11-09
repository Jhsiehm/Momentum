import copy
import unittest
from scripts.freeze_matched_text_comparison_v1 import memberships_only, specification, freeze


def source():
    return {'memberships': {str(c): {'core_ids': ['113-hr1'], 'calibration_ids': ['113-s2'],
                                   'evaluation_ids': [f'{c}-hr3']} for c in (115, 116, 117)}}


class MatchedTextSpecificationTests(unittest.TestCase):
    def test_blocked_and_no_outcomes_or_label_counts(self):
        value = specification(source())
        self.assertFalse(value['predictive_execution_permitted'])
        self.assertEqual(value['actual_fits'], 0)
        self.assertIsNone(value['eligible_memberships'])
        self.assertIsNone(value['eligible_counts'])
        self.assertTrue(all(not gate['satisfied'] for gate in value['gates'].values()))
        self.assertNotIn('outcomes', value)

    def test_fixed_six_fits_and_original_parameters(self):
        value = specification(source())
        self.assertEqual((value['fit_cap'], len(value['arms']), value['wallclock_cap_seconds']), (6, 2, 21600))
        self.assertEqual(value['text']['ngram_range'], [1, 2])
        self.assertEqual(value['text']['min_df'], 5)
        self.assertEqual(value['text']['max_df'], .95)
        self.assertEqual(value['text']['max_features'], 10000)
        self.assertEqual(value['objective']['slope_l2'], .05)
        self.assertEqual(value['solver']['max_absolute_gradient'], 1e-6)
        self.assertEqual(value['solver']['max_iterations'], 20000)
        self.assertIsNone(value['solver']['minimum_iterations'])
        self.assertEqual(value['uncertainty']['seed'], 20261105)

    def test_identity_snapshot_deterministic_and_nonmutating(self):
        original = source(); before = copy.deepcopy(original)
        first = specification(original)
        self.assertEqual(first, specification(original))
        self.assertEqual(original, before)
        first['planned_memberships']['115']['core_ids'].append('113-hr9')
        self.assertEqual(original, before)

    def test_extra_top_level_outcomes_never_copied(self):
        original = source(); original['outcomes'] = 'DO NOT COPY'
        self.assertEqual(specification(original), specification(source()))

    def test_duplicate_and_role_overlap_rejected(self):
        for role, ids in [('core_ids', ['113-hr1', '113-hr1']), ('calibration_ids', ['113-hr1'])]:
            original = source(); original['memberships']['115'][role] = ids
            with self.assertRaises(ValueError): memberships_only(original)

    def test_missing_fold_empty_role_and_extra_fields_rejected(self):
        originals = [source() for _ in range(3)]
        del originals[0]['memberships']['117']
        originals[1]['memberships']['115']['core_ids'] = []
        originals[2]['memberships']['115']['outcomes'] = [0]
        for original in originals:
            with self.assertRaises(ValueError): memberships_only(original)

    def test_future_training_wrong_evaluation_and_bad_id_rejected(self):
        for role, identity in [('core_ids', '115-hr1'), ('evaluation_ids', '114-hr3'), ('core_ids', '113-hres1')]:
            original = source(); original['memberships']['115'][role] = [identity]
            with self.assertRaises(ValueError): memberships_only(original)

    def test_protected_output_path_rejected(self):
        with self.assertRaises(ValueError): freeze('/tmp/not-a-momentum-study')
