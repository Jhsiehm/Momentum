import unittest
from scripts import bicam_inventory_target_v3 as m

class TargetTests(unittest.TestCase):
    def data(self, rows):
        header=['bill_id','bill_type','bill_number','congress','title','introduced_at']+[f'x{i}' for i in range(18)]
        return (','.join(header)+'\n'+'\n'.join(','.join(row+['OUTCOME_SENTINEL']*18) for row in rows)+'\n').encode()
    def row(self,bid='hr1-113',congress='113.0',date='2013-01-03'):
        import re
        a=re.fullmatch(r'([a-z]+)(\d+)-(\d+)',bid)
        return [bid,a[1],a[2],congress,'title',date]
    def test_target_valid_and_exposure(self):
        r=m.target_inventory(self.data([self.row()]),{})
        self.assertTrue(r['target_internal_consistency']);self.assertEqual(len(r['sample']),1)
        self.assertFalse(r['official_coverage_complete']);self.assertNotIn('OUTCOME_SENTINEL',str(r))
        self.assertIn('not_untouched',r['sample'][0]['evaluation_exposure'])
    def test_outside_blank_quarantined(self):
        r=m.target_inventory(self.data([self.row(),self.row('s1-112','','')]),{})
        self.assertTrue(r['target_internal_consistency']);self.assertEqual(len(r['quarantine']),1)
        self.assertEqual(r['quarantine'][0]['original']['congress'],'')
    def test_unhandled_target_blank_blocks(self):
        r=m.target_inventory(self.data([self.row(),self.row('s1-113','','')]),{})
        self.assertFalse(r['target_internal_consistency']);self.assertEqual(r['sample'],[])
    def test_sidecar_preserves_original(self):
        repairs={'s1-113':{'original':{'congress':'','introduced_at':''},'proposed':{'congress':113,'introduced_at':'2013-01-03'},'evidence_sha256':'a'*64}}
        r=m.target_inventory(self.data([self.row('s1-113','','')]),repairs)
        self.assertTrue(r['target_internal_consistency']);self.assertEqual(r['rows'][0]['original']['introduced_at'],'')
        self.assertEqual(r['rows'][0]['introduced_at'],'2013-01-03')
    def test_duplicate_conflict_date_errors_accumulate(self):
        rows=[self.row(),self.row(),self.row('hr2-113','114.0'),self.row('hr3-113',date='2015-01-03')]
        r=m.target_inventory(self.data(rows),{})
        self.assertEqual(len(r['errors']),3);self.assertEqual(r['sample'],[])
    def test_outside_identity_conflict_blocks(self):
        r=m.target_inventory(self.data([self.row(),self.row('s1-112','111.0')]),{})
        self.assertFalse(r['target_internal_consistency'])
    def test_sample_order(self):
        rows=[self.row(f'hr{i}-113') for i in range(1,121)]
        a=m.target_inventory(self.data(rows),{});b=m.target_inventory(self.data(rows[::-1]),{})
        self.assertEqual(a['sample'],b['sample']);self.assertEqual(len(a['sample']),100)
    def test_midnight_date_forms(self):
        for value in ['2013-01-03 00:00:00', '2013-01-03T00:00:00.000']:
            r=m.target_inventory(self.data([self.row(date=value)]),{})
            self.assertTrue(r['target_internal_consistency'])
            self.assertEqual(r['rows'][0]['introduced_at'],'2013-01-03')
            self.assertEqual(r['rows'][0]['original']['introduced_at'],value)
        r=m.target_inventory(self.data([self.row(date='2013-01-03T01:00:00')]),{})
        self.assertFalse(r['target_internal_consistency'])
    def test_cr_title_reversible(self):
        row=self.row();row[4]='a\rb'
        r=m.target_inventory(self.data([row]),{})
        self.assertEqual(len(r['title_cr_offsets']),1)
if __name__=='__main__':unittest.main()
