import unittest
from scripts import official_context_conditioning_diagnostic_v1 as m
CASE=dict(bill_id='hr1-113',congress=113,bill_number=1,bill_type='hr')
F=dict(anchor=None,feature_errors=['Missing date'],stage=None)
class ConditioningTests(unittest.TestCase):
    def raw(self,laws='',date='<date/>'):
        return ('<billStatus><bill><congress>113</congress><number>1</number><type>HR</type>'+laws+'<textVersions><item><type>Enrolled Bill</type>'+date+'<formats><item><url>https://www.govinfo.gov/content/pkg/BILLS-113hr1enr/pdf/BILLS-113hr1enr.pdf</url></item></formats></item></textVersions></bill></billStatus>').encode()
    def test_public_assertion_empty_enrolled_date(self):
        r=m.inspect(self.raw('<laws><item><type>Public</type><number>113-1</number></item></laws>'),CASE,F)
        self.assertEqual(r['assertion_category'],'public_law_assertion');self.assertEqual(r['recognized_edition_metadata'][0]['date_status'],'empty');self.assertFalse(r['anchor_valid'])
    def test_absence_not_negative_label(self):
        r=m.inspect(self.raw(),CASE,F);self.assertEqual(r['assertion_category'],'no_public_law_assertion');self.assertNotIn('y',r)
    def test_ambiguous_law(self):
        r=m.inspect(self.raw('<laws><item><type>Public</type><number>114-1</number></item></laws>'),CASE,F)
        self.assertEqual(r['assertion_category'],'ambiguous_law_metadata')
    def test_missing_vs_present_date(self):
        self.assertEqual(m.inspect(self.raw(date=''),CASE,F)['recognized_edition_metadata'][0]['date_status'],'absent')
        self.assertEqual(m.inspect(self.raw(date='<date>2014-01-01</date>'),CASE,F)['recognized_edition_metadata'][0]['date_status'],'present')
    def test_wrong_identity_rejected(self):
        with self.assertRaises(ValueError):m.inspect(self.raw().replace(b'<number>1</number>',b'<number>2</number>'),CASE,F)
if __name__=='__main__':unittest.main()
