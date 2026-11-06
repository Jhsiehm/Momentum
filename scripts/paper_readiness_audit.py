"""Read existing artifacts only: no imports, fits, new predictions or scores."""
import json
import hashlib
from pathlib import Path
from engine.store import ROOT, digest

SURVIVOR = 'ffb089cff396415431c2e2b04cb99ebf7d75fe040a777da661bb58d6af9d255c'
CHALLENGER = '149b5f618cd74bcc1974cd502581490e8e8cb3c390baf25b9279e213bb35c0c5'


def audit(root=ROOT):
    base = Path(root)/'data/research-runs'
    checked = {}
    def read(relative, internal=False):
        path = base/relative
        raw = path.read_bytes()
        body = json.loads(raw)
        checked[relative] = hashlib.sha256(raw).hexdigest()
        if internal and digest({k:v for k,v in body.items() if k!='hash'}) != body['hash']:
            raise ValueError('Internal artifact hash mismatch: '+relative)
        return body
    survivor = read('survivor1000-20261105/artifact.json')
    challenger = read('convergence-einsum-20261105/candidate-lock.json',True)
    if digest(survivor)!=SURVIVOR or challenger['hash']!=CHALLENGER:
        raise ValueError('Frozen model changed')
    training = read('cross-congress-scale-20261105/final-training.json')
    if digest(training)!=challenger['training_hash']:
        raise ValueError('Final training changed')
    core,cal=set(challenger['core_ids']),set(challenger['calibration_ids'])
    if core & cal or core | cal != {r['bill_id'] for r in training}:
        raise ValueError('Frozen membership mismatch')
    folds = {}
    for c in range(114,118):
        fold=read(f'cross-congress-scale-20261105/fold-{c}.json')
        folds[str(c)]=fold['counts']
    convergence=read('convergence-einsum-20261105/result.json',True)
    confirmation=read('cross-congress-confirmation-20261105/result.json',True)
    # Only previously saved counts/scores are read. Do not recalculate outcomes.
    return dict(schema=1,scope='Read-only frozen-artifact audit; no new outcome scoring',
        survivor_hash=SURVIVOR,challenger_hash=CHALLENGER,
        training=dict(n=len(training),positives=sum(r['y'] for r in training),
                      congresses=sorted({r['congress'] for r in training}),
                      core=len(core),calibration=len(cal),latest_label=max(r['label_available_at'] for r in training)),
        development_folds=folds,convergence_saved_gain=convergence['mean_relative_brier_gain'],
        confirmation_saved_hash=confirmation['hash'],artifact_file_sha256=checked,
        independent_historical_validation_ready=False,
        blockers=['No certified untouched historical period','Historical source and family reviews incomplete',
                  'No protected outcome custodian or certified paired day180 prospective ledger'],
        release_eligible=False)


if __name__=='__main__':
    print(json.dumps(audit(),indent=2,sort_keys=True))
