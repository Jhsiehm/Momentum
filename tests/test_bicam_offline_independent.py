import unittest
from scripts import bicam_inventory_offline_v2 as m

class IndependentOfflineTests(unittest.TestCase):
    def fixture(self,title):
        header=['bill_id','bill_type','bill_number','congress','title','introduced_at']+[f'x{i}' for i in range(18)]
        return (','.join(header)+'\r\n'+','.join(['hr1-113','hr','1','113.00',title,'2013-01-03']+['OUTCOME_SENTINEL']*18)+'\r\n').encode()
    def test_multiple_escapes_reconstruct_exact_source(self):
        raw=self.fixture('first\rsecond\rliteral\\r')
        transformed,ledger=m.escape_title_cr(raw)
        self.assertEqual(len(ledger),2)
        for item in reversed(ledger):
            p=item['projected_offset'];self.assertEqual(transformed[p:p+2],b'\\r')
            transformed=transformed[:p]+b'\r'+transformed[p+2:]
        self.assertEqual(raw,transformed)
        projection,_,rows,converted,_=m.project(raw)
        self.assertEqual((rows,converted),(1,1))
        self.assertNotIn(b'OUTCOME_SENTINEL',projection)
    def test_quoted_commas_newlines_quotes_do_not_change_columns(self):
        raw=self.fixture('"a,b\nwith\rreturn and ""quote"""')
        projection,ledger,rows,_,_=m.project(raw)
        self.assertEqual((ledger,rows),([],1))
        self.assertIn(b'hr1-113',projection)
    def test_non_title_bare_cr_rejected(self):
        raw=self.fixture('valid').replace(b'hr1-113',b'hr1\r-113')
        with self.assertRaisesRegex(ValueError,'Bare CR outside title'):
            m.project(raw)
    def test_content_after_closing_quote_rejected(self):
        with self.assertRaises(Exception):m.project(self.fixture('"valid"invalid'))
    def test_wrong_fifth_column_blocks_assumption(self):
        raw=self.fixture('title\rline').replace(b',title,',b',other,',1)
        with self.assertRaisesRegex(ValueError,'Unexpected schema'):m.project(raw)
if __name__=='__main__':unittest.main()
