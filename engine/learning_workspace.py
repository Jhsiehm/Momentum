"""Read models and run the existing frozen-evidence learning workflow.

This surface never modifies the frozen learning implementation or promotes models.
"""
from collections import Counter
from . import sessions

BASE_NAMES = ['Legislative stage', 'Bill age', 'Event count', 'Time since last event',
              'Senate bill', 'Recent activity']


def weights(artifact):
    if not artifact:
        return []
    width = artifact.get('feature_manifest', {}).get('base_width', len(artifact['means']))
    names = [BASE_NAMES[i] if i < len(BASE_NAMES) else f'Feature {i+1}' for i in range(width)]
    if artifact.get('feature_policy') == 'structured_context':
        names += [f'Topic hash bin {i+1}' for i in range(16)]
        names += [f'Title hash bin {i+1}' for i in range(16)]
        names += ['Stage × recent activity', 'Stage × inactivity']
    return [dict(feature='Intercept', coefficient=artifact['weights'][0], mean=None, scale=None)] + [
        dict(feature=names[i], coefficient=w, mean=artifact['means'][i], scale=artifact['scales'][i])
        for i, w in enumerate(artifact['weights'][1:])]


def brief(session):
    record = session.get('learning') or {}
    result = session.get('result') or {}
    metrics, fixed = record.get('metrics'), record.get('fixed_metrics')
    return dict(id=session['id'], title=session['title'], dataset=session['config']['dataset'],
                created_at=session['created_at'], status=session['status'],
                learning_status=record.get('status'), blockers=session['preflight']['blockers'],
                trained_cases=record.get('eligible_count', 0), adjusted_cases=record.get('adjusted_count', 0),
                metrics=metrics, fixed_metrics=fixed, baseline=result.get('baseline'),
                brier_change=metrics['brier']-fixed['brier'] if metrics and fixed else None,
                reused=record.get('status') == 'reused', release_eligible=False)


def summary(store, dataset='official'):
    if dataset not in ('official', 'demo'):
        raise ValueError('Choose official or demo evidence')
    items=[brief(s) for s in sessions.list_sessions(store) if s['config']['dataset']==dataset]
    return dict(dataset=dataset, sessions=items, history_limit=100,
                note='Latest 100 research sessions, filtered by evidence type. Scores from different populations are not pooled.')


def detail(store, identity):
    session=sessions.get_session(store, identity)
    record=session.get('learning') or {}
    fixed={r['bill_id']:r for r in (session.get('result') or {}).get('results', [])}
    cases=[]
    for case in record.get('cases', []):
        original=fixed.get(case['bill_id'], {})
        cases.append(dict(bill_id=case['bill_id'], cutoff=original.get('cutoff'),
                          status=case['status'], reason=case.get('reason'),
                          probability=case.get('probability'), fixed_probability=case.get('original_probability'),
                          outcome=case.get('outcome'), feature_policy=case.get('selected_feature_policy'),
                          l2=case.get('selected_l2'), weights=weights(case.get('artifact')),
                          fixed_weights=weights(original.get('model_artifact')),
                          inner_validation=case.get('inner_validation'), training_hash=case.get('training_hash')))
    return dict(brief(session), cases=cases, evidence_hash=session['evidence_hash'],
                reproducibility_hash=record.get('reproducibility_hash'),
                reasons=dict(Counter(c['reason'] for c in cases if c.get('reason'))),
                note=record.get('note'), policy=record.get('selection_policy'))


def train(store, identity):
    # execute enforces source hashes, frozen code, audit gates and idempotence.
    sessions.execute(store, identity)
    return detail(store, identity)
