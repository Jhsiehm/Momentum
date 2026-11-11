import unittest
from scripts import action_label_contract_diagnostic_v1 as m
class IndependentContractTests(unittest.TestCase):
    case=dict(bill_id='hr1-113',congress=113,bill_type='hr',bill_number=1)
    def action(self,text,code='36000',source='9',date='2013-12-01'):
        return f'<item><actionDate>{date}</actionDate><actionCode>{code}</actionCode><sourceSystem><code>{source}</code></sourceSystem><text>{text}</text></item>'
    def raw(self,actions,laws='<item><type>Public</type><number>113-1</number></item>'):
        return ('<billStatus><bill><congress>113</congress><billNumber>1</billNumber><billType>H</billType><introducedDate>2013-01-03</introducedDate><laws>'+laws+'</laws><actions>'+actions+'</actions></bill></billStatus>').encode()
    def test_signature_never_independent_law_evidence(self):
        r=m.inspect(self.raw(self.action('Signed by President.')),self.case)
        self.assertEqual(r['concordant_assertion_count'],0);self.assertFalse(r['all_problem_dates_match_concordant']);self.assertNotIn('y',r)
    def test_exact_signature_with_complete_concordance(self):
        r=m.inspect(self.raw(self.action('Became Public Law No: 113-1.')+self.action('Signed by President.')),self.case)
        self.assertEqual(r['concordant_assertion_count'],1);self.assertTrue(r['all_problem_dates_match_concordant']);self.assertEqual(r['concordant_date_count'],1)
    def test_conflicting_signature_date_retained(self):
        r=m.inspect(self.raw(self.action('Became Public Law No: 113-1.')+self.action('Signed by President.',date='2013-12-02')),self.case)
        self.assertFalse(r['all_problem_dates_match_concordant'])
    def test_broad_signing_phrase_not_exact(self):
        r=m.inspect(self.raw(self.action('Signed by President with exceptions.')),self.case)
        self.assertEqual(r['terminal_assertions'][0]['assertion_kind'],'other_terminal_text')
    def test_wrong_source_and_law_identity_not_concordant(self):
        for action in [self.action('Became Public Law No: 113-1.',source='2'),self.action('Became Public Law No: 113-2.')]:
            self.assertEqual(m.inspect(self.raw(action),self.case)['concordant_assertion_count'],0)
    def test_multiple_dates_not_single_concordance(self):
        r=m.inspect(self.raw(self.action('Became Public Law No: 113-1.')+self.action('Became Public Law No: 113-1.',date='2013-12-02')),self.case)
        self.assertEqual(r['concordant_date_count'],2)
if __name__=='__main__':unittest.main()
