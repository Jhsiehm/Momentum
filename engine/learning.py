"""Bounded per-checkpoint adaptation, separate from immutable fixed-model results.

The latest eligible prior Congress is inner validation, never the target outcomes.
Thresholds are engineering safeguards, not claims of statistical validation.
"""
import json
import math
import re
from pathlib import Path
from .store import digest, now, timestamp
from .model import sigmoid, predict, score

VERSION = 'adaptive-context-v2'
CONFIGS = (0.05, 0.01, 0.2)
FEATURE_POLICIES = ('structured', 'structured_context')
FEATURE_VERSION = 'frozen-title-topic-hash16-v1'
SCHEMA = '''
CREATE TABLE IF NOT EXISTS learning_records(session_id TEXT PRIMARY KEY, evidence_identity TEXT NOT NULL, body TEXT NOT NULL);
CREATE INDEX IF NOT EXISTS learning_identity ON learning_records(evidence_identity);
CREATE TRIGGER IF NOT EXISTS learning_no_update BEFORE UPDATE ON learning_records BEGIN SELECT RAISE(ABORT,'Learning records are immutable'); END;
CREATE TRIGGER IF NOT EXISTS learning_no_delete BEFORE DELETE ON learning_records BEGIN SELECT RAISE(ABORT,'Learning records are immutable'); END;
'''


def get(store, session_id):
    store.db.executescript(SCHEMA)
    row = store.db.execute('SELECT body FROM learning_records WHERE session_id=?', (session_id,)).fetchone()
    return json.loads(row[0]) if row else None


def reproducibility_hash(record):
    """Stable adaptation content; excludes session identity and repeat bookkeeping."""
    return digest({key:record.get(key) for key in ('version','evidence_identity','code_hashes','cases',
                   'metrics','fixed_metrics','adjusted_count','eligible_count','selection_policy','release_eligible',
                   'supported_features','unused_information')})


def _fit(rows, l2):
    count, width = len(rows), len(rows[0]['x'])
    means = [sum(r['x'][j] for r in rows) / count for j in range(width)]
    scales = [max(.1, math.sqrt(sum((r['x'][j]-means[j])**2 for r in rows)/count)) for j in range(width)]
    xs = [[1.] + [(r['x'][j]-means[j])/scales[j] for j in range(width)] for r in rows]
    rate = (sum(r['y'] for r in rows)+1)/(count+2)
    weights = [math.log(rate/(1-rate))] + [0.] * width
    for _ in range(300):
        gradient = [0.] * (width+1)
        for row, x in zip(rows, xs):
            error = sigmoid(sum(a*b for a,b in zip(weights,x))) - row['y']
            for j in range(width+1): gradient[j] += error*x[j]/count
        for j in range(width+1): weights[j] -= .12*(gradient[j]+(l2*weights[j] if j else 0))
    return dict(weights=weights, means=means, scales=scales, iterations=300, l2=l2)


def features(row, policy):
    """Stateless hashing of frozen checkpoint metadata, never live bill metadata.

    Fixed hashing avoids fitting a vocabulary on validation or target records.
    Collisions are an explicit tradeoff; these features are not semantic embeddings.
    """
    base=list(row['x'])
    if policy == 'structured': return base
    if policy != 'structured_context': raise ValueError('Unknown feature policy')
    topic=[0.] * 16
    category=str(row.get('topic') or '').strip().casefold()
    if category: topic[int(digest(['topic',category])[:8],16)%16]=1.
    title=[0.] * 16
    tokens=re.findall(r'[a-z0-9]+',str(row.get('title') or '').casefold())[:128]
    for token in tokens: title[int(digest(['title',token])[:8],16)%16] += 1./max(1,len(tokens))
    stage=base[0] if base else 0.
    return base+topic+title+[stage*(base[5] if len(base)>5 else 0.),stage*(base[3] if len(base)>3 else 0.)]


def _transform(rows, policy):
    return [dict(r,x=features(r,policy)) for r in rows]


def _artifact(rows, l2, policy):
    transformed=_transform(rows,policy)
    return dict(_fit(transformed,l2),feature_policy=policy,feature_version=FEATURE_VERSION,
                feature_manifest={'base_width':len(rows[0]['x']),'topic_bins':16 if policy=='structured_context' else 0,
                                  'title_bins':16 if policy=='structured_context' else 0,
                                  'title_token_limit':128,'interactions':['stage*recent_activity','stage*inactivity'] if policy=='structured_context' else []},
                transformed_training_hash=digest([{'bill_id':r['bill_id'],'x':r['x'],'y':r['y']} for r in transformed]))


def _select(rows, resolutions):
    result = {'status':'no_adjustment', 'selected_l2':.05, 'selected_feature_policy':'structured', 'training_hash':digest(rows)}
    if len(rows) < 30 or len({r['family_id'] for r in rows}) != len(rows):
        return dict(result, reason='Need at least 30 distinct prior families for an inner split.')
    latest = max(r['congress'] for r in rows)
    validation = [r for r in rows if r['congress'] == latest]
    cutoff = min(timestamp(r['cutoff']) for r in validation)
    families = {r['family_id'] for r in validation}
    train = [r for r in rows if r['congress'] < latest and r['family_id'] not in families
             and r['resolution_id'] in resolutions
             and resolutions[r['resolution_id']]['available_at'] <= cutoff
             and resolutions[r['resolution_id']]['effective_at'] <= cutoff]
    audit = {'train_ids':[r['bill_id'] for r in train], 'validation_ids':[r['bill_id'] for r in validation],
             'train_families':[r['family_id'] for r in train], 'validation_families':sorted(families),
             'label_availability_cutoff':cutoff, 'validation_congress':latest,
             'excluded_train_count':len(rows)-len(validation)-len(train)}
    result['inner_validation'] = audit
    if len(train)<20 or len(validation)<10 or len({r['y'] for r in train})<2 or len({r['y'] for r in validation})<2:
        return dict(result, reason='Need 20 prior training families and 10 later validation families, both outcomes, with labels available before inner validation.')
    trials=[]
    for policy in FEATURE_POLICIES:
        for l2 in CONFIGS:
            artifact=_artifact(train,l2,policy)
            probabilities=[predict(artifact,features(r,policy)) for r in validation]
            trials.append({'l2':l2,'feature_policy':policy,'metrics':score(probabilities,[r['y'] for r in validation]),
                           'transformed_training_hash':artifact['transformed_training_hash'],
                           'predictions':[{'bill_id':r['bill_id'],'probability':p,'outcome':r['y']} for r,p in zip(validation,probabilities)]})
    selected=min(trials,key=lambda t:t['metrics']['brier'])
    # Preserve the reference on ties or numerical noise.
    if trials[0]['metrics']['brier']-selected['metrics']['brier'] <= 1e-6: selected=trials[0]
    audit.update(trials=trials, selection_metric='brier', minimum_improvement=1e-6)
    return dict(result,status='adjusted' if selected['l2'] != .05 or selected['feature_policy']!='structured' else 'retained',
                selected_l2=selected['l2'],selected_feature_policy=selected['feature_policy'],
                artifact=_artifact(rows,selected['l2'],selected['feature_policy']),
                reason='Feature policy and regularization selected using prior-data inner validation; refit on full eligible prior training.')


def process(store, session):
    existing=get(store,session['id'])
    if existing: return existing
    result=session.get('result')
    if not result or result.get('status') != 'completed':
        raise ValueError('Adaptive learning requires a completed research session')
    frozen=store.db.execute('SELECT evidence FROM research_sessions WHERE id=?',(session['id'],)).fetchone()
    if not frozen: raise ValueError('Frozen research session evidence is required')
    evidence=json.loads(frozen[0])
    resolutions={r['id']:r for r in evidence if r['kind']=='resolution'}
    code_hashes={name:digest(Path(__file__).with_name(name).read_text()) for name in ('learning.py','model.py')}
    inputs=[{k:r.get(k) for k in ('bill_id','cutoff','training_manifest','input_snapshot','probability','outcome')} for r in result['results']]
    identity=digest({'version':VERSION,'dataset':session['config']['dataset'],'inputs':inputs,
                     'evidence_hash':session['evidence_hash'],'code_hashes':code_hashes})
    prior=store.db.execute('SELECT body FROM learning_records WHERE evidence_identity=? ORDER BY rowid LIMIT 1',(identity,)).fetchone()
    if prior:
        previous=json.loads(prior[0])
        record=dict(previous,session_id=session['id'],id=digest([session['id'],identity]),created_at=now(),
                    status='reused',source_learning_id=previous['id'],new_learning=False,
                    note='Identical frozen evidence and checkpoints: reused adaptation, not new independent learning.')
    else:
        cases=[]; cache={}
        for row in result['results']:
            case={'bill_id':row['bill_id'],'status':'no_adjustment','original_probability':row.get('probability')}
            rows=row.get('training_manifest',[])
            if row.get('status')!='available' or not rows:
                cases.append(dict(case,reason='No eligible fixed-model prediction or training manifest.')); continue
            key=digest(rows)
            if key not in cache: cache[key]=_select(rows,resolutions)
            selection=cache[key]
            case.update(selection)
            snap=row['input_snapshot']
            target=dict(snap.get('bill',{}),x=snap['features'])
            case['probability']=predict(selection['artifact'],features(target,selection['selected_feature_policy'])) if selection.get('artifact') else row['probability']
            case['outcome']=row.get('outcome')
            cases.append(case)
        scored=[c for c in cases if c.get('probability') is not None and c.get('outcome') is not None]
        adjusted=sum(c['status']=='adjusted' for c in cases)
        eligible=sum(c['status'] in ('adjusted','retained') for c in cases)
        record={'id':digest([session['id'],identity]),'session_id':session['id'],'created_at':now(),
                'status':'adjusted' if adjusted else 'retained' if eligible else 'no_adjustment',
                'cases':cases,'adjusted_count':adjusted,'eligible_count':eligible,'new_learning':bool(eligible),
                'metrics':score([c['probability'] for c in scored],[c['outcome'] for c in scored]) if scored else None,
                'fixed_metrics':score([c['original_probability'] for c in scored],[c['outcome'] for c in scored]) if scored else None,
                'note':'Bounded per-checkpoint adaptation from prior training only. Target outcomes are descriptive diagnostics, never optimization inputs. No global promotion or validated accuracy claim.'}
    record.update(version=VERSION,evidence_identity=identity,code_hashes=code_hashes,release_eligible=False,
                  supported_features=['legislative stage','bill age','event count','time since last event','chamber','recent activity count','frozen topic category hashing','frozen title token hashing','stage × recent activity','stage × inactivity'],
                  unused_information=['bill full text','sponsor and cosponsor networks','committee membership','LLM-generated interpretations'],
                  selection_policy={'l2_candidates':list(CONFIGS),'feature_policies':list(FEATURE_POLICIES),'maximum_trials':6,'feature_version':FEATURE_VERSION,'inner_train_min':20,'inner_validation_min':10,'iterations':300,
                                    'guard_note':'Engineering safeguards, not statistical validation.'})
    record['reproducibility_hash']=reproducibility_hash(record)
    with store.db:
        store.db.execute('INSERT OR IGNORE INTO learning_records VALUES (?,?,?)',(session['id'],identity,json.dumps(record)))
    return get(store,session['id'])
