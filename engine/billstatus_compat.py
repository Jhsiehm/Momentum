"""Explicit legacy BILLSTATUS identifier aliases; original source bytes retained."""
import hashlib
import xml.etree.ElementTree as ET
from .sample_publication_v2 import Sources


def normalize(raw):
 if b'<!DOCTYPE' in raw.upper() or b'<!ENTITY' in raw.upper():raise ValueError('DTD/entity declarations rejected')
 root=ET.fromstring(raw);bill=root.find('bill')
 if bill is None:raise ValueError('Missing bill')
 changes=[]
 for node in [bill]+bill.findall('relatedBills/item'):
  for current,legacy in [('type','billType'),('number','billNumber')]:
   a,b=node.findtext(current),node.findtext(legacy)
   if a and b and a.lower()!=b.lower():raise ValueError('Conflicting BILLSTATUS identifier aliases')
   if not a and b:
    existing=node.find(current)
    if existing is None:existing=ET.SubElement(node,current)
    existing.text=b;changes.append(dict(from_field=legacy,to_field=current,value=b))
 if not changes:return raw,None
 converted=ET.tostring(root,encoding='utf-8')
 return converted,dict(adapter='identifier-aliases-v1',changes=changes,original_sha256=hashlib.sha256(raw).hexdigest(),parsed_sha256=hashlib.sha256(converted).hexdigest())


class AuditedSources(Sources):
 def get(self,url):
  raw,record=super().get(url)
  if '/bulkdata/BILLSTATUS/' not in url or not url.endswith('.xml'):return raw,record
  converted,transformation=normalize(raw)
  return converted,dict(record,transformation=transformation) if transformation else record
