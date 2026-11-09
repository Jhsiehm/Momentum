import unittest
import copy
from scripts.run_mechanism_validity_v4 import compare, CODE, check_legacy_preservation
from scripts.mechanism_design_extractor_v2 import extract as v2
from scripts.mechanism_design_extractor_v4 import extract as v4
from tests.test_mechanism_design_extractor import view, clause
from scripts.mechanism_design_extractor import MECHANISMS


def output(rows, proposals=(), quarantine=()):
    return dict(candidates=[dict(mechanism=m, hits=[dict(start=a, end=b)]) for m,a,b in rows],
                proposals=list(proposals), legacy_proposals=list(quarantine))


def decisions(rows, flagged=()):
    return {k: dict(status='flagged' if k in flagged else 'retain') for k in rows}


class ValidityRunnerTests(unittest.TestCase):
    def test_half_open_matching_and_mechanism_boundaries(self):
        mechanism = MECHANISMS[0]; other = MECHANISMS[1]
        rows = [(mechanism, 0, 5), (mechanism, 10, 15), (other, 6, 9)]
        ref = dict(effects=[dict(mechanism=mechanism, start=5, end=10)])
        result = compare(ref, output(rows), output(rows), decisions(rows), decisions(rows))
        counts = result['by_mechanism'][mechanism]
        self.assertEqual(counts['reference_effects'], 1)
        self.assertEqual(counts['old_raw_overlap'], 0)
        self.assertEqual(counts['new_raw_overlap'], 0)

    def test_raw_loss_recovery_and_retained_transitions_distinct(self):
        m = MECHANISMS[0]
        old = [(m, 0, 2), (m, 5, 7), (m, 10, 12)]
        new = [(m, 5, 7), (m, 10, 12), (m, 15, 17)]
        ref = dict(effects=[dict(mechanism=m, start=i, end=i+2) for i in (0,5,10,15)])
        result = compare(ref, output(old, [1]), output(new, quarantine=[1]),
                         decisions(old, [old[1]]), decisions(new, [new[1]]))
        c = result['by_mechanism'][m]
        self.assertEqual((c['raw_lost'], c['raw_recovered']), (1,1))
        self.assertEqual((c['retained_lost'], c['retained_recovered']), (2,2))
        self.assertEqual((c['common_flag_to_retain'], c['common_retain_to_flag']), (1,1))
        self.assertEqual((c['old_raw_overlap'], c['new_raw_overlap']), (3,3))
        self.assertEqual(result['removed_hit_identities'], [list(old[0])])
        self.assertEqual(result['added_hit_identities'], [list(new[-1])])
        self.assertEqual(result['quarantined_proposals'], 1)
        self.assertEqual(result['new_active_proposals'], 0)
        self.assertEqual(len(result['reference_intersections']), 4)

    def test_multiple_hits_count_reference_once_and_fail_incomplete_decisions(self):
        m=MECHANISMS[0]; rows=[(m,0,2),(m,3,5)]
        ref=dict(effects=[dict(mechanism=m,start=0,end=6)])
        result=compare(ref,output(rows),output(rows),decisions(rows,[rows[0]]),decisions(rows))
        c=result['by_mechanism'][m]
        self.assertEqual(c['old_retained_overlap'],1)
        self.assertEqual(c['old_hits'],2)
        with self.assertRaises(ValueError):
            compare(ref,output(rows),output(rows),{},decisions(rows))

    def test_legacy_invariants_detect_loss_mutation_and_quarantine_loss(self):
        source=view(clause('No person may receive a grant.'))
        baseline=v2(source); current=v4(source)
        check_legacy_preservation(baseline,current)
        mutations=[]
        changed=copy.deepcopy(current); changed['candidates'][0]['hits']=[]; mutations.append(changed)
        changed=copy.deepcopy(current); changed['candidates'][0]['quote']='wrong'; mutations.append(changed)
        changed=copy.deepcopy(current); changed['legacy_proposals']=[]; mutations.append(changed)
        self.assertTrue(baseline['proposals'])
        for changed in mutations:
            with self.assertRaises(ValueError): check_legacy_preservation(baseline,changed)

    def test_quarantine_order_and_completeness_are_exact(self):
        baseline=dict(candidates=[],proposals=[{'id':'first'},{'id':'second'}])
        current=dict(candidates=[],proposals=[],legacy_proposals=[
            {'proposal':p,'quarantine_reason':'unvalidated'} for p in baseline['proposals']])
        check_legacy_preservation(baseline,current)
        for quarantined in (current['legacy_proposals'][:1],list(reversed(current['legacy_proposals']))):
            changed=dict(current,legacy_proposals=quarantined)
            with self.assertRaises(ValueError): check_legacy_preservation(baseline,changed)

    def test_freeze_manifest_includes_runner_guard_and_new_implementations(self):
        for name in ('scripts/run_mechanism_validity_v4.py','scripts/mechanism_validity_guard.py',
                     'scripts/mechanism_design_extractor_v4.py','scripts/mechanism_context_filter_v2.py',
                     'tests/test_mechanism_validity_v4_runner.py'):
            self.assertIn(name,CODE)
        self.assertEqual(len(CODE),len(set(CODE)))


if __name__ == '__main__': unittest.main()
