import json
import sqlite3
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from engine import intelligence, prospective
from engine.store import Store, digest

NOW='2026-11-03T12:00:00Z'

class IntelligenceTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.store=Store(Path(self.tmp.name)/'db')
        self.clock=patch('engine.intelligence.now',return_value=NOW);self.clock.start()
        self.base=dict(dataset='official',source_url='https://www.govinfo.gov/example',source_name='GovInfo',effective_at='2025-01-03',observed_at='2025-01-04',introduced_at='2025-01-03',title='Energy Research Act',topic='Energy',congress=119,type='hr')
        for i in range(1,4):self.add_bill(i)
    def tearDown(self):self.clock.stop();self.store.close();self.tmp.cleanup()
    def add_bill(self,i,**kw):
        return self.store.add('bill',dict(self.base,bill_id=f'119-hr{i}',family_id=f'119-hr{i}',source_key=f'b{i}',**kw))
    def resolution(self,i):
        self.store.add('resolution',dict(self.base,bill_id=f'119-hr{i}',family_id=f'119-hr{i}',value=1,effective_at='2026-10-01',observed_at='2026-10-02'))
    def test_unknown_outcomes_overlap_and_bounded_display(self):
        self.resolution(1)
        r=intelligence.analyze(self.store,dict(limit=1,groups=[dict(name='Energy',filters={'topics':['Energy']}),dict(name='Selected',filters={'bill_ids':['119-hr1','119-hr2']})]))
        self.assertEqual(r['summary']['unknown'],2);self.assertEqual(r['summary']['observed_rate'],1)
        self.assertEqual(r['summary']['not_enacted'],0);self.assertEqual(len(r['rows']),1)
        self.assertEqual(r['overlaps'][-1]['total'],2);self.assertEqual(r['coverage']['matched'],3)
        self.assertEqual(sum(g['total'] for g in r['overlaps']),3)
        self.assertEqual(r['overlaps'][0]['groups'],[]);self.assertEqual(r['overlaps'][0]['total'],0)
        self.assertEqual(next(g for g in r['overlaps'] if g['groups']==['Energy'])['total'],1)
        self.assertEqual(len(r['frozen_rows']),3)
    def test_cutoff_prevents_later_outcomes_and_later_metadata(self):
        self.resolution(1);self.add_bill(4,observed_at='2026-10-02')
        r=intelligence.analyze(self.store,{'cutoff':'2026-09-01'})
        self.assertEqual(r['summary']['total'],3);self.assertEqual(r['summary']['resolved'],0)
    def test_reports_immutable_and_content_reproducible(self):
        a=intelligence.analyze(self.store,{});b=intelligence.analyze(self.store,{})
        self.assertEqual(a,b);self.assertEqual(len(intelligence.reports(self.store)),1)
        payload={k:v for k,v in a.items() if k not in ('id','content_hash','created_at')}
        self.assertEqual(digest(payload),a['content_hash'])
        with self.assertRaises(sqlite3.IntegrityError):self.store.db.execute('UPDATE intelligence_reports SET kind=?',('changed',))
        self.store.db.rollback()
        with self.assertRaises(sqlite3.IntegrityError):
            self.store.db.execute('INSERT OR REPLACE INTO intelligence_reports VALUES (?,?,?,?)',(a['id'],NOW,'forged','{}'))
        self.store.db.rollback()
        self.assertEqual(intelligence.report(self.store,a['id']),a)
    def receipt(self,bid,**kw):
        prospective.initialize(self.store)
        b=self.store.bill('official',bid)
        r=dict(id='receipt-'+bid,identity='receipt-'+bid,bill_id=bid,dataset='official',issued_at=NOW,cutoff=NOW,status='captured',prospective_eligible=True,synthetic=False,
               forecast=dict(status='available',probability=.2,target='Enactment by Congress end',deadline='2027-01-03T17:00:00Z',model_version='m1',feature_version='f1',calibration_version='none',cutoff=NOW),source_records=[dict(id=b['id'],bill_id=bid)])
        r.update(kw)
        with self.store.db:self.store.db.execute('INSERT INTO prospective_receipts VALUES (?,?,?,?,?,?)',(r['id'],r['identity'],'official',bid,r['issued_at'],json.dumps(r)))
        return r
    def test_ranking_excludes_missing_resolved_and_stale_receipts(self):
        self.receipt('119-hr1');self.receipt('119-hr2',issued_at='2026-09-01T12:00:00Z')
        r=intelligence.rank(self.store,{})
        self.assertEqual(r['eligible'],1);self.assertEqual(r['excluded'],{'stale_receipt':1,'no_saved_receipt':1})
        self.assertFalse(r['release_eligible']);self.assertEqual(r['groups'][0]['rows'][0]['probability'],.2)
        self.resolution(1);r=intelligence.rank(self.store,{})
        self.assertEqual(r['eligible'],0);self.assertIn('resolved_or_congress_ended',r['excluded'])
    def test_ranking_keeps_different_models_separate_and_rejects_demo(self):
        a=self.receipt('119-hr1')
        self.receipt('119-hr2',forecast={**a['forecast'],'model_version':'different-model','probability':.8})
        self.receipt('119-hr3',synthetic=True)
        r=intelligence.rank(self.store,{})
        self.assertEqual(r['eligible'],2);self.assertEqual(len(r['groups']),2)
        self.assertEqual(r['excluded']['not_eligible_prospective'],1)
        self.assertTrue(all(g['total']==1 for g in r['groups']))

    def test_ranking_new_evidence_invalidates_old_receipt(self):
        self.receipt('119-hr1')
        self.store.add('event',dict(self.base,bill_id='119-hr1',family_id='119-hr1',stage=1,text='Committee action',effective_at='2026-11-02',observed_at='2026-11-02'))
        r=intelligence.rank(self.store,{})
        self.assertEqual(r['eligible'],0);self.assertEqual(r['excluded']['changed_evidence'],1)
    def test_scenario_cannot_emit_causal_probability_or_label(self):
        before=len(self.store.records('resolution','official'))
        r=intelligence.scenario(self.store,dict(question='What happens if control changes?',assumptions=['Democrats control House']))
        self.assertIsNone(r['probability']);self.assertIsNone(r['probability_shift'])
        self.assertEqual(r['status'],'unsupported_for_numeric_forecast')
        self.assertEqual(before,len(self.store.records('resolution','official')))
        self.assertEqual(len(r['evidence']['bill_ids']),3)
    def test_rejects_unknown_fields_and_invalid_groups(self):
        for args in ({'filters':{'party':['D']}},{'limit':True},{'cutoff':'2099-01-01'},{'groups':[{'name':'a'},{'name':'a'}]},{'groups':'bad'}):
            with self.assertRaises(ValueError):intelligence.analyze(self.store,args)
        with self.assertRaises(ValueError):intelligence.scenario(self.store,{'question':'hello','assumptions':[]})
        with self.assertRaises(ValueError):intelligence.rank(self.store,{'max_age_days':400})
