"""Bounded historical calendar label evidence across Congresses; no scoring."""
import hashlib,io,json
from pathlib import Path
import pypdf
from engine import cohort,sample_publication_v2 as pub
from engine.earlier_labels import parse_calendar
from engine.label_investigation import law_identity
from engine.survivor_batch import save
from engine.store import ROOT,digest
D=ROOT/'data/research-runs/cross-congress-labels-20261105'
P=ROOT/'data/research-runs/cross-congress-20261105'


def run():
 sources=pub.Sources(D);proofs={};failures=[]
 for c in range(113,118):
  try:
   laws=json.loads((P/f'laws-{c}.json').read_text())['laws'];package=f'CCAL-{c}hcal-S2'
   mods,proof=cohort.package_audit(sources,package)
   title=mods.findtext('m:titleInfo/m:title',namespaces=cohort.M)
   assert title==f'House Calendars, Final - {c}th Congress, 2nd Session'
   assert any(e.findtext('m:edition',namespaces=cohort.M)=='FINAL' and e.findtext('m:congress',namespaces=cohort.M)==str(c) for e in mods.findall('m:extension',cohort.M))
   urls=[u.text for item in mods.findall('m:relatedItem',cohort.M) if 'PUBLIC LAWS' in [x.text for x in item.findall('m:titleInfo/m:partName',cohort.M)] for u in item.findall('.//m:url',cohort.M) if u.get('displayLabel')=='PDF rendition']
   assert len(urls)==1
   raw,receipt=sources.get(urls[0]);reader=pypdf.PdfReader(io.BytesIO(raw));text='\n'.join(page.extract_text(extraction_mode='layout') for page in reader.pages)
   rows=parse_calendar(text,c,len(laws))
   corrections=[]
   mapped={r['law']:r['bill_id'] for r in rows}
   for law in laws:
    if mapped[law['law']]!=law['bill_id']:
     lm,lp=cohort.package_audit(sources,f"PLAW-{c}publ{law['law']}")
     actual=law_identity(lm,c,law['law'])
     assert actual['bill_id']==mapped[law['law']] and actual['enacted']==law['enacted'],'Unresolved official disagreement'
     corrections.append(dict(original=law,corrected=actual,proof=lp))
   proofs[str(c)]=dict(congress=c,complete_laws=len(rows),available_at=proof['available_at'],publication=proof,source=receipt,rows=rows,corrections=corrections,extraction=dict(tool='pypdf',version=pypdf.__version__,text_hash=hashlib.sha256(text.encode()).hexdigest(),pages=len(reader.pages)))
   print(c,'verified',len(rows),proof['available_at'],flush=True)
  except Exception as e:failures.append(dict(congress=c,error=str(e)));print(c,'BLOCKED',str(e),flush=True)
 report=dict(proofs=proofs,failures=failures,sources=sources.manifest(),human_certified=False,release_eligible=False,limitations='Bounded publication preservation proxies; complete census proves binary mapping, individual law publication still required for date-boundary positives.')
 report['hash']=digest(report);save(D,'calendar-evidence-v2.json',report)
 return report

if __name__=='__main__':run()
