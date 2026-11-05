"""Read-only, snapshot-scoped import integrity audit; never certifies eligibility.

Run: python3 -m engine.import_quality --output data/audits/import-quality.json
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import sqlite3
from .store import ROOT, digest, now


def audit(database, raw_directory):
    started = now()
    db = sqlite3.connect(Path(database).resolve().as_uri() + '?mode=ro', uri=True)
    try:
        db.execute('BEGIN')
        tables = {r[0] for r in db.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        def bodies(table):
            return [json.loads(r[0]) for r in db.execute('SELECT body FROM ' + table)] if table in tables else []
        records = [(r[0], r[1], json.loads(r[2])) for r in db.execute(
            "SELECT id,kind,body FROM records WHERE dataset='official' ORDER BY available_at,effective_at,id")]
        plans = bodies('coverage_plans')
        inventories = bodies('sample_inventories')
        jobs = {j['id']: j for j in bodies('bulk_import_jobs')}
        receipts = {r[0]: json.loads(r[1]) for r in db.execute('SELECT name,body FROM checkpoints')}
        snapshot = now()
    finally:
        db.close()
    latest = {}
    kind_counts = Counter()
    record_failures = []
    raw_hashes = set()
    for ident, kind, body in records:
        kind_counts[kind] += 1
        if ident != digest({k: v for k, v in body.items() if k != 'id'}) or body.get('id') != ident:
            record_failures.append(ident)
        if body.get('raw_hash'):
            raw_hashes.add(body['raw_hash'])
        if kind == 'bill':
            latest[body['bill_id']] = body
    for inv in inventories:
        raw_hashes.update(s['raw_hash'] for s in inv['strata'])
    missing_raw, corrupt_raw = [], []
    for sha in sorted(raw_hashes):
        if len(sha) != 64 or any(c not in '0123456789abcdef' for c in sha):
            corrupt_raw.append(sha)
            continue
        path = Path(raw_directory) / sha
        if not path.is_file():
            missing_raw.append(sha)
        elif hashlib.sha256(path.read_bytes()).hexdigest() != sha:
            corrupt_raw.append(sha)
    missing_receipts, bad_receipts = [], []
    # Current bulk snapshots have fetch/raw receipts; archived pilot sources use
    # a different provenance contract, and are counted separately.
    bulk_bills = {b: r for b, r in latest.items() if 'current bulk snapshot' in r.get('coverage', '')}
    for bill_id, body in sorted(bulk_bills.items()):
        sha = body['raw_hash']
        receipt = receipts.get(f'raw:{bill_id}:{sha}')
        if not receipt:
            missing_receipts.append(bill_id)
        elif receipt.get('hash') != sha or receipt.get('retrieved_at') != body['observed_at']:
            bad_receipts.append(bill_id)
    resolutions = {}
    actions = set()
    for _, kind, body in records:
        if kind == 'resolution':
            resolutions.setdefault(body['bill_id'], set()).add(body['value'])
        if kind == 'event':
            actions.add(body['bill_id'])
    def population_stats(ids):
        imported = set(ids) & latest.keys()
        return dict(population=len(set(ids)), imported=len(imported), missing_ids=sorted(set(ids)-latest.keys()),
            missing_fields={field: sum(not latest[b].get(field) or latest[b].get(field) in
                                      ('Unknown', 'Unclassified', 'Untitled measure') for b in imported)
                            for field in ('title', 'topic', 'sponsor', 'introduced_at', 'raw_hash')},
            without_actions=len(imported-actions),
            outcomes=dict(positive=sum(resolutions.get(b)=={1} for b in imported),
                          negative=sum(resolutions.get(b)=={0} for b in imported),
                          conflicting=sum(len(resolutions.get(b,set()))>1 for b in imported),
                          unresolved=sum(b not in resolutions for b in imported)),
            family_unadjudicated=sum(not latest[b].get('family_status') or
                                     'unadjudicated' in latest[b]['family_status'].lower() for b in imported),
            historically_verified_metadata=sum(bool(latest[b].get('verified_available_at') and
                                                    latest[b].get('archive_proof')) for b in imported))
    plan_reports = []
    for plan in plans:
        job_list = [jobs[b['job_id']] for b in plan['batches'] if b.get('job_id') in jobs]
        batch_ids = [bid for batch in plan['batches'] for bid in batch['bill_ids']]
        inv = next((i for i in inventories if i['id']==plan['inventory_id']), None)
        expected = {b for b in inv['bill_ids'] if int(b.split('-')[0]) in plan['congresses']} if inv else set()
        pop = {k: plan[k] for k in ('inventory_id','inventory_hash','congresses','bill_ids')}
        plan_reports.append(dict(id=plan['id'], status=plan['status'], congresses=plan['congresses'],
            finished_at=plan.get('finished_at'), population_hash=plan['population_hash'],
            population_hash_valid=digest(pop)==plan['population_hash'], inventory_found=bool(inv),
            exact_inventory_population=bool(inv) and set(plan['bill_ids'])==expected,
            population_duplicates=len(plan['bill_ids'])-len(set(plan['bill_ids'])),
            batch_duplicates=len(batch_ids)-len(set(batch_ids)), batches_exact=set(batch_ids)==set(plan['bill_ids']),
            batches=len(plan['batches']), completed_batches=sum(j['status']=='completed' for j in job_list),
            job_completed=sum(j['completed'] for j in job_list), job_failed=sum(j['failed'] for j in job_list),
            **population_stats(plan['bill_ids'])))
    report = dict(schema_version=1, started_at=started, database_snapshot_at=snapshot, finished_at=now(),
        database=str(Path(database).resolve()), scope='Official local records and saved inventory/coverage plans in one read-only SQLite snapshot.',
        record_counts=dict(kind_counts), unique_bills=len(latest), extra_bill_versions=kind_counts['bill']-len(latest),
        official_population=population_stats(latest), plans=plan_reports,
        integrity=dict(record_ids_checked=len(records), invalid_record_ids=record_failures,
            raw_hashes_checked=len(raw_hashes), missing_raw=missing_raw, corrupt_raw=corrupt_raw,
            bulk_receipts_checked=len(bulk_bills), other_provenance_bills=len(latest)-len(bulk_bills),
            missing_bulk_receipts=missing_receipts, invalid_bulk_receipts=bad_receipts,
            inventories=[dict(id=i['id'], hash_valid=digest({k:v for k,v in i.items() if k not in ('id','hash')})==i['hash']) for i in inventories]),
        interpretation='Presence, content hashes and retrieval receipts establish retained-source integrity, not historical availability, correct outcome adjudication, or training/evaluation eligibility. Unresolved outcomes must not be treated as negative labels.')
    report['report_hash'] = digest(report)
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--database', type=Path, default=ROOT/'data'/'engine.sqlite')
    parser.add_argument('--raw-directory', type=Path, default=ROOT/'data'/'raw')
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = audit(args.database, args.raw_directory)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(dict(output=str(args.output.resolve()), report_hash=result['report_hash'], unique_bills=result['unique_bills'], plans=result['plans']), indent=2))


if __name__ == '__main__':
    main()
