"""Immutable, collection-scoped research sessions with frozen evidence."""
import json
import tempfile
import uuid
from collections import Counter
from datetime import timedelta
from pathlib import Path
from .store import Store, ROOT, now, digest, congress_end
from .model import date, snapshot, resolution, training_rows, fit, predict, score, MODEL_VERSION, FEATURE_VERSION

SCHEMA = '''
CREATE TABLE IF NOT EXISTS research_sessions(id TEXT PRIMARY KEY, created_at TEXT, body TEXT NOT NULL, evidence TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS session_results(session_id TEXT PRIMARY KEY, body TEXT NOT NULL);
CREATE TRIGGER IF NOT EXISTS sessions_no_update BEFORE UPDATE ON research_sessions BEGIN SELECT RAISE(ABORT,'Research sessions are immutable'); END;
CREATE TRIGGER IF NOT EXISTS sessions_no_delete BEFORE DELETE ON research_sessions BEGIN SELECT RAISE(ABORT,'Research sessions are immutable'); END;
CREATE TRIGGER IF NOT EXISTS session_results_no_update BEFORE UPDATE ON session_results BEGIN SELECT RAISE(ABORT,'Session results are immutable'); END;
CREATE TRIGGER IF NOT EXISTS session_results_no_delete BEFORE DELETE ON session_results BEGIN SELECT RAISE(ABORT,'Session results are immutable'); END;
'''
LIMITATIONS = ['Development evaluation, not a protected holdout or evidence of release readiness.',
              'Historical availability and family provenance are stored assertions, not independently authenticated by this runner.',
              'No calibrated probability interval or clustered uncertainty estimate is implemented.',
              'Synthetic results test pipeline behavior only; official imported subsets are not a census.']


def initialize(store):
    store.db.executescript(SCHEMA)


def _code():
    return {name: digest((ROOT / 'engine' / name).read_text()) for name in ('sessions.py', 'model.py', 'store.py', 'learning.py')}


def _row(store, identity):
    initialize(store)
    row = store.db.execute('SELECT body,evidence FROM research_sessions WHERE id=?', (identity,)).fetchone()
    if not row:
        raise ValueError('Research session not found')
    return json.loads(row[0]), json.loads(row[1])


def get_session(store, identity):
    proposal, _ = _row(store, identity)
    row = store.db.execute('SELECT body FROM session_results WHERE session_id=?', (identity,)).fetchone()
    result = json.loads(row[0]) if row else None
    output = dict(proposal, result=result, status=result['status'] if result else proposal['status'])
    if result:
        from . import learning
        output['learning'] = learning.get(store, identity)
    return output


def list_sessions(store):
    initialize(store)
    return [get_session(store, r[0]) for r in store.db.execute('SELECT id FROM research_sessions ORDER BY created_at DESC,rowid DESC LIMIT 100')]


class _Frozen:
    def __init__(self, records):
        self.tmp = tempfile.TemporaryDirectory()
        self.store = Store(Path(self.tmp.name) / 'frozen.sqlite')
        with self.store.db:
            for row in records:
                self.store.db.execute('INSERT INTO records VALUES (?,?,?,?,?,?,?)', tuple(row[k] for k in ('id','kind','bill_id','dataset','available_at','effective_at','body')))
    def __enter__(self):
        return self.store
    def __exit__(self, *args):
        self.store.close(); self.tmp.cleanup()


def _case(store, proposal, bill_id):
    dataset = proposal['config']['dataset']
    # The checkpoint definition itself must not use later metadata revisions.
    first = store.db.execute(
        "SELECT body FROM records WHERE kind='bill' AND dataset=? AND bill_id=? ORDER BY available_at,effective_at,id LIMIT 1",
        (dataset, bill_id)).fetchone()
    bill = json.loads(first[0]) if first else None
    row = {'bill_id': bill_id, 'status': 'unavailable', 'outcome': None}
    if not bill:
        return dict(row, reason='Selected bill has no imported metadata'), None, []
    cutoff = (date(bill['introduced_at']) + timedelta(days=proposal['config']['age_days'])).isoformat()
    row.update(cutoff=cutoff)
    outcome = resolution(store, dataset, bill_id, proposal['created_at'])
    if outcome:
        row.update(outcome=outcome['value'], resolution_id=outcome['id'])
    if date(cutoff) > date(proposal['created_at']):
        return dict(row, reason='Checkpoint is in the future'), None, []
    snap = snapshot(store, dataset, bill_id, cutoff)
    if not snap:
        return dict(row, reason='No point-in-time metadata'), None, []
    if date(snap['bill']['introduced_at']) != date(bill['introduced_at']) or snap['age_days'] != proposal['config']['age_days']:
        return dict(row, reason='Historical introduction metadata conflicts with the fixed-age checkpoint'), None, []
    row.update(title=snap['bill']['title'], family_id=snap['bill']['family_id'])
    if snap['stage'] == 4 or resolution(store, dataset, bill_id, cutoff) or date(cutoff) >= date(congress_end(bill['congress'])):
        return dict(row, reason='Target resolved or Congress ended at checkpoint'), None, []
    training = training_rows(store, snap)
    if len(training) < 20 or len({r['y'] for r in training}) < 2:
        return dict(row, reason='Need 20 prior resolved families and both outcomes', training_count=len(training)), snap, training
    return dict(row, status='eligible', reason=None, training_count=len(training)), snap, training


def _preflight(store, proposal):
    cases = [_case(store, proposal, identity)[0] for identity in proposal['collection']['bill_ids']]
    counts = dict(Counter(r['reason'] for r in cases if r['status'] != 'eligible'))
    eligible = sum(r['status'] == 'eligible' for r in cases)
    scoreable = sum(r['status'] == 'eligible' and r['outcome'] is not None for r in cases)
    blockers = [] if scoreable else ['No selected bill has an eligible checkpoint, sufficient prior training and an observed outcome for scoring.']
    blockers.extend(proposal.get('sample_context', {}).get('blockers', []))
    blockers = list(dict.fromkeys(blockers))
    return {'status': 'blocked' if blockers else 'ready_for_development', 'target_count': len(cases), 'eligible_count': eligible,
            'scoreable_count': scoreable, 'exclusion_counts': counts, 'unknown_outcomes': sum(r['outcome'] is None for r in cases),
            'blockers': blockers, 'cases': cases, 'warnings': LIMITATIONS, 'release_eligible': False,
            'next_step': ('Review the existing audited publication-history pilot in Experiments, or supply independently audited historical availability and outcomes. Current retrieval dates cannot establish old action-history snapshots.' if blockers and proposal['config']['dataset'] == 'official' else 'Inspect the proposal, then execute explicitly.'),
            'alternative_view': 'experiments' if blockers and proposal['config']['dataset'] == 'official' else None}


def propose(store, args):
    from .collections import get_collection
    allowed = {'collection_id','title','hypothesis','age_days','candidate','target','track','feature_families'}
    if set(args) - allowed:
        raise ValueError('Unsupported session fields: ' + ', '.join(sorted(set(args) - allowed)))
    if args.get('candidate','B') != 'B' or args.get('target','enactment_by_congress_end') != 'enactment_by_congress_end' or args.get('track','structured_development') != 'structured_development' or args.get('feature_families',['structured']) != ['structured']:
        raise ValueError('Only candidate B, structured development and enactment by Congress end are implemented')
    age = args.get('age_days',180)
    if isinstance(age, bool) or not isinstance(age, int) or not 1 <= age <= 700:
        raise ValueError('age_days must be an integer from 1 to 700')
    title, hypothesis = args.get('title','Research session').strip(), args.get('hypothesis','').strip()
    if not 3 <= len(title) <= 160 or not 10 <= len(hypothesis) <= 3000:
        raise ValueError('Provide a title and a hypothesis of 10–3,000 characters')
    collection = get_collection(store, args.get('collection_id'))
    if not collection['bill_ids'] or len(collection['bill_ids']) > 500:
        raise ValueError('Choose a collection containing 1–500 bills')
    records = [dict(r) for r in store.db.execute('SELECT * FROM records WHERE dataset=? ORDER BY id', (collection['dataset'],))]
    return _save_proposal(store, title, hypothesis, age, collection, records)


def _save_proposal(store, title, hypothesis, age, collection, records, parent_id=None, change=None, sample_context=None):
    initialize(store)
    proposal = {'id': str(uuid.uuid4()), 'created_at': now(), 'title': title, 'hypothesis': hypothesis,
                'collection': collection, 'config': {'dataset': collection['dataset'], 'age_days': age,
                'candidate':'B','target':'enactment_by_congress_end','track':'structured_development','feature_families':['structured']},
                'parent_id': parent_id, 'change': change, 'evidence_hash': digest(records), 'implementation_hashes': _code(),
                'model_version': MODEL_VERSION, 'feature_version': FEATURE_VERSION, 'release_eligible': False,
                'limitations': LIMITATIONS, 'registration_note': 'Exploratory development; local registration does not establish an untouched test set.',
                'split': 'All eligible earlier-Congress training families; evaluation restricted to frozen collection membership.'}
    if sample_context is not None:
        if not isinstance(sample_context, dict) or not isinstance(sample_context.get('blockers', []), list) or any(not isinstance(item, str) or not item.strip() for item in sample_context.get('blockers', [])):
            raise ValueError('Sample context requires a list of nonempty blocker messages')
        # Snapshot the audit state; later review edits must create a fresh proposal.
        proposal['sample_context'] = json.loads(json.dumps(sample_context))
    with _Frozen(records) as frozen:
        proposal['preflight'] = _preflight(frozen, proposal)
    proposal['status'] = 'blocked' if proposal['preflight']['blockers'] else 'proposed'
    proposal['proposal_hash'] = digest(proposal)
    with store.db:
        store.db.execute('INSERT INTO research_sessions VALUES (?,?,?,?)', (proposal['id'],proposal['created_at'],json.dumps(proposal),json.dumps(records)))
    return get_session(store, proposal['id'])


def execute(store, identity):
    proposal, records = _row(store, identity)
    existing = get_session(store, identity)
    if existing['result']:
        from . import learning
        if existing.get('learning') is None and proposal['implementation_hashes'] == _code():
            learning.process(store, existing)
        return get_session(store, identity)
    if proposal['implementation_hashes'] != _code():
        raise ValueError('Implementation changed since proposal; create a new proposal before executing')
    if digest(records) != proposal['evidence_hash']:
        raise ValueError('Frozen evidence integrity check failed')
    if proposal['preflight']['blockers']:
        raise ValueError('Session blocked: ' + '; '.join(proposal['preflight']['blockers']))
    results = []
    with _Frozen(records) as frozen:
        for bill_id in proposal['collection']['bill_ids']:
            row, snap, training = _case(frozen, proposal, bill_id)
            if row['status'] == 'eligible':
                artifact = fit(training)
                row.update(status='available', probability=predict(artifact, snap['features']),
                           baseline_probability=(sum(r['y'] for r in training)+1)/(len(training)+2),
                           model_artifact=artifact, input_snapshot=snap, training_manifest=training)
            results.append(row)
    scored = [r for r in results if r['status'] == 'available' and r['outcome'] is not None]
    labels = [r['outcome'] for r in scored]
    metrics = score([r['probability'] for r in scored],labels) if scored else None
    baseline = score([r['baseline_probability'] for r in scored],labels) if scored else None
    result = {'status':'completed','session_id':identity,'completed_at':now(),'results':results,'metrics':metrics,'baseline':baseline,
              'attempted':len(results),'available':sum(r['status']=='available' for r in results),'scored':len(scored),
              'families':len({r['family_id'] for r in scored}), 'release_eligible':False,
              'brier_difference': metrics['brier'] - baseline['brier'] if metrics else None,
              'conclusion':'Development scores only. A lower Brier score is better; this run cannot establish validated forecasting skill.'}
    result['reproducibility_hash'] = _result_hash(proposal, result)
    with store.db:
        store.db.execute('INSERT OR IGNORE INTO session_results VALUES (?,?)',(identity,json.dumps(result)))
    from . import learning
    learning.process(store, get_session(store, identity))
    return get_session(store,identity)


def revise(store, identity, changes):
    from .collections import get_collection
    proposal, records = _row(store, identity)
    if not isinstance(changes,dict) or len(changes) != 1 or not set(changes) <= {'age_days','collection_id','hypothesis'}:
        raise ValueError('Change exactly one assumption: age_days, collection_id or hypothesis')
    key, value = next(iter(changes.items()))
    if key == 'collection_id' and proposal.get('sample_context') is not None:
        raise ValueError('An audited sample has frozen membership. Create a new audited sample and proposal to change the collection.')
    collection, age, hypothesis = proposal['collection'], proposal['config']['age_days'], proposal['hypothesis']
    previous = {'age_days':age,'hypothesis':hypothesis,'collection_id':collection['id']}[key]
    if value == previous:
        raise ValueError('The revised assumption must differ from the original')
    if key == 'age_days':
        if isinstance(value,bool) or not isinstance(value,int) or not 1 <= value <= 700: raise ValueError('age_days must be 1–700')
        age = value
    elif key == 'hypothesis':
        if not isinstance(value,str) or not 10 <= len(value.strip()) <= 3000: raise ValueError('Provide a hypothesis of 10–3,000 characters')
        hypothesis = value.strip()
    else:
        collection = get_collection(store,value)
        if collection['dataset'] != proposal['collection']['dataset'] or not 1 <= len(collection['bill_ids']) <= 500:
            raise ValueError('Revised collection must use the same dataset and contain 1–500 bills')
    return _save_proposal(store,proposal['title'],hypothesis,age,collection,records,identity,{'field':key,'before':previous,'after':value},sample_context=proposal.get('sample_context'))


def compare(store, left_id, right_id):
    a,b = get_session(store,left_id),get_session(store,right_id)
    output = {'left_id':left_id,'right_id':right_id,'release_eligible':False,'status':'not_comparable'}
    if not a['result'] or not b['result']:
        return dict(output,reason='Execute both sessions before comparison')
    output.update(left_metrics=a['result']['metrics'],right_metrics=b['result']['metrics'],same_frozen_evidence=a['evidence_hash']==b['evidence_hash'],same_checkpoints=a['config']['age_days']==b['config']['age_days'])
    if a['config']['dataset'] != b['config']['dataset'] or not output['same_frozen_evidence'] or not output['same_checkpoints']:
        return dict(output,reason='Different checkpoint or evidence definitions: aggregate scores may be inspected but are not a controlled paired comparison.')
    left={r['bill_id']:r for r in a['result']['results'] if r.get('probability') is not None and r['outcome'] is not None}
    right={r['bill_id']:r for r in b['result']['results'] if r.get('probability') is not None and r['outcome'] is not None}
    ids=sorted(k for k in set(left)&set(right) if left[k]['outcome']==right[k]['outcome'] and left[k]['cutoff']==right[k]['cutoff'])
    if not ids: return dict(output,reason='No shared scored bill/checkpoint pairs')
    ls=score([left[k]['probability'] for k in ids],[left[k]['outcome'] for k in ids]); rs=score([right[k]['probability'] for k in ids],[right[k]['outcome'] for k in ids])
    return dict(output,status='descriptive_comparison',pairs=len(ids),left_only=len(set(left)-set(right)),right_only=len(set(right)-set(left)),left_scores=ls,right_scores=rs,brier_difference_right_minus_left=rs['brier']-ls['brier'],note='Paired development scores; identical predictions are replication, not new evidence.')


def export_bundle(store, identity):
    proposal,records = _row(store,identity)
    bundle={'format':'research-session-bundle-v1','session':get_session(store,identity),'evidence':records,
            'raw_source_hashes':sorted({json.loads(r['body']).get('raw_hash') for r in records if json.loads(r['body']).get('raw_hash')}),
            'reproduction':'Restore evidence into an isolated Store and call sessions._case then model.fit/predict for each selected bill. Compare reproducibility_hash. Requires the recorded implementation hashes.',
            'source_note':'Normalized evidence is included. Raw source payloads are referenced by hash and remain in the local data/raw archive; this JSON does not embed them.'}
    bundle['bundle_hash']=digest(bundle)
    return bundle


def _result_hash(proposal, result):
    return digest({'evidence_hash': proposal['evidence_hash'], 'config': proposal['config'],
                   'bill_ids': proposal['collection']['bill_ids'], 'results': result['results'],
                   'metrics': result['metrics'], 'baseline': result['baseline']})


def _verify_result(proposal, result):
    if _result_hash(proposal, result) != result.get('reproducibility_hash'):
        raise ValueError('Result content does not match its reproducibility hash')
    rows = result['results']
    if [r['bill_id'] for r in rows] != proposal['collection']['bill_ids']:
        raise ValueError('Result population does not match the frozen collection')
    scored = [r for r in rows if r['status'] == 'available' and r['outcome'] is not None]
    labels = [r['outcome'] for r in scored]
    metrics = score([r['probability'] for r in scored], labels) if scored else None
    baseline = score([r['baseline_probability'] for r in scored], labels) if scored else None
    computed = {'metrics': metrics, 'baseline': baseline, 'attempted': len(rows),
                'available': sum(r['status'] == 'available' for r in rows), 'scored': len(scored),
                'families': len({r['family_id'] for r in scored}), 'release_eligible': False,
                'session_id': proposal['id'],
                'brier_difference': metrics['brier'] - baseline['brier'] if metrics else None}
    for key, value in computed.items():
        if result.get(key) != value:
            raise ValueError('Reported result aggregate does not match its cases: ' + key)


def reproduce_bundle(bundle):
    """Offline deterministic refit, independent of the application's current database."""
    if not isinstance(bundle,dict) or bundle.get('format') != 'research-session-bundle-v1':
        raise ValueError('Unsupported research bundle format')
    if digest({k:v for k,v in bundle.items() if k != 'bundle_hash'}) != bundle.get('bundle_hash'):
        raise ValueError('Bundle integrity check failed')
    session = dict(bundle['session'])
    expected_learning = session.pop('learning', None)
    expected = session.pop('result',None)
    if not expected or expected.get('status') != 'completed':
        raise ValueError('Only completed session bundles can be reproduced')
    session['status'] = 'blocked' if session['preflight']['blockers'] else 'proposed'
    if digest({k:v for k,v in session.items() if k != 'proposal_hash'}) != session.get('proposal_hash'):
        raise ValueError('Proposal integrity check failed')
    _verify_result(session, expected)
    with tempfile.TemporaryDirectory() as tmp:
        isolated = Store(Path(tmp)/'reproduce.sqlite')
        try:
            initialize(isolated)
            with isolated.db:
                isolated.db.execute('INSERT INTO research_sessions VALUES (?,?,?,?)',(session['id'],session['created_at'],json.dumps(session),json.dumps(bundle['evidence'])))
            executed = execute(isolated,session['id'])
            actual = executed['result']
            matched = actual['reproducibility_hash'] == expected['reproducibility_hash']
            learning_match = None
            if expected_learning:
                from . import learning
                learning_match = (learning.reproducibility_hash(expected_learning) == expected_learning.get('reproducibility_hash')
                                  and executed['learning']['reproducibility_hash'] == expected_learning['reproducibility_hash'])
                matched = matched and learning_match
            return {'status':'reproduced' if matched else 'mismatch','matches':matched,'expected_hash':expected['reproducibility_hash'],
                    'actual_hash':actual['reproducibility_hash'],'learning_matches':learning_match,'metrics':actual['metrics'],'baseline':actual['baseline'],'release_eligible':False}
        finally:
            isolated.close()


def replicate(store, identity):
    """Create a distinct proposal for an unchanged frozen-data replication."""
    proposal, records = _row(store,identity)
    return _save_proposal(store,proposal['title'],proposal['hypothesis'],proposal['config']['age_days'],
                          proposal['collection'],records,identity,{'replication':True},sample_context=proposal.get('sample_context'))
