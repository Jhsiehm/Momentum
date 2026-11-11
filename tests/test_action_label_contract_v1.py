import unittest
from scripts import action_label_contract_diagnostic_v1 as m
from tests import test_official_context_v1 as fixture

def action(text,code='36000',source='9',when='2014-01-01'):
    return f'<item><actionDate>{when}</actionDate><actionCode>{code}</actionCode><sourceSystem><code>{source}</code></sourceSystem><text>{text}</text></item>'

def raw(actions,law='113-1'):
    return fixture.ContextTests().raw(f'<laws><item><type>Public</type><number>{law}</number></item></laws>',actions=actions)

class ContractTests(unittest.TestCase):
    def test_mixed_signing_kept_without_label(self):
        r=m.inspect(raw(action('Became Public Law No: 113-1.')+action('Signed by President.')),fixture.CASE)
        self.assertEqual(r['concordant_assertion_count'],1);self.assertTrue(r['all_problem_dates_match_concordant']);self.assertNotIn('y',r)
        self.assertEqual(r['terminal_assertions'][1]['text'],'Signed by President.')
    def test_disagreement_not_hidden(self):
        r=m.inspect(raw(action('Became Public Law No: 113-1.')+action('Signed by President.',when='2014-01-02')),fixture.CASE)
        self.assertFalse(r['all_problem_dates_match_concordant'])
    def test_wrong_source_not_concordant(self):
        r=m.inspect(raw(action('Became Public Law No: 113-1.',source='1')),fixture.CASE)
        self.assertEqual(r['concordant_assertion_count'],0)
    def test_law_mismatch_and_othertext(self):
        r=m.inspect(raw(action('Became Public Law No: 113-2.')+action('Other assertion')),fixture.CASE)
        self.assertEqual(r['concordant_assertion_count'],0);self.assertEqual(r['terminal_assertions'][1]['assertion_kind'],'other_terminal_text')
    def test_fixed_denominator(self):
        with self.assertRaises(ValueError):m.select_cases({},[])
if __name__=='__main__':unittest.main()
