import copy,unittest
from engine.negative_passage_audit import entries,classify
from engine.negative_passage_adjudication import adjudicate

class NegativeAuditTests(unittest.TestCase):
    def row(self):
        return dict(bill_id='118-hr1',congress=118,kind='hr',positive_control=False,status='corroborated_pending_negative_candidate',calendar_entry='H.R. 1.-- Reported. Union Calendar.....Union 42',actions=[dict(date='2023-01-04',code='1000',text='Introduced in House',source_system='9'),dict(date='2023-03-01',code='H12410',text='Placed on the Union Calendar, Calendar No. 42.',source_system='2')],versions=['ih','rh'],calendar_available_at='2025-04-10T23:59:59Z',calendar_source=dict(url='https://example.org/final',sha256='fixture'),billstatus_source=dict(url='https://example.org/status',sha256='fixture'))
    def test_missing_calendar_is_unknown(self):self.assertEqual(classify(None,[],[],[],'hr'),'not_listed_no_inference')
    def test_companion_reference_does_not_create_entry(self):
        raw=b'<pre>Final HISTORY OF BILLS AND RESOLUTIONS\nH.R. 1 (H.R. 2).-- Text.\nH.R. 3.-- Other.</pre>';self.assertEqual(set(entries(raw,'hr')),{1,3})
    def test_duplicate_entry_rejected(self):
        with self.assertRaises(AssertionError):entries(b'<pre>Final HISTORY OF BILLS AND RESOLUTIONS\nH.R. 1.-- A\nH.R. 1.-- B</pre>','hr')
    def test_passage_overrides_pending_marker(self):
        r=self.row();self.assertNotEqual(classify('Passed House. '+r['calendar_entry'],r['actions'],r['versions'],[],'hr'),'corroborated_pending_negative_candidate')
    def test_engrossed_version_blocks_negative(self):
        r=self.row();self.assertEqual(classify(r['calendar_entry'],r['actions'],['eh'],[],'hr'),'status_or_version_contradiction')
    def test_current_time_label_not_backdated(self):
        x=adjudicate(self.row(),'2026-11-05T19:00:00Z');self.assertEqual(x['available_at'],'2026-11-05T19:00:00Z');self.assertEqual(x['value'],0);self.assertFalse(x['human_reviewed']);self.assertFalse(x['historical_training_eligible'])
    def test_calendar_number_mismatch_blocks(self):
        r=self.row();r['actions'][-1]['text']='Placed on the Union Calendar, Calendar No. 43.'
        with self.assertRaises(ValueError):adjudicate(r,'2026-11-05T19:00:00Z')
    def test_later_action_blocks(self):
        r=self.row();r['actions'].append(dict(date='2023-03-02',code=None,text='Committee action.',source_system='1'))
        with self.assertRaises(ValueError):adjudicate(r,'2026-11-05T19:00:00Z')
    def test_positive_control_blocks(self):
        r=self.row();r['positive_control']=True
        with self.assertRaises(ValueError):adjudicate(r,'2026-11-05T19:00:00Z')
