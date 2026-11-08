"""Read-only independent scalar and bootstrap replay; never fit or write artifacts.

Run from repository root with Python containing NumPy:
    python3 docs/operations/reproducers/verify_exploratory_calendar_20261108.py
"""
import hashlib
import json
import math
import sys
from datetime import datetime
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from engine.store import digest
from engine.cohort import family_groups
from scripts.cross_congress_evaluate import load_rows, make_split

D = ROOT / 'data/research-runs/exploratory-calendar-20261108-v1'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read(path):
    item = json.loads(path.read_text())
    require(digest(item['body']) == item['hash'], f'Seal mismatch: {path}')
    return item['body']


def features(row, arm):
    cutoff = datetime.fromisoformat(row['cutoff'].replace('Z', '+00:00'))
    end = datetime(1789 + 2 * row['congress'], 1, 3, 17, tzinfo=cutoff.tzinfo)
    remaining = (end - cutoff).total_seconds() / 63072000
    extra = [] if arm == 'control' else [remaining] if arm == 'time' else [remaining, row['x'][0] * remaining]
    return row['x'] + extra


def sigmoid(value):
    return 1 / (1 + math.exp(-max(-35, min(35, value))))


def prediction(base, values):
    return sigmoid(base['weights'][0] + sum(w * (v-m) / s for w,v,m,s in zip(base['weights'][1:], values, base['means'], base['scales'])))


def run():
    registration = read(D / 'registration.json')
    rows = load_rows()
    lookup = {row['bill_id']: row for row in rows}
    groups = family_groups(rows)
    require(digest(rows) == registration['population_hash'], 'Population mismatch')
    require(digest(groups) == registration['family_hash'], 'Family graph mismatch')
    for path, hashed in registration['code'].items():
        require(hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == hashed, f'Code mismatch: {path}')
    require(hashlib.sha256((ROOT / 'docs/research/EXPLORATORY_CALENDAR_PROTOCOL_V1.md').read_bytes()).hexdigest() == registration['protocol_sha256'], 'Protocol mismatch')
    folds = []
    for congress in (115, 116, 117):
        fold = read(D / f'fold-{congress}.json')
        folds.append(fold)
        training, test = make_split(rows, congress, groups)
        core = [lookup[i] for i in fold['core_ids']]
        calibration = [lookup[i] for i in fold['calibration_ids']]
        require(set(fold['core_ids'] + fold['calibration_ids']) == {r['bill_id'] for r in training}, 'Training identity mismatch')
        require([r['bill_id'] for r in fold['predictions']] == [r['bill_id'] for r in test], 'Evaluation order mismatch')
        families = [{groups[r['bill_id']] for r in part} for part in (core, calibration, test)]
        require(all(not families[i] & families[j] for i in range(3) for j in range(i)), 'Family overlap')
        require(max(r['label_available_at'] for r in training) < min(r['cutoff'] for r in test), 'Temporal overlap')
        rate = (sum(r['y'] for r in training) + 1) / (len(training) + 2)
        stages = {s: (sum(r['y'] for r in training if r['x'][0]*4 == s) + 5*rate) / (sum(r['x'][0]*4 == s for r in training) + 5) for s in range(4)}
        for arm in ('control', 'time', 'interaction'):
            base = fold['models'][arm]['base']
            xs = [features(r, arm) for r in core]
            n, width = len(core), len(xs[0])
            means = [sum(x[j] for x in xs)/n for j in range(width)]
            scales = [max(.1, math.sqrt(sum((x[j]-means[j])**2 for x in xs)/n)) for j in range(width)]
            require(means == base['means'] and scales == base['scales'], 'Core scaling mismatch')
            gradient = [0.] * (width + 1)
            maximum_logit = 0
            for x, row in zip(xs, core):
                values = [1.] + [(t-m)/s for t,m,s in zip(x, means, scales)]
                z = sum(w*t for w,t in zip(base['weights'], values))
                maximum_logit = max(maximum_logit, abs(z))
                error = 1/(1+math.exp(-z)) - row['y']
                for j in range(width+1):
                    gradient[j] += error*values[j]/n
            for j in range(1, width+1):
                gradient[j] += .05*base['weights'][j]
            require(max(map(abs, gradient)) <= 1e-6 and maximum_logit < 35 and 300 <= base['iterations'] <= 20000, 'Convergence/clipping failure')
        for pair, row in zip(fold['predictions'], test):
            require(pair['outcome'] == row['y'] and pair['family_id'] == groups[row['bill_id']], 'Label/family mismatch')
            require(pair['rate'] == rate and pair['stage'] == stages[int(row['x'][0]*4)], 'Baseline mismatch')
            for arm in ('control', 'time', 'interaction'):
                model = fold['models'][arm]
                raw = prediction(model['base'], features(row, arm))
                require(abs(raw-pair[arm+'_raw']) < 1e-12, 'Raw prediction mismatch')
                q = min(1-1e-12, max(1e-12, raw))
                adjust = model['calibration']
                adjusted = sigmoid(adjust['intercept'] + adjust['slope']*math.log(q/(1-q)))
                require(abs(adjusted-pair[arm]) < 1e-12, 'Calibrated prediction mismatch')
        for arm, metric in fold['metrics'].items():
            pairs = fold['predictions']
            brier = sum((p[arm]-p['outcome'])**2 for p in pairs)/len(pairs)
            loss = -sum(p['outcome']*math.log(max(p[arm],1e-12))+(1-p['outcome'])*math.log(max(1-p[arm],1e-12)) for p in pairs)/len(pairs)
            require(brier == metric['brier'] and loss == metric['log_loss'], 'Metric mismatch')
        print(f'Fold {congress}: scalar replay passed', flush=True)
    result = read(D / 'result.json')
    require(result['folds'] == folds, 'Result/fold mismatch')
    means = {arm: sum(f['metrics'][arm]['brier'] for f in folds)/3 for arm in folds[0]['metrics']}
    require(means == result['summary']['mean_brier'], 'Aggregate mismatch')
    leads = [arm for arm in ('time','interaction') if all(f['metrics'][arm]['brier'] < f['metrics']['control']['brier'] and f['metrics'][arm]['log_loss'] <= f['metrics']['control']['log_loss'] for f in folds)]
    require(leads == [] and result['summary']['exploratory_lead'] is None, 'Lead decision mismatch')
    families = sorted({p['family_id'] for f in folds for p in f['predictions']})
    index = {v:i for i,v in enumerate(families)}
    rng = np.random.default_rng(20261108)
    contrasts = [tuple(k.split('_minus_')) for k in result['bootstrap']['intervals']]
    matrix = np.zeros((len(families), 3, len(contrasts)+1))
    for j, fold in enumerate(folds):
        for pair in fold['predictions']:
            i = index[pair['family_id']]
            matrix[i,j,0] += 1
            for k, (a,b) in enumerate(contrasts):
                matrix[i,j,k+1] += (pair[a]-pair['outcome'])**2-(pair[b]-pair['outcome'])**2
    replicates, invalid = [], 0
    for _ in range(10000):
        weights = rng.multinomial(len(families), np.full(len(families), 1/len(families)))
        aggregate = np.einsum('i,ijk->jk', weights, matrix, optimize=False)
        if np.any(aggregate[:,0] == 0):
            invalid += 1
            continue
        replicates.append(np.mean(aggregate[:,1:]/aggregate[:,0,None], axis=0))
    bounds = np.quantile(replicates, [.025,.975], axis=0)
    require(invalid == result['bootstrap']['invalid'] == 0, 'Invalid draw mismatch')
    for k, (a,b) in enumerate(contrasts):
        require(np.max(np.abs(bounds[:,k]-result['bootstrap']['intervals'][a+'_minus_'+b])) < 1e-14, 'Interval mismatch')
    print(f'PASS: nine fits replayed without refitting; 10000 bootstrap draws, {invalid} invalid, {len(families)} global families.')


if __name__ == '__main__':
    run()
