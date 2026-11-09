"""Independent synthetic helper checks; no real labels, text or model fits."""
import copy
import math
import unittest

import numpy as np

from scripts.retrospective_text_diagnostic_v1 import bootstrap, metric, select_memberships


def fixture():
    sources = {bid: {'bill_id': bid, 'congress': int(bid.split('-')[0]), 'family_id': 'family-' + bid}
               for bid in ('113-hr1', '114-s2', '115-hr3', '116-s4', '113-s5')}
    memberships = {
        '115': {'core_ids': ['113-hr1', '113-s5'], 'calibration_ids': ['114-s2'],
                'evaluation_ids': ['115-hr3']},
        '116': {'core_ids': ['113-hr1', '115-hr3'], 'calibration_ids': ['114-s2'],
                'evaluation_ids': ['116-s4']},
    }
    return memberships, sources


def prediction(family, outcome, text, anchor, rate=.3, stage=.4):
    return dict(family_id=family, outcome=outcome, text=text,
                anchor=anchor, rate=rate, stage=stage)


class RetrospectiveMembershipTests(unittest.TestCase):
    def test_order_merge_and_input_immutability(self):
        memberships, sources = fixture()
        before = copy.deepcopy((memberships, sources))
        result = select_memberships(memberships, sources, set(), set())
        self.assertEqual(result['115']['train'], ['113-hr1', '113-s5', '114-s2'])
        self.assertEqual(result['115']['evaluation'], ['115-hr3'])
        self.assertEqual((memberships, sources), before)

    def test_source_intersection_and_identity_exclusion(self):
        memberships, sources = fixture()
        del sources['113-s5']
        result = select_memberships(memberships, sources, {'114-s2'}, set())
        self.assertEqual(result['115']['train'], ['113-hr1'])
        self.assertEqual(result['116']['train'], ['113-hr1', '115-hr3'])

    def test_whole_family_exclusion(self):
        memberships, sources = fixture()
        sources['113-s5']['family_id'] = sources['113-hr1']['family_id']
        result = select_memberships(memberships, sources, set(), {'family-113-hr1'})
        self.assertEqual(result['115']['train'], ['114-s2'])

    def test_duplicate_role_identity_rejected(self):
        memberships, sources = fixture()
        memberships['115']['calibration_ids'].append('113-hr1')
        with self.assertRaises(ValueError):
            select_memberships(memberships, sources, set(), set())

    def test_same_partition_family_duplicates_rejected(self):
        memberships, sources = fixture()
        sources['113-s5']['family_id'] = sources['113-hr1']['family_id']
        with self.assertRaises(ValueError):
            select_memberships(memberships, sources, set(), set())

    def test_cross_partition_family_overlap_rejected(self):
        memberships, sources = fixture()
        sources['115-hr3']['family_id'] = sources['113-hr1']['family_id']
        with self.assertRaises(ValueError):
            select_memberships(memberships, sources, set(), set())

    def test_future_training_identity_rejected_before_labels(self):
        memberships, sources = fixture()
        memberships['115']['core_ids'] = ['116-s4']
        with self.assertRaises(ValueError):
            select_memberships(memberships, sources, set(), set())

    def test_wrong_evaluation_congress_rejected_before_labels(self):
        memberships, sources = fixture()
        memberships['115']['evaluation_ids'] = ['116-s4']
        with self.assertRaises(ValueError):
            select_memberships(memberships, sources, set(), set())


class RetrospectiveMetricTests(unittest.TestCase):
    def test_exact_scalar_losses_and_counts(self):
        p, y = [.2, .7, .4], [0, 1, 0]
        result = metric(p, y)
        self.assertEqual((result['n'], result['positives']), (3, 1))
        self.assertAlmostEqual(result['brier'], (.04 + .09 + .16) / 3)
        self.assertAlmostEqual(result['log_loss'], -(math.log(.8) + math.log(.7) + math.log(.6)) / 3)
        self.assertAlmostEqual(result['expected_events'], 1.3)
        self.assertAlmostEqual(result['by_outcome']['0']['brier'], .1)
        self.assertAlmostEqual(result['by_outcome']['1']['brier'], .09)

    def test_boundary_bins_and_empty_class(self):
        result = metric([0, .1, .9, 1], [0, 0, 0, 0])
        self.assertEqual([b['n'] for b in result['reliability']], [1, 1, 0, 0, 0, 0, 0, 0, 0, 2])
        self.assertEqual(result['by_outcome']['1'], {'n': 0, 'brier': None})
        self.assertEqual(result['reliability'][2]['predicted'], None)
        self.assertTrue(math.isfinite(result['log_loss']))

    def test_invalid_metric_arguments(self):
        for p, y in [([], []), ([.1], []), ([[.1]], [[0]]), ([float('nan')], [0]),
                     ([float('inf')], [0]), ([1.01], [1]), ([-.01], [0]), ([.1], [2]), ([.1], [float('nan')])]:
            with self.subTest(p=p, y=y), self.assertRaises(ValueError):
                metric(p, y)


class RetrospectiveBootstrapTests(unittest.TestCase):
    def test_zero_paired_difference_is_zero(self):
        folds = [{'predictions': [prediction('a', 0, .2, .2, .2, .2)]},
                 {'predictions': [prediction('a', 1, .8, .8, .8, .8)]}]
        result = bootstrap(folds, draws=100)
        self.assertEqual((result['valid'], result['invalid'], result['global_families']), (100, 0, 1))
        self.assertTrue(all(bounds == [0., 0.] for bounds in result['intervals'].values()))

    def test_shared_family_weights_and_equal_fold_aggregation(self):
        folds = [
            {'predictions': [prediction('a', 0, .1, .5), prediction('b', 1, .7, .4)]},
            {'predictions': [prediction('a', 1, .9, .2), prediction('b', 0, .8, .3)]},
        ]
        before = copy.deepcopy(folds)
        result = bootstrap(folds, draws=250)
        rng = np.random.default_rng(20261108)
        manual = []
        for _ in range(250):
            weights = rng.multinomial(2, [.5, .5])
            effects = []
            for fold in folds:
                effects.append(sum(weights[i] * ((r['text'] - r['outcome']) ** 2 -
                                                (r['anchor'] - r['outcome']) ** 2)
                                   for i, r in enumerate(fold['predictions'])) / 2)
            manual.append(sum(effects) / 2)
        np.testing.assert_allclose(result['intervals']['text_minus_anchor'], np.quantile(manual, [.025, .975]))
        self.assertEqual(folds, before)
        self.assertEqual(result, bootstrap(folds, draws=250))

    def test_insufficient_valid_draws_suppresses_intervals(self):
        folds = [{'predictions': [prediction('a', 0, .2, .4)]},
                 {'predictions': [prediction('b', 1, .7, .5)]}]
        result = bootstrap(folds, draws=200)
        self.assertEqual(result['valid'] + result['invalid'], 200)
        self.assertLess(result['valid'], 180)
        self.assertIsNone(result['intervals'])

    def test_empty_partitions_and_invalid_draws_rejected(self):
        good = [{'predictions': [prediction('a', 0, .2, .4)]}]
        for folds, draws in [([], 100), ([{'predictions': []}], 100), (good, 0), (good, -1), (good, 1.5), (good, True)]:
            with self.subTest(folds=folds, draws=draws), self.assertRaises(ValueError):
                bootstrap(folds, draws=draws)
