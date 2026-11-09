import unittest
from scripts import official_context_conditioning_diagnostic_v2 as m
CASE=dict(bill_id='hr1-113',congress=113,bill_number=1,bill_type='hr')
F=dict(anchor=None,feature_errors=['Missing date'],stage=None)
class ConditioningV2Tests(unittest.TestCase):
    def raw(self,identity='<number>1</number><type>HR</type>',laws=''):
        return ('<billStatus><bill><congress>113</congress>'+identity+'<introducedDate>2013-01-03</introducedDate>'+laws+'<textVersions><item><type>Enrolled Bill</type><date/><formats><item><url>https://www.govinfo.gov/content/pkg/BILLS-113hr1enr/pdf/BILLS-113hr1enr.pdf</url></item></formats></item></textVersions></bill></billStatus>').encode()
    def test_legacy_equivalent_to_modern(self):
        a=m.inspect(self.raw(),CASE,F);b=m.inspect(self.raw('<billNumber>1</billNumber><billType>HR</billType>'),CASE,F)
        self.assertEqual(a,b)
        self.assertEqual(a,m.inspect(self.raw('<billNumber>1</billNumber><billType>H</billType>'),CASE,F))
    def test_whitespace_scalar_supported(self):
        self.assertEqual(m.inspect(self.raw('<number> 1 </number><type> HR </type>'),CASE,F),m.inspect(self.raw(),CASE,F))
    def test_mixed_and_duplicate_aliases_rejected(self):
        for identity in ['<number>1</number><type>HR</type><billNumber>1</billNumber><billType>HR</billType>','<number>1</number><number>1</number><type>HR</type>']:
            with self.assertRaises(ValueError):m.inspect(self.raw(identity),CASE,F)
    def test_wrong_identity_rejected(self):
        with self.assertRaises(ValueError):m.inspect(self.raw('<billNumber>2</billNumber><billType>HR</billType>'),CASE,F)
    def test_assertion_and_missing_date_unchanged(self):
        r=m.inspect(self.raw(laws='<laws><item><type>Public</type><number>113-1</number></item></laws>'),CASE,F)
        self.assertEqual(r['assertion_category'],'public_law_assertion');self.assertEqual(r['recognized_edition_metadata'][0]['date_status'],'empty');self.assertNotIn('y',r)
    def test_absence_not_negative(self):
        r=m.inspect(self.raw(),CASE,F);self.assertEqual(r['assertion_category'],'no_public_law_assertion');self.assertNotIn('y',r)
if __name__=='__main__':unittest.main()
