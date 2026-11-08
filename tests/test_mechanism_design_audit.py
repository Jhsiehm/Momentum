import copy
import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from engine.paper_evaluation import seal, save
from scripts.mechanism_design_audit import validate, compare, verify_adjudication


class MechanismDesignAuditTests(unittest.TestCase):
    def setUp(self):
        self.spec={'selected_ids':['113-hr1'],'mechanisms':['authorize'],'labels':['present','absent','uncertain']}
        self.inputs=[{'bill_id':'113-hr1','text':'Shall not authorize new spending.'}]
        self.review={'reviewer':'agent_a','registration_hash':'hash','human_certified':False,'historical_feature_eligible':False,
                     'records':[{'bill_id':'113-hr1','summary':'Restricts spending authority.','labels':{'authorize':{'status':'absent','quote':'not authorize','rationale':'Negated, not affirmative authorization.'}}}]}

    def test_exact_quote_span_and_unknown_allowed(self):
        spans=validate(self.review,self.spec,self.inputs,'hash','agent_a')
        self.assertEqual(self.inputs[0]['text'][spans[0]['start']:spans[0]['end']],'not authorize')
        self.review['records'][0]['labels']['authorize'].update(status='uncertain',quote=None)
        self.assertEqual(validate(self.review,self.spec,self.inputs,'hash','agent_a'),[])

    def test_unsupported_present_and_certification_rejected(self):
        label=self.review['records'][0]['labels']['authorize'];label.update(status='present',quote=None)
        with self.assertRaisesRegex(ValueError,'lacks evidence'):validate(self.review,self.spec,self.inputs,'hash','agent_a')
        label['quote']='authorizes spending'
        with self.assertRaisesRegex(ValueError,'does not resolve'):validate(self.review,self.spec,self.inputs,'hash','agent_a')
        label['quote']='not authorize';self.review['human_certified']=True
        with self.assertRaisesRegex(ValueError,'certification'):validate(self.review,self.spec,self.inputs,'hash','agent_a')

    def test_missing_field_or_wrong_identity_rejected(self):
        self.review['records'][0]['bill_id']='113-hr2'
        with self.assertRaisesRegex(ValueError,'identity'):validate(self.review,self.spec,self.inputs,'hash','agent_a')
        self.review['records'][0]['bill_id']='113-hr1';self.review['records'][0]['labels']={}
        with self.assertRaisesRegex(ValueError,'mechanism'):validate(self.review,self.spec,self.inputs,'hash','agent_a')

    def test_disagreement_and_immutable_replay(self):
        with tempfile.TemporaryDirectory() as temp:
            path=Path(temp)
            spec=dict(self.spec,reviewers=['agent_a','agent_b'],adjudicator='agent_c',inputs_hash=hashlib.sha256(json.dumps(self.inputs,sort_keys=True).encode()).hexdigest())
            registration=seal(spec);save(path/'registration.json',registration);save(path/'inputs.json',seal(self.inputs))
            a=copy.deepcopy(self.review);a['registration_hash']=registration['hash']
            b=copy.deepcopy(a);b['reviewer']='agent_b';b['records'][0]['labels']['authorize']['status']='uncertain'
            save(path/'agent_a.json',seal(a));save(path/'agent_b.json',seal(b))
            result=compare(path)
            self.assertEqual(result['body']['comparisons'],1)
            self.assertEqual(result['body']['agreements'],0)
            self.assertEqual(len(result['body']['disagreements']),1)
            self.assertEqual(compare(path),result)
            c=copy.deepcopy(a);c['reviewer']='agent_c'
            c.update(comparison_hash=result['hash'],review_hashes=result['body']['review_hashes'],original_disagreements=result['body']['disagreements'],
                     challenges=[dict(bill_id='113-hr1',mechanism='authorize',agent_a=a['records'][0]['labels']['authorize'],
                                      agent_b=b['records'][0]['labels']['authorize'],original_agreement=False,
                                      adjudicated_status='absent',challenge_rationale='Explicit negation retained.')])
            save(path/'adjudication.json',seal(c))
            self.assertEqual(verify_adjudication(path)['body']['challenge_count'],1)
            c['challenges'][0]['agent_a']=dict(status='present')
            (path/'adjudication.json').write_text(json.dumps(seal(c)))
            with self.assertRaisesRegex(ValueError,'Original review label changed'):verify_adjudication(path)


if __name__=='__main__':unittest.main()
