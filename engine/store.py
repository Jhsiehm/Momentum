import hashlib
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def now():
    return datetime.now(timezone.utc).isoformat(timespec='seconds').replace('+00:00', 'Z')

def timestamp(value):
    if len(value) == 10:
        value += 'T23:59:59Z'
    parsed = datetime.fromisoformat(value.replace('Z', '+00:00'))
    if parsed.tzinfo is None:
        raise ValueError('Timestamp must include a timezone')
    return parsed.astimezone(timezone.utc).isoformat(timespec='seconds').replace('+00:00', 'Z')

def digest(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(',', ':')).encode()).hexdigest()

def congress_end(congress):
    return f'{1789 + 2 * congress:04d}-01-03T17:00:00Z'

def available(record):
    verified = record.get('verified_available_at')
    if verified and not record.get('archive_proof'):
        raise ValueError('Verified availability needs archive provenance')
    return timestamp(verified or record['observed_at'])

SCHEMA = '''
PRAGMA journal_mode=WAL;
CREATE TABLE IF NOT EXISTS records (
 id TEXT PRIMARY KEY, kind TEXT NOT NULL, bill_id TEXT NOT NULL,
 dataset TEXT NOT NULL, available_at TEXT NOT NULL, effective_at TEXT NOT NULL,
 body TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS records_lookup ON records(dataset,bill_id,kind,available_at);
CREATE TABLE IF NOT EXISTS forecasts (
 id TEXT PRIMARY KEY, bill_id TEXT NOT NULL, dataset TEXT NOT NULL,
 cutoff TEXT NOT NULL, model_version TEXT NOT NULL, issued_at TEXT NOT NULL,
 body TEXT NOT NULL, UNIQUE(bill_id,dataset,cutoff,model_version)
);
CREATE TRIGGER IF NOT EXISTS forecasts_no_update BEFORE UPDATE ON forecasts BEGIN SELECT RAISE(ABORT,'Forecasts are immutable'); END;
CREATE TRIGGER IF NOT EXISTS forecasts_no_delete BEFORE DELETE ON forecasts BEGIN SELECT RAISE(ABORT,'Forecasts are immutable'); END;
CREATE TRIGGER IF NOT EXISTS records_no_update BEFORE UPDATE ON records BEGIN SELECT RAISE(ABORT,'Evidence is append-only'); END;
CREATE TRIGGER IF NOT EXISTS records_no_delete BEFORE DELETE ON records BEGIN SELECT RAISE(ABORT,'Evidence is append-only'); END;
CREATE TABLE IF NOT EXISTS watchlist (dataset TEXT, bill_id TEXT, PRIMARY KEY(dataset,bill_id));
CREATE TABLE IF NOT EXISTS ai_runs (id TEXT PRIMARY KEY, created_at TEXT, body TEXT);
CREATE TABLE IF NOT EXISTS checkpoints (name TEXT PRIMARY KEY, body TEXT);
'''

class Store:
    def __init__(self, path=None):
        self.path = Path(path or ROOT / 'data' / 'engine.sqlite')
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.db = sqlite3.connect(str(self.path), timeout=30)
        self.db.row_factory = sqlite3.Row
        self.db.executescript(SCHEMA)

    def close(self):
        self.db.close()

    def add(self, kind, record):
        record = dict(record)
        if kind not in ('bill', 'event', 'resolution') or record.get('dataset') not in ('demo', 'official'):
            raise ValueError('Unsupported record kind or dataset')
        for field in ('bill_id', 'family_id', 'source_url', 'source_name', 'effective_at', 'observed_at'):
            if field not in record:
                raise ValueError('Missing field: ' + field)
        if kind == 'event' and (not isinstance(record.get('stage'), int) or record['stage'] not in range(5)):
            raise ValueError('Event stage must be an integer from 0 to 4')
        if kind == 'bill' and (record.get('type') not in ('hr', 's') or not isinstance(record.get('congress'), int)):
            raise ValueError('Bill requires valid type and Congress')
        if kind == 'resolution':
            if record.get('value') not in (0, 1):
                raise ValueError('Resolution value must be binary')
            if record['value'] == 0 and not record.get('complete_coverage'):
                raise ValueError('Negative resolution requires adjudicated complete coverage')
            bill = self.bill(record['dataset'], record['bill_id'])
            if record['value'] == 0 and bill and timestamp(record['effective_at']) < congress_end(bill['congress']):
                raise ValueError('Non-enactment cannot resolve before Congress end')
        record['effective_at'] = timestamp(record['effective_at'])
        record['observed_at'] = timestamp(record['observed_at'])
        known = available(record)
        if record.get('published_at'):
            record['published_at'] = timestamp(record['published_at'])
            if known < record['published_at']:
                raise ValueError('Availability cannot precede publication')
        record['id'] = digest({k: v for k, v in record.items() if k != 'id'})
        with self.db:
            self.db.execute('INSERT OR IGNORE INTO records VALUES (?,?,?,?,?,?,?)',
                            (record['id'], kind, record['bill_id'], record['dataset'], known,
                             record['effective_at'], json.dumps(record, sort_keys=True)))
        return record['id']

    def records(self, kind, dataset, bill_id=None, cutoff=None):
        query = 'SELECT body FROM records WHERE kind=? AND dataset=?'
        args = [kind, dataset]
        if bill_id:
            query += ' AND bill_id=?'
            args.append(bill_id)
        if cutoff:
            cutoff = timestamp(cutoff)
            query += ' AND available_at<=? AND effective_at<=?'
            args += [cutoff, cutoff]
        query += ' ORDER BY available_at,effective_at,id'
        rows = [json.loads(row[0]) for row in self.db.execute(query, args)]
        latest = {}
        for row in rows:
            latest[row.get('source_key', row['id'])] = row
        return list(latest.values())

    def bills(self, dataset, cutoff=None):
        latest = {}
        for row in self.records('bill', dataset, cutoff=cutoff):
            latest[row['bill_id']] = row
        return sorted(latest.values(), key=lambda b: (b['congress'], b['bill_id']), reverse=True)

    def bill(self, dataset, bill_id, cutoff=None):
        rows = self.records('bill', dataset, bill_id, cutoff)
        return rows[-1] if rows else None

    def saved(self, dataset, bill_id, cutoff, model_version):
        row = self.db.execute('SELECT body FROM forecasts WHERE dataset=? AND bill_id=? AND cutoff=? AND model_version=?',
                              (dataset, bill_id, timestamp(cutoff), model_version)).fetchone()
        return json.loads(row[0]) if row else None

    def save(self, record):
        with self.db:
            self.db.execute('INSERT OR IGNORE INTO forecasts VALUES (?,?,?,?,?,?,?)',
                            (record['id'], record['bill_id'], record['dataset'], record['cutoff'],
                             record['model_version'], record['issued_at'], json.dumps(record, sort_keys=True)))
        return self.saved(record['dataset'], record['bill_id'], record['cutoff'], record['model_version'])

    def ledger(self, dataset):
        return [json.loads(r[0]) for r in self.db.execute('SELECT body FROM forecasts WHERE dataset=? ORDER BY issued_at', (dataset,))]

    def checkpoint(self, name, value=None):
        if value is not None:
            with self.db:
                self.db.execute('INSERT OR REPLACE INTO checkpoints VALUES (?,?)', (name, json.dumps(value)))
        row = self.db.execute('SELECT body FROM checkpoints WHERE name=?', (name,)).fetchone()
        return json.loads(row[0]) if row else None

    def watch(self, dataset, bill_id, enabled):
        with self.db:
            if enabled:
                self.db.execute('INSERT OR IGNORE INTO watchlist VALUES (?,?)', (dataset, bill_id))
            else:
                self.db.execute('DELETE FROM watchlist WHERE dataset=? AND bill_id=?', (dataset, bill_id))

    def watched(self, dataset):
        return [row[0] for row in self.db.execute('SELECT bill_id FROM watchlist WHERE dataset=?', (dataset,))]
