"""Append-only captures made now, never backdated into prospective evidence."""
import json
from pathlib import Path
from . import model
from .store import now, digest, congress_end

SCHEMA='''
CREATE TABLE IF NOT EXISTS prospective_receipts(id TEXT PRIMARY KEY, identity TEXT UNIQUE NOT NULL, dataset TEXT NOT NULL, bill_id TEXT NOT NULL, issued_at TEXT NOT NULL, body TEXT NOT NULL);
CREATE INDEX IF NOT EXISTS prospective_bill ON prospective_receipts(dataset,bill_id,issued_at);
CREATE TRIGGER IF NOT EXISTS prospective_no_update BEFORE UPDATE ON prospective_receipts BEGIN SELECT RAISE(ABORT,'Prospective receipts are immutable'); END;
CREATE TRIGGER IF NOT EXISTS prospective_no_delete BEFORE DELETE ON prospective_receipts BEGIN SELECT RAISE(ABORT,'Prospective receipts are immutable'); END;
'''


def initialize(store):store.db.executescript(SCHEMA)


def _validate(dataset,bill_id):
    if dataset not in ('official','demo'):raise ValueError('Choose official or demo data')
    if not isinstance(bill_id,str) or not 1<=len(bill_id)<=100:raise ValueError('Provide a bill ID')


def get_receipt(store,identity):
    initialize(store)
    row=store.db.execute('SELECT body FROM prospective_receipts WHERE id=?',(identity,)).fetchone()
    if not row:raise ValueError('Prospective receipt not found')
    return json.loads(row[0])


def list_receipts(store,dataset=None,bill_id=None,limit=100):
    initialize(store)
    if dataset is not None and dataset not in ('official','demo'):raise ValueError('Choose official or demo data')
    if bill_id is not None and (not isinstance(bill_id,str) or not 1<=len(bill_id)<=100):raise ValueError('Provide a bill ID')
    if type(limit) is not int or not 1<=limit<=500:raise ValueError('limit must be 1–500')
    clauses=[];args=[]
    for key,value in [('dataset',dataset),('bill_id',bill_id)]:
        if value is not None:clauses.append(key+'=?');args.append(value)
    query='SELECT body FROM prospective_receipts'+(' WHERE '+' AND '.join(clauses) if clauses else '')+' ORDER BY issued_at DESC,rowid DESC LIMIT ?'
    return [json.loads(r[0]) for r in store.db.execute(query,args+[limit])]


def capture(store,dataset,bill_id):
    _validate(dataset,bill_id);initialize(store)
    cutoff=now();snap=model.snapshot(store,dataset,bill_id,cutoff)
    outcome=model.resolution(store,dataset,bill_id,cutoff)
    code={name:digest(Path(__file__).with_name(name).read_text()) for name in ('model.py','store.py','prospective.py')}
    eligible=bool(snap and snap['stage']<4 and not outcome and cutoff<congress_end(snap['bill']['congress']))
    if not snap:
        status='unavailable';reason='No bill metadata demonstrably available at the capture time.'
        forecast=dict(status='unavailable',reason=reason)
    elif not eligible:
        status='ineligible';reason='The bill is already resolved or its Congress has ended. This capture is not a prospective prediction.'
        forecast=dict(status='unavailable',reason=reason)
    else:
        forecast=model.forecast(store,dataset,bill_id,cutoff,persist=False)
        status='captured' if forecast['status']=='available' else 'unavailable'
        reason=forecast.get('reason')
    selected={bill_id}|{r['bill_id'] for r in forecast.get('training_manifest',[])}
    sources=[dict(row) for row in store.db.execute('SELECT * FROM records WHERE dataset=? AND available_at<=? AND effective_at<=? ORDER BY id',(dataset,cutoff,cutoff)) if row['bill_id'] in selected]
    # Source hashes and numerical features are stable across repeated refreshes. The
    # exact cutoff is preserved in the receipt but does not manufacture new evidence.
    basis=dict(dataset=dataset,bill_id=bill_id,source_hash=digest(sources),features=snap['features'] if snap else None,
               implementation_hashes=code,status=status,reason=reason,outcome=outcome,
               forecast={k:forecast.get(k) for k in ('probability','baseline_probability','reference_probability','model_artifact','training_manifest','training_count','model_version','feature_version')})
    identity=digest(basis)
    existing=store.db.execute('SELECT body FROM prospective_receipts WHERE identity=?',(identity,)).fetchone()
    if existing:return dict(json.loads(existing[0]),reused=True)
    if eligible and forecast['status']=='available':forecast=model.forecast(store,dataset,bill_id,cutoff,persist=True)
    receipt=dict(id=identity,identity=identity,issued_at=now(),cutoff=cutoff,dataset=dataset,bill_id=bill_id,status=status,
                 prospective_eligible=eligible and dataset=='official',synthetic=dataset=='demo',reason=reason,input_snapshot=snap,
                 source_records=sources,source_hash=basis['source_hash'],forecast=forecast,forecast_hash=digest(forecast),
                 implementation_hashes=code,outcome_at_issue=outcome,release_eligible=False,
                 interpretation='Recorded by this local application at issuance, not independently timestamp-attested. No accuracy claim or calibrated interval. Synthetic data is not prospective real-world evidence.')
    with store.db:
        store.db.execute('INSERT OR IGNORE INTO prospective_receipts VALUES (?,?,?,?,?,?)',(receipt['id'],identity,dataset,bill_id,receipt['issued_at'],json.dumps(receipt)))
    return get_receipt(store,identity)
