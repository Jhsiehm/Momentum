import copy
import math
import unittest

from engine import passage90 as p


def candidate(number=1, congress=118, kind='hr', **changes):
    value = dict(bill_id=f'{kind}{number}-{congress}', congress=congress, type=kind,
                 introduced_at=f'{1787 + 2 * congress}-02-01', family_id=f'f-{congress}-{number}',
                 stage='introduced', feature_available_at=f'{1787 + 2 * congress}-02-02')
    value.update(changes)
    return value


def label(bill, value=0, **changes):
    bounds = p.window(bill)
    first = p._time(bounds['checkpoint']) + p.timedelta(days=1)
    data = dict(bill_id=bill['bill_id'], target=p.TARGET, value=value,
                first_passage_at=p._stamp(first) if value else None,
                first_passage_verified=True, complete_coverage=True,
                coverage_from=bill['introduced_at'], coverage_through=bounds['horizon'],
                available_at=bounds['horizon'], source_url='https://example.org/fixture.xml',
                source_hash='a' * 64, audit_note='Synthetic complete first-passage adjudication')
    data.update(changes)
    return data


def prepared(bills=None, values=None):
    bills = bills or [candidate(i + 1) for i in range(4)]
    values = values or [0, 1] * (len(bills) // 2)
    return p.prepare(bills, [label(b, v) for b, v in zip(bills, values)], '2026-11-12', mode='synthetic')


def predictions(rows, model=0.2, baseline=0.3):
    return {name: [dict(bill_id=r['bill_id'], probability=probability, target=p.TARGET,
                       checkpoint=r['checkpoint']) for r in rows]
            for name, probability in [('structured', model), ('stage_reference', baseline)]}


class Passage90Tests(unittest.TestCase):
    def test_exact_window_and_date_only_convention(self):
        result = p.window(candidate())
        self.assertEqual(result['checkpoint'], '2023-03-03T23:59:59Z')
        self.assertEqual(result['horizon'], '2023-06-01T23:59:59Z')
        self.assertTrue(result['full_window'])

    def test_timezone_precision_preserved(self):
        bounds = p.window(candidate(introduced_at='2023-02-01T00:00:00.500-05:00'))
        self.assertEqual(bounds['checkpoint'], '2023-03-03T05:00:00.500000Z')

    def test_bad_identity_or_introduction_rejected(self):
        for changes in [dict(bill_id='s1-118'), dict(type='hjres'), dict(congress=True),
                        dict(introduced_at='2022-12-01'), dict(introduced_at='2025-01-04'),
                        dict(introduced_at='2023-02-01T12:00:00')]:
            with self.subTest(changes=changes), self.assertRaises(ValueError):
                p.window(candidate(**changes))

    def test_late_congress_kept_with_disposition(self):
        bill = candidate(introduced_at='2024-11-12')
        report = p.prepare([bill], [], '2026-11-12')
        self.assertEqual(report['counts'], {'incomplete_90_day_window': 1})
        self.assertEqual(report['inventory_count'], 1)
        self.assertFalse(report['rows'])

    def test_full_inventory_unknown_is_never_negative(self):
        bills = [candidate(1), candidate(2), candidate(3, family_id='')]
        report = p.prepare(bills, [label(bills[0])], '2026-11-12')
        self.assertEqual(report['counts'], {'eligible': 1, 'invalid_evidence': 1, 'missing_label': 1})
        self.assertEqual(len(report['dispositions']), 3)
        self.assertEqual(len(report['rows']), 1)

    def test_missing_stage_retained_as_unknown(self):
        bill = candidate()
        del bill['stage']
        self.assertEqual(prepared([bill], [0])['rows'][0]['stage'], 'unknown')

    def test_duplicate_and_foreign_identities_rejected(self):
        bill = candidate()
        for candidates, labels in [([bill, bill], []), ([bill], [label(bill)] * 2),
                                   ([bill], [label(candidate(2))])]:
            with self.assertRaises(ValueError):
                p.prepare(candidates, labels, '2026-11-12')

    def test_empty_inventory_is_not_success(self):
        report = p.prepare([], [], '2026-11-12')
        self.assertEqual(report['inventory_count'], 0)
        self.assertFalse(report['release_eligible'])

    def test_first_passage_before_checkpoint_excluded(self):
        bill = candidate()
        outcome = label(bill, 1, first_passage_at='2023-02-15')
        report = p.prepare([bill], [outcome], '2026-11-12')
        self.assertEqual(report['counts'], {'already_passed': 1})

    def test_date_only_boundary_uncertainty_preserved(self):
        bill = candidate()
        for date in ['2023-03-03', '2023-06-01']:
            report = p.prepare([bill], [label(bill, 1, first_passage_at=date)], '2026-11-12')
            self.assertEqual(report['counts'], {'boundary_ambiguous': 1})

    def test_precise_horizon_inclusive_checkpoint_exclusive(self):
        bill = candidate()
        bounds = p.window(bill)
        end = p.prepare([bill], [label(bill, 1, first_passage_at=bounds['horizon'])], '2026-11-12')
        start = p.prepare([bill], [label(bill, 1, first_passage_at=bounds['checkpoint'])], '2026-11-12')
        self.assertEqual(end['counts'], {'eligible': 1})
        self.assertEqual(start['counts'], {'already_passed': 1})

    def test_missing_complete_history_cannot_manufacture_negative(self):
        bill = candidate()
        changes_list = [dict(complete_coverage=False), dict(first_passage_verified=False),
                        dict(coverage_through='2023-05-01'), dict(coverage_from='2023-02-03'),
                        dict(available_at='2023-05-01'), dict(value=False), dict(source_hash='fake'),
                        dict(target='originating_chamber_passage_by_congress_end'),
                        dict(first_passage_at='2023-04-01')]
        for changes in changes_list:
            with self.subTest(changes=changes):
                report = p.prepare([bill], [label(bill, **changes)], '2026-11-12')
                self.assertEqual(report['counts'], {'invalid_evidence': 1})
                self.assertFalse(report['rows'])

    def test_future_label_never_used(self):
        bill = candidate()
        report = p.prepare([bill], [label(bill, available_at='2027-01-01')], '2026-11-12')
        self.assertEqual(report['counts'], {'label_pending': 1})

    def test_unmatured_horizon_never_scored(self):
        bill = candidate()
        outcome = label(bill, 1, coverage_through='2023-04-01', available_at='2023-04-01')
        report = p.prepare([bill], [outcome], '2023-04-02')
        self.assertEqual(report['counts'], {'horizon_pending': 1})

    def test_retrospective_availability_not_certification(self):
        bill = candidate(feature_available_at='2026-11-12')
        report = p.prepare([bill], [label(bill)], '2026-11-12')
        self.assertEqual(len(report['rows']), 1)
        self.assertFalse(report['rows'][0]['availability_asserted_by_checkpoint'])
        self.assertFalse(report['certified_historical'])
        self.assertFalse(report['certified_prospective'])
        with self.assertRaises(ValueError):
            p.prepare([bill], [label(bill)], '2026-11-12', mode='prospective')

    def test_forward_split_checks_label_timing_and_families(self):
        bills = [candidate(1, 117, family_id='shared'), candidate(2, 117), candidate(3, 117),
                 candidate(4, 118, family_id='shared'), candidate(5, 118)]
        outcomes = [label(b, i % 2) for i, b in enumerate(bills)]
        outcomes[1]['available_at'] = '2024-01-01'
        rows = p.prepare(bills, outcomes, '2026-11-12', 'synthetic')['rows']
        result = p.chronological_split(rows, 118)
        self.assertEqual([r['bill_id'] for r in result['train']], ['hr3-117'])
        self.assertEqual({r['reason'] for r in result['exclusions']},
                         {'evaluation_family_overlap', 'label_unavailable_at_training_origin'})

    def test_future_evaluation_families_reserved_before_training(self):
        bills = [candidate(1, 116, family_id='future'), candidate(2, 117),
                 candidate(3, 118, family_id='future')]
        rows = p.prepare(bills, [label(b, i % 2) for i, b in enumerate(bills)], '2026-11-12', 'synthetic')['rows']
        result = p.chronological_split(rows, 117)
        self.assertFalse(result['train'])
        self.assertEqual(result['exclusions'][0]['reason'], 'evaluation_family_overlap')

    def test_reference_exact_shrinkage_and_empty_group_fallback(self):
        rows = prepared([candidate(1, 117), candidate(2, 117)], [0, 1])['rows']
        artifact = p.fit_reference(rows)
        self.assertEqual(artifact['global_rate'], 0.5)
        self.assertEqual(artifact['groups']['house:introduced']['probability'], 0.5)
        evaluation = prepared([candidate(9, 118, kind='s', stage='unknown')], [0])['rows'][0]
        self.assertEqual(p.predict_reference(artifact, evaluation), 0.5)

    def test_reference_rejects_one_class_empty_and_duplicate_families(self):
        rows = prepared()['rows']
        for values in [[], rows[:1], [rows[0], dict(rows[1], family_id=rows[0]['family_id'])]]:
            with self.assertRaises(ValueError):
                p.fit_reference(values)

    def test_reference_rejects_tamper_overlap_and_temporal_leak(self):
        train = prepared([candidate(1, 117), candidate(2, 117)], [0, 1])['rows']
        artifact = p.fit_reference(train)
        evaluation = prepared([candidate(3, 118)], [0])['rows'][0]
        altered = copy.deepcopy(artifact)
        altered['global_rate'] = 0.99
        with self.assertRaises(ValueError):
            p.predict_reference(altered, evaluation)
        for row in [train[0], dict(evaluation, family_id=train[0]['family_id'])]:
            with self.assertRaises(ValueError):
                p.predict_reference(artifact, row)
        train[0]['label_available_at'] = '2024-01-01'
        artifact = p.fit_reference(train)
        with self.assertRaises(ValueError):
            p.predict_reference(artifact, evaluation)

    def test_training_evidence_mode_cannot_cross_to_real_rows(self):
        train = prepared([candidate(1, 117), candidate(2, 117)], [0, 1])['rows']
        artifact = p.fit_reference(train)
        row = prepared([candidate(9, 118)], [0])['rows'][0]
        row['evidence_mode'] = 'retrospective'
        with self.assertRaises(ValueError):
            p.predict_reference(artifact, row)

    def test_tampered_row_dates_rejected(self):
        rows = prepared()['rows']
        changes = [dict(checkpoint='2021-03-03', horizon='2021-06-01'),
                   dict(label_effective_at='2023-04-01'),
                   dict(label_available_at='2023-01-01'),
                   dict(checkpoint='2023-02-01', horizon='2023-05-02')]
        for change in changes:
            altered = copy.deepcopy(rows)
            altered[0].update(change)
            with self.subTest(change=change), self.assertRaises(ValueError):
                p.evaluate_paired(altered, predictions(altered), bootstrap_draws=10)

    def test_one_class_evaluation_is_explicitly_inconclusive(self):
        rows = prepared([candidate(1), candidate(2)], [0, 0])['rows']
        report = p.evaluate_paired(rows, predictions(rows, .01, .99), bootstrap_draws=10)
        self.assertEqual(report['diagnostic_status'], 'inconclusive_one_class')
        self.assertFalse(report['independent_success'])
        self.assertIsNone(report['by_period']['118']['structured']['top_k']['recall'])

    def test_reference_time_bucket_uses_hierarchical_shrinkage(self):
        bills = [candidate(1, 117), candidate(2, 117, introduced_at='2022-02-01'),
                 candidate(3, 117, stage='reported')]
        rows = prepared(bills, [0, 0, 1])['rows']
        artifact = p.fit_reference(rows)
        self.assertAlmostEqual(artifact['global_rate'], 2 / 5)
        stage_rate = 2 / 7
        self.assertAlmostEqual(artifact['groups']['house:introduced']['probability'], stage_rate)
        self.assertAlmostEqual(artifact['time_groups']['house:introduced:90_to_365_days']['probability'],
                               5 * stage_rate / 6)
        self.assertEqual(p.remaining_time_band(rows[0]), 'over_365_days')
        self.assertEqual(p.remaining_time_band(rows[1]), '90_to_365_days')

    def test_metrics_match_manual_arithmetic(self):
        rows = prepared()['rows']
        report = p.evaluate_paired(rows, predictions(rows), bootstrap_draws=50, top_k=2)
        metric = report['by_period']['118']['structured']
        self.assertAlmostEqual(metric['brier'], 0.34)
        self.assertEqual(metric['class_metrics']['negative']['n'], 2)
        self.assertEqual(metric['class_metrics']['positive']['n'], 2)
        self.assertAlmostEqual(metric['class_metrics']['negative']['brier'], 0.04)
        self.assertAlmostEqual(metric['class_metrics']['positive']['brier'], 0.64)
        self.assertAlmostEqual(metric['log_loss'], -(math.log(0.2) + math.log(0.8)) / 2)
        self.assertEqual(metric['top_k']['bill_ids'], ['hr1-118', 'hr2-118'])
        self.assertEqual(metric['top_k']['recall'], 0.5)
        self.assertEqual(metric['reliability_bins'][2]['n'], 4)
        self.assertAlmostEqual(report['practical_2pct_contrast'], .34 - .98 * .29)
        self.assertFalse(report['independent_success'])
        self.assertFalse(report['release_eligible'])

    def test_prediction_missing_extra_duplicate_target_and_time_rejected(self):
        rows = prepared()['rows']
        changed = []
        a = predictions(rows); a['structured'].pop(); changed.append(a)
        a = predictions(rows); a['structured'].append(a['structured'][0]); changed.append(a)
        a = predictions(rows); a['structured'][0]['target'] = 'enactment'; changed.append(a)
        a = predictions(rows); a['structured'][0]['checkpoint'] = '2023-04-01'; changed.append(a)
        a = predictions(rows); a['structured'][0]['bill_id'] = 'hr999-118'; changed.append(a)
        for values in changed:
            with self.assertRaises(ValueError):
                p.evaluate_paired(rows, values, bootstrap_draws=10)

    def test_nonfinite_and_boolean_probabilities_rejected(self):
        rows = prepared()['rows']
        for bad in [float('nan'), float('inf'), -.01, 1.01, True, '0.2']:
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                p.evaluate_paired(rows, predictions(rows, bad), bootstrap_draws=10)

    def test_empty_and_mixed_populations_rejected(self):
        with self.assertRaises(ValueError):
            p.evaluate_paired([], {}, bootstrap_draws=10)
        rows = prepared()['rows']
        rows[0]['evidence_mode'] = 'retrospective'
        with self.assertRaises(ValueError):
            p.evaluate_paired(rows, predictions(rows), bootstrap_draws=10)

    def test_perfect_reference_skill_undefined(self):
        rows = prepared()['rows']
        values = predictions(rows)
        for item, row in zip(values['stage_reference'], rows):
            item['probability'] = row['y']
        report = p.evaluate_paired(rows, values, bootstrap_draws=10)
        self.assertIsNone(report['brier_skill'])

    def test_family_bootstrap_is_reproducible(self):
        rows = prepared()['rows']
        rows[1]['family_id'] = rows[0]['family_id']
        first = p.evaluate_paired(rows, predictions(rows), bootstrap_draws=100, evaluation_as_of='2026-11-12')
        second = p.evaluate_paired(rows, predictions(rows), bootstrap_draws=100, evaluation_as_of='2026-11-12')
        self.assertEqual(first, second)
        self.assertEqual(first['family_count'], 3)

    def test_registered_bootstrap_draws_are_executed(self):
        rows = prepared()['rows']
        report = p.evaluate_paired(rows, predictions(rows), evaluation_as_of='2026-11-12')
        self.assertEqual(report['bootstrap']['valid'], 10000)
        self.assertTrue(report['bootstrap']['registered_draw_count'])
        self.assertTrue(report['bootstrap']['valid_draw_floor_met'])
        self.assertEqual(len(report['bootstrap']['intervals_95pct']['practical_2pct_contrast']), 2)

    def test_real_evaluation_rejects_future_and_immature_cutoffs(self):
        bills = [candidate(1), candidate(2)]
        rows = p.prepare(bills, [label(bills[0]), label(bills[1], 1)], '2026-11-12')['rows']
        for cutoff in ('2999-01-01', '2023-03-15'):
            with self.subTest(cutoff=cutoff), self.assertRaises(ValueError):
                p.evaluate_paired(rows, predictions(rows), bootstrap_draws=10, evaluation_as_of=cutoff)
        result = p.evaluate_paired(rows, predictions(rows), bootstrap_draws=10, evaluation_as_of='2026-11-12')
        self.assertEqual(result['evaluation_as_of'], '2026-11-12T23:59:59Z')

    def test_periods_have_equal_weight_not_pooled_weight(self):
        bills = [candidate(1, 117), candidate(2, 117), candidate(3, 118)]
        rows = prepared(bills, [0, 0, 1])['rows']
        result = p.evaluate_paired(rows, predictions(rows, .2, .3), bootstrap_draws=100)
        self.assertAlmostEqual(result['equal_period_means']['structured']['brier'], .34)
        self.assertLess(result['bootstrap']['valid'], 100)
        self.assertAlmostEqual(result['pooled_metrics']['structured']['brier'], (0.04 + 0.04 + 0.64) / 3)
        self.assertEqual(result['pooled_metrics']['structured']['n'], 3)


if __name__ == '__main__':
    unittest.main()
