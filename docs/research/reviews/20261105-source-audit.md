# Retained-source provenance audit — 2026-11-05

Status: automated retained-evidence checks passed for this bounded sample; historical source certification remains pending. This is an agent audit, not a human sign-off, independent validation result, or release approval.

## Scope and selection

Read repository AGENTS.md, paper protocol sections 3 and 10, readiness documentation, acquisition/parser code and frozen artifacts. Selected the first 12 of 11,871 final-training rows ordered by `(engine.store.digest(bill_id), bill_id)`. This digest hashes canonical JSON, including the string quotation marks; it is not raw UTF-8 bill-ID SHA-256. Selection uses no outcomes, features, model probabilities or performance. An initial exploratory ID listing used raw UTF-8 hashes; no provenance checks were made on that set, and it was replaced by this coordinated canonical-digest rule before the audit. No fitting, predictions, outcome scoring, downloads or frozen-data writes occurred. Reading the training JSON necessarily loads existing labels, but neither the selection nor the checks consult them.

Input: `data/research-runs/cross-congress-scale-20261105/final-training.json`.

- Raw training SHA-256: `5f3027cabbf1da78602bfbb67392cf7d7efe1a3a3f1d40067a59cc4ef4dd63eb`.
- Canonical training hash: `efa358303c3e2780acfa7d5a47ea23aaa751591aa291ac08879d280a7523ee9f`; equals candidate lock's training hash.
- Candidate lock canonical hash: `149b5f618cd74bcc1974cd502581490e8e8cb3c390baf25b9279e213bb35c0c5`; internal digest verified.

## Actual checks and results

Verified **40 unique raw files, totaling 4,376,740 bytes**: 12 BILLSTATUS XML files plus MODS/PREMIS for 14 bill-publication versions. Each raw file matched its row receipt SHA-256 and byte count; the cache sidecar matched URL, retrieval timestamp, checksum and length. All source URLs use the retained official `https://www.govinfo.gov/` origin. This verifies the recorded source identity, not a new network authentication.

Independently parsed BILLSTATUS identity (including legacy type/number aliases) and introduction date; MODS package identity, issued/ingested dates and explicit introduction actions; earliest successful Ingestion, ACP Creation and Parsing events from PREMIS. Converted offset event timestamps to UTC before comparing stored events and recomputing the end-of-day maximum plus one day availability bound. All 14 replayed bounds and all 12 eligible-package sets matched. All 12 introduction validation records still explicitly have `human_audit_satisfied=false`.

An initial audit-script assertion compared offset timestamp strings directly with UTC strings and failed. After normalizing equivalent timestamps to UTC, the complete check passed. This was an audit-script correction; frozen evidence and parser code were not changed.

| Bill ID | Versions | Latest retained version availability (UTC) | Checkpoint (UTC) | Raw files |
|---|---:|---|---|---:|
| 113-hr4401 | 1 | 2014-04-09T23:59:59Z | 2014-10-01T23:59:59Z | 3 |
| 117-hr6116 | 1 | 2021-12-12T23:59:59Z | 2022-05-30T23:59:59Z | 3 |
| 116-s4142 | 1 | 2020-07-17T23:59:59Z | 2020-12-28T23:59:59Z | 3 |
| 114-s1259 | 1 | 2015-05-21T23:59:59Z | 2015-11-03T23:59:59Z | 3 |
| 113-s1772 | 1 | 2013-12-04T23:59:59Z | 2014-05-20T23:59:59Z | 3 |
| 115-hr4885 | 1 | 2018-01-28T23:59:59Z | 2018-07-24T23:59:59Z | 3 |
| 115-hr4920 | 1 | 2018-02-04T23:59:59Z | 2018-08-01T23:59:59Z | 3 |
| 116-hr2943 | 3 | 2019-07-26T23:59:59Z | 2019-11-19T23:59:59Z | 7 |
| 114-s375 | 1 | 2015-02-20T23:59:59Z | 2015-08-03T23:59:59Z | 3 |
| 117-hr1662 | 1 | 2021-05-07T23:59:59Z | 2021-09-04T23:59:59Z | 3 |
| 114-hr3803 | 1 | 2015-10-25T23:59:59Z | 2016-04-19T23:59:59Z | 3 |
| 116-hr846 | 1 | 2019-02-14T23:59:59Z | 2019-07-28T23:59:59Z | 3 |

## Unresolved provenance blockers

1. All checked retrieval timestamps fall between `2026-11-05T21:35:05Z` and `2026-11-05T22:17:37Z`, years after the historical checkpoints. Matching today's retained bytes to today's recorded checksum does not prove that rendition was available unchanged at the historical checkpoint. Package preservation metadata supports the adopted availability bound but is not byte-identical archived rendition evidence.
2. The sampled receipt fields contain URL, retrieval time, byte length and SHA-256 but no `parser_version`. Parser and implementation snapshots exist elsewhere in the run; this audit did not establish an explicit source-to-parser-version link for each receipt. Paper protocol section 3 requires parser identification. Add a reviewed association in a new evidence packet, preserving original receipts.
3. This audit checks XML metadata, not bill PDF/text rendition content, title/relationship semantics, exhaustive inventory completeness, final law calendars, slip-law dates or outcome custody. It does not certify the completeness or correctness of source availability beyond the 12 retained rows. No conclusion about unseen training rows or evaluation eligibility follows.
4. Explicit human/action-history review remains outstanding, including interpretation of preservation events and retrospective contamination. Hash replay cannot supply that review. Family adjudication is a separate gate and is not resolved here.
5. Evidence is ignored runtime data. A fresh clone cannot rerun these checks without the retained acquisition bundle. Publication still needs an appropriately licensed bundle or reproducible acquisition recipe with historical-availability limitations.

## Packet recommendation

Export only outcome-free reviewer fields: selection rule and exact hashes, frozen parent hashes, bill ID/checkpoint, each package/version and claimed availability basis, original source receipt, resolved raw-file path, recomputed checksum/length, parser association, independent replay result and reviewer-question list. Keep `human_audit_satisfied=false`, `source_review_status=pending` and `release_eligible=false`; do not manufacture reviewer identity or certify readiness. Include all available versions so an excluded post-checkpoint version cannot silently disappear. Keep raw evidence under ignored `data/` and commit only suitable summaries/manifests.

Raw cache resolution: for each receipt, compute `sha256(url.encode("utf-8")).hexdigest()` and locate `<hash>.raw` plus `<hash>.json` under `data/research-runs/cross-congress-scale-20261105/sources/` or `data/research-runs/cross-congress-reserve-20261105/sources/`. Require actual raw checksum/length and sidecar metadata to match the frozen receipt; do not assume the first filename match is valid. Both roots were needed for this sample.

## Reproduction

Run the following Python from the repository root in an environment with the retained runtime evidence. It only reads existing evidence and prints its audit summary. No acquisition or model-scoring helper is called.

```python
import hashlib,json,re
from pathlib import Path
from datetime import date,timedelta,datetime,timezone
import xml.etree.ElementTree as ET
from engine.store import digest
base=Path('data/research-runs')
directory=base/'cross-congress-scale-20261105'
paths=[directory/'sources',base/'cross-congress-reserve-20261105/sources']
raw_training=(directory/'final-training.json').read_bytes()
training=json.loads(raw_training)
rows=sorted(training,key=lambda r:(digest(r['bill_id']),r['bill_id']))[:12]
lock=json.loads((base/'convergence-einsum-20261105/candidate-lock.json').read_text())
assert digest(training)==lock['training_hash']
assert digest({k:v for k,v in lock.items() if k!='hash'})==lock['hash']
checked={};resolved={};results=[]
def source(s):
 key=hashlib.sha256(s['url'].encode()).hexdigest()
 candidates=[p/(key+'.raw') for p in paths if (p/(key+'.raw')).exists()]
 assert candidates,s['url']
 valid=[]
 for p in candidates:
  raw=p.read_bytes()
  if hashlib.sha256(raw).hexdigest()==s['sha256'] and len(raw)==s['bytes']:valid.append((p,raw))
 assert valid,s['url']
 p,raw=valid[0];meta=json.loads(p.with_suffix('.json').read_text())
 assert all(meta[k]==s[k] for k in ('url','bytes','sha256','retrieved_at'))
 assert s['url'].startswith('https://www.govinfo.gov/')
 assert s['retrieved_at'] and 'parser_version' not in s
 checked[s['url']]=s;resolved[s['url']]=str(p)
 assert b'<!ENTITY' not in raw.upper()
 return ET.fromstring(raw)
for r in rows:
 b=source(r['source']).find('bill')
 kind=b.findtext('type') or b.findtext('billType');number=b.findtext('number') or b.findtext('billNumber')
 assert f"{b.findtext('congress')}-{kind.lower()}{int(number)}"==r['bill_id']
 assert b.findtext('introducedDate')==r['introduced_at'][:10]
 packages=[]
 for v in r['versions']:
  m,p=[source(s) for s in v['sources']]
  assert m.findtext('{*}recordInfo/{*}recordIdentifier')==v['package']
  issued=m.findtext('{*}originInfo/{*}dateIssued');ingested=m.findtext('{*}extension/{*}dateIngested')
  events={}
  for e in p.findall('{*}event'):
   kind=e.findtext('{*}eventType');success=e.findtext('{*}eventOutcomeInformation/{*}eventOutcome')
   if kind in ('Ingestion','ACP Creation','Parsing') and success=='Success':
    t=datetime.fromisoformat(e.findtext('{*}eventDateTime').replace('Z','+00:00')).astimezone(timezone.utc).isoformat().replace('+00:00','Z');events[kind]=min(events.get(kind,t),t)
  assert len(events)==3
  bound=(date.fromisoformat(max([issued[:10],ingested[:10]]+[t[:10] for t in events.values()]))+timedelta(days=1)).isoformat()+'T23:59:59Z'
  assert bound==v['available_at'] and issued==v['issued_at'][:10]
  assert ingested==v['ingested_date']
  assert {k:t.replace('+00:00','Z') for k,t in events.items()}==v['preservation_events'], (v['package'],events,v['preservation_events'])
  if v['version'] in ('ih','is'):
   actions=[a for a in m.findall('{*}extension/{*}action') if re.search(r'\bintroduced\s+the\s+following\s+bill\b',' '.join(a.itertext()),re.I)]
   assert actions and all(a.get('date')==r['introduced_at'][:10] for a in actions)
   assert v['introduction_validation']['human_audit_satisfied'] is False
  if bound<=r['cutoff'] and v['issued_at']<=r['cutoff']:packages.append(v['package'])
 assert set(packages)==set(r['eligible_packages'])
 results.append(dict(bill_id=r['bill_id'],selection_hash=digest(r['bill_id']),cutoff=r['cutoff'],versions=len(r['versions']),latest_available=max(v['available_at'] for v in r['versions']),source_checks=1+2*len(r['versions'])))
print(json.dumps(dict(training_raw_sha256=hashlib.sha256(raw_training).hexdigest(),training_canonical_hash=digest(training),candidate_hash=lock['hash'],rows=results,unique_sources=len(checked),total_bytes=sum(s['bytes'] for s in checked.values()),retrieval_min=min(s['retrieved_at'] for s in checked.values()),retrieval_max=max(s['retrieved_at'] for s in checked.values()),source_roots=sorted({str(Path(p).parent) for p in resolved.values()})),indent=2))
```
