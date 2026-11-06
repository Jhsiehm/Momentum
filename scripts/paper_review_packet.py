"""Export bounded real publication evidence for review; never certify or score."""
import argparse
import hashlib
import json
from pathlib import Path

from engine.paper_evaluation import seal, unseal, save
from engine.store import ROOT, digest, now
from scripts.paper_readiness_audit import audit

RULE = 'first n rows sorted by canonical JSON SHA256(bill_id), then bill_id; outcomes unused'


def select(rows, count):
    if type(count) is not int or not 1 <= count <= 100:
        raise ValueError('Review count must be 1–100')
    ids = [r['bill_id'] for r in rows]
    if len(ids) != len(set(ids)) or len(rows) < count:
        raise ValueError('Duplicate or insufficient training identities')
    return sorted(rows, key=lambda r:(digest(r['bill_id']),r['bill_id']))[:count]


def resolve(source, caches, root):
    key = hashlib.sha256(source['url'].encode()).hexdigest()
    matches = []
    for cache in caches:
        raw, meta = cache/(key+'.raw'), cache/(key+'.json')
        if not raw.exists() or not meta.exists():
            continue
        receipt = json.loads(meta.read_text())
        data = raw.read_bytes()
        hashed = hashlib.sha256(data).hexdigest()
        if (receipt.get('url') == source['url'] and receipt.get('sha256') == hashed
                and hashed == source['sha256'] and len(data) == source['bytes']
                and receipt.get('bytes') == len(data)):
            matches.append(dict(raw_path=str(raw.relative_to(root)),receipt_path=str(meta.relative_to(root)),
                                receipt_sha256=hashlib.sha256(meta.read_bytes()).hexdigest()))
    if not matches:
        raise ValueError('Missing or corrupt matching retained source: '+source['url'])
    return dict(source, retained_matches=matches)


def packet(rows, caches, root):
    records=[]
    for row in rows:
        versions=[]
        for version in row['versions']:
            versions.append(dict(package=version['package'],stage=version['stage'],
                issued_at=version['issued_at'],available_at=version['available_at'],
                used_as_feature=version['package'] in row['eligible_packages'],
                availability_basis=version.get('basis'),
                introduction_validation=version.get('introduction_validation'),
                sources=[resolve(s,caches,root) for s in version['sources']]))
        records.append(dict(bill_id=row['bill_id'],congress=row['congress'],family_id=row['family_id'],
            introduced_at=row['introduced_at'],cutoff=row['cutoff'],features=row['x'],
            discovery_source=resolve(row['source'],caches,root),versions=versions,
            human_review=dict(status='pending',reviewer=None,decision=None),
            required_reviews=['Historical rendition identity and retrospective contamination',
                              'Introduction identity/date and every feature availability bound',
                              'Complete cross-period family genealogy; stored family ID is not certification'],
            outcome_review='Not included: this packet covers feature provenance only; no outcome certification'))
    return dict(selection_ids=[r['bill_id'] for r in rows],records=records,
                source_references=sum(1+sum(len(v['sources']) for v in r['versions']) for r in records),
                feature_review_ready=True,human_certified=False,release_eligible=False,
                independent_validation=False,scope='Retained real training feature evidence; no outcomes, predictions or scores')


def persist_or_compare(path, envelope):
    if path.exists():
        stored=json.loads(path.read_text());unseal(stored)
        if stored != envelope:
            raise ValueError('Immutable packet replay mismatch: '+str(path))
    else:
        save(path,envelope)


def run(directory, count=12, root=ROOT):
    root=Path(root);directory=Path(directory)
    before=audit(root)
    training_path=root/'data/research-runs/cross-congress-scale-20261105/final-training.json'
    rows=select(json.loads(training_path.read_text()),count)
    code_hash=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    spec=dict(rule=RULE,count=count,training_file_sha256=hashlib.sha256(training_path.read_bytes()).hexdigest(),
              selected_ids=[r['bill_id'] for r in rows],code_sha256=code_hash)
    protocol_path=directory/'protocol.json'
    if protocol_path.exists():
        protocol=json.loads(protocol_path.read_text())
        if unseal(protocol)['spec']!=spec:raise ValueError('Review protocol changed')
    else:
        protocol=seal(dict(spec=spec,registered_at=now()));save(protocol_path,protocol)
    # Bounded known source locations, not a scan of private workspace data.
    base=root/'data/research-runs'
    caches=[base/name/'sources' for name in ('cross-congress-scale-20261105','cross-congress-reserve-20261105')]
    try:
        body=packet(rows,caches,root)
        if audit(root)!=before:raise ValueError('Frozen artifacts changed during packet creation')
        result=seal(dict(protocol_hash=protocol['hash'],**body))
        persist_or_compare(directory/'packet.json',result)
        return result
    except Exception as error:
        # Failure is separately retained and never converted to an exclusion/negative.
        failure=seal(dict(protocol_hash=protocol['hash'],error=str(error),release_eligible=False))
        persist_or_compare(directory/('blocked-'+failure['hash']+'.json'),failure)
        raise


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--count',type=int,default=12)
    args=parser.parse_args()
    result=run(args.output,args.count)
    print(json.dumps(dict(hash=result['hash'],selected=len(result['body']['records']),
                         source_references=result['body']['source_references'],human_certified=False)))
