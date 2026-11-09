import unittest
import xml.etree.ElementTree as ET
from scripts import action_context_features_v1 as m
from tests import test_official_context_v1 as fixtures
CASE=fixtures.CASE

def action(code='1000',source='9',when='2013-01-03'):
    return f'<item><actionDate>{when}</actionDate><actionCode>{code}</actionCode><sourceSystem><code>{source}</code></sourceSystem></item>'

def raw(actions=None,extra=''):
    root=ET.fromstring(fixtures.ContextTests().raw(extra,actions=actions));bill=root.find('bill');bill.remove(bill.find('textVersions'));return ET.tostring(root)

class ActionTests(unittest.TestCase):
    def test_no_publication_gate(self):
        f=m.extract_features(raw(extra='<textVersions><item><date/></item></textVersions>'),CASE)
        self.assertEqual(f['anchor'],[0,0]);self.assertEqual(len(f['context']),3)
    def test_house_mapping_and_nonmilestones(self):
        for code,stage in [('5000',1),('8000',2),('28000',3),('14000',0),('17000',0),('H30000',0),('36000',0),('37000',0)]:
            self.assertEqual(m.extract_features(raw(action(code)),CASE)['stage'],stage)
    def test_senate_mapping(self):
        case=dict(CASE,bill_id='s1-113',bill_type='s')
        for code,stage in [('14000',1),('17000',2),('28000',3),('5000',0),('8000',0)]:
            f=m.extract_features(raw(action(code)).replace(b'<type>HR</type>',b'<type>S</type>'),case)
            self.assertEqual(f['anchor'],[stage/3,1])
    def test_source_nine_only(self):
        for source in ('0','1','2'):
            self.assertEqual(m.extract_features(raw(action('8000',source)),CASE)['stage'],0)
        named=action('8000').replace('<code>9</code>','<name>Senate</name>')
        self.assertEqual(m.extract_features(raw(named),CASE)['stage'],0)
    def test_cutoff_and_maximum(self):
        f=m.extract_features(raw(action('5000')+action('8000',when='2013-07-02')+action('28000',when='2014-01-01')),CASE)
        self.assertEqual(f['stage'],1);self.assertEqual(len(f['milestone_evidence']),1)
    def test_later_invalid_history_excludes(self):
        for extra in (action('1000','77','2014-01-01'),action('1000','9','2014-99-01')):
            self.assertIsNone(m.extract_features(raw(action()+extra),CASE)['anchor'])
    def test_empty_or_no_early_actions(self):
        for acts in ('',action(when='2013-07-02')):
            self.assertIsNone(m.extract_features(raw(acts),CASE)['anchor'])
    def test_opaque_activity_does_not_invent_semantics(self):
        f=m.extract_features(raw(action('OTHER-X'),'<committees/>'),CASE)
        self.assertEqual(f['anchor'],[0,0]);self.assertEqual(f['context'][1],0);self.assertIsNone(f['context'][2])
    def test_resolver_unchanged(self):self.assertIs(m.resolve_outcome,m.v2.resolve_outcome)

if __name__=='__main__':unittest.main()
