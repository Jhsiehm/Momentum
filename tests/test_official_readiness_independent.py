import hashlib
import pathlib
import tempfile
import unittest
from unittest import mock
from scripts import official_billstatus_readiness_v1 as m

class IndependentReadinessTests(unittest.TestCase):
    def case(self):return dict(bill_id='hr1-113',congress=113,bill_type='hr',bill_number=1,url='https://www.govinfo.gov/bulkdata/BILLSTATUS/113/hr/BILLSTATUS-113hr1.xml')
    def xml(self,inside=''):
        return ('<billStatus><bill><congress>113</congress><number>1</number><type>HR</type><introducedDate>2013-01-03</introducedDate>'+inside+'</bill></billStatus>').encode()
    def test_dtd_entity_nul_and_size_rejected(self):
        for raw in [b'<!DOCTYPE x>'+self.xml(),b'<!ENTITY x "abc">'+self.xml(),b'\x00'+self.xml(),b'x'*(m.CAP+1)]:
            with self.assertRaises(ValueError):m.inspect_xml(raw,self.case())
    def test_duplicate_identity_scalar_and_mixed_schema_rejected(self):
        for extra in ['<number>1</number>','<billNumber>1</billNumber><billType>H</billType>']:
            r=m.inspect_xml(self.xml(extra),self.case());self.assertFalse(r['identity_valid']);self.assertTrue(r['errors'])
    def test_no_final_action_text_or_status_values_retained(self):
        raw=self.xml('<latestAction><text>FORBIDDEN_FINAL_SENTINEL</text></latestAction><actions><item><actionDate>2013-01-04</actionDate><text>FORBIDDEN_ACTION_SENTINEL</text></item></actions>')
        r=m.inspect_xml(raw,self.case());self.assertNotIn('FORBIDDEN',str(r));self.assertEqual(r['actions']['valid_date_count'],1)
    def test_wrong_identity_rejected(self):
        r=m.inspect_xml(self.xml().replace(b'<number>1',b'<number>2'),self.case());self.assertFalse(r['identity_valid'])
    def test_day180_calendar_flag_is_distinct_from_identity(self):
        raw=self.xml().replace(b'2013-01-03',b'2015-01-03')
        r=m.inspect_xml(raw,self.case());self.assertTrue(r['identity_valid']);self.assertFalse(r['introduction_in_calendar_congress']);self.assertFalse(r['day180_before_congress_end'])
    def test_empty_context_containers_not_invented_values(self):
        r=m.inspect_xml(self.xml('<cosponsors/>'),self.case())
        self.assertTrue(r['cosponsors']['container_present']);self.assertEqual(r['cosponsors']['item_count'],0)
        self.assertFalse(r['actions']['container_present'])
    def test_oversized_response_retained_but_not_parsed(self):
        response=mock.MagicMock();response.__enter__.return_value=response;response.status=200;response.headers={};response.read.return_value=b'x'*(m.CAP+1)
        opener=mock.Mock();opener.open.return_value=response
        with tempfile.TemporaryDirectory() as tmp:
            receipt=m.fetch_case(self.case(),pathlib.Path(tmp),opener)
            response.read.assert_called_once_with(m.CAP+1)
            self.assertTrue(receipt['truncated']);self.assertFalse(receipt['parsed']);self.assertEqual(receipt['bytes'],m.CAP+1)
            self.assertFalse((pathlib.Path(tmp)/'hr1-113-inspection.json').exists())
    def test_text_version_urls_are_metadata_not_fetched(self):
        raw=self.xml('<textVersions><item><type>Introduced in House</type><date>2013-01-03</date><formats><item><url>https://example.com/source</url></item></formats></item></textVersions>')
        r=m.inspect_xml(raw,self.case());self.assertEqual(r['text_versions']['records'][0]['source_urls'],['https://example.com/source'])
if __name__=='__main__':unittest.main()
