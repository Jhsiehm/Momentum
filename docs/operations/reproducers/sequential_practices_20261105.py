"""Run official readiness and a separately labelled synthetic sequential check.
Run from repository root: python3 -m docs.operations.reproducers.sequential_practices_20261105
No source downloads or backdated official observations are performed.
"""
import json,random,sqlite3,hashlib,subprocess
from pathlib import Path
from collections import Counter
from engine.store import Store,ROOT,now,digest,congress_end
from engine.model import date,snapshot
from engine.sequential import benchmark,TARGET
from datetime import timedelta
D=ROOT/'data/research-runs/sequential-practices-20261105'

def save(name,value):
    path=D/name;body=json.dumps(value,indent=2)+'\n'
    if path.exists():assert path.read_text()==body,'Immutable artifact differs: '+name
    else:path.write_text(body)

def main():
    D.mkdir(parents=True,exist_ok=True)
    protocol=dict(target=TARGET,checkpoint_days=30,start=110,first_test=113,last_test=118,as_of='2026-11-05',official_labels='No adjudicated passage manifest found; explicitly empty, missing never negative',synthetic=dict(seed=20261105,congresses=list(range(110,119)),bills_per_congress=120,purpose='Software check only; fixed synthetic distribution, no real forecasting claim'),code_commit=(json.loads((D/'protocol.json').read_text())['spec']['code_commit'] if (D/'protocol.json').exists() else subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()),release_eligible=False)
    save('protocol.json',dict(spec=protocol,hash=digest(protocol)))
    db=D/'official-snapshot.sqlite'
    if not db.exists():
        source=sqlite3.connect('file:'+str(ROOT/'data/engine.sqlite')+'?mode=ro',uri=True);dest=sqlite3.connect(db);source.backup(dest);dest.close();source.close()
    official=Store(db);bills=official.bills('official',protocol['as_of']);counts=Counter();ready=Counter();rows=[]
    for b in bills:
        c=b['congress'];counts[c]+=1;cutoff=(date(b['introduced_at'])+timedelta(days=30)).isoformat();snap=snapshot(official,'official',b['bill_id'],cutoff)
        if snap:ready[c]+=1
        rows.append(dict(bill_id=b['bill_id'],congress=c,checkpoint=cutoff,metadata_at_checkpoint=bool(snap)))
    labels=[]
    # Explicitly run the official benchmark with the available audited label set (empty).
    result=benchmark(official,'official',labels,110,113,118,protocol['as_of']);official.close()
    save('official-'+result['id']+'.json',result)
    readiness=dict(counts_by_congress=dict(sorted(counts.items())),checkpoint_metadata_by_congress={str(c):ready[c] for c in sorted(counts)},labels=0,exclusions=dict(Counter(r['reason'] for r in result['exclusions'])),rows=rows)
    save('readiness.json',readiness)
    demo=Store(D/'synthetic.sqlite');rng=random.Random(20261105);synthetic=[]
    for c in range(110,119):
        year=1787+2*c
        for i in range(120):
            bid=f'synthetic-{c}-hr{i+1}';intro=f'{year}-02-01T12:00:00Z';signal=rng.random()<.35;outcome=int(rng.random() < (.45 if signal else .08));source='https://example.org/synthetic-sequential-check'
            common=dict(bill_id=bid,family_id=bid,dataset='demo',source_url=source,source_name='Synthetic software check')
            demo.add('bill',dict(common,congress=c,type='hr',title=f'Synthetic bill {i}',introduced_at=intro,effective_at=intro,observed_at=intro))
            if signal:demo.add('event',dict(common,stage=1,effective_at=f'{year}-02-10T12:00:00Z',observed_at=f'{year}-02-10T12:00:00Z',text='Synthetic committee event'))
            synthetic.append(dict(bill_id=bid,target=TARGET,value=outcome,effective_at=f'{year}-06-01T12:00:00Z' if outcome else congress_end(c),available_at=congress_end(c),complete_coverage=True,coverage_through=congress_end(c),source_url=source,source_hash=digest(dict(seed=20261105,bill_id=bid,value=outcome)),audit_note='Generated synthetic fixture; timestamps simulated, not official evidence'))
    save('synthetic-labels.json',synthetic)
    check=benchmark(demo,'demo',synthetic,110,113,118,protocol['as_of']);replay=benchmark(demo,'demo',synthetic,110,113,118,protocol['as_of']);assert check==replay;demo.close();save('synthetic-'+check['id']+'.json',check)
    assert all(f['status']=='blocked' for f in result['folds']) and result['frozen_artifact'] is None
    assert check['status']=='completed' and all(f['training_count']==120*(f['congress']-110) for f in check['folds'])
    for f in check['folds']:
        assert all(r['congress']<f['congress'] and r['available_at']<=f['training_origin'] for r in f['training_manifest'])
        assert len({m['n'] for m in f['metrics'].values()})==1
    summary=dict(protocol_hash=digest(protocol),official_id=result['id'],official_status=result['status'],official_bill_count=len(bills),official_checkpoint_metadata=sum(ready.values()),official_passage_labels=0,official_folds=[{k:f[k] for k in ('congress','status','reason','training_count','test_count')} for f in result['folds']],synthetic_id=check['id'],synthetic_status=check['status'],synthetic_bill_count=len(synthetic),synthetic_folds=[dict(congress=f['congress'],training=f['training_count'],test=f['test_count'],events=f['metrics']['frozen']['events'],brier={k:m['brier'] for k,m in f['metrics'].items()}) for f in check['folds']],verification='Synthetic report reproduced exactly; temporal and equal-case assertions passed; official run blocked with no model',release_eligible=False)
    save('summary.json',summary);print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
