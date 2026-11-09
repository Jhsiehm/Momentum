import copy
import unittest
from scripts.run_mechanism_validity_v5 import check_v4_preservation,decision_changes,CODE

class V5RunnerTests(unittest.TestCase):
    def test_preservation_rejects_loss_and_quarantine_change(self):
        old=dict(candidates=[dict(mechanism='prohibit',hits=[dict(start=1,end=2)])],legacy_proposals=[{'proposal':{'id':'x'}}],proposals=[])
        check_v4_preservation(old,copy.deepcopy(old))
        for key,value in [('candidates',[]),('legacy_proposals',[]),('proposals',[1])]:
            bad=copy.deepcopy(old);bad[key]=value
            with self.assertRaises(ValueError):check_v4_preservation(old,bad)
    def test_reason_and_evidence_changes_count_without_status_change(self):
        key=('prohibit',1,2);old={key:dict(status='flagged',reasons=['heading'],evidence=[{'quote':'a'}])}
        for field,value in [('reasons',['heading','struck_inline_quote']),('evidence',[{'quote':'b'}]),('status','retain')]:
            new=copy.deepcopy(old);new[key][field]=value
            changes=decision_changes(old,new)
            self.assertEqual(len(changes),1)
            self.assertEqual(changes[0]['before'][field],old[key][field])
            self.assertEqual(changes[0]['after'][field],value)
        self.assertEqual(decision_changes(old,old),[])
    def test_manifest_pins_all_new_modules_and_tests(self):
        self.assertEqual(len(CODE),len(set(CODE)))
        for path in ('scripts/run_mechanism_validity_v5.py','scripts/mechanism_design_extractor_v5.py','scripts/mechanism_context_filter_v3.py','tests/test_mechanism_v5_independent.py'):
            self.assertIn(path,CODE)

if __name__=='__main__':unittest.main()
