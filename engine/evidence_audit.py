"""Machine-assisted source audit; never creates human receipts or alters evidence."""
import csv
import hashlib
import json
import shutil
from . import cohort, sampling
from .store import ROOT, Store, digest, now

SAMPLE_ID = '51ee0efb-22bc-406a-87d4-75494e573623'
DIRECTORY = ROOT / 'data/samples/historical-development-v1'


def seed_cache(store, sample, sources):
    """Reuse exact retained source bytes with their original retrieval timestamp."""
    for bid in sample['bill_ids']:
        bill = store.bill('official', bid)
        if not bill:
            continue
        path = ROOT / 'data/raw' / bill['raw_hash']
        raw = path.read_bytes()
        if hashlib.sha256(raw).hexdigest() != bill['raw_hash']:
            raise ValueError('Retained source checksum mismatch: ' + bid)
        key = hashlib.sha256(bill['source_url'].encode()).hexdigest()
        dest = sources.directory / (key + '.raw')
        if not dest.exists():
            dest.write_bytes(raw)
            cohort.write_json(sources.directory / (key + '.json'), dict(url=bill['source_url'], retrieved_at=bill['observed_at'], sha256=bill['raw_hash'], bytes=len(raw)))
    old = cohort.DIRECTORY / 'sources'
    for path in old.glob('*'):
        dest = sources.directory / path.name
        if path.is_file() and not dest.exists():
            shutil.copyfile(path, dest)


def get_audit(store, sample_id):
    sample = sampling.get_sample(store, sample_id)
    path = DIRECTORY / 'assisted-audit.json'
    if not path.exists():
        return None
    report = json.loads(path.read_text())
    if report['sample_id'] != sample_id or report['sample_hash'] != sample['hash']:
        return None
    if digest(report['rows']) != report['findings_hash']:
        raise ValueError('Assisted audit findings checksum mismatch')
    return report


def export_audit_csv(report):
    import io
    output = io.StringIO(newline='')
    columns = ['bill_id','title','identity','source','availability','family','outcome','own_bill_enactment','publication_exclusion','human_review','source_url','notes']
    writer=csv.DictWriter(output,fieldnames=columns);writer.writeheader()
    for row in report['rows']:
        values={k:row.get(k,'') for k in columns};values['notes']=' '.join(row.get('notes',[]))
        writer.writerow({k:("'"+str(v) if str(v).lstrip().startswith(('=','+','-','@')) else v) for k,v in values.items()})
    return output.getvalue()


def run(store, sample_id=SAMPLE_ID, directory=DIRECTORY, offline=False):
    sample = sampling.get_sample(store, sample_id)
    prepared = ROOT / 'data/cohorts/seeded-publication-v1/cohort.json'
    experiment = json.loads(prepared.read_text()) if prepared.exists() else {}
    if experiment:
        if digest(experiment['rows']) != experiment.get('cohort_hash'):
            raise ValueError('Publication cohort checksum mismatch')
        if sorted(r['bill_id'] for r in experiment['rows']) != sorted(sample['bill_ids']):
            raise ValueError('Publication cohort differs from frozen sample membership')
    evidence_rows = {r['bill_id']:r for r in experiment.get('rows',[])}
    rows=[]
    for bid in sample['audit_bill_ids']:
        record = store.bill('official',bid)
        row = dict(bill_id=bid,identity='unsupported',source='unsupported',availability='unsupported',family='review_required',outcome='unsupported',human_review='pending',historical_action_history_eligible=False,notes=[])
        if record:
            raw = (ROOT / 'data/raw' / record['raw_hash']).read_bytes()
            if hashlib.sha256(raw).hexdigest() != record['raw_hash']:
                raise ValueError('Retained source checksum mismatch: '+bid)
            bill = cohort.xml(raw).find('bill')
            congress,kind,number=sampling.collections.parse_bill_id(bid)
            identity=bill is not None and bill.findtext('congress')==str(congress) and bill.findtext('type','').lower()==kind and bill.findtext('number')==str(number)
            row.update(identity='passed' if identity else 'unsupported',source='passed',title=record['title'],source_url=record['source_url'],source_record=dict(url=record['source_url'],sha256=record['raw_hash'],retrieved_at=record['observed_at']))
            row['reported_related_bills']=[f"{x.findtext('congress')}-{x.findtext('type','').lower()}{x.findtext('number')}" for x in bill.findall('relatedBills/item')] if bill is not None else []
        publication = evidence_rows.get(bid)
        if publication and publication.get('versions'):
            row['publication_audit']=publication
            row['availability']='passed' if publication.get('eligible_packages') else 'unsupported'
            row['publication_exclusion']=publication.get('exclusion')
            row['outcome']='passed'
            row['own_bill_enactment']=publication['y']
            row['law_census_sources']=experiment.get('law_census_sources',[])
        else:
            row['publication_exclusion']='Publication and complete outcome census audit pending.'
        row['notes']=['Machine-assisted findings only; no human receipt was created.', 'Publication metadata supports document-version proxy features only; current action history is not historically eligible.', 'Related-bill links and title matching are incomplete family screens; provision genealogy requires human review.', 'Own-bill enactment does not measure provisions enacted in another vehicle.']
        rows.append(row)
    report=dict(sample_id=sample_id,sample_hash=sample['hash'],created_at=now(),kind='machine_assisted_audit',human_receipts_modified=False,rows=rows,findings_hash=digest(rows),limitations=cohort.LIMITATIONS,experiment_source=str(prepared) if prepared.exists() else None)
    report['training_label_provenance'] = experiment.get('training_label_provenance', {})
    report['experiment_failures'] = experiment.get('failures', [])
    report['scoring_authorized'] = False
    report['scope_note'] = 'Source checks support a publication-only research audit, not authorization to score or promote a model. Training-label chronology and whole-cohort exclusions must pass the experiment protocol separately.'
    report['summary']={k:sum(r[k]=='passed' for r in rows) for k in ('identity','source','availability','family','outcome')}
    report['summary'].update(total=len(rows),human_review_pending=len(rows),historical_action_history_eligible=0)
    directory.mkdir(parents=True,exist_ok=True)
    cohort.write_json(directory / 'assisted-audit.json',report)
    (directory / 'assisted-audit.csv').write_text(export_audit_csv(report))
    return report

if __name__ == '__main__':
    store=Store()
    try:
        report=run(store)
        print(json.dumps(dict(rows=len(report['rows']), findings_hash=report['findings_hash'], checks={k:sum(r[k]=='passed' for r in report['rows']) for k in ('identity','source','availability','family','outcome')}, exclusions=[dict(bill_id=r['bill_id'],reason=r.get('publication_exclusion')) for r in report['rows'] if r.get('publication_exclusion')]),indent=2))
    finally:store.close()
