import unittest
from unittest.mock import patch
from xml.etree import ElementTree as ET
from engine import passage_evidence as p

class EvidenceTests(unittest.TestCase):
    def action(self,code='8000',chamber='House',system='9'):
        return f'<item><actionDate>2023-04-01</actionDate><actionCode>{code}</actionCode><sourceSystem><code>{system}</code></sourceSystem><text>Passed/agreed to in {chamber}: Passed.</text></item>'
    def test_other_chamber_and_system_are_not_origin_passage(self):
        b=ET.fromstring('<bill><actions>'+self.action('17000','Senate')+self.action(system='2')+'</actions></bill>')
        self.assertEqual(p.passage_actions(b,'hr'),[])
        self.assertEqual(len(p.passage_actions(b,'s')),1)
    def audit(self,action=True,engrossed_date='2023-04-01',intro_available='2023-01-03T23:59:59Z'):
        text='<root><bill><congress>118</congress><type>HR</type><number>1</number><introducedDate>2023-01-01</introducedDate><actions>'+(self.action() if action else '')+'</actions><textVersions>'
        for version in ['ih','eh']:text+=f'<item><formats><item><url>https://www.govinfo.gov/content/pkg/BILLS-118hr1{version}/pdf/x.pdf</url></item></formats></item>'
        text+='</textVersions></bill></root>'
        class Source:
            def get(self,url):return text.encode(),dict(url=url,sha256='fixture')
        def package(s,key):
            intro=key.endswith('ih');issued='2023-01-01' if intro else engrossed_date
            return ET.Element('mods'),dict(package=key,issued_at=p.timestamp(issued),available_at=intro_available if intro else '2023-04-03T23:59:59Z')
        with patch.object(p.cohort,'package_audit',side_effect=package),patch.object(p,'validate_introduction',return_value={'valid':True}):return p.audit_bill(Source(),'118-hr1')
    def test_positive_requires_matching_dated_publication(self):
        self.assertEqual(self.audit()['label']['value'],1)
        self.assertIsNone(self.audit(engrossed_date='2023-04-02')['label'])
    def test_missing_action_never_becomes_negative(self):
        row=self.audit(action=False);self.assertIsNone(row['label']);self.assertIn('no_complete_negative',row['label_blocker'])
    def test_late_introduction_blocks_historical_checkpoint(self):
        row=self.audit(intro_available='2023-02-10T23:59:59Z');self.assertEqual(row['checkpoint']['status'],'blocked')
    def test_future_passage_not_in_checkpoint_features(self):
        row=self.audit();self.assertEqual(row['checkpoint']['eligible_packages'],['BILLS-118hr1ih']);self.assertEqual(row['checkpoint']['publication_proxy_features'][0],0)
    def test_evidence_not_claimed_complete_or_human_reviewed(self):
        row=self.audit();self.assertFalse(row['checkpoint']['complete_action_history']);self.assertFalse(row['label']['human_reviewed'])
