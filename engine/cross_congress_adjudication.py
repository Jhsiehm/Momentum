"""Explicit evidence-conflict disposition; never invents an introduction date."""
import re
from datetime import date,timedelta
from . import cohort
from .store import congress_end


def late_introduction_conflict(sources,bid):
 match=re.fullmatch(r'(\d+)-(hr|s)(\d+)',bid)
 if not match:raise ValueError('Invalid bill identity')
 c,kind,number=int(match[1]),match[2],int(match[3])
 url=f'https://www.govinfo.gov/bulkdata/BILLSTATUS/{c}/{kind}/BILLSTATUS-{c}{kind}{number}.xml'
 raw,source=sources.get(url);bill=cohort.xml(raw).find('bill')
 assert int(bill.findtext('congress'))==c and bill.findtext('type').lower()==kind and int(bill.findtext('number'))==number
 package=f'BILLS-{c}{kind}{number}'+('ih' if kind=='hr' else 'is')
 mods,proof=cohort.package_audit(sources,package)
 assert mods.findtext('m:recordInfo/m:recordIdentifier',namespaces=cohort.M)==package
 actions=[a.get('date') for a in mods.findall('m:extension/m:action',cohort.M) if re.search(r'\bintroduced\s+the\s+following\s+bill\b',' '.join(a.itertext()),re.I)]
 assert actions,'Missing explicit introduction actions'
 dates=[bill.findtext('introducedDate')]+actions
 assert len(set(dates))>1,'No introduction-date disagreement'
 cutoffs=[(date.fromisoformat(d)+timedelta(days=180)).isoformat() for d in dates]
 assert all(d>=congress_end(c)[:10] for d in cutoffs),'Disagreement could change checkpoint eligibility; block'
 row=cohort.excluded_slot(bid,c,kind,'Checkpoint after Congress end under every conflicting official introduction date',source,bill.findtext('title'))
 row['versions']=[proof]
 row['related']=[f"{x.findtext('congress')}-{x.findtext('type').lower()}{int(x.findtext('number'))}" for x in bill.findall('relatedBills/item') if x.findtext('congress') and x.findtext('type') and x.findtext('number')]
 row['adjudication']=dict(rule='late-under-all-official-dates-v1',official_dates=dates,possible_cutoffs=cutoffs,explanation='Date conflict remains unresolved. Every official candidate date makes day180 later than Congress end; exclude without selecting a date or reading outcome.',human_certified=False)
 return row


def missing_introduction_action(sources,bid):
 """Quarantine a complete source with missing mandatory introduction evidence."""
 match=re.fullmatch(r'(\d+)-(hr|s)(\d+)',bid)
 if not match:raise ValueError('Invalid bill identity')
 c,kind,number=int(match[1]),match[2],int(match[3])
 url=f'https://www.govinfo.gov/bulkdata/BILLSTATUS/{c}/{kind}/BILLSTATUS-{c}{kind}{number}.xml'
 raw,source=sources.get(url);bill=cohort.xml(raw).find('bill')
 assert int(bill.findtext('congress'))==c and bill.findtext('type').lower()==kind and int(bill.findtext('number'))==number
 package=f'BILLS-{c}{kind}{number}'+('ih' if kind=='hr' else 'is')
 mods,proof=cohort.package_audit(sources,package)
 assert mods.findtext('m:recordInfo/m:recordIdentifier',namespaces=cohort.M)==package
 actions=[a for a in mods.findall('m:extension/m:action',cohort.M) if re.search(r'\bintroduced\s+the\s+following\s+bill\b',' '.join(a.itertext()),re.I)]
 assert not actions,'Mandatory introduction action exists; do not quarantine under this rule'
 row=cohort.excluded_slot(bid,c,kind,'Quarantined: missing mandatory historical introduction-date evidence',source,bill.findtext('title'))
 row['versions']=[proof]
 row['related']=[f"{x.findtext('congress')}-{x.findtext('type').lower()}{int(x.findtext('number'))}" for x in bill.findall('relatedBills/item') if x.findtext('congress') and x.findtext('type') and x.findtext('number')]
 row['adjudication']=dict(rule='missing-introduction-action-quarantine-v1',reason='Required independent introduction-date evidence is absent. No features/outcome assigned; not eligible for training or scoring.',resolved=False,human_certified=False)
 return row
