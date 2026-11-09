import datetime as dt
import math
import unittest
from scripts import official_context_features_v1 as m
from scripts import official_context_acquisition_v1 as a
CASE=dict(bill_id='hr1-113',congress=113,bill_type='hr',bill_number=1)

class ContextTests(unittest.TestCase):
    def raw(self,extra='',intro='2013-01-03',actions=None):
        if actions is None:actions='<item><actionDate>2013-01-03</actionDate><actionCode>1000</actionCode><sourceSystem><code>9</code></sourceSystem></item>'
        return (f'<billStatus><bill><number>1</number><type>HR</type><congress>113</congress><introducedDate>{intro}</introducedDate><updateDate>2016-01-04T00:00:00Z</updateDate><actions>{actions}</actions><textVersions><item><date>{intro}T05:00:00Z</date><type>Introduced in House</type><formats><item><url>https://www.govinfo.gov/content/pkg/BILLS-113hr1ih/pdf/BILLS-113hr1ih.pdf</url></item></formats></item></textVersions>'+extra+'</bill></billStatus>').encode()
    def test_anchor_formulas(self):
        f=m.extract_features(self.raw('<cosponsors/><committees/>'),CASE)
        self.assertEqual(f['anchor'],[0,180/730,1/30,180/730,0,0]);self.assertEqual(f['context'],[0,0,1])
    def test_delayed_introduced_edition(self):
        raw=self.raw().replace(b'<date>2013-01-03T05:00:00Z</date>',b'<date>2013-01-10T05:00:00Z</date>')
        self.assertIsNotNone(m.extract_features(raw,CASE)['anchor'])
        for d in (b'2013-01-02',b'2013-07-02'):
            changed=self.raw().replace(b'<date>2013-01-03T05:00:00Z</date>',b'<date>'+d+b'T05:00:00Z</date>')
            self.assertIsNone(m.extract_features(changed,CASE)['anchor'])
    def test_missing_not_zero(self):
        f=m.extract_features(self.raw(),CASE);self.assertEqual(f['context'][:2],[None,None]);self.assertEqual(f['missing'],[1,1,0])
    def cosponsor(self,join,withdraw=''):
        return f'<cosponsors><item><bioguideId>A000001</bioguideId><sponsorshipDate>{join}</sponsorshipDate>'+ (f'<sponsorshipWithdrawnDate>{withdraw}</sponsorshipWithdrawnDate>'if withdraw else '')+'</item></cosponsors>'
    def test_active_withdrawal_and_boundary(self):
        for join,withdraw,expected in [('2013-01-04','',math.log1p(1)),('2013-01-04','2013-02-01',0),('2013-07-02','',None),('2013-01-04','2013-07-02',None),('2013-01-04','2013-01-04',0)]:
            f=m.extract_features(self.raw(self.cosponsor(join,withdraw)),CASE);self.assertEqual(f['context'][0],expected)
    def test_conflicting_cosponsor_duplicate(self):
        extra=self.cosponsor('2013-01-04').replace('</cosponsors>','<item><bioguideId>A000001</bioguideId><sponsorshipDate>2013-02-01</sponsorshipDate></item></cosponsors>')
        self.assertIsNone(m.extract_features(self.raw(extra),CASE)['context'][0])
    def test_committee_referrals_dedup_and_cutoff(self):
        extra='<committees><item><systemCode>hsag00</systemCode><activities><item><date>2013-01-04</date><name>Referred to</name></item><item><date>2013-02-01</date><name>Referred to</name></item></activities></item><item><systemCode>hswm00</systemCode><activities><item><date>2013-07-02</date><name>Referred to</name></item></activities></item></committees>'
        self.assertEqual(m.extract_features(self.raw(extra),CASE)['context'][1],math.log1p(1))
    def test_unsupported_container_not_zero(self):
        f=m.extract_features(self.raw('<cosponsors><unknown/></cosponsors><committees><unknown/></committees>'),CASE)
        self.assertEqual(f['context'][:2],[None,None])
    def test_external_edition_url_reject(self):
        raw=self.raw().replace(b'www.govinfo.gov',b'evil.example')
        self.assertIsNone(m.extract_features(raw,CASE)['anchor'])
    def test_intro_outside_calendar_reject(self):
        with self.assertRaises(ValueError):m.extract_features(self.raw(intro='2012-12-01'),CASE)
    def test_no_action_prose_feature(self):
        raw=self.raw(actions='<item><actionDate>2013-01-03</actionDate><actionCode>1000</actionCode><text>SECRET</text></item>')
        self.assertNotIn('SECRET',str(m.extract_features(raw,CASE)))
    def enact(self,day='2014-01-01',code='36000',system='9',text='Became Public Law No: 113-1.'):
        actions=f'<item><actionDate>{day}</actionDate><actionCode>{code}</actionCode><sourceSystem><code>{system}</code></sourceSystem><text>{text}</text></item>'
        return self.raw('<laws><item><type>Public</type><number>113-1</number></item></laws>',actions=actions)
    def test_positive_law_action(self):
        r=m.resolve_outcome(self.enact(),CASE,'2013-07-02');self.assertEqual(r['y'],1)
    def test_negative_explicit_proxy(self):
        r=m.resolve_outcome(self.raw(),CASE,'2013-07-02');self.assertEqual(r['y'],0);self.assertFalse(r['certified_negative']);self.assertEqual(r['label_matured_at'],'2015-01-03')
    def test_negative_missing_coverage_unknown(self):
        for raw in [self.raw(actions=''),self.raw().replace(b'2016-01-04T00:00:00Z',b'2014-01-01')]:
            self.assertIsNone(m.resolve_outcome(raw,CASE,'2013-07-02')['y'])
    def test_label_boundaries(self):
        for day in ['2013-07-02','2013-07-01','2015-01-03']:
            self.assertIsNone(m.resolve_outcome(self.enact(day),CASE,'2013-07-02')['y'])
    def test_law_conflict_wrongsource_or_reference_unknown(self):
        for raw in [self.enact(system='2'),self.enact(text='Amends Public Law 113-1.'),self.enact().replace(b'<number>113-1</number>',b'<number>113-2</number>')]:
            self.assertIsNone(m.resolve_outcome(raw,CASE,'2013-07-02')['y'])
    def test_unpaired_latest_or_edition_assertion_unknown(self):
        raw=self.raw('<latestAction><text>Became Public Law No: 113-1.</text></latestAction>')
        self.assertIsNone(m.resolve_outcome(raw,CASE,'2013-07-02')['y'])
    def test_signed_only_unknown_and_uncoded_source_valid(self):
        for code in ('37000','E30000'):
            actions=f'<item><actionDate>2014-01-01</actionDate><actionCode>{code}</actionCode><sourceSystem><code>9</code></sourceSystem><text>Signed by President.</text></item>'
            self.assertIsNone(m.resolve_outcome(self.raw(actions=actions),CASE,'2013-07-02')['y'])
        raw=self.raw(actions='<item><actionDate>2013-01-04</actionDate><sourceSystem><code>0</code></sourceSystem></item>')
        self.assertEqual(m.resolve_outcome(raw,CASE,'2013-07-02')['y'],0)
        self.assertAlmostEqual(m.extract_features(raw,CASE)['context'][2],179/180)
    def test_canonical_and_selection_exclusion(self):
        self.assertEqual(a.canonical('113-hr12'),'hr12-113')
        pop={f'hr{n}-{c}':dict(bill_id=f'hr{n}-{c}',congress=c)for c in range(113,119)for n in range(1,5)}
        selected,ledger=a.select(pop,{'hr1-113'},per_congress=2)
        self.assertEqual(len(selected),12);self.assertEqual([r['congress']for r in selected[:6]],list(range(113,119)))
        self.assertNotIn('hr1-113',[r['bill_id']for r in selected]);self.assertEqual(len(ledger),1)
if __name__=='__main__':unittest.main()
