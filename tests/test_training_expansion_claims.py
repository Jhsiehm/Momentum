import copy
import unittest

from engine.paper_evaluation import seal, unseal
from scripts.mechanism_training_coverage import coverage
from scripts.verify_training_expansion_claims import check_claims


class ClaimTests(unittest.TestCase):
    def fixture(self):
        baseline = [f'113-hr{x}' for x in range(1,233)]
        selected = [dict(bill_id='114-hr1', congress=114), dict(bill_id='114-hr2', congress=114)]
        plan = dict(cycle=1, bill_ids=[s['bill_id'] for s in selected], acquisition_cap=100)
        spec = dict(selection=selected, cycles=[plan], baseline_available_ids=baseline, baseline={'ids':baseline},
                    memberships={'115':dict(core_ids=baseline+['114-hr1'], calibration_ids=['114-hr2'])},
                    historical_feature_eligible=False, human_certified=False, quality_texts_opened=False)
        records = {}
        for i, s in enumerate(selected):
            r = dict(**s, registration_hash='reg', historical_feature_eligible=False, human_certified=False,
                     mechanism_labels_created=0, status='blocked' if i else 'metadata_dated_current_xml')
            if i:r['error']='404'
            else:r['historical_rendition_identity']='uncertified'
            records[s['bill_id']] = seal(r)
        failures = [dict(bill_id='114-hr2',error='404')]
        cr = seal(dict(**plan, registration_hash='reg'))
        cycle = seal(dict(cycle=1, registration_hash='reg', cycle_registration_hash=cr['hash'],
                          record_hashes={bid:e['hash'] for bid,e in records.items()}, attempted=2, usable=1,
                          failures=failures, historical_feature_eligible=False, frozen_files_unchanged=True))
        # A downloaded file may belong to a blocked rendering case and still counts.
        manifest = [dict(bytes=10),dict(bytes=20)]
        result = dict(registration_hash='reg', selected=2, attempted=2, completed_cycles=1, baseline_unique=232,
                      total_unique=233, usable_metadata_dated_current_xml=1, downloaded_documents=2, source_bytes=30,
                      certified_historical=0, models_fitted=0, outcomes_scored=0, mechanism_labels_created=0,
                      frozen_artifacts_unchanged=True, failures=failures, usable_by_congress={'114':1},
                      historical_feature_eligible=False, human_certified=False, quality_texts_opened=False,
                      coverage_before=coverage(spec['memberships'],baseline),
                      coverage_after=coverage(spec['memberships'],baseline+['114-hr1']),
                      coverage_increment=coverage(spec['memberships'],['114-hr1']))
        return spec,'reg',result,records,[(cr,cycle)],manifest,baseline

    def test_success_includes_downloaded_but_blocked_source(self):
        counts=check_claims(*self.fixture())
        self.assertEqual((counts['downloaded_documents'],counts['source_bytes'],counts['total_unique']),(2,30,233))

    def test_resealed_result_mutations_rejected(self):
        mutations = {k:True for k in ('historical_feature_eligible','human_certified','quality_texts_opened')}
        mutations.update({k:999 for k in ('selected','attempted','completed_cycles','baseline_unique','total_unique',
                                        'usable_metadata_dated_current_xml','downloaded_documents','source_bytes',
                                        'certified_historical','models_fitted','outcomes_scored','mechanism_labels_created')})
        mutations.update(registration_hash='other', frozen_artifacts_unchanged=False, failures=[],usable_by_congress={'114':2},coverage_before={})
        for key,value in mutations.items():
            with self.subTest(key=key):
                args=list(self.fixture());args[2][key]=value
                args[2]=unseal(seal(args[2]))
                with self.assertRaises(ValueError):check_claims(*args)

    def test_resealed_cycle_mutations_rejected(self):
        for key,value in dict(cycle=2, registration_hash='wrong', cycle_registration_hash='wrong',record_hashes={},
                              attempted=3,usable=2,failures=[],historical_feature_eligible=True,frozen_files_unchanged=False).items():
            with self.subTest(key=key):
                args=list(self.fixture());reg,env=args[4][0];body=copy.deepcopy(env['body']);body[key]=value
                args[4]=[(reg,seal(body))]
                with self.assertRaises(ValueError):check_claims(*args)

    def test_baseline_identity_and_record_claim_mutations_rejected(self):
        args=list(self.fixture());args[6]=args[6][:-1]+[args[6][0]]
        with self.assertRaisesRegex(ValueError,'Baseline'):check_claims(*args)
        for field,value in [('human_certified',True),('historical_feature_eligible',True),('mechanism_labels_created',1),('historical_rendition_identity','certified')]:
            args=list(self.fixture());body=copy.deepcopy(args[3]['114-hr1']['body']);body[field]=value;args[3]['114-hr1']=seal(body)
            with self.subTest(field=field),self.assertRaises(ValueError):check_claims(*args)

    def test_boolean_count_is_not_an_integer_claim(self):
        args=list(self.fixture());args[2]['completed_cycles']=True
        with self.assertRaisesRegex(ValueError,'count'):check_claims(*args)


if __name__=='__main__':unittest.main()
