import datetime as dt
import unittest
from scripts import action_context_features_v1 as m
class IndependentActionFeatures(unittest.TestCase):
    case=dict(bill_id='hr1-113',congress=113,bill_type='hr',bill_number=1)
    def action(self,code='8000',source='9',date='2013-02-01'):
        return f'<item><actionDate>{date}</actionDate><actionCode>{code}</actionCode><sourceSystem><code>{source}</code></sourceSystem></item>'
    def raw(self,actions,extra='',legacy=False):
        identity='<billNumber>1</billNumber><billType>H</billType>'if legacy else'<number>1</number><type>HR</type>'
        return ('<billStatus><bill><congress>113</congress>'+identity+'<introducedDate>2013-01-03</introducedDate><actions>'+actions+'</actions>'+extra+'</bill></billStatus>').encode()
    def test_no_edition_requirement_and_malformed_edition_irrelevance(self):
        a=m.extract_features(self.raw(self.action()),self.case)
        b=m.extract_features(self.raw(self.action(),'<textVersions><item><date/><type>Enrolled Bill</type></item></textVersions>'),self.case)
        self.assertEqual(a,b);self.assertEqual(a['anchor'],[2/3,0.])
    def test_cutoff_equality_future_and_outcome_not_milestones(self):
        cutoff=(dt.date(2013,1,3)+dt.timedelta(days=180)).isoformat()
        r=m.extract_features(self.raw(self.action('5000')+self.action('28000',date=cutoff)+self.action('36000')+self.action('28000',date='2014-01-01')),self.case)
        self.assertEqual(r['stage'],1)
    def test_wrong_source_and_opposite_chamber_do_not_advance(self):
        r=m.extract_features(self.raw(self.action('8000','2')+self.action('17000')+self.action('H30000','2')),self.case)
        self.assertEqual(r['stage'],0)
    def test_legacy_identity_matches_modern(self):
        self.assertEqual(m.extract_features(self.raw(self.action(),legacy=True),self.case),m.extract_features(self.raw(self.action()),self.case))
    def test_later_bad_source_remains_explicit_exclusion(self):
        r=m.extract_features(self.raw(self.action()+self.action('8000','77','2014-01-01')),self.case)
        self.assertIsNone(r['anchor']);self.assertTrue(r['feature_errors'])
    def test_no_pre_cutoff_action_is_ineligible(self):
        r=m.extract_features(self.raw(self.action(date='2014-01-01')),self.case)
        self.assertIsNone(r['anchor'])
    def test_label_resolver_exact_frozen_function(self):
        from scripts import official_context_features_v2 as old
        self.assertIs(m.resolve_outcome,old.resolve_outcome)
    def test_duplicate_action_date_fails(self):
        action=self.action().replace('<actionCode>','<actionDate>2013-02-01</actionDate><actionCode>')
        self.assertIsNone(m.extract_features(self.raw(action),self.case)['anchor'])
if __name__=='__main__':unittest.main()
