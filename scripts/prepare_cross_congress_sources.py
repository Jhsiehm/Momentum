"""Discover official inventories and reconstruct complete law lists for the audit."""
import argparse,json
from pathlib import Path
from engine import cohort,sampling,sample_publication_v2 as pub
from engine.store import Store
from engine.cross_congress import DIRECTORY
from engine.survivor_batch import save
COUNTS={113:296,114:329,115:442,116:344,117:362}
NORMALIZATION='Replace /P.L. header abbreviation with / Public Law before existing parser; raw sources unchanged'


def parse_final(raw,congress):
 return cohort.parse_law_list(raw.replace(b'/P.L.',b'/ Public Law '),congress)


def prepare(directory=DIRECTORY,offline=False):
 directory=Path(directory);directory.mkdir(exist_ok=True)
 if not (directory/'inventory.json').exists():
  if offline:raise ValueError('Missing frozen inventory')
  store=Store()
  try:inventory=sampling.discover_inventory(store,dict(congresses=list(range(113,119))))
  finally:store.close()
  save(directory,'inventory.json',inventory)
 sources=pub.Sources(directory,offline)
 for c,n in COUNTS.items():
  if c in (113,115):
   rows=[];proofs=[]
   for session in ('first','second'):
    url='https://www.archives.gov/files/federal-register/laws/'+('past/' if c==113 else '')+f'{c}-{session}-session.txt'
    raw,proof=sources.get(url);rows+=parse_final(raw,c);proofs.append(proof)
   value=dict(laws=rows,proofs=proofs,normalization=NORMALIZATION)
  else:
   rows,proofs=pub.law_census(sources,c,n);value=dict(laws=rows,proofs=proofs)
  assert len(rows)==n and {r['law'] for r in rows}==set(range(1,n+1)) and len({r['bill_id'] for r in rows})==n
  save(directory,f'laws-{c}.json',value)
 print('All five complete law lists reconstructed exactly')

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--offline',action='store_true');a=p.parse_args();prepare(offline=a.offline)
