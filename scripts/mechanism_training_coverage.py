"""Bounded introduced-text coverage expansion; no annotation, fit or score.

Current downloads plus dated package metadata are never certified historical
renditions. Selection consumes identities, family groups and availability dates,
not outcome values; it preserves the existing core/calibration populations.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import time
import uuid

from engine.cohort import Sources, family_groups, provenance
from engine.paper_evaluation import require, seal, unseal
from engine.research_lease import lease
from engine.store import ROOT, Store, digest, now, timestamp
from scripts.bill_context_execution import xml_url
from scripts.bill_context_design_text_v2 import render
from scripts.cross_congress_evaluate import D, load_rows, make_split
from scripts.paper_review_packet import packet, persist_or_compare

PILOT = ROOT/'data/research-runs/bill-context-20261108-v1'
FOLDS = (115, 116, 117)
CONGRESSES = (113, 114, 115, 116)


def read_sealed(path):
    envelope = json.loads(Path(path).read_text())
    return envelope, unseal(envelope)


def fingerprints(paths):
    return {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(set(paths))}


def frozen_paths():
    # Byte hashing only: no quality text rendering or outcome/score inspection.
    base = ROOT/'data/research-runs'
    paths = list(PILOT.rglob('*'))
    for name in ('survivor1000-20261105/artifact.json',
                 'convergence-einsum-20261105/candidate-lock.json',
                 'cross-congress-scale-20261105/final-training.json'):
        paths.append(base/name)
    paths += list(D.glob('fold-*.json'))
    return [p for p in paths if p.is_file()]


def replay_memberships(rows, groups, encoding):
    """Check saved identities and timing without calculating or emitting scores."""
    lookup = {r['bill_id']:r for r in rows}
    require(len(lookup) == len(rows), 'Duplicate population identity')
    require(set(encoding) == {str(c) for c in FOLDS}, 'Unexpected fold set')
    result = {}
    for c in FOLDS:
        train, test = make_split(rows, c, groups)
        f = encoding[str(c)]
        core, cal = f['core_ids'], f['calibration_ids']
        require(len(set(core+cal)) == len(core+cal), 'Repeated training partition identity')
        require(set(core+cal) == {r['bill_id'] for r in train}, 'Training membership changed')
        require(f['evaluation_ids'] == [r['bill_id'] for r in test], 'Evaluation membership changed')
        legacy = json.loads((D/f'fold-{c}-models.json').read_text())['calibrated_all_history']
        require(core == legacy['core_ids'] and cal == legacy['calibration_ids'], 'Core/calibration membership changed')
        threshold = min(timestamp(r['cutoff']) for r in test)
        for bid in core+cal:
            require(lookup[bid]['congress'] < c and timestamp(lookup[bid]['label_available_at']) < threshold,
                    'Training label timing violation')
        fs = [{groups[x] for x in ids} for ids in (core, cal, f['evaluation_ids'])]
        require(all(len(family) == len(ids) for family, ids in zip(fs, (core, cal, f['evaluation_ids']))), 'Repeated partition family')
        require(all(not fs[i]&fs[j] for i in range(3) for j in range(i+1,3)), 'Within-fold family overlap')
        result[str(c)] = dict(core_ids=list(core), calibration_ids=list(cal),
                              first_evaluation_cutoff=threshold)
    return result


def select_training(rows, groups, memberships, pilot_selection, quota=50):
    require(type(quota) is int and 1 <= quota <= 50, 'Quota must be 1–50 per Congress')
    lookup = {r['bill_id']:r for r in rows}
    require(len(lookup) == len(rows), 'Duplicate population identity')
    pilot_ids = {r['bill_id'] for r in pilot_selection}
    require(len(pilot_ids) == len(pilot_selection), 'Duplicate pilot identity')
    excluded_families = {groups[bid] for bid in pilot_ids}
    require(all(groups[r['bill_id']] == r['family_id'] for r in pilot_selection), 'Pilot family changed')
    roles = {}
    for fold, f in memberships.items():
        for role in ('core_ids', 'calibration_ids'):
            for bid in f[role]:
                require(bid in lookup, 'Unknown training identity')
                row = lookup[bid]
                require(row['congress'] < int(fold) and timestamp(row['label_available_at']) < timestamp(f['first_evaluation_cutoff']), 'Label timing violation')
                roles.setdefault(bid, []).append(dict(fold=fold, role=role.removesuffix('_ids'),
                    first_evaluation_cutoff=f['first_evaluation_cutoff']))
    selected, ledger, used = [], [], set(excluded_families)
    for congress in CONGRESSES:
        count = 0
        for bid in sorted((bid for bid in roles if lookup[bid]['congress'] == congress), key=lambda bid:(digest(bid), bid)):
            row = lookup[bid]; family = groups[bid]
            reason = ('pilot_identity_or_family' if bid in pilot_ids or family in excluded_families else
                      'already_selected_family' if family in used else
                      'row_excluded' if row.get('exclusion') else
                      'outside_fixed_quota' if count >= quota else None)
            ledger.append(dict(bill_id=bid, congress=congress, family_id=family, disposition=reason or 'selected'))
            if reason: continue
            selected.append(dict(bill_id=bid, congress=congress, family_id=family,
                                 cutoff=timestamp(row['cutoff']), label_available_at=timestamp(row['label_available_at']),
                                 memberships=roles[bid]))
            used.add(family); count += 1
    require(len(selected) <= 200, 'Acquisition cap exceeded')
    return selected, ledger


def introduced_evidence(record, root=ROOT):
    package, url = xml_url(record, root)
    version = next(v for v in record['versions'] if v['package'] == package)
    require(version['used_as_feature'], 'Introduced version not eligible at cutoff')
    def retained(suffix):
        source = next(s for s in version['sources'] if s['url'].endswith(suffix))
        raw = (root/source['retained_matches'][0]['raw_path']).read_bytes()
        require(len(raw) == source['bytes'] and hashlib.sha256(raw).hexdigest() == source['sha256'], 'Retained metadata changed')
        return raw
    proof = provenance(retained('/mods.xml'), retained('/premis.xml'), package)
    require(timestamp(proof['issued_at']) <= timestamp(record['cutoff']) and
            timestamp(proof['available_at']) <= timestamp(record['cutoff']), 'Publication metadata later than cutoff')
    require(timestamp(version['issued_at']) == timestamp(proof['issued_at']) and
            timestamp(version['available_at']) == timestamp(proof['available_at']), 'Publication metadata replay mismatch')
    expected = re.fullmatch(r'BILLS-(\d+)(hr|s)(\d+)(ih|is)', package)
    require(expected is not None and f'{expected[1]}-{expected[2]}{expected[3]}' == record['bill_id'], 'Package/bill identity mismatch')
    require(expected[4] == ('ih' if expected[2] == 'hr' else 'is'), 'Introduced rendition chamber mismatch')
    return package, url, proof


def coverage(memberships, available_ids):
    available_ids = set(available_ids)
    return {fold:{role:dict(total=len(f[role+'_ids']), metadata_dated_xml=sum(b in available_ids for b in f[role+'_ids']),
                            certified_historical=0)
                  for role in ('core','calibration')} for fold,f in memberships.items()}


def population_snapshot(rows, groups):
    # Excluded discovery rows may never have acquired a valid checkpoint.
    return [dict(bill_id=r['bill_id'], congress=r['congress'], family_id=groups[r['bill_id']],
                 cutoff=r.get('cutoff'), label_available_at=r['label_available_at'],
                 exclusion=r.get('exclusion')) for r in rows]


def run(directory, quota=50):
    directory = Path(directory)
    require(ROOT/'data' in directory.resolve().parents, 'Output must be under ignored data')
    require(not directory.exists(), 'Use a new immutable run directory')
    owner = 'mechanism-training-coverage-'+uuid.uuid4().hex
    store = Store(); acquired_lease = False
    try:
        require(lease(store,'acquire',owner)['granted'], 'Research lease unavailable')
        acquired_lease = True
        directory.mkdir(parents=True, exist_ok=False)
        before = fingerprints(frozen_paths())
        rows = load_rows(); groups = family_groups(rows); lookup = {r['bill_id']:r for r in rows}
        pilot_envelope,pilot_spec = read_sealed(PILOT/'registration.json')
        input_envelope,encoding = read_sealed(PILOT/'e1-unapproved-inputs.json')
        require(len(pilot_spec['selection']) == 100 and {r['partition'] for r in pilot_spec['selection']} == {'design','quality'}, 'Pilot firewall incomplete')
        memberships = replay_memberships(rows, groups, encoding)
        selected,ledger = select_training(rows,groups,memberships,pilot_spec['selection'],quota)
        # Selection already fixed; packet errors become failures, never replacements.
        source_rows = [dict(lookup[s['bill_id']], family_id=s['family_id']) for s in selected]
        # Baseline counts use only design records, without opening quality sources.
        baseline_ids = set()
        pilot_packet = read_sealed(PILOT/'source-packet.json')[1]
        pilot_evidence = {r['bill_id']:r for r in pilot_packet['records']}
        training_union = {b for f in memberships.values() for role in ('core_ids','calibration_ids') for b in f[role]}
        for s in pilot_spec['selection']:
            if s['partition'] != 'design' or s['bill_id'] not in training_union: continue
            _,record = read_sealed(PILOT/'records'/(s['bill_id']+'.json'))
            if 'source' not in record: continue
            _,url,_ = introduced_evidence(pilot_evidence[s['bill_id']])
            require(record['source']['url'] == url, 'Baseline source identity mismatch')
            raw = (PILOT/'sources'/(hashlib.sha256(url.encode()).hexdigest()+'.raw')).read_bytes()
            require(hashlib.sha256(raw).hexdigest() == record['source']['sha256'], 'Baseline source changed')
            render(raw,s['bill_id'])
            baseline_ids.add(s['bill_id'])
        deps = ('scripts/mechanism_training_coverage.py','scripts/bill_context_execution.py',
                'scripts/bill_context_design_text_v2.py','scripts/paper_review_packet.py',
                'scripts/cross_congress_evaluate.py','engine/cohort.py','engine/ingest.py','engine/store.py','engine/research_lease.py')
        projected_population = population_snapshot(rows, groups)
        registration = seal(dict(registered_at=now(),rule='Congress113–116 ascending; digest(bill_id),ID; at most50 perCongress; unique global family; exclude100pilot IDs and families; no replacement after source failure',
            selection=selected,quota_per_congress=quota,acquisition_cap=200,selected_count=len(selected),
            selected_by_congress=dict(Counter(str(s['congress']) for s in selected)),
            pilot_registration_hash=pilot_envelope['hash'],e1_inputs_hash=input_envelope['hash'],
            memberships=memberships,selection_ledger_hash=digest(ledger),family_graph_hash=digest(groups),
            selection_population_hash=digest(projected_population),
            excluded_pilot_ids=[s['bill_id'] for s in pilot_spec['selection']],
            excluded_pilot_families=sorted({groups[s['bill_id']] for s in pilot_spec['selection']}),
            baseline_design_ids=sorted(baseline_ids),coverage_before=coverage(memberships,baseline_ids),
            implementation_hashes=fingerprints([ROOT/p for p in deps]),frozen_files=before,
            scope='Current introduced XML acquisition and metadata/identity validation only; outcome values unused in selection; no fit or score, no mechanism extraction',
            historical_feature_eligible=False,human_certified=False,quality_texts_opened=False,lease_owner=owner))
        persist_or_compare(directory/'registration.json',registration)
        persist_or_compare(directory/'selection-ledger.json',seal(ledger))
        persist_or_compare(directory/'selection-population.json',seal(projected_population))
        sources = Sources(directory); records=[]; good=set(); failures=[]
        caches = [D/'sources',ROOT/'data/research-runs/cross-congress-reserve-20261105/sources']
        for selected_row,row in zip(selected,source_rows):
            require(lease(store,'renew',owner)['granted'], 'Lost research lease')
            item=dict(**selected_row,registration_hash=registration['hash'],historical_feature_eligible=False,
                      human_certified=False,mechanism_labels_created=0,status='blocked')
            try:
                evidence=packet([row],caches,ROOT)['records'][0]
                persist_or_compare(directory/'packets'/(row['bill_id']+'.json'),seal(evidence))
                package,url,proof=introduced_evidence(evidence)
                raw,receipt=sources.get(url)
                require(timestamp(receipt['retrieved_at']) >= timestamp(registration['body']['registered_at']), 'Backdated acquisition receipt')
                view=seal(dict(**render(raw,row['bill_id']),source=receipt,registration_hash=registration['hash'],historical_feature_eligible=False))
                persist_or_compare(directory/'views'/(row['bill_id']+'.json'),view)
                item.update(status='metadata_dated_current_xml',package=package,source=receipt,publication_metadata=proof,
                            source_view_hash=view['hash'],historical_rendition_identity='uncertified')
                good.add(row['bill_id'])
            except Exception as error:
                item['error']=str(error);failures.append(dict(bill_id=row['bill_id'],error=str(error)))
            persist_or_compare(directory/'records'/(row['bill_id']+'.json'),seal(item));records.append(item)
            print(json.dumps(dict(processed=len(records),selected=len(selected),usable_metadata_dated=len(good),failures=len(failures))),flush=True)
            time.sleep(.15)
        require(fingerprints(frozen_paths()) == before, 'Frozen artifacts changed')
        result=seal(dict(registration_hash=registration['hash'],completed_at=now(),selected=len(selected),
            attempted=len(records),downloaded_documents=len(sources.manifest()),usable_metadata_dated_current_xml=len(good),
            usable_by_congress=dict(Counter(str(s['congress']) for s in selected if s['bill_id'] in good)),
            failures=failures,source_bytes=sum(s['bytes'] for s in sources.manifest()),
            coverage_before=coverage(memberships,baseline_ids),coverage_after=coverage(memberships,baseline_ids|good),
            coverage_increment=coverage(memberships,good),certified_historical=0,historical_feature_eligible=False,
            human_certified=False,quality_texts_opened=False,frozen_artifacts_unchanged=True,
            models_fitted=0,outcomes_scored=0,mechanism_labels_created=0,
            limitation='Current XML with dated official package metadata is not archived historic byte identity. Family screening is automated, not certified genealogy. Selection is outcome-blind within existing legacy training/calibration memberships, not a representative sample. Earlier-fold evaluation IDs may appear only as later-fold training;117 evaluation-only IDs never selected.'))
        persist_or_compare(directory/'result.json',result)
        return result
    except Exception as error:
        if directory.exists():persist_or_compare(directory/'failure.json',seal(dict(error=str(error),historical_feature_eligible=False)))
        raise
    finally:
        if acquired_lease:lease(store,'release',owner)
        store.close()


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--quota',type=int,default=50)
    args=parser.parse_args()
    result=run(args.output,args.quota)
    print(json.dumps(dict(hash=result['hash'],**result['body']),indent=2))
