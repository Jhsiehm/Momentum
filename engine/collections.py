"""Versioned user collections and bounded, explicit GovInfo import jobs."""
import json
import re
import threading
import uuid
from .store import Store, now
from .ingest import ingest_bill

MAX_BILLS = 100
SCHEMA = '''
CREATE TABLE IF NOT EXISTS collections (id TEXT, version INTEGER, body TEXT NOT NULL, PRIMARY KEY(id,version));
CREATE TRIGGER IF NOT EXISTS collections_no_update BEFORE UPDATE ON collections BEGIN SELECT RAISE(ABORT,'Collection versions are immutable'); END;
CREATE TRIGGER IF NOT EXISTS collections_no_delete BEFORE DELETE ON collections BEGIN SELECT RAISE(ABORT,'Collection versions are immutable'); END;
CREATE TABLE IF NOT EXISTS collection_import_jobs (id TEXT PRIMARY KEY, status TEXT NOT NULL, body TEXT NOT NULL);
'''


def initialize(store):
    store.db.executescript(SCHEMA)


def parse_bill_id(value):
    match = re.fullmatch(r'(\d{2,3})-(hr|s)([1-9]\d{0,5})', str(value).strip().lower())
    if not match or not 93 <= int(match[1]) <= 200:
        raise ValueError('Use official bill identifiers such as 119-hr22 (Congress 93–200, H.R. or S.).')
    return int(match[1]), match[2], int(match[3])


def validate_bill_ids(values, dataset='official'):
    if not isinstance(values, list) or not 1 <= len(values) <= MAX_BILLS:
        raise ValueError('Supply between 1 and 100 bill identifiers.')
    result = []
    for value in values:
        if not isinstance(value, str):
            raise ValueError('Bill identifiers must be strings.')
        value = value.strip().lower()
        prefix = 'demo-' if dataset == 'demo' else ''
        if prefix and not value.startswith(prefix):
            raise ValueError('Demo collections require demo bill identifiers.')
        congress, kind, number = parse_bill_id(value[len(prefix):])
        normalized = f'{prefix}{congress}-{kind}{number}'
        if normalized not in result:
            result.append(normalized)
    return result


def _coverage(store, item):
    imported = sum(store.bill(item['dataset'], bid) is not None for bid in item['bill_ids'])
    return dict(item, coverage={'total':len(item['bill_ids']), 'imported':imported,
        'missing':len(item['bill_ids'])-imported,
        'note':'Imported records are not proof of historical availability or experiment eligibility.'})


def get_collection(store, collection_id, version=None):
    initialize(store)
    sql, args = 'SELECT body FROM collections WHERE id=?', [collection_id]
    if version is not None:
        sql += ' AND version=?'
        args.append(version)
    row = store.db.execute(sql + ' ORDER BY version DESC LIMIT 1', args).fetchone()
    if row is None:
        raise ValueError('Collection not found.')
    return _coverage(store, json.loads(row[0]))


def list_collections(store):
    initialize(store)
    rows = store.db.execute('SELECT c.body FROM collections c JOIN (SELECT id,MAX(version) v FROM collections GROUP BY id) latest ON c.id=latest.id AND c.version=latest.v ORDER BY c.id').fetchall()
    return [_coverage(store,json.loads(row[0])) for row in rows]


def save_collection(store, args):
    initialize(store)
    name = args.get('name', '')
    if not isinstance(name,str) or not 1 <= len(name.strip()) <= 100:
        raise ValueError('Collection name must contain 1–100 characters.')
    dataset = args.get('dataset','official')
    if dataset not in ('official','demo'):
        raise ValueError('Unknown dataset.')
    bill_ids = validate_bill_ids(args.get('bill_ids'),dataset)
    collection_id = args.get('id') or str(uuid.uuid4())
    if not isinstance(collection_id,str) or len(collection_id)>100:
        raise ValueError('Invalid collection identifier.')
    try:
        store.db.execute('BEGIN IMMEDIATE')
        row = store.db.execute('SELECT body FROM collections WHERE id=? ORDER BY version DESC LIMIT 1',(collection_id,)).fetchone()
        previous = json.loads(row[0]) if row else None
        if args.get('id') and previous is None:
            raise ValueError('Collection not found.')
        if previous and (type(args.get('expected_version')) is not int or args['expected_version'] != previous['version']):
            raise ValueError('Collection changed. Reload it and retry using its current expected_version.')
        if previous and previous['dataset'] != dataset:
            raise ValueError('A collection cannot change datasets.')
        item = dict(id=collection_id, name=name.strip(), dataset=dataset, bill_ids=bill_ids,
                    version=previous['version']+1 if previous else 1,
                    created_at=previous['created_at'] if previous else now(), updated_at=now())
        store.db.execute('INSERT INTO collections VALUES (?,?,?)',(collection_id,item['version'],json.dumps(item)))
        store.db.commit()
    except Exception:
        store.db.rollback()
        raise
    return _coverage(store,item)


def get_import_job(store, job_id):
    initialize(store)
    row=store.db.execute('SELECT body FROM collection_import_jobs WHERE id=?',(job_id,)).fetchone()
    if not row:
        raise ValueError('Import job not found.')
    return json.loads(row[0])


def list_import_jobs(store):
    initialize(store)
    return [json.loads(row[0]) for row in store.db.execute('SELECT body FROM collection_import_jobs ORDER BY rowid DESC LIMIT 30')]


def _save_job(store, job):
    with store.db:
        store.db.execute('UPDATE collection_import_jobs SET status=?,body=? WHERE id=?',(job['status'],json.dumps(job),job['id']))


def run_import_job(db_path, job_id):
    store=Store(db_path)
    try:
        job=get_import_job(store,job_id)
        if job['status']!='queued':
            return job
        job.update(status='running',started_at=now())
        with store.db:
            claimed=store.db.execute('UPDATE collection_import_jobs SET status=?,body=? WHERE id=? AND status=?',('running',json.dumps(job),job_id,'queued')).rowcount
        if not claimed:
            return get_import_job(store,job_id)
        for bid in job['bill_ids']:
            try:
                result=ingest_bill(store,*parse_bill_id(bid),refresh=job['refresh'])
                job['results'].append(dict(bill_id=bid,status='success',result=result))
            except Exception:
                job['results'].append(dict(bill_id=bid,status='failed',error='Official source refresh failed; retry this bill.'))
            job['completed']=len(job['results'])
            _save_job(store,job)
        job.update(status='completed' if all(r['status']=='success' for r in job['results']) else 'completed_with_errors',finished_at=now())
        _save_job(store,job)
        return job
    finally:
        store.close()


def start_import_job(store,args,launch=True):
    initialize(store)
    collection=get_collection(store,args['collection_id']) if args.get('collection_id') else None
    if collection and collection['dataset']!='official':
        raise ValueError('Only official collections use network imports.')
    ids=validate_bill_ids(collection['bill_ids'] if collection else args.get('bill_ids'))
    if type(args.get('refresh',False)) is not bool:
        raise ValueError('refresh must be boolean.')
    job=dict(id=str(uuid.uuid4()),status='queued',bill_ids=ids,total=len(ids),completed=0,results=[],refresh=args.get('refresh',False),created_at=now(),collection_id=collection['id'] if collection else None,collection_version=collection['version'] if collection else None)
    try:
        store.db.execute('BEGIN IMMEDIATE')
        active=store.db.execute("SELECT COUNT(*) FROM collection_import_jobs WHERE status IN ('queued','running')").fetchone()[0]
        if active>=2:
            raise ValueError('Two import jobs are already active. Wait for one to finish.')
        store.db.execute('INSERT INTO collection_import_jobs VALUES (?,?,?)',(job['id'],job['status'],json.dumps(job)))
        store.db.commit()
    except Exception:
        store.db.rollback()
        raise
    if launch:
        threading.Thread(target=run_import_job,args=(store.path,job['id']),daemon=True,name='collection-import').start()
    return job


def recover_import_jobs(store):
    """Call once at server startup, before accepting requests (no network)."""
    initialize(store)
    for row in store.db.execute("SELECT body FROM collection_import_jobs WHERE status IN ('queued','running')").fetchall():
        job=json.loads(row[0]); job.update(status='interrupted',finished_at=now(),error='Local server stopped before completion. Start a new import to retry; existing evidence is preserved.')
        _save_job(store,job)
