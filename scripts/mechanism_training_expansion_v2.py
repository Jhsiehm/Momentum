"""Fixed 1,000-case source expansion; current retrieval is not historic proof.

The preceding 200-case implementation and its artifacts are immutable. This
runner registers a new outcome-blind sample, excludes every earlier selected
family, and creates no annotations, fits, scores or promotion decisions.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import signal
import time
import uuid

from engine.cohort import Sources, family_groups
from engine.paper_evaluation import require, seal
from engine.research_lease import lease
from engine.store import ROOT, Store, digest, now, timestamp
from scripts.bill_context_design_text_v2 import render
from scripts.cross_congress_evaluate import D, load_rows
from scripts.mechanism_training_coverage import (PILOT, CONGRESSES, coverage,
    fingerprints, frozen_paths, introduced_evidence, population_snapshot,
    read_sealed, replay_memberships)
from scripts.paper_review_packet import packet, persist_or_compare

PRIOR = ROOT/'data/research-runs/mechanism-training-coverage-20261108-v2'
CAP = 1000
QUOTA = 250


class AcquisitionDeadline(RuntimeError):
    """Global deadline must bypass the HTTP transport's TimeoutError retries."""


def cycle_specs(selected):
    require(len(selected)<=CAP,'Acquisition cap exceeded')
    ids=[s['bill_id'] for s in selected]
    require(len(ids)==len(set(ids)),'Duplicate cycle identity')
    return [dict(cycle=i//100+1,bill_ids=ids[i:i+100],acquisition_cap=100)
            for i in range(0,len(ids),100)]


def select_expansion(rows, groups, memberships, excluded):
    lookup={r['bill_id']:r for r in rows}
    require(len(lookup)==len(rows),'Duplicate population identity')
    excluded_ids={s['bill_id'] for s in excluded}
    require(len(excluded_ids)==len(excluded),'Duplicate exclusion identity')
    require(all(groups[s['bill_id']]==s['family_id'] for s in excluded),'Excluded family changed')
    forbidden={groups[x] for x in excluded_ids};used=set(forbidden);roles={}
    for fold,f in memberships.items():
        require(set(f['core_ids']).isdisjoint(f['calibration_ids']),'Core/calibration overlap')
        for role in ('core_ids','calibration_ids'):
            require(len(f[role])==len(set(f[role])),'Duplicate partition identity')
            for bid in f[role]:
                require(bid in lookup,'Unknown training identity')
                r=lookup[bid]
                require(r['congress']<int(fold) and timestamp(r['label_available_at'])<timestamp(f['first_evaluation_cutoff']),'Training label timing violation')
                roles.setdefault(bid,[]).append(dict(fold=fold,role=role.removesuffix('_ids'),first_evaluation_cutoff=f['first_evaluation_cutoff']))
    selected=[];ledger=[]
    for congress in CONGRESSES:
        n=0
        for bid in sorted((x for x in roles if lookup[x]['congress']==congress),key=lambda x:(digest(x),x)):
            r=lookup[bid];family=groups[bid]
            reason=('prior_selected_identity_or_family' if bid in excluded_ids or family in forbidden else
                    'already_selected_family' if family in used else 'excluded_population_row' if r.get('exclusion') else
                    'outside_fixed_quota' if n>=QUOTA else None)
            ledger.append(dict(bill_id=bid,congress=congress,family_id=family,disposition=reason or 'selected'))
            if reason:continue
            selected.append(dict(bill_id=bid,congress=congress,family_id=family,cutoff=timestamp(r['cutoff']),
                                 label_available_at=timestamp(r['label_available_at']),memberships=roles[bid]))
            used.add(family);n+=1
    require(len(selected)<=CAP,'Acquisition cap exceeded')
    return selected,ledger


def validate_current_record(directory, selected, registration_hash, registered_at):
    """Offline replay; returns true only for a source-complete successful record."""
    bid=selected['bill_id'];_,r=read_sealed(directory/'records'/(bid+'.json'))
    require(all(r[k]==v for k,v in selected.items()),'Selected record identity/timing changed')
    require(r['registration_hash']==registration_hash and r['historical_feature_eligible'] is False and r['human_certified'] is False,'Record binding/certification changed')
    if r['status']=='blocked':
        require(isinstance(r.get('error'),str) and bool(r['error']),'Unexplained blocked record')
        return False
    require(r['status']=='metadata_dated_current_xml','Unknown record status')
    _,evidence=read_sealed(directory/'packets'/(bid+'.json'))
    require(evidence['bill_id']==bid and evidence['cutoff']==selected['cutoff'] and evidence['family_id']==selected['family_id'],'Packet row binding changed')
    package,url,proof=introduced_evidence(evidence)
    require(r['package']==package and r['publication_metadata']==proof,'Publication proof changed')
    key=hashlib.sha256(url.encode()).hexdigest();raw=(directory/'sources'/(key+'.raw')).read_bytes()
    receipt=json.loads((directory/'sources'/(key+'.json')).read_text())
    require(receipt==r['source'] and receipt['url']==url and receipt['bytes']==len(raw) and receipt['sha256']==hashlib.sha256(raw).hexdigest(),'Source receipt changed')
    require(timestamp(receipt['retrieved_at'])>=timestamp(registered_at),'Backdated receipt')
    view,body=read_sealed(directory/'views'/(bid+'.json'))
    require(view['hash']==r['source_view_hash'],'View hash binding changed')
    require(body==dict(**render(raw,bid),source=receipt,registration_hash=registration_hash,historical_feature_eligible=False),'Source view replay differs')
    return True


def baseline(prior=PRIOR):
    """Validate all 232 baseline sources; never open the pilot quality texts."""
    reg,spec=read_sealed(prior/'registration.json');result,body=read_sealed(prior/'result.json')
    require(body['registration_hash']==reg['hash'],'Prior result binding changed')
    require(fingerprints([ROOT/p for p in spec['implementation_hashes']])==spec['implementation_hashes'],'Prior implementation changed')
    require(fingerprints([ROOT/p for p in spec['frozen_files']])==spec['frozen_files'],'Prior frozen files changed')
    _,pop=read_sealed(prior/'selection-population.json');_,ledger=read_sealed(prior/'selection-ledger.json')
    require(digest(pop)==spec['selection_population_hash'] and digest(ledger)==spec['selection_ledger_hash'],'Prior population/selection binding changed')
    from scripts.mechanism_training_coverage import select_training
    pilot_reg,pilot=read_sealed(PILOT/'registration.json')
    require(pilot_reg['hash']==spec['pilot_registration_hash'],'Pilot registration changed')
    groups={r['bill_id']:r['family_id'] for r in pop}
    selection,replayed=select_training(pop,groups,spec['memberships'],pilot['selection'],spec['quota_per_congress'])
    require(selection==spec['selection'] and replayed==ledger,'Prior selection replay differs')
    good={s['bill_id'] for s in selection if validate_current_record(prior,s,reg['hash'],spec['registered_at'])}
    require(len(good)==body['usable_metadata_dated_current_xml']==200,'Prior usable baseline differs')
    _,pilot_packet=read_sealed(PILOT/'source-packet.json');evidence={r['bill_id']:r for r in pilot_packet['records']}
    pilot_selection={r['bill_id']:r for r in pilot['selection']}
    for bid in spec['baseline_design_ids']:
        require(pilot_selection[bid]['partition']=='design','Baseline would open quality text')
        _,r=read_sealed(PILOT/'records'/(bid+'.json'));_,url,_=introduced_evidence(evidence[bid])
        require(r['bill_id']==bid and r['partition']=='design' and r['source']['url']==url,'Pilot design binding changed')
        raw=(PILOT/'sources'/(hashlib.sha256(url.encode()).hexdigest()+'.raw')).read_bytes()
        require(hashlib.sha256(raw).hexdigest()==r['source']['sha256'] and len(raw)==r['source']['bytes'],'Pilot design source changed')
        render(raw,bid);good.add(bid)
    require(len(good)==232,'Expected 232 distinct validated baseline identities')
    require(coverage(spec['memberships'],good)==body['coverage_after'],'Baseline coverage differs')
    return dict(ids=sorted(good),prior_registration_hash=reg['hash'],prior_result_hash=result['hash'],
                excluded=pilot['selection']+spec['selection'],prior_memberships=spec['memberships'])


def preservation_paths():
    prior_files=[]
    for sub in ('records','packets','sources','views'):
        prior_files.extend((PRIOR/sub).glob('*'))
    prior_files += [PRIOR/n for n in ('registration.json','result.json','selection-population.json','selection-ledger.json','verification.json')]
    return frozen_paths()+[p for p in prior_files if p.is_file()]


def verify(directory):
    directory=Path(directory);reg,spec=read_sealed(directory/'registration.json');res,result=read_sealed(directory/'result.json')
    require(result['registration_hash']==reg['hash'],'Result registration changed')
    require(fingerprints([ROOT/p for p in spec['implementation_hashes']])==spec['implementation_hashes'],'Registered code changed')
    require(fingerprints([ROOT/p for p in spec['frozen_files']])==spec['frozen_files'],'Frozen files changed')
    base=baseline();require(base==spec['baseline'],'Baseline binding changed')
    _,pop=read_sealed(directory/'selection-population.json');_,ledger=read_sealed(directory/'selection-ledger.json')
    require(digest(pop)==spec['population_hash'] and digest(ledger)==spec['ledger_hash'],'Population/ledger changed')
    selected,replayed=select_expansion(pop,{r['bill_id']:r['family_id'] for r in pop},spec['memberships'],base['excluded'])
    require(selected==spec['selection'] and replayed==ledger,'Selection replay changed')
    require(spec['cycles']==cycle_specs(selected),'Cycle plan changed')
    good=set();failures=[]
    for s in selected:
        if validate_current_record(directory,s,reg['hash'],spec['registered_at']):good.add(s['bill_id'])
        else:
            _,r=read_sealed(directory/'records'/(s['bill_id']+'.json'));failures.append(dict(bill_id=s['bill_id'],error=r['error']))
    require(failures==result['failures'],'Failure ledger changed')
    require(len(good)==result['usable_metadata_dated_current_xml'],'Usable count changed')
    require(result['coverage_before']==coverage(spec['memberships'],base['ids']) and
            result['coverage_after']==coverage(spec['memberships'],set(base['ids'])|good) and
            result['coverage_increment']==coverage(spec['memberships'],good),'Coverage replay differs')
    require(all(result[k]==0 for k in ('certified_historical','models_fitted','outcomes_scored','mechanism_labels_created')),'Unapproved learning/certification claim')
    for cycle in spec['cycles']:
        cycle_reg,cycle_body=read_sealed(directory/'cycles'/f"cycle-{cycle['cycle']:02d}-registration.json")
        require(cycle_body==dict(**cycle,registration_hash=reg['hash']),'Cycle registration changed')
        _,cycle_result=read_sealed(directory/'cycles'/f"cycle-{cycle['cycle']:02d}-result.json")
        hashes={bid:read_sealed(directory/'records'/(bid+'.json'))[0]['hash'] for bid in cycle['bill_ids']}
        require(cycle_result['cycle_registration_hash']==cycle_reg['hash'] and cycle_result['record_hashes']==hashes,'Cycle record binding changed')
        require(cycle_result['attempted']==len(hashes) and cycle_result['usable']==sum(b in good for b in hashes) and cycle_result['frozen_files_unchanged'] is True,'Cycle counts/audit changed')
    receipt=seal(dict(registration_hash=reg['hash'],result_hash=res['hash'],baseline_sources_validated=len(base['ids']),
        selected_replayed=len(selected),sources_replayed=len(good),blocked=len(failures),frozen_files_unchanged=True,
        quality_texts_opened=False,outcome_values_read=False,historical_feature_eligible=False))
    persist_or_compare(directory/'verification.json',receipt)
    return receipt


def run(directory):
    directory=Path(directory)
    require(ROOT/'data' in directory.resolve().parents and not directory.exists(),'Use a new directory under ignored data')
    owner='mechanism-training-expansion-'+uuid.uuid4().hex;store=Store();held=False
    previous_handler=None
    try:
        require(lease(store,'acquire',owner)['granted'],'Research lease unavailable');held=True
        directory.mkdir(parents=True,exist_ok=False)
        previous_handler=signal.signal(signal.SIGALRM,lambda *_:(_ for _ in ()).throw(AcquisitionDeadline('Six-hour acquisition cap reached')))
        signal.alarm(21600)
        base=baseline();before=fingerprints(preservation_paths())
        rows=load_rows();groups=family_groups(rows);lookup={r['bill_id']:r for r in rows}
        input_reg,encoding=read_sealed(PILOT/'e1-unapproved-inputs.json')
        memberships=replay_memberships(rows,groups,encoding)
        require(memberships==base['prior_memberships'],'Legacy partition changed since prior run')
        selected,ledger=select_expansion(rows,groups,memberships,base['excluded'])
        pop=population_snapshot(rows,groups)
        deps=('scripts/mechanism_training_expansion_v2.py','scripts/mechanism_training_coverage.py',
              'scripts/bill_context_execution.py','scripts/bill_context_design_text_v2.py',
              'scripts/paper_review_packet.py','scripts/cross_congress_evaluate.py','engine/cohort.py',
              'engine/ingest.py','engine/store.py','engine/research_lease.py','engine/paper_evaluation.py')
        cycles=cycle_specs(selected)
        reg=seal(dict(registered_at=now(),selection=selected,selected_count=len(selected),cap=CAP,quota_per_congress=QUOTA,cycles=cycles,
            rule='Congress113–116 ascending; digest(billID),ID;250perCongress max; global family uniqueness; exclude original100pilot and prior200selected IDs/families; no outcome-based selection or failure replacements',
            baseline=base,baseline_available_ids=base['ids'],memberships=memberships,e1_inputs_hash=input_reg['hash'],population_hash=digest(pop),ledger_hash=digest(ledger),
            implementation_hashes=fingerprints([ROOT/p for p in deps]),frozen_files=before,wallclock_cap_seconds=21600,
            source_request_concurrency=1,lease_owner=owner,source_failure_policy='Record failure and continue fixed selection without replacement; global integrity/time/lease failure aborts with immutable failure receipt',
            human_certified=False,historical_feature_eligible=False,quality_texts_opened=False,
            scope='Current introduced XML and dated package metadata only; no annotations,fits,outcome scores or model promotion'))
        persist_or_compare(directory/'registration.json',reg)
        persist_or_compare(directory/'selection-population.json',seal(pop));persist_or_compare(directory/'selection-ledger.json',seal(ledger))
        cycle_registrations={}
        for cycle in cycles:
            envelope=seal(dict(**cycle,registration_hash=reg['hash']))
            persist_or_compare(directory/'cycles'/f"cycle-{cycle['cycle']:02d}-registration.json",envelope)
            cycle_registrations[cycle['cycle']]=envelope
        sources=Sources(directory);good=set();failures=[];attempted=0
        caches=[D/'sources',ROOT/'data/research-runs/cross-congress-reserve-20261105/sources']
        for s in selected:
            require(lease(store,'renew',owner)['granted'],'Lost research lease')
            bid=s['bill_id'];item=dict(**s,registration_hash=reg['hash'],historical_feature_eligible=False,human_certified=False,
                                     status='blocked',mechanism_labels_created=0)
            try:
                row=dict(lookup[bid],family_id=s['family_id']);evidence=packet([row],caches,ROOT)['records'][0]
                persist_or_compare(directory/'packets'/(bid+'.json'),seal(evidence));package,url,proof=introduced_evidence(evidence)
                raw,source=sources.get(url)
                require(timestamp(source['retrieved_at'])>=timestamp(reg['body']['registered_at']),'Backdated retrieval')
                view=seal(dict(**render(raw,bid),source=source,registration_hash=reg['hash'],historical_feature_eligible=False))
                persist_or_compare(directory/'views'/(bid+'.json'),view)
                item.update(status='metadata_dated_current_xml',package=package,source=source,publication_metadata=proof,
                            source_view_hash=view['hash'],historical_rendition_identity='uncertified');good.add(bid)
            except (AcquisitionDeadline, TimeoutError):
                # Includes the global alarm; never treat exhausted run time as a replaceable case failure.
                raise
            except Exception as error:
                item['error']=str(error);failures.append(dict(bill_id=bid,error=str(error)))
            persist_or_compare(directory/'records'/(bid+'.json'),seal(item));attempted+=1
            if attempted%100==0 or attempted==len(selected):
                cycle=cycles[(attempted-1)//100]
                batch=selected[((attempted-1)//100)*100:attempted]
                checked={x['bill_id'] for x in batch if validate_current_record(directory,x,reg['hash'],reg['body']['registered_at'])}
                require(checked==good.intersection(cycle['bill_ids']),'Cycle source replay mismatch')
                require(fingerprints(preservation_paths())==before,'Frozen files changed at cycle boundary')
                cycle_result=seal(dict(cycle=cycle['cycle'],registration_hash=reg['hash'],
                    cycle_registration_hash=cycle_registrations[cycle['cycle']]['hash'],completed_at=now(),
                    attempted=len(batch),usable=len(checked),failures=[f for f in failures if f['bill_id'] in cycle['bill_ids']],
                    record_hashes={x['bill_id']:read_sealed(directory/'records'/(x['bill_id']+'.json'))[0]['hash'] for x in batch},
                    frozen_files_unchanged=True,historical_feature_eligible=False))
                persist_or_compare(directory/'cycles'/f"cycle-{cycle['cycle']:02d}-result.json",cycle_result)
            if attempted%25==0 or attempted==len(selected):print(json.dumps(dict(attempted=attempted,selected=len(selected),usable=len(good),failures=len(failures))),flush=True)
            time.sleep(.15)
        require(fingerprints(preservation_paths())==before,'Frozen artifacts changed during acquisition')
        manifest=sources.manifest()
        result=seal(dict(registration_hash=reg['hash'],completed_at=now(),selected=len(selected),attempted=attempted,
            downloaded_documents=len(manifest),source_bytes=sum(r['bytes'] for r in manifest),usable_metadata_dated_current_xml=len(good),completed_cycles=len(cycles),
            usable_by_congress=dict(Counter(str(s['congress']) for s in selected if s['bill_id'] in good)),failures=failures,
            baseline_unique=len(base['ids']),total_unique=len(set(base['ids'])|good),coverage_before=coverage(memberships,base['ids']),
            coverage_after=coverage(memberships,set(base['ids'])|good),coverage_increment=coverage(memberships,good),
            certified_historical=0,historical_feature_eligible=False,human_certified=False,quality_texts_opened=False,
            models_fitted=0,outcomes_scored=0,mechanism_labels_created=0,frozen_artifacts_unchanged=True,
            limitation='Dated package metadata does not certify original historical XML bytes; family genealogy and labels remain uncertified. Fixed convenience subset of prior legacy memberships, not representative independent validation. Earlier evaluated bills may enter later training only through existing dated memberships.'))
        persist_or_compare(directory/'result.json',result)
        receipt=verify(directory)
        print(json.dumps(dict(result_hash=result['hash'],verification_hash=receipt['hash'],**result['body']),indent=2),flush=True)
        return result
    except Exception as error:
        if directory.exists():persist_or_compare(directory/'failure.json',seal(dict(error=str(error),record_count=len(list((directory/'records').glob('*.json'))),historical_feature_eligible=False)))
        raise
    finally:
        signal.alarm(0)
        if previous_handler is not None:signal.signal(signal.SIGALRM,previous_handler)
        if held:lease(store,'release',owner)
        store.close()


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True);parser.add_argument('--verify-only',action='store_true')
    args=parser.parse_args()
    if args.verify_only:print(json.dumps(verify(args.output),indent=2))
    else:run(args.output)
