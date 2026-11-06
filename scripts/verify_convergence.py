"""Scalar verification of vector-trained models, convergence and frozen candidate."""
import json,math
from engine.store import digest
from scripts.convergence_experiment import D, SOURCE, TOL
from scripts.cross_congress_evaluate import load_rows
from scripts.granular_transfer_audit import objective_gradient


def scalar_probability(m,x):
    b=m['base'];z=b['weights'][0]+sum(w*(v-a)/s for w,v,a,s in zip(b['weights'][1:],x,b['means'],b['scales']))
    raw=1/(1+math.exp(-max(-35,min(35,z))));p=min(1-1e-12,max(1e-12,raw));c=m['calibration']
    z=c['intercept']+c['slope']*math.log(p/(1-p))
    return raw,1/(1+math.exp(-max(-35,min(35,z))))


def verify():
    result=json.loads((D/'result.json').read_text());protocol=json.loads((D/'protocol.json').read_text())
    assert digest({k:v for k,v in result.items() if k!='hash'})==result['hash']
    assert digest(protocol['spec'])==protocol['hash']==result['protocol_hash']
    lookup={r['bill_id']:r for r in load_rows()};n=0
    for fold in result['folds']:
        for name,model in fold['models'].items():
            rows=[lookup[i] for i in fold['core_ids']]
            gradient=objective_gradient(model['base'],rows)['max_absolute_gradient']
            assert gradient<=TOL+1e-12
            assert abs(gradient-fold['diagnostics'][name]['max_absolute_gradient'])<1e-12
            raw=[];cal=[]
            for row in fold['predictions']:
                a,b=scalar_probability(model,row['x']);raw.append(a);cal.append(b);n+=2
                assert abs(a-row[name+'_raw'])<1e-12 and abs(b-row[name])<1e-12
            for key,values in [(name,cal),(name+'_raw',raw)]:
                brier=sum((v-r['outcome'])**2 for v,r in zip(values,fold['predictions']))/len(values)
                loss=sum(-r['outcome']*math.log(max(v,1e-12))-(1-r['outcome'])*math.log(max(1-v,1e-12)) for v,r in zip(values,fold['predictions']))/len(values)
                assert abs(brier-fold['metrics'][key]['brier'])<1e-13
                assert abs(loss-fold['metrics'][key]['log_loss'])<1e-13
    passed=all(f['metrics']['weaker_l2']['brier']<f['metrics']['control']['brier'] and f['metrics']['weaker_l2']['log_loss']<=f['metrics']['control']['log_loss'] for f in result['folds'])
    assert passed==result['development_gate_passed']
    lock=json.loads((D/'candidate-lock.json').read_text());train=json.loads((SOURCE/'final-training.json').read_text());byid={r['bill_id']:r for r in train}
    assert digest({k:v for k,v in lock.items() if k!='hash'})==lock['hash']
    assert digest(train)==lock['training_hash']
    assert set(lock['core_ids']).isdisjoint(lock['calibration_ids'])
    assert set(lock['core_ids'])|set(lock['calibration_ids'])==set(byid)
    assert {byid[i]['family_id'] for i in lock['core_ids']}.isdisjoint(byid[i]['family_id'] for i in lock['calibration_ids'])
    gradient=objective_gradient(lock['model']['base'],[byid[i] for i in lock['core_ids']])['max_absolute_gradient']
    assert gradient<=TOL+1e-12
    assert max(r['label_available_at'] for r in train)==lock['latest_training_label']
    verification=dict(status='passed',probabilities=n,result_hash=result['hash'],lock_hash=lock['hash'],final_training_n=len(train),final_training_positive=sum(r['y'] for r in train),independent_validation=False)
    (D/'verification.json').write_text(json.dumps(verification,indent=2));print(json.dumps(verification))


if __name__=='__main__':verify()
