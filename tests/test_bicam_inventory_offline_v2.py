import unittest
from scripts import bicam_inventory_offline_v2 as m

class OfflineTests(unittest.TestCase):
    def test_title_escape_reversible(self):
        raw=b'a,b,c,d,title\rmore,f\n'
        out,ledger=m.escape_title_cr(raw)
        self.assertEqual(out,b'a,b,c,d,title\\rmore,f\n')
        self.assertEqual(ledger[0]['source_offset'],13)
    def test_quoted_cr_lf_and_doubled_quote_unchanged(self):
        raw=b'a,b,c,d,"title\rwith\nline and ""quote""",f\r\n'
        self.assertEqual(m.escape_title_cr(raw),(raw,[]))
    def test_literal_backslash_preserved(self):
        raw=b'a,b,c,d,x\\r\ry\\r,f\n'
        out,ledger=m.escape_title_cr(raw)
        self.assertEqual(len(ledger),1);self.assertIn(b'x\\r\\ry\\r',out)
    def test_cr_outside_title_reject(self):
        for raw in [b'a\r,b,c,d,title,f\n',b'a,b,c,d,title,f\rmore\n']:
            with self.assertRaises(ValueError):m.escape_title_cr(raw)
    def test_unclosed_quote(self):
        with self.assertRaises(ValueError):m.escape_title_cr(b'a,b,c,d,"title')
    def test_integral_congress(self):
        for value in ['113','113.0','113.000']:
            self.assertEqual(m.integral_congress(value),'113')
        for value in ['113.1','1e2','nan','inf','0','-1',' 113','0113']:
            with self.assertRaises(ValueError):m.integral_congress(value)
    def test_projection_and_width(self):
        header=['bill_id','bill_type','bill_number','congress','title','introduced_at']+[f'x{i}' for i in range(18)]
        row=['hr1-113','hr','1','113.0','title\rhere','2013-01-03']+['sentinel']*18
        raw=(','.join(header)+'\n'+','.join(row)+'\n').encode()
        projected,ledger,count,converted,_=m.project(raw)
        self.assertEqual((count,converted,len(ledger)),(1,1,1))
        self.assertNotIn(b'sentinel',projected);self.assertNotIn(b'title',projected)
        with self.assertRaises(ValueError):m.project(raw.rstrip(b'\n')+b',extra\n')
if __name__=='__main__':unittest.main()
