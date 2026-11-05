import copy
import json
import math
import sqlite3
import tempfile
import unittest
from pathlib import Path
from engine.store import Store, timestamp, available
from engine.fixtures import seed
from engine.model import snapshot, forecast, resolution, training_rows, score, locked_snapshot
from engine.ai import validate_claims, extract
from engine.ingest import import_xml
from engine.evaluate import evaluate


class TemporalTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.store = Store(Path(self.tmp.name) / 'test.sqlite')
        seed(self.store)
        self.bill = 'demo-118-hr101'
        self.cutoff = '2023-07-01'

    def tearDown(self):
        self.store.close()
        self.tmp.cleanup()

    def test_date_only_is_conservative_utc(self):
        self.assertEqual(timestamp('2023-01-01'), '2023-01-01T23:59:59Z')
        self.assertEqual(timestamp('2023-01-01T12:00:00-05:00'), '2023-01-01T17:00:00Z')
        with self.assertRaises(ValueError): timestamp('2023-01-01T12:00:00')

    def test_late_arrival_and_future_event_excluded(self):
        before = snapshot(self.store, 'demo', self.bill, self.cutoff)
        source = copy.deepcopy(before['events'][0])
        for key in ('id', 'verified_available_at', 'archive_proof'): source.pop(key, None)
        source.update(source_key='late', observed_at='2024-01-01', effective_at='2023-02-01', stage=4)
        self.store.add('event', source)
        future = dict(source, source_key='future', observed_at='2023-02-01', effective_at='2024-01-01', published_at=None)
        self.store.add('event', future)
        after = snapshot(self.store, 'demo', self.bill, self.cutoff)
        self.assertEqual(before['snapshot_hash'], after['snapshot_hash'])

    def test_backfill_requires_archive_proof(self):
        with self.assertRaises(ValueError):
            available({'observed_at':'2024-01-01','verified_available_at':'2023-01-01'})

    def test_metadata_versions_respect_cutoff(self):
        original = self.store.bill('demo', self.bill, self.cutoff)
        newer = dict(original, observed_at='2024-01-01', verified_available_at='2024-01-01', title='Future title')
        self.store.add('bill', newer)
        self.assertEqual(self.store.bill('demo', self.bill, self.cutoff)['title'], original['title'])
        self.assertEqual(self.store.bill('demo', self.bill, '2024-03-01')['title'], 'Future title')

    def test_training_prior_resolved_unique_families(self):
        target = snapshot(self.store, 'demo', self.bill, self.cutoff)
        rows = training_rows(self.store, target)
        self.assertTrue(rows)
        self.assertTrue(all(r['congress'] < 118 for r in rows))
        self.assertEqual(len(rows), len({r['family_id'] for r in rows}))
        for row in rows:
            res = resolution(self.store, 'demo', row['bill_id'], self.cutoff)
            self.assertLessEqual(available(res), timestamp(self.cutoff))
            self.assertLess(row['cutoff'], res['effective_at'])

    def test_companion_family_does_not_inflate_training(self):
        before = training_rows(self.store, snapshot(self.store, 'demo', self.bill, self.cutoff))
        source_id = 'demo-117-hr101'
        twin = 'demo-117-hr99998'
        for kind in ('bill', 'event', 'resolution'):
            for record in self.store.records(kind, 'demo', source_id):
                record = dict(record, bill_id=twin, source_key=twin + record['id'])
                self.store.add(kind, record)
        after = training_rows(self.store, snapshot(self.store, 'demo', self.bill, self.cutoff))
        self.assertEqual(len(before), len(after))
        self.assertEqual(len(after), len({r['family_id'] for r in after}))

    def test_unresolved_training_label_is_excluded(self):
        original = self.store.bill('demo', 'demo-117-hr101')
        pending_id = 'demo-117-hr99999'
        pending = dict(original, bill_id=pending_id, family_id=pending_id, source_key=pending_id)
        self.store.add('bill', pending)
        rows = training_rows(self.store, snapshot(self.store,'demo',self.bill,self.cutoff))
        self.assertNotIn(pending_id, [r['bill_id'] for r in rows])

    def test_saved_forecast_immutable_reveal_and_denominators(self):
        f = forecast(self.store, 'demo', self.bill, self.cutoff)
        self.assertEqual(f['status'], 'available')
        c = f['cohort']
        self.assertEqual(c['resolved'], len(c['rows']))
        self.assertEqual(c['successes'], sum(r['y'] for r in c['rows']))
        resolution(self.store, 'demo', self.bill)
        self.assertEqual(f, forecast(self.store, 'demo', self.bill, self.cutoff))
        with self.assertRaises(sqlite3.IntegrityError):
            self.store.db.execute('UPDATE forecasts SET issued_at=?', ('2000-01-01',))
        self.store.db.rollback()
        with self.assertRaises(sqlite3.IntegrityError):
            self.store.db.execute('DELETE FROM forecasts')
        self.store.db.rollback()

    def test_saved_inputs_survive_audited_backfill(self):
        f = forecast(self.store, 'demo', self.bill, self.cutoff)
        original = locked_snapshot(self.store, f)
        new_event = dict(original['events'][0], source_key='audited-new', text='Backfilled event', stage=3)
        self.store.add('event', new_event)
        self.assertNotEqual(snapshot(self.store, 'demo', self.bill, self.cutoff)['snapshot_hash'], f['snapshot_hash'])
        self.assertEqual(locked_snapshot(self.store, forecast(self.store, 'demo', self.bill, self.cutoff)), original)

    def test_invalid_negative_resolution_rejected(self):
        r = dict(resolution(self.store, 'demo', self.bill), value=0, complete_coverage=False)
        with self.assertRaises(ValueError): self.store.add('resolution', r)
        r.update(complete_coverage=True, effective_at='2023-01-01')
        with self.assertRaises(ValueError): self.store.add('resolution', r)

    def test_no_input_after_cutoff(self):
        f = forecast(self.store, 'demo', self.bill, self.cutoff)
        rows = self.store.records('bill','demo',self.bill,self.cutoff)+self.store.records('event','demo',self.bill,self.cutoff)
        self.assertEqual(set(f['evidence_ids']), {r['id'] for r in rows})
        self.assertTrue(all(available(r)<=timestamp(self.cutoff) for r in rows))

    def test_unavailable_not_zero(self):
        f = forecast(self.store, 'official', '119-hr1', self.cutoff)
        self.assertEqual(f['status'], 'unavailable')
        self.assertNotIn('probability', f)
        f = forecast(self.store, 'demo', self.bill, '2025-02-01')
        self.assertEqual(f['status'], 'unavailable')

    def test_model_is_deterministic(self):
        first = forecast(self.store, 'demo', self.bill, self.cutoff, persist=False)
        second = forecast(self.store, 'demo', self.bill, self.cutoff, persist=False)
        self.assertEqual(first['probability'], second['probability'])
        self.assertEqual(first['model_artifact'], second['model_artifact'])

    def test_xml_import_idempotent_and_not_backdated(self):
        xml=b'<billStatus><bill><congress>117</congress><type>HR</type><number>1</number><introducedDate>2021-01-04</introducedDate><title>Current title</title><actions><item><actionDate>2021-12-01</actionDate><actionCode>36000</actionCode><text>Became Public Law</text></item></actions></bill></billStatus>'
        a=import_xml(self.store,xml,'https://www.govinfo.gov/test','2026-01-01')
        b=import_xml(self.store,xml,'https://www.govinfo.gov/test','2026-01-02')
        self.assertEqual(a['status'],'imported');self.assertEqual(b['status'],'unchanged')
        self.assertIsNone(snapshot(self.store,'official','117-hr1','2021-12-15'))
        self.assertEqual(len(self.store.records('event','official','117-hr1')),1)
        self.assertEqual(resolution(self.store,'official','117-hr1')['value'],1)

    def test_missing_enactment_not_failure(self):
        xml=b'<billStatus><bill><congress>117</congress><type>S</type><number>1</number><introducedDate>2021-01-04</introducedDate></bill></billStatus>'
        import_xml(self.store,xml,'https://www.govinfo.gov/test','2026-01-01')
        self.assertIsNone(resolution(self.store,'official','117-s1'))

    def test_evidence_spans_fail_closed(self):
        evidence=[{'id':'a','text':'Committee reported the measure.','source_url':''}]
        self.assertEqual(len(validate_claims({'claims':[{'claim':'Reported','quote':'Committee reported','evidence_id':'a'}]},evidence)),1)
        with self.assertRaises(ValueError):
            validate_claims({'claims':[{'claim':'Enacted','quote':'Enacted into law','evidence_id':'a'}]},evidence)
        with self.assertRaises(ValueError):
            validate_claims({'claims':[{'claim':'Reported','quote':'Committee reported','evidence_id':'future'}]},evidence)

    def test_scores_and_invalid_values(self):
        result=score([.25,.75],[0,1])
        self.assertAlmostEqual(result['brier'],.0625)
        self.assertAlmostEqual(result['log_loss'],-math.log(.75))
        with self.assertRaises(ValueError):score([float('nan')],[1])
        with self.assertRaises(ValueError):score([],[])

    def test_evaluator_rejects_late_prospective_forecast(self):
        p=Path(self.tmp.name)/'p.jsonl';y=Path(self.tmp.name)/'y.jsonl'
        p.write_text(json.dumps({'bill_id':'a','family_id':'a','cutoff':'2023-01-01','issued_at':'2025-01-01','track':'prospective shadow','probability':.5})+'\n')
        y.write_text(json.dumps({'bill_id':'a','value':1,'resolved_at':'2024-01-01'})+'\n')
        with self.assertRaises(ValueError):evaluate(p,y)

if __name__=='__main__': unittest.main()
