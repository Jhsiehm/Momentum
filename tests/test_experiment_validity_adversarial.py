"""Independent synthetic integrity challenges; no legal-accuracy certification.

These exercise a supplemental boundary, leaving registered experiment code intact.
All examples are authored fixtures, not held-out observations.
"""
import copy
import unittest
from xml.sax.saxutils import escape

from engine.paper_evaluation import seal, unseal
from scripts.bill_context_design_text_v2 import render
from scripts.mechanism_design_extractor_v3 import extract
from scripts.mechanism_design_extractor import MECHANISMS
from scripts.mechanism_validity_guard import (
    validate_view, validate_output, validate_reference, validate_semantic_sources, evaluate_guarded,
)


def source(bid='113-hr1', sentence='The Secretary shall submit an annual report.'):
    number=bid.split('hr')[1]
    raw=('<bill><form><congress>113th CONGRESS</congress><legis-num>H. R. '+number+
         '</legis-num></form><legis-body><section><header>Administration</header><text>'+
         escape(sentence)+'</text></section></legis-body></bill>').encode()
    body=render(raw,bid)
    return dict(body,view_hash=seal(body)['hash'])


def reference(view):
    text=view['text'];q='The Secretary shall submit an annual report.';a=text.index(q)
    effect=dict(mechanism='reporting',operation='create',dimension='procedure',actor='Secretary',
                target='Annual report submission',conditions=None,quote=q,start=a,end=a+len(q),
                rationale='The supplied operative clause imposes an annual submission duty.')
    statuses={m:('present' if m=='reporting' else 'absent') for m in MECHANISMS}
    row=dict(bill_id=view['bill_id'],source_view_hash=view['view_hash'],summary='Requires annual report submission.',
             mechanisms=statuses,uncertainties={},unresolved_effects=[],effects=[effect])
    return dict(records=[row],human_certified=False,historical_feature_eligible=False,
                semantic_accuracy_verified=False)


def semantic(view, effect_id):
    row=reference(view)['records'][0];e=row['effects'][0]
    effect={k:e[k] for k in ('mechanism','operation','dimension','actor','target','conditions')}
    effect.update(effect_id=effect_id,evidence=dict(source_view_hash=view['view_hash'],
                  **{k:e[k] for k in ('start','end','quote')}))
    return dict(scope='synthetic',records=[dict(bill_id=view['bill_id'],mechanisms=row['mechanisms'],effects=[effect])],
                human_certified=False,historical_feature_eligible=False)


class ExperimentValidityAdversarialTests(unittest.TestCase):
    def setUp(self):
        self.view=source();self.output=extract(self.view)
        self.views={self.view['bill_id']:self.view}

    def test_valid_synthetic_boundaries_pass_without_mutation(self):
        original=copy.deepcopy((self.view,self.output))
        validate_view(self.view)
        self.assertIsInstance(validate_output(self.view,self.output),dict)
        self.assertIsInstance(validate_reference(reference(self.view),self.views),dict)
        validate_semantic_sources(seal(semantic(self.view,'p')),seal(semantic(self.view,'r')),
                                  {self.view['view_hash']:self.view})
        self.assertEqual(original,(self.view,self.output))

    def test_output_identity_flags_counts_and_context_fail_closed(self):
        mutations=[
            lambda o:o.update(bill_id='113-hr2'),
            lambda o:o.update(source_view_hash='0'*64),
            lambda o:o.update(input_text_sha256='0'*64),
            lambda o:o.update(human_certified=True),
            lambda o:o.update(historical_feature_eligible=True),
            lambda o:o.update(accepted_v2_labels_created=1),
            lambda o:o.update(accepted_v2_labels_created=False),
            lambda o:o.update(trained_model=True),
            lambda o:o['coverage'].update(characters_scanned=1),
            lambda o:o['coverage'].update(scan_ranges=[[0,1]]),
            lambda o:o['coverage'].update(truncated=True),
            lambda o:o['assessments']['reporting'].update(candidate_count=999),
            lambda o:o['assessments']['reporting'].update(status='present'),
            lambda o:o['candidates'][0].update(quote='invented context'),
            lambda o:o['candidates'][0].update(context_path='/bill[1]/unknown[1]'),
            lambda o:o['candidates'][0]['hits'][0].update(start=True),
            lambda o:o['candidates'][0]['hits'][0].update(semantic_governance_verified=True),
            lambda o:o['candidates'][0]['hits'][0]['structural_context'][0].update(span_id='unbound'),
        ]
        for index,mutate in enumerate(mutations):
            with self.subTest(mutation=index):
                bad=copy.deepcopy(self.output);mutate(bad)
                with self.assertRaises(ValueError):validate_output(self.view,bad)

    def test_view_boolean_offset_and_forged_span_rejected(self):
        for mutate in (
            lambda v:v['spans'][0].update(start=False),
            lambda v:v['spans'][0].update(text_sha256='0'*64),
            lambda v:v['spans'].append(copy.deepcopy(v['spans'][0])),
        ):
            bad=copy.deepcopy(self.view);mutate(bad)
            with self.assertRaises(ValueError):validate_view(bad)

    def test_reference_status_schema_and_evidence_fail_closed(self):
        mutations=[
            lambda r:r['records'][0].update(source_view_hash='0'*64),
            lambda r:r['records'][0]['mechanisms'].pop('sunset'),
            lambda r:r['records'][0]['mechanisms'].update(deadline='present'),
            lambda r:r['records'][0]['mechanisms'].update(reporting='absent'),
            lambda r:r['records'][0]['mechanisms'].update(tax='uncertain'),
            lambda r:r['records'][0]['effects'][0].pop('conditions'),
            lambda r:r['records'][0]['effects'][0].update(dimension='invented'),
            lambda r:r['records'][0]['effects'][0].update(start=True),
            lambda r:r['records'][0]['effects'][0].update(quote='X'*len(r['records'][0]['effects'][0]['quote'])),
            lambda r:r['records'][0]['unresolved_effects'].append(dict(mechanism='tax',reason='Missing source context')),
            lambda r:r['records'].append(copy.deepcopy(r['records'][0])),
            lambda r:r.update(human_certified=True),
        ]
        for index,mutate in enumerate(mutations):
            with self.subTest(mutation=index):
                bad=reference(self.view);mutate(bad)
                with self.assertRaises(ValueError):validate_reference(bad,self.views)

    def test_cross_bill_view_cannot_be_relabelled_even_with_matching_quote(self):
        other=source('113-hr2')
        bad=reference(self.view);bad['records'][0]['source_view_hash']=other['view_hash']
        with self.assertRaises(ValueError):
            validate_reference(bad,{self.view['bill_id']:other})
        pred=semantic(self.view,'p');ref=semantic(self.view,'r')
        for body in (pred,ref):
            body['records'][0]['effects'][0]['evidence']['source_view_hash']=other['view_hash']
        with self.assertRaises(ValueError):
            validate_semantic_sources(seal(pred),seal(ref),{other['view_hash']:other})

    def test_semantic_same_length_fabrication_and_unknown_source_rejected(self):
        for mode in ('quote','hash','bool','missing_actor'):
            with self.subTest(mode=mode):
                pred=semantic(self.view,'p');ref=semantic(self.view,'r')
                e=pred['records'][0]['effects'][0]
                if mode=='quote':e['evidence']['quote']='X'*len(e['evidence']['quote'])
                elif mode=='hash':e['evidence']['source_view_hash']='f'*64
                elif mode=='bool':e['evidence']['start']=True
                else:e.pop('actor')
                with self.assertRaises(ValueError):
                    validate_semantic_sources(seal(pred),seal(ref),{self.view['view_hash']:self.view})

    def test_explicit_certification_overclaims_rejected(self):
        bad=reference(self.view);bad['semantic_accuracy_verified']=True
        with self.assertRaises(ValueError):validate_reference(bad,self.views)
        for flag in ('human_certified','historical_feature_eligible','semantic_accuracy_verified'):
            pred=semantic(self.view,'p');pred[flag]=True
            with self.subTest(flag=flag), self.assertRaises(ValueError):
                validate_semantic_sources(seal(pred),seal(semantic(self.view,'r')),
                                          {self.view['view_hash']:self.view})

    def test_proposal_schema_and_enums_are_not_optional(self):
        self.assertTrue(self.output['proposals'])
        for mutate in (
            lambda o:o.pop('proposals'),
            lambda o:o['proposals'][0].update(suggested_operation='invented'),
            lambda o:o['proposals'][0].update(suggested_dimension='invented'),
            lambda o:o['proposals'][0].pop('suggested_operation'),
        ):
            bad=copy.deepcopy(self.output);mutate(bad)
            with self.assertRaises(ValueError):validate_output(self.view,bad)

    def test_overlapping_unrelated_source_nodes_are_not_valid_hierarchy(self):
        bad=copy.deepcopy(self.view)
        node=copy.deepcopy(next(s for s in bad['spans'] if s['tag']=='text'))
        node['path']=node['path'].rsplit('/',1)[0]+'/text[999]'
        bad['spans'].append(node)
        with self.assertRaises(ValueError):validate_view(bad)

    def test_empty_effect_rows_still_require_complete_manifest_identity(self):
        body=semantic(self.view,'unused')
        body['records'][0]['effects']=[]
        body['records'][0]['mechanisms']={m:'absent' for m in MECHANISMS}
        good=seal(body)
        validate_semantic_sources(good,good,{self.view['view_hash']:self.view})
        for mode in ('wrong_bill','missing_row','partial_statuses','wrong_manifest_key'):
            bad=copy.deepcopy(body);manifest={self.view['view_hash']:self.view}
            if mode=='wrong_bill':bad['records'][0]['bill_id']='113-hr2'
            elif mode=='missing_row':bad['records']=[]
            elif mode=='partial_statuses':bad['records'][0]['mechanisms'].pop('tax')
            else:manifest={'f'*64:self.view}
            with self.subTest(mode=mode), self.assertRaises(ValueError):
                validate_semantic_sources(seal(bad),good,manifest)

    def test_quarantine_corruption_and_reactivation_rejected(self):
        from scripts.mechanism_design_extractor_v4 import extract as extract_v4
        output=extract_v4(self.view)
        self.assertTrue(output['legacy_proposals'])
        validate_output(self.view,output)
        for mutate in (
            lambda o:o['legacy_proposals'][0].update(quarantine_reason=''),
            lambda o:o['legacy_proposals'][0]['proposal'].update(candidate_id='unknown'),
            lambda o:o['legacy_proposals'][0]['proposal'].update(suggested_dimension='invented'),
            lambda o:o['legacy_proposals'][0]['proposal'].update(quote='invented'),
            lambda o:o['legacy_proposals'].append(copy.deepcopy(o['legacy_proposals'][0])),
            lambda o:o['proposals'].append(copy.deepcopy(o['legacy_proposals'][0]['proposal'])),
        ):
            bad=copy.deepcopy(output);mutate(bad)
            with self.assertRaises(ValueError):validate_output(self.view,bad)

    def test_guarded_scoring_binds_sources_but_does_not_certify_graph(self):
        p=seal(semantic(self.view,'p'));r=seal(semantic(self.view,'r'))
        g=seal(dict(scope='synthetic',prediction_hash=p['hash'],reference_hash=r['hash'],
                    origin=dict(kind='synthetic_fixture',adjudicator='fixture',method='Explicit fixture edge'),
                    edges=[dict(bill_id=self.view['bill_id'],prediction_id='p',reference_id='r')]))
        manifest={self.view['view_hash']:self.view}
        out=unseal(evaluate_guarded(p,r,g,manifest))
        self.assertEqual(out['effect_metrics']['tp'],1)
        self.assertTrue(out['source_content_verified'])
        self.assertFalse(out['semantic_accuracy_verified'])
        self.assertFalse(out['human_certified'])
        bad=copy.deepcopy(unseal(p));ev=bad['records'][0]['effects'][0]['evidence'];ev['quote']='X'*len(ev['quote'])
        bad=seal(bad);badgraph=copy.deepcopy(unseal(g));badgraph['prediction_hash']=bad['hash']
        with self.assertRaises(ValueError):evaluate_guarded(bad,r,seal(badgraph),manifest)
        wrong=copy.deepcopy(unseal(g));wrong['edges'][0]['reference_id']='unknown'
        with self.assertRaises(ValueError):evaluate_guarded(p,r,seal(wrong),manifest)

    def test_matching_source_spans_do_not_verify_actor_meaning(self):
        pred=semantic(self.view,'p');ref=semantic(self.view,'r')
        pred['records'][0]['effects'][0]['actor']='A different actor needing semantic adjudication'
        # Structural source guards must not masquerade as an entailment judge.
        validate_semantic_sources(seal(pred),seal(ref),{self.view['view_hash']:self.view})


if __name__=='__main__':unittest.main()
