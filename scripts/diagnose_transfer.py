"""Exposed-data diagnosis and fixed weight-shrinkage experiments; never promotes."""
import json
from pathlib import Path
from engine.model import predict, score
from engine.store import ROOT, digest, now
from engine.survivor_batch import save

D = ROOT / 'data/research-runs/weight-diagnosis-20261105'
NAMES = ['publication_stage', 'age', 'publication_count', 'time_since_publication', 'senate', 'recent_publications']
SURVIVOR_HASH = 'ffb089cff396415431c2e2b04cb99ebf7d75fe040a777da661bb58d6af9d255c'


def raw(artifact):
    weights = [w / s for w, s in zip(artifact['weights'][1:], artifact['scales'])]
    return [artifact['weights'][0] - sum(w*m for w, m in zip(weights, artifact['means']))] + weights


def artifact(coefficients):
    return dict(weights=coefficients, means=[0.] * 6, scales=[1.] * 6)


def blend(left, right, fraction):
    if not 0 <= fraction <= 1:
        raise ValueError('Weight fraction outside [0,1]')
    return artifact([(1-fraction)*a + fraction*b for a, b in zip(raw(left), raw(right))])


def summarize(rows, names):
    labels = [r['outcome'] for r in rows]
    metrics = {name: score([r[name] for r in rows], labels) for name in names}
    return dict(n=len(rows), positives=sum(labels), metrics=metrics,
                mean_probability={k: sum(r[k] for r in rows)/len(rows) for k in names},
                brier_difference_sum={k: sum((r[k]-r['outcome'])**2-(r['original']-r['outcome'])**2 for r in rows) for k in names})


def run():
    D.mkdir(parents=True, exist_ok=True)
    source = ROOT / 'data/research-runs/cross-congress-confirmation-20261105/result.json'
    lockpath = ROOT / 'data/research-runs/cross-congress-scale-20261105/challenger-lock.json'
    originalpath = ROOT / 'data/research-runs/survivor1000-20261105/artifact.json'
    result, lock, original = [json.loads(p.read_text()) for p in (source, lockpath, originalpath)]
    assert digest(original) == SURVIVOR_HASH
    assert digest({k:v for k,v in result.items() if k!='hash'}) == result['hash']
    assert digest({k:v for k,v in lock.items() if k!='hash'}) == lock['hash']
    spec = dict(source_result_hash=result['hash'], survivor_hash=SURVIVOR_HASH, lock_hash=lock['hash'],
                target='Day180 own-bill public-law enactment by Congress end', fractions=[.25,.5],
                status='exposed-data exploratory development',
                selection='Lowest Brier among two fixed blends, provided log loss does not worsen versus survivor; no promotion',
                independent_evaluation='Not performed. All 2315 outcomes were previously exposed. No new holdout claim.',
                release_eligible=False)
    if (D/'protocol.json').exists():
        registered = json.loads((D/'protocol.json').read_text())
        assert registered['spec'] == spec
    else:
        save(D,'protocol.json',dict(spec=spec,registered_at=now(),hash=digest(spec)))
    base = lock['artifact']['base']; calibration = lock['artifact']['calibration']
    effective = [v*calibration['slope'] for v in raw(base)]
    effective[0] += calibration['intercept']
    calibrated = artifact(effective)
    models = dict(original=original, uncalibrated=base, calibrated=calibrated,
                  shrink25=blend(original,calibrated,.25), shrink50=blend(original,calibrated,.5))
    rows = []
    for r in result['predictions']:
        values = {k:predict(m,r['input_features']) for k,m in models.items()}
        assert abs(values['original']-r['baseline_probability']) < 1e-12
        assert abs(values['calibrated']-r['probability']) < 1e-12
        rows.append(dict(r,**values))
    summary = summarize(rows,models)
    strata = {}
    for dimension, key in [('outcome',lambda r:str(r['outcome'])),
                           ('chamber',lambda r:'senate' if r['input_features'][4] else 'house'),
                           ('publication_stage',lambda r:str(r['input_features'][0]*4)),
                           ('survivor_probability',lambda r:'below_2pct' if r['original']<.02 else '2_to_5pct' if r['original']<.05 else '5_to_10pct' if r['original']<.1 else '10pct_plus')]:
        strata[dimension] = {value:summarize([r for r in rows if key(r)==value],models) for value in sorted({key(r) for r in rows})}
    coefficients = {k:dict(zip(['intercept']+NAMES,raw(m))) for k,m in models.items()}
    changes = [b-a for a,b in zip(raw(original),effective)]
    attribution = {}
    for y in (0,1):
        group = [r for r in rows if r['outcome']==y]
        attribution[str(y)] = dict(zip(['intercept']+NAMES,
            [changes[0]]+[changes[j+1]*sum(r['input_features'][j] for r in group)/len(group) for j in range(6)]))
    viable = [k for k in ('shrink25','shrink50') if summary['metrics'][k]['brier'] < summary['metrics']['original']['brier'] and summary['metrics'][k]['log_loss'] <= summary['metrics']['original']['log_loss']]
    selected = min(viable,key=lambda k:summary['metrics'][k]['brier']) if viable else None
    report = dict(title='Transfer diagnosis and constrained weight experiments',protocol_hash=digest(spec),summary=summary,strata=strata,
                  raw_coefficients=coefficients,mean_logit_change_contributions=attribution,models=models,predictions=rows,
                  selected_development_lead=selected,release_eligible=False,human_certified=False,
                  limitations=['Previously exposed outcomes; selection is exploratory.',
                               'Feature contributions explain logit changes algebraically, not causal effects.',
                               'Only 29 positive cases; subgroup findings are unstable.',
                               'No new model fitted to the 118th Congress outcomes; blending fraction selected using them.',
                               'Historical publication and family linkage limitations remain.'])
    report['hash'] = digest(report)
    if (D/'result.json').exists():
        assert json.loads((D/'result.json').read_text()) == report, 'Replay differs'
    else:
        save(D,'result.json',report)
    assert digest(json.loads(originalpath.read_text())) == SURVIVOR_HASH
    print(json.dumps(dict(summary=summary,strata_outcome=strata['outcome'],coefficients=coefficients,selected=selected,hash=report['hash']),indent=2))
    return report


if __name__ == '__main__':
    run()
