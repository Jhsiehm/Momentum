import copy
import tempfile
import unittest
from pathlib import Path
from engine.store import Store, congress_end
from engine.sequential import TARGET, benchmark, prepare


class SequentialTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.store = Store(Path(self.temp.name) / 'test.sqlite')
        self.labels = []
        for congress in range(110, 115):
            year = 1787 + 2 * congress
            for i in range(24):
                bid = f'hr{i+1}-{congress}'
                introduced = f'{year}-02-01T12:00:00Z'
                self.store.add('bill', dict(bill_id=bid, family_id=bid, dataset='demo',
                    congress=congress, type='hr', title=f'Bill {i}', introduced_at=introduced,
                    effective_at=introduced, observed_at=introduced, source_url='https://example.org', source_name='fixture'))
                self.labels.append(dict(bill_id=bid, target=TARGET, value=i % 2,
                    effective_at=f'{year}-06-01T12:00:00Z' if i % 2 else congress_end(congress),
                    available_at=congress_end(congress), complete_coverage=True,
                    coverage_through=congress_end(congress), source_url='https://example.org',
                    source_hash='synthetic-fixture', audit_note='Synthetic only'))

    def tearDown(self):
        self.store.close()
        self.temp.cleanup()

    def run_benchmark(self, labels=None):
        return benchmark(self.store, 'demo', labels or self.labels, 110, 113, 114, '2026-11-05')

    def test_forward_learning_and_reproducibility(self):
        report = self.run_benchmark()
        self.assertEqual(report['status'], 'completed')
        self.assertEqual([f['training_count'] for f in report['folds']], [72, 96])
        self.assertEqual(report['id'], self.run_benchmark()['id'])
        self.assertFalse(report['release_eligible'])
        for fold in report['folds']:
            self.assertEqual({m['n'] for m in fold['metrics'].values()}, {24})
            self.assertTrue(all(r['congress'] < fold['congress'] for r in fold['training_manifest']))

    def test_target_outcomes_do_not_select_models(self):
        before = self.run_benchmark()
        changed = copy.deepcopy(self.labels)
        for label in changed:
            if label['bill_id'].endswith('-114'):
                label['value'] = 1 - label['value']
                label['effective_at'] = congress_end(114)
        after = self.run_benchmark(changed)
        self.assertEqual(before['folds'][1]['artifacts'], after['folds'][1]['artifacts'])
        self.assertEqual(before['folds'][1]['selection'], after['folds'][1]['selection'])
        self.assertEqual([p['adaptive'] for p in before['folds'][1]['predictions']],
                         [p['adaptive'] for p in after['folds'][1]['predictions']])

    def test_delayed_labels_not_used_for_training(self):
        changed = copy.deepcopy(self.labels)
        for label in changed:
            if label['bill_id'].endswith('-112'):
                label['available_at'] = '2020-01-01'
        report = self.run_benchmark(changed)
        self.assertEqual(report['folds'][0]['training_count'], 48)

    def test_invalid_negatives_and_duplicate_labels_rejected(self):
        changed = copy.deepcopy(self.labels)
        changed[0]['complete_coverage'] = False
        with self.assertRaises(ValueError):
            self.run_benchmark(changed)
        with self.assertRaises(ValueError):
            self.run_benchmark(self.labels + self.labels[:1])

    def test_early_passage_excluded_and_missing_labels_reported(self):
        changed = copy.deepcopy(self.labels[:2])
        changed[1]['effective_at'] = '2007-02-02'
        rows, exclusions = prepare(self.store, 'demo', changed, '2026-11-05')
        self.assertEqual(len(rows), 1)
        self.assertEqual(exclusions[0]['reason'], 'already_passed_at_checkpoint')
        self.assertEqual(sum(r['reason'] == 'missing_passage_label' for r in exclusions), 118)

    def test_sparse_data_blocks(self):
        report = self.run_benchmark(self.labels[-24:])
        self.assertEqual(report['status'], 'incomplete')
        self.assertTrue(all(f['status'] == 'blocked' for f in report['folds']))

    def test_unfinished_congress_is_blocked(self):
        report = benchmark(self.store, 'demo', self.labels, 110, 113, 114, '2015-08-01')
        self.assertEqual(report['folds'][1]['status'], 'blocked')
        self.assertIn('has not ended', report['folds'][1]['reason'])

    def test_family_overlap_excluded(self):
        bill = self.store.bill('demo', 'hr1-110')
        bill['family_id'] = 'hr1-113'
        bill['observed_at'] = '2007-02-02T12:00:00Z'
        self.store.add('bill', bill)
        report = self.run_benchmark()
        self.assertNotIn('hr1-113', {r['family_id'] for r in report['frozen_training_manifest']})
        self.assertNotIn('hr1-113', {r['family_id'] for r in report['folds'][0]['training_manifest']})
