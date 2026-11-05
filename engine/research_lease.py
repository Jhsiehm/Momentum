"""Cross-process lease for scheduled research agents, separate from model code."""
import argparse
import json
import time
from .store import Store


def lease(store, action, owner, ttl=1800):
    if action not in ('acquire', 'renew', 'release', 'status'):
        raise ValueError('Unknown lease action')
    if not isinstance(owner,str) or not owner.strip() or len(owner)>200:
        raise ValueError('A unique run owner is required')
    if type(ttl) is not int or not 60<=ttl<=3600:
        raise ValueError('Lease duration must be 60–3600 seconds')
    store.db.execute('CREATE TABLE IF NOT EXISTS research_run_lease (singleton INTEGER PRIMARY KEY CHECK(singleton=1), owner TEXT NOT NULL, expires REAL NOT NULL)')
    try:
        store.db.execute('BEGIN IMMEDIATE')
        row=store.db.execute('SELECT owner,expires FROM research_run_lease WHERE singleton=1').fetchone()
        current=time.time(); active=bool(row and row[1]>current)
        allowed=action=='acquire' and (not active or row[0]==owner) or action=='renew' and active and row[0]==owner
        if allowed:
            store.db.execute('INSERT OR REPLACE INTO research_run_lease VALUES (1,?,?)',(owner,current+ttl))
            row=(owner,current+ttl);active=True
        elif action=='release' and row and row[0]==owner:
            store.db.execute('DELETE FROM research_run_lease WHERE singleton=1');row=None;active=False;allowed=True
        result=dict(action=action,granted=bool(allowed),active=active,owner=row[0] if active else None,expires_at=row[1] if active else None)
        store.db.commit();return result
    except Exception:
        store.db.rollback();raise


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('action',choices=['acquire','renew','release','status']);p.add_argument('owner');p.add_argument('--ttl',type=int,default=1800)
    a=p.parse_args();s=Store()
    try:print(json.dumps(lease(s,a.action,a.owner,a.ttl)))
    finally:s.close()
