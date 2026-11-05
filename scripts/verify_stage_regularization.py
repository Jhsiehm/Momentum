"""Separate arithmetic and split checks for the fixed development experiment."""
import json, math
from engine.store import digest
from scripts.stage_regularization_experiment import D, SOURCE


def verify():
    result=json.loads((D/'result.json').read_text());protocol=json.loads((D/'protocol.json').read_text())
    assert digest({k:v for k,v in result.items() if k!='hash'})==result['hash']
    assert digest(protocol['spec'])==result['protocol_hash']==protocol['hash']
    count=0
    for fold in result['folds']:
        prior=json.loads((SOURCE/f"fold-{fold['congress']}.json").read_text())
        assert digest(prior)==protocol['spec']['source_hashes'][str(fold['congress'])]
        source_models=json.loads((SOURCE/f"fold-{fold['congress']}-models.json").read_text())
        assert digest(source_models)==prior['models_hash']
        original=source_models['calibrated_all_history']
        assert fold['core_ids']==original['core_ids'] and fold['calibration_ids']==original['calibration_ids']
        assert not set(fold['core_ids'])&set(fold['calibration_ids'])
        assert [r['bill_id'] for r in fold['predictions']]==[r['bill_id'] for r in prior['predictions']]
        for name,model in fold['models'].items():
            probabilities=[];raw=[]
            for row in fold['predictions']:
                x=row['x']
                values=x if model['encoding']=='linear' else [float(x[0]==.25),float(x[0]==.5),float(x[0]==.75)]+x[1:]
                base=model['base'];z=base['weights'][0]+sum(w*(v-m)/s for w,v,m,s in zip(base['weights'][1:],values,base['means'],base['scales']))
                p=1/(1+math.exp(-max(-35,min(35,z))));raw.append(p)
                q=min(1-1e-12,max(1e-12,p));cal=model['calibration'];z=cal['intercept']+cal['slope']*math.log(q/(1-q))
                p=1/(1+math.exp(-max(-35,min(35,z))));probabilities.append(p)
                assert abs(p-row[name])<1e-12 and abs(raw[-1]-row[name+'_raw'])<1e-12
                count+=2
            for key,values in [(name,probabilities),(name+'_raw',raw)]:
                brier=sum((p-r['outcome'])**2 for p,r in zip(values,fold['predictions']))/len(values)
                loss=sum(-r['outcome']*math.log(max(p,1e-12))-(1-r['outcome'])*math.log(max(1-p,1e-12)) for p,r in zip(values,fold['predictions']))/len(values)
                assert abs(brier-fold['metrics'][key]['brier'])<1e-13 and abs(loss-fold['metrics'][key]['log_loss'])<1e-13
            for stage,stats in fold['stages'].items():
                subset=[r for r in fold['predictions'] if r['stage']==float(stage)]
                assert len(subset)==stats['n'] and sum(r['outcome'] for r in subset)==stats['positive']
                assert abs(sum(r[name] for r in subset)-stats['expected'][name])<1e-12
    for name,comparison in result['comparisons'].items():
        gains=[1-f['metrics'][name]['brier']/f['metrics']['control']['brier'] for f in result['folds']]
        assert abs(sum(gains)/len(gains)-comparison['mean_relative_brier_gain'])<1e-14
        assert sum(f['metrics'][name]['brier']<f['metrics']['control']['brier'] and f['metrics'][name]['log_loss']<=f['metrics']['control']['log_loss'] for f in result['folds'])==comparison['joint_wins']
    verification=dict(status='passed',result_hash=result['hash'],probabilities=count,independent_validation=False)
    (D/'verification.json').write_text(json.dumps(verification,indent=2));print(json.dumps(verification))


if __name__=='__main__':verify()
