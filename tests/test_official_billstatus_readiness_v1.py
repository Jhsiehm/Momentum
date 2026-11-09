import unittest
from scripts import official_billstatus_readiness_v1 as m

CASE=dict(bill_id='hr1-113',congress=113,bill_type='hr',bill_number=1,url='https://www.govinfo.gov/bulkdata/BILLSTATUS/113/hr/BILLSTATUS-113hr1.xml')

class ReadinessTests(unittest.TestCase):
    def xml(self,extra='',identity='<congress>113</congress><type>HR</type><number>1</number>'):
        return ('<billStatus version="3.0.0"><bill>'+identity+'<introducedDate>2013-01-03</introducedDate>'+extra+'</bill></billStatus>').encode()
    def test_identity_modern(self):
        r=m.inspect_xml(self.xml(),CASE);self.assertTrue(r['identity_valid']);self.assertEqual(r['identity_schema'],'modern')
    def test_identity_legacy(self):
        r=m.inspect_xml(self.xml(identity='<congress>113</congress><billType>H</billType><billNumber>1</billNumber>'),CASE)
        self.assertTrue(r['identity_valid']);self.assertEqual(r['identity_schema'],'legacy')
    def test_mismatch(self):
        r=m.inspect_xml(self.xml(identity='<congress>114</congress><type>HR</type><number>1</number>'),CASE)
        self.assertFalse(r['identity_valid']);self.assertTrue(r['errors'])
    def test_unknown_schema_fingerprint(self):
        r=m.inspect_xml(b'<unknown><entry/></unknown>',CASE)
        self.assertFalse(r['identity_valid']);self.assertIn('unknown/entry',r['schema_paths'])
    def test_dtd_entity_and_utf16_reject(self):
        for raw in [b'<!DOCTYPE billStatus><billStatus/>',b'<!ENTITY x "x"><billStatus/>','<billStatus/>'.encode('utf-16')]:
            with self.assertRaises(ValueError):m.inspect_xml(raw,CASE)
    def test_no_outcome_values(self):
        r=m.inspect_xml(self.xml('<laws><item><number>SECRET_OUTCOME</number></item></laws><actions><item><text>SECRET_ACTION</text><actionDate>2013-01-03</actionDate></item></actions>'),CASE)
        self.assertNotIn('SECRET_OUTCOME',str(r));self.assertNotIn('SECRET_ACTION',str(r));self.assertEqual(r['actions']['valid_date_count'],1)
    def test_context_counts(self):
        extra='<cosponsors><item><sponsorshipDate>2013-01-04</sponsorshipDate><sponsorshipWithdrawnDate>BAD</sponsorshipWithdrawnDate></item></cosponsors><textVersions><item><type>Introduced in House</type><date>2013-01-03</date><formats><item><url>https://www.govinfo.gov/x</url></item></formats></item></textVersions>'
        r=m.inspect_xml(self.xml(extra),CASE)
        self.assertEqual(r['cosponsors']['valid_join_date_count'],1);self.assertEqual(r['cosponsors']['valid_withdrawal_date_count'],0)
        self.assertEqual(r['text_versions']['records'][0]['url_count'],1)
    def test_sample_exact_observed_urls(self):
        results=[];pages={}
        for c in range(113,119):
            for kind in ('hr','s'):
                ids=[f'{kind}{n}-{c}' for n in range(1,11)]
                results.append(dict(congress=c,bill_type=kind,ids=ids,unique_count=10,accepted_index=True))
                pages[f'{c}-{kind}']=''.join(f'<a href="/bulkdata/BILLSTATUS/{c}/{kind}/BILLSTATUS-{c}{kind}{n}.xml">x</a>' for n in range(1,11))
        index=dict(all_indexes_accepted=True,results=results,unique_ids=120)
        pop,sample=m.population_and_sample(index,pages)
        expected=sorted(pop,key=lambda bid:m.common.digest((m.VERSION+'\n'+bid).encode()))[:100]
        self.assertEqual([r['bill_id'] for r in sample],expected)
        pages['113-hr']=''
        with self.assertRaises(ValueError):m.population_and_sample(index,pages)
if __name__=='__main__':unittest.main()
