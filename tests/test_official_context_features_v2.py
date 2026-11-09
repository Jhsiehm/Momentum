import datetime as dt
import math
import unittest
import xml.etree.ElementTree as ET
from scripts import official_context_features_v2 as m
from tests import test_official_context_v1 as fixtures
CASE=fixtures.CASE

class V2Tests(unittest.TestCase):
    def raw(self,*args,**kwargs):return fixtures.ContextTests().raw(*args,**kwargs)
    def test_hyphenated_observed_actions(self):
        for code in ('Intro-H','H11100-A'):
            action=f'<item><actionDate>2013-01-04</actionDate><actionCode>{code}</actionCode><sourceSystem><code>2</code></sourceSystem></item>'
            f=m.extract_features(self.raw(actions=action),CASE)
            self.assertEqual(f['context'][2],179/180)
    def test_named_senate_without_numeric_imputation(self):
        node=ET.fromstring('<item><sourceSystem><name>Senate</name></sourceSystem></item>')
        self.assertEqual(m.action_source(node),'name:Senate');self.assertIsNone(node.find('sourceSystem/code'))
    def test_unknown_hyphen_code_remains_missing(self):
        action='<item><actionDate>2013-01-04</actionDate><actionCode>UNKNOWN-X</actionCode><sourceSystem><code>2</code></sourceSystem></item>'
        self.assertIsNone(m.extract_features(self.raw(actions=action),CASE)['context'][2])
    def test_independent_referral_when_action_invalid(self):
        committee='<committees><item><systemCode>hsag00</systemCode><activities><item><name>Referred to</name><date>2013-01-04</date></item></activities></item></committees>'
        action='<item><actionDate>2013-01-04</actionDate><sourceSystem><name>Unsupported</name></sourceSystem></item>'
        f=m.extract_features(self.raw(committee,actions=action),CASE)
        self.assertEqual(f['context'][1],math.log1p(1));self.assertIsNone(f['context'][2])
    def test_independent_recency_when_committee_invalid(self):
        f=m.extract_features(self.raw('<committees><unknown/></committees>'),CASE)
        self.assertIsNone(f['context'][1]);self.assertEqual(f['context'][2],1)
    def test_unchanged_anchor_cosponsor_family(self):
        raw=self.raw('<cosponsors/>')
        before=m.v1.extract_features(raw,CASE);after=m.extract_features(raw,CASE)
        for key in ('anchor','stage','cutoff','related'):
            self.assertEqual(before[key],after[key])
        self.assertEqual(before['context'][0],after['context'][0])
    def test_named_senate_ordinary_history_negative_proxy(self):
        raw=self.raw(actions='<item><actionDate>2013-01-04</actionDate><sourceSystem><name>Senate</name></sourceSystem></item>')
        r=m.resolve_outcome(raw,CASE,'2013-07-02')
        self.assertEqual(r['y'],0);self.assertFalse(r['certified_negative'])
    def test_named_senate_terminal_not_inferred_to_loc(self):
        raw=fixtures.ContextTests().enact().replace(b'<sourceSystem><code>9</code></sourceSystem>',b'<sourceSystem><name>Senate</name></sourceSystem>')
        self.assertIsNone(m.resolve_outcome(raw,CASE,'2013-07-02')['y'])
    def test_signing_only_still_unknown(self):
        raw=self.raw(actions='<item><actionDate>2014-01-01</actionDate><sourceSystem><name>Senate</name></sourceSystem><text>Signed by President.</text></item>')
        self.assertIsNone(m.resolve_outcome(raw,CASE,'2013-07-02')['y'])
if __name__=='__main__':unittest.main()
