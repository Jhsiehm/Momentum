import datetime as dt
import math
import unittest
import xml.etree.ElementTree as E
from scripts import official_context_features_v2 as m

class IndependentV2Tests(unittest.TestCase):
    intro=dt.date(2013,1,3);cutoff=intro+dt.timedelta(days=180)
    case=dict(bill_id='hr1-113',congress=113,bill_type='hr',bill_number=1)
    def action(self,code='Intro-H',source='<code>2</code>'):
        return '<actions><item><actionDate>2013-01-04</actionDate><actionCode>'+code+'</actionCode><sourceSystem>'+source+'</sourceSystem><text>Introduced.</text></item></actions>'
    def bill(self,extra):return E.fromstring('<bill>'+extra+'</bill>')
    def raw(self,extra):
        return ('<billStatus><bill><congress>113</congress><number>1</number><type>HR</type><introducedDate>2013-01-03</introducedDate><textVersions><item><date>2013-01-03</date><type>Introduced in House</type><formats><item><url>https://www.govinfo.gov/content/pkg/BILLS-113hr1ih/xml/BILLS-113hr1ih.xml</url></item></formats></item></textVersions>'+extra+'</bill></billStatus>').encode()
    def test_explicit_hyphen_codes_supported(self):
        for code in ['Intro-H','H11100-A']:
            value,reason=m.action_recency(self.bill(self.action(code)),self.intro,self.cutoff)
            self.assertAlmostEqual(value,179/180);self.assertIsNone(reason)
    def test_unknown_hyphen_not_generalized(self):
        with self.assertRaises(ValueError):m.action_recency(self.bill(self.action('OTHER-X')),self.intro,self.cutoff)
    def test_named_senate_preserves_distinct_source(self):
        a=E.fromstring('<item><sourceSystem><name>Senate</name></sourceSystem></item>')
        self.assertEqual(m.action_source(a),'name:Senate')
        b=E.fromstring('<item><sourceSystem><code>3</code><name>Senate</name></sourceSystem></item>')
        with self.assertRaises(ValueError):m.action_source(b)
    def test_referral_survives_unsupported_action(self):
        raw=self.raw(self.action('UNKNOWN-X')+'<committees><item><systemCode>hsag00</systemCode><activities><item><date>2013-01-04</date><name>Referred to</name></item></activities></item></committees>')
        r=m.extract_features(raw,self.case)
        self.assertEqual(r['context'][1],math.log1p(1));self.assertIsNone(r['context'][2])
    def test_anchor_and_cosponsor_unchanged(self):
        raw=self.raw(self.action()+'<cosponsors/>')
        before=m.v1.extract_features(raw,self.case);after=m.extract_features(raw,self.case)
        for key in ['anchor','stage','cutoff','related']:self.assertEqual(before[key],after[key])
        self.assertEqual(before['context'][0],after['context'][0])
    def test_named_senate_ordinary_history_negative_proxy_only(self):
        raw=self.raw(self.action('10000','<name>Senate</name>')+'<updateDate>2016-01-01</updateDate>')
        result=m.resolve_outcome(raw,self.case,self.cutoff.isoformat());self.assertEqual(result['y'],0);self.assertFalse(result['certified_negative'])
    def test_named_senate_cannot_stand_in_for_terminal_code_source(self):
        raw=self.raw('<laws><item><type>Public</type><number>113-1</number></item></laws><actions><item><actionDate>2013-12-01</actionDate><actionCode>E40000</actionCode><sourceSystem><name>Senate</name></sourceSystem><text>Became Public Law No: 113-1.</text></item></actions>')
        self.assertIsNone(m.resolve_outcome(raw,self.case,self.cutoff.isoformat())['y'])
if __name__=='__main__':unittest.main()
