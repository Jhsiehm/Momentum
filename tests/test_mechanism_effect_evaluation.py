import copy
from itertools import combinations
import unittest

from engine.paper_evaluation import seal,unseal
from engine.store import digest
from scripts.mechanism_effect_evaluation import evaluate,match_effects


def effect(ident,actor='Agency',operation='create',quote='The Agency may not disclose records.'):
    return dict(effect_id=ident,mechanism='prohibit',operation=operation,dimension='authority_scope',actor=actor,target='disclosure of records',conditions=None,
                evidence=dict(source_view_hash=digest('synthetic-source'),start=0,end=len(quote),quote=quote))


def submission(effects,status='present',bill='113-hr1'):
    return seal(dict(scope='synthetic',records=[dict(bill_id=bill,mechanisms={'prohibit':status},effects=effects)]))


def graph(pred,ref,edges):
    return seal(dict(scope='synthetic',prediction_hash=pred['hash'],reference_hash=ref['hash'],
                     origin=dict(kind='synthetic_fixture',adjudicator='test-fixture-author',method='Explicit supplied compatibility; no automatic semantic judgment'),
                     edges=[dict(bill_id='113-hr1',prediction_id=p,reference_id=r) for p,r in edges]))


class EffectEvaluationTests(unittest.TestCase):
    def test_maximum_matching_avoids_greedy_trap_and_is_lexical(self):
        self.assertEqual(match_effects(['p1','p2'],['r1','r2'],[('p1','r1'),('p1','r2'),('p2','r1')]),[('p1','r2'),('p2','r1')])
        self.assertEqual(match_effects(['p2','p1'],['r2','r1'],[(p,r) for p in ['p2','p1'] for r in ['r2','r1']]),[('p1','r1'),('p2','r2')])

    def test_small_graphs_match_exhaustive_maximum_lexical_oracle(self):
        preds=['p1','p2','p3'];refs=['r1','r2','r3'];possible=[(p,r) for p in preds for r in refs]
        for mask in range(1<<len(possible)):
            edges=[e for i,e in enumerate(possible) if mask&(1<<i)]
            valid=[[]]
            for size in range(1,4):
                valid += [list(pairs) for pairs in combinations(edges,size) if len({p for p,r in pairs})==size and len({r for p,r in pairs})==size]
            best=min(valid,key=lambda pairs:(-len(pairs),pairs))
            self.assertEqual(match_effects(preds,refs,edges),best)

    def test_duplicate_prediction_is_false_positive_and_omission_false_negative(self):
        pred=submission([effect('p1'),effect('p2')]);ref=submission([effect('r1'),effect('r2')])
        result=unseal(evaluate(pred,ref,graph(pred,ref,[('p1','r1'),('p2','r1')])))
        self.assertEqual(result['effect_metrics'],dict(tp=1,fp=1,fn=1,precision=.5,recall=.5,f1=.5))
        self.assertEqual(result['effect_results'][0]['unmatched_prediction_ids'],['p2'])
        self.assertEqual(result['effect_results'][0]['unmatched_reference_ids'],['r2'])

    def test_actor_direction_and_negation_errors_need_supplied_compatibility(self):
        # Identical source text does not make these incompatible interpretations match.
        for bad in [effect('p',actor='Public'),effect('p',operation='remove'),dict(effect('p'),target='permission to disclose records')]:
            pred=submission([bad]);ref=submission([effect('r')])
            out=unseal(evaluate(pred,ref,graph(pred,ref,[])))
            self.assertEqual((out['effect_metrics']['tp'],out['effect_metrics']['fp'],out['effect_metrics']['fn']),(0,1,1))
            self.assertEqual(out['span_diagnostic']['equal_span_pairs'],1)
            self.assertEqual(out['span_diagnostic']['equal_span_matched_pairs'],0)

    def test_different_spans_can_match_when_external_graph_says_compatible(self):
        pred=submission([effect('p',quote='Agency disclosure is barred.')]);ref=submission([effect('r')])
        out=unseal(evaluate(pred,ref,graph(pred,ref,[('p','r')])))
        self.assertEqual(out['effect_metrics']['tp'],1)
        self.assertEqual(out['span_diagnostic']['equal_span_pairs'],0)
        self.assertFalse(out['semantic_accuracy_verified']);self.assertFalse(out['human_certified'])
        self.assertEqual(out['graph_origin']['kind'],'synthetic_fixture')

    def test_status_uncertain_false_negative_and_reference_exclusion(self):
        pred=submission([],status='uncertain');ref=submission([effect('r')])
        out=unseal(evaluate(pred,ref,graph(pred,ref,[])))
        self.assertEqual(out['status_evaluation']['counts']['fn'],1)
        self.assertEqual(out['status_evaluation']['positive_metrics']['recall'],0)
        ref=submission([],status='uncertain')
        out=unseal(evaluate(pred,ref,graph(pred,ref,[])))
        self.assertEqual(out['status_evaluation']['excluded_count'],1)
        self.assertEqual(out['status_evaluation']['records'],[])
        self.assertIsNone(out['effect_metrics']['precision'])
        self.assertIsNone(out['effect_metrics']['recall'])
        self.assertIsNone(out['effect_metrics']['f1'])

    def test_uncertain_negative_is_abstention_not_true_negative(self):
        pred=submission([],status='uncertain');ref=submission([],status='absent')
        out=unseal(evaluate(pred,ref,graph(pred,ref,[])))['status_evaluation']
        self.assertEqual(out['counts']['abstain_negative'],1);self.assertEqual(out['counts']['tn'],0)
        self.assertEqual(sum(x['count'] for x in out['confusion']),1)

    def test_corrupt_seal_and_wrong_graph_bindings_rejected(self):
        pred=submission([effect('p')]);ref=submission([effect('r')]);g=graph(pred,ref,[('p','r')])
        bad=copy.deepcopy(pred);bad['body']['records'][0]['effects'][0]['actor']='changed'
        with self.assertRaisesRegex(ValueError,'hash mismatch'):evaluate(bad,ref,g)
        bad=copy.deepcopy(g['body']);bad['reference_hash']=pred['hash']
        with self.assertRaisesRegex(ValueError,'binding mismatch'):evaluate(pred,ref,seal(bad))

    def test_duplicate_ids_edges_and_unknown_endpoints_rejected(self):
        pred=submission([effect('p'),effect('p')]);ref=submission([effect('r')])
        with self.assertRaisesRegex(ValueError,'duplicate effect'):evaluate(pred,ref,graph(pred,ref,[]))
        pred=submission([effect('p')])
        with self.assertRaisesRegex(ValueError,'Duplicate compatibility'):evaluate(pred,ref,graph(pred,ref,[('p','r'),('p','r')]))
        with self.assertRaisesRegex(ValueError,'Unknown compatibility'):evaluate(pred,ref,graph(pred,ref,[('missing','r')]))

    def test_cross_bill_edges_and_incomplete_bill_coverage_rejected(self):
        pred=submission([effect('p')]);ref=submission([effect('r')],bill='113-hr2')
        with self.assertRaisesRegex(ValueError,'bill coverage'):evaluate(pred,ref,graph(pred,ref,[]))
        pbody=copy.deepcopy(pred['body']);rbody=copy.deepcopy(ref['body'])
        pbody['records'].append(dict(bill_id='113-hr2',mechanisms={'prohibit':'absent'},effects=[]))
        rbody['records'].append(dict(bill_id='113-hr1',mechanisms={'prohibit':'absent'},effects=[]))
        pred,ref=seal(pbody),seal(rbody)
        with self.assertRaisesRegex(ValueError,'Cross-bill'):evaluate(pred,ref,graph(pred,ref,[('p','r')]))

    def test_present_requires_effect_and_graph_respects_structural_semantics(self):
        pred=submission([]);ref=submission([effect('r')])
        with self.assertRaisesRegex(ValueError,'requires a supported effect'):evaluate(pred,ref,graph(pred,ref,[]))
        for field,value in [('operation','remove'),('dimension','duration'),('mechanism','authorize')]:
            body=copy.deepcopy(submission([effect('p')])['body'])
            body['records'][0]['effects'][0][field]=value
            if field=='mechanism':
                body['records'][0]['mechanisms']={'prohibit':'absent','authorize':'present'}
            pred=seal(body)
            with self.assertRaisesRegex(ValueError,'Incompatible mechanism'):evaluate(pred,ref,graph(pred,ref,[('p','r')]))
        pred=submission([dict(effect('p'),dimension='invented')])
        with self.assertRaisesRegex(ValueError,'operation/dimension'):evaluate(pred,ref,graph(pred,ref,[]))

    def test_origin_scope_and_span_validation(self):
        pred=submission([effect('p')]);ref=submission([effect('r')]);g=graph(pred,ref,[])
        body=copy.deepcopy(g['body']);body.pop('origin')
        with self.assertRaisesRegex(ValueError,'origin'):evaluate(pred,ref,seal(body))
        body=copy.deepcopy(pred['body']);body['scope']='quality';bad=seal(body)
        with self.assertRaisesRegex(ValueError,'design/synthetic'):evaluate(bad,ref,graph(bad,ref,[]))
        body=copy.deepcopy(pred['body']);body['records'][0]['effects'][0]['evidence']['start']=True;bad=seal(body)
        with self.assertRaisesRegex(ValueError,'offsets'):evaluate(bad,ref,graph(bad,ref,[]))


if __name__=='__main__':unittest.main()
