import unittest
from scripts import action_outcome_resolver_v1 as m
from scripts import official_context_features_v2 as old
class IndependentOutcomeTests(unittest.TestCase):
    case=dict(bill_id='hr1-113',congress=113,bill_type='hr',bill_number=1)
    cutoff='2013-07-02'
    def a(self,text='Became Public Law No: 113-1.',code='36000',source='9',date='2013-12-01'):
        return f'<item><actionDate>{date}</actionDate><actionCode>{code}</actionCode><sourceSystem><code>{source}</code></sourceSystem><text>{text}</text></item>'
    def raw(self,actions,laws='<laws><item><type>Public</type><number>113-1</number></item></laws>'):
        return ('<billStatus><bill><congress>113</congress><billNumber>1</billNumber><billType>H</billType><introducedDate>2013-01-03</introducedDate>'+laws+'<actions>'+actions+'</actions><updateDate>2016-01-01</updateDate></bill></billStatus>').encode()
    def resolve(self,actions,laws=None):return m.resolve_outcome(self.raw(actions)if laws is None else self.raw(actions,laws),self.case,self.cutoff)
    def test_exact_annotation_does_not_supply_event(self):
        r=self.resolve(self.a()+self.a('Signed by President.'));self.assertEqual(r['y'],1);self.assertEqual(r['enacted_at'],'2013-12-01')
        self.assertIsNone(self.resolve(self.a('Signed by President.'))['y'])
    def test_wrong_source_or_code_or_phrase_not_normalized(self):
        for code,source,text in [('36000','2','Signed by President.'),('E40000','9','Signed by President.'),('36000','9','signed by president.'),('36000','9','Signed by President'),('36000','9','Signed by President. Additional text')]:
            self.assertIsNone(self.resolve(self.a()+self.a(text,code,source))['y'])
    def test_conflicting_signing_date_unknown(self):
        self.assertIsNone(self.resolve(self.a()+self.a('Signed by President.',date='2013-12-02'))['y'])
    def test_missing_law_and_wrong_law_unknown(self):
        self.assertIsNone(self.resolve(self.a()+self.a('Signed by President.'),'')['y'])
        self.assertIsNone(self.resolve(self.a('Became Public Law No: 113-2.')+self.a('Signed by President.'))['y'])
    def test_cutoff_end_risk_boundaries_preserved(self):
        for date,reason in [(self.cutoff,'already_enacted_or_cutoff_date_ambiguous'),('2015-01-03','outside_horizon_or_end_date_ambiguous')]:
            r=self.resolve(self.a(date=date)+self.a('Signed by President.',date=date));self.assertIsNone(r['y']);self.assertEqual(r['reason'],reason)
    def test_ordinary_negative_and_positive_exactly_unchanged(self):
        for raw in [self.raw(self.a('Introduced.','Intro-H','2'),''),self.raw(self.a())]:
            self.assertEqual(m.resolve_outcome(raw,self.case,self.cutoff),old.resolve_outcome(raw,self.case,self.cutoff))
    def test_public_dates_multiplicity_stays_unknown(self):
        self.assertIsNone(self.resolve(self.a()+self.a(date='2013-12-02')+self.a('Signed by President.'))['y'])
    def test_duplicate_source_not_normalized(self):
        sig=self.a('Signed by President.').replace('<code>9</code>','<code>9</code><code>9</code>')
        self.assertIsNone(self.resolve(self.a()+sig)['y'])
if __name__=='__main__':unittest.main()
