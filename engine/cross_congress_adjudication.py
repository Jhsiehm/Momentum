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


def legislative_day_validator(sources,mods,package,introduced_at):
 """Corroborate both legislative/calendar dates in the official bill header."""
 from datetime import datetime
 from .publication_identity import validate_introduction
 from html import unescape
 raw,receipt=sources.get(f'https://www.govinfo.gov/content/pkg/{package}/html/{package}.htm')
 text=unescape(re.sub('<[^>]+>',' ',raw.decode('utf-8')))
 match=re.fullmatch(r'BILLS-(\d+)(hr|s)(\d+)(ih|is)',package)
 assert match
 c,kind,number,version=match.groups()
 assert f'{c}th Congress' in text
 expected=f"[{'H.R.' if kind=='hr' else 'S.'} {number} Introduced in {'House (IH)' if kind=='hr' else 'Senate (IS)'}]"
 assert expected in text,'Header bill identity mismatch'
 header=text.split('A BILL')[0]
 matches=re.findall(r'([A-Za-z]+)\s+(\d{1,2})\s*\(legislative day,\s*([A-Za-z]+)\s+(\d{1,2})\),\s*(\d{4})',header)
 assert len(matches)==1,'Missing/ambiguous explicit legislative-day header'
 month,day,lmonth,lday,year=matches[0]
 calendar=datetime.strptime(f'{month} {day} {year}','%B %d %Y').date().isoformat()
 legislative=datetime.strptime(f'{lmonth} {lday} {year}','%B %d %Y').date().isoformat()
 assert legislative==str(introduced_at)[:10],'BILLSTATUS does not match explicit legislative day'
 proof=validate_introduction(mods,package,calendar)
 proof.update(rule='explicit-legislative-day-header-v1',introduced_at=legislative,calendar_introduction_at=calendar,header_source=receipt,basis='Official introduced bill header explicitly corroborates BILLSTATUS legislative date and MODS calendar action date; checkpoint retains original BILLSTATUS date convention.')
 return proof


def sample_legislative_day(sources,congress,kind,number,spec,labels):
 from .sample_publication_v2 import sample_bill
 return sample_bill(sources,congress,kind,number,spec,labels,introduction_validator=lambda mods,package,intro:legislative_day_validator(sources,mods,package,intro))
