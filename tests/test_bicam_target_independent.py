import csv
import datetime
import hashlib
import io
import unittest
from scripts import bicam_inventory_target_v3 as m

class IndependentTargetTests(unittest.TestCase):
    def data(self,rows):
        out=io.StringIO();w=csv.writer(out)
        w.writerow(['bill_id','bill_type','bill_number','congress','title','introduced_at']+[f'x{i}' for i in range(18)])
        for row in rows:w.writerow(row+['OUTCOME_SENTINEL']*18)
        return out.getvalue().encode()
    def row(self,n=1,date='2013-01-03',kind='hr',congress=113):
        return [f'{kind}{n}-{congress}',kind,str(n),str(congress),'title',date]
    def test_exact_hash_sample_and_no_label(self):
        rows=[self.row(n) for n in range(1,122)]
        r=m.target_inventory(self.data(rows),{})
        expected=sorted([x[0] for x in rows],key=lambda bid:hashlib.sha256((m.VERSION+'\n'+bid).encode()).hexdigest())[:100]
        self.assertEqual([x['bill_id'] for x in r['sample']],expected)
        self.assertNotIn('OUTCOME_SENTINEL',str(r));self.assertFalse(r['official_coverage_complete'])
    def test_day180_boundary_excludes_equal_end(self):
        end=datetime.date(2015,1,3);date=end-datetime.timedelta(days=180)
        rows=[self.row(1,date.isoformat()),self.row(2,(date-datetime.timedelta(days=1)).isoformat())]
        r=m.target_inventory(self.data(rows),{})
        self.assertEqual([x['day180_before_congress_end'] for x in r['rows']],[False,True])
        self.assertEqual(len(r['sample']),2)
    def test_outside_resolution_missing_metadata_quarantined(self):
        outside=self.row(2,kind='sres');outside[3]=outside[5]=''
        r=m.target_inventory(self.data([self.row(),outside]),{})
        self.assertTrue(r['target_internal_consistency']);self.assertEqual(len(r['quarantine']),1)
        self.assertEqual(r['quarantine'][0]['original']['congress'],'')
    def test_case_equivalent_duplicate_blocks_sample(self):
        a=self.row();b=self.row();b[0]=b[0].upper();b[1]=b[1].upper()
        r=m.target_inventory(self.data([a,b]),{})
        self.assertFalse(r['target_internal_consistency']);self.assertEqual(r['sample'],[])
    def test_target_missing_date_cannot_be_quarantined(self):
        bad=self.row(2,date='')
        r=m.target_inventory(self.data([self.row(),bad]),{})
        self.assertEqual(r['sample'],[]);self.assertEqual(r['quarantine'],[])
        self.assertEqual(r['errors'][0]['issue'],'invalid_target_introduction')
    def test_repair_requires_exact_original(self):
        row=self.row(kind='s');row[3]=''
        repair={row[0]:{'original':{'congress':'','introduced_at':''},'proposed':{'congress':113,'introduced_at':'2013-01-03'},'evidence_sha256':'a'*64}}
        r=m.target_inventory(self.data([row]),repair)
        self.assertEqual(r['sample'],[]);self.assertEqual(r['applied_repairs'],[])
    def test_missing_registered_repair_blocks_sample(self):
        repair={'s1-113':{'original':{'congress':'','introduced_at':''},'proposed':{'congress':113,'introduced_at':'2013-01-03'},'evidence_sha256':'a'*64}}
        r=m.target_inventory(self.data([self.row()]),repair)
        self.assertEqual(r['sample'],[]);self.assertIn({'issue':'repair_cases_not_all_applied'},r['errors'])
    def test_five_registered_dates_all_lack_day180_window(self):
        dates=[(116,'2020-09-22'),(117,'2022-09-20'),(118,'2024-11-13'),(118,'2024-12-16'),(118,'2024-12-17')]
        r=m.target_inventory(self.data([self.row(i,date,congress=c) for i,(c,date) in enumerate(dates,1)]),{})
        self.assertTrue(all(not x['day180_before_congress_end'] for x in r['rows']))
        self.assertEqual(len(r['sample']),5)
if __name__=='__main__':unittest.main()
