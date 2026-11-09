import datetime as dt
import unittest
import xml.etree.ElementTree as ET
from scripts import official_context_features_v1 as m

class IndependentContextTests(unittest.TestCase):
    case=dict(bill_id='hr1-113',congress=113,bill_type='hr',bill_number=1)
    intro=dt.date(2013,1,3)
    cutoff=intro+dt.timedelta(days=180)
    def bill(self,extra='',url='https://www.govinfo.gov/content/pkg/BILLS-113hr1ih/xml/BILLS-113hr1ih.xml'):
        return ET.fromstring('<bill><congress>113</congress><number>1</number><type>HR</type><introducedDate>2013-01-03</introducedDate><textVersions><item><date>2013-01-03T05:00:00Z</date><type>Introduced in House</type><formats><item><url>'+url+'</url></item></formats></item></textVersions>'+extra+'</bill>')
    def test_baseline_rejects_nonofficial_source_host(self):
        with self.assertRaises(ValueError):m.baseline(self.bill(url='https://evil.example/content/pkg/BILLS-113hr1ih/xml/BILLS-113hr1ih.xml'),self.case,self.intro,self.cutoff)
    def test_introduction_outside_congress_not_eligible(self):
        raw=b'<billStatus>'+ET.tostring(self.bill()).replace(b'2013-01-03',b'2012-01-03')+b'</billStatus>'
        try:r=m.extract_features(raw,self.case)
        except ValueError:return
        self.assertIsNone(r['anchor']);self.assertTrue(r['feature_errors'])
    def test_unsupported_cosponsor_shape_not_zero(self):
        bill=self.bill('<cosponsors><member><bioguideId>A000001</bioguideId></member></cosponsors>')
        try:value,reason=m.cosponsors(bill,self.intro,self.cutoff)
        except ValueError:return
        self.assertIsNone(value);self.assertTrue(reason)
    def test_unsupported_committee_shape_not_zero(self):
        bill=self.bill('<actions><item><actionDate>2013-01-03</actionDate><actionCode>1000</actionCode></item></actions><committees><committee><systemCode>hsag00</systemCode></committee></committees>')
        try:breadth,recency=m.procedural(bill,self.intro,self.cutoff)
        except ValueError:return
        self.assertIsNone(breadth[0]);self.assertTrue(breadth[1])
    def test_cutoff_join_is_unknown(self):
        bill=self.bill('<cosponsors><item><bioguideId>A000001</bioguideId><sponsorshipDate>'+self.cutoff.isoformat()+'</sponsorshipDate></item></cosponsors>')
        value,reason=m.cosponsors(bill,self.intro,self.cutoff);self.assertIsNone(value);self.assertTrue(reason)
    def test_same_earlier_day_join_and_withdraw_is_inactive(self):
        bill=self.bill('<cosponsors><item><bioguideId>A000001</bioguideId><sponsorshipDate>2013-01-04</sponsorshipDate><sponsorshipWithdrawnDate>2013-01-04</sponsorshipWithdrawnDate></item></cosponsors>')
        self.assertEqual(m.cosponsors(bill,self.intro,self.cutoff),(0.0,None))
    def test_no_update_does_not_make_negative(self):
        bill=self.bill('<actions><item><actionDate>2013-01-03</actionDate><actionCode>1000</actionCode><text>Introduced.</text></item></actions>')
        raw=b'<billStatus>'+ET.tostring(bill)+b'</billStatus>'
        self.assertIsNone(m.resolve_outcome(raw,self.case,self.cutoff.isoformat())['y'])
    def test_terminal_code_nonterminal_law_reference_not_positive(self):
        bill=self.bill('<laws><item><type>Public</type><number>113-1</number></item></laws><actions><item><actionDate>2013-12-01</actionDate><actionCode>E40000</actionCode><text>Discussed amendment to Public Law 113-1.</text></item></actions>')
        raw=b'<billStatus>'+ET.tostring(bill)+b'</billStatus>'
        self.assertIsNone(m.resolve_outcome(raw,self.case,self.cutoff.isoformat())['y'])
    def test_signed_only_cannot_be_negative_proxy(self):
        bill=self.bill('<updateDate>2016-01-01</updateDate><actions><item><actionDate>2013-12-01</actionDate><actionCode>37000</actionCode><sourceSystem><code>9</code></sourceSystem><text>Signed by President.</text></item></actions>')
        raw=b'<billStatus>'+ET.tostring(bill)+b'</billStatus>'
        self.assertIsNone(m.resolve_outcome(raw,self.case,self.cutoff.isoformat())['y'])
    def test_cutoff_date_enactment_is_excluded(self):
        bill=self.bill('<laws><item><type>Public</type><number>113-1</number></item></laws><actions><item><actionDate>'+self.cutoff.isoformat()+'</actionDate><actionCode>E40000</actionCode><sourceSystem><code>2</code></sourceSystem><text>Became Public Law No: 113-1.</text></item></actions>')
        raw=b'<billStatus>'+ET.tostring(bill)+b'</billStatus>'
        self.assertIsNone(m.resolve_outcome(raw,self.case,self.cutoff.isoformat())['y'])
    def test_future_withdrawal_does_not_reduce_earlier_count(self):
        bill=self.bill('<cosponsors><item><bioguideId>A000001</bioguideId><sponsorshipDate>2013-01-04</sponsorshipDate><sponsorshipWithdrawnDate>2014-01-01</sponsorshipWithdrawnDate></item></cosponsors>')
        import math
        self.assertEqual(m.cosponsors(bill,self.intro,self.cutoff),(math.log1p(1),None))
    def test_invalid_timestamp_not_silently_truncated(self):
        with self.assertRaises(ValueError):m.date('2013-01-03T99:99:99Z',True)
    def test_mixed_unknown_action_layout_cannot_be_negative(self):
        bill=self.bill('<updateDate>2016-01-01</updateDate><actions><item><actionDate>2013-01-03</actionDate><sourceSystem><code>0</code></sourceSystem><text>Introduced.</text></item><unknownAction>unparsed</unknownAction></actions>')
        raw=b'<billStatus>'+ET.tostring(bill)+b'</billStatus>'
        self.assertIsNone(m.resolve_outcome(raw,self.case,self.cutoff.isoformat())['y'])
    def test_duplicate_related_container_rejected(self):
        with self.assertRaises(ValueError):m.related_ids(self.bill('<relatedBills/><relatedBills/>'))
if __name__=='__main__':unittest.main()
