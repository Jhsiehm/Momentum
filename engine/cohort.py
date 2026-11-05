"""Fixed real-data pilot. Source audit and scoring are separate, replay is offline.

Uses publication-version features, not the general action-based engine model.
Never backdates the currently fetched BILLSTATUS snapshots.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import timedelta, datetime
import hashlib
from html.parser import HTMLParser
import json
import math
from pathlib import Path
import random
import re
import uuid
import xml.etree.ElementTree as ET

from .ingest import fetch
from .model import date, fit, predict, score
from .store import ROOT, Store, congress_end, digest, now, timestamp

SPEC = ROOT / 'docs/cohorts/pilot-v1.json'
DIRECTORY = ROOT / 'data/cohorts/historical-pilot-v1'
M = {'m': 'http://www.loc.gov/mods/v3'}
P = {'p': 'info:lc/xmlns/premis-v2'}
VERSION_STAGE = {'ih': 0, 'is': 0, 'rh': 1, 'rs': 1, 'eh': 2, 'es': 2, 'enr': 3}
LIMITATIONS = [
    'A low-numbered convenience cohort and one test Congress; not a representative or protected holdout.',
    'Publication metadata and successful preservation events support package availability; historical rendition byte identity and exact first public access were not independently proven.',
    'Document versions proxy procedural activity; these are not complete congressional action histories.',
    'Related-bill links and identical titles are a conservative automated family screen, not a complete human-adjudicated provision genealogy.',
    'Bootstrap intervals condition on this fitted model and test Congress; they omit training-sample and Congress-level uncertainty.',
    'No calibrated probability intervals, causal claim, model promotion or deployment validation.'
]


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')


def frozen_spec(directory=DIRECTORY):
    directory.mkdir(parents=True, exist_ok=True)
    value = json.loads(SPEC.read_text())
    path = directory / 'protocol.json'
    if path.exists():
        frozen = json.loads(path.read_text())
        if frozen['spec_hash'] != digest(value):
            raise ValueError('Frozen pilot specification differs; create a new protocol, do not overwrite this experiment.')
        return frozen
    frozen = {'registered_at': now(), 'spec': value, 'spec_hash': digest(value)}
    write_json(path, frozen)
    return frozen


class Sources:
    def __init__(self, directory=DIRECTORY, offline=False):
        self.directory, self.offline = directory / 'sources', offline
        self.directory.mkdir(parents=True, exist_ok=True)

    def get(self, url):
        key = hashlib.sha256(url.encode()).hexdigest()
        body, meta = self.directory / (key + '.raw'), self.directory / (key + '.json')
        if meta.exists() and body.exists():
            record = json.loads(meta.read_text()); raw = body.read_bytes()
            if record['sha256'] != hashlib.sha256(raw).hexdigest() or record['url'] != url:
                raise ValueError('Cached source checksum mismatch: ' + url)
            return raw, record
        if self.offline:
            raise ValueError('Missing frozen source: ' + url)
        raw = fetch(url)
        record = {'url': url, 'retrieved_at': now(), 'sha256': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw)}
        body.write_bytes(raw); write_json(meta, record)
        return raw, record

    def manifest(self):
        records = []
        for path in sorted(self.directory.glob('*.json')):
            meta = json.loads(path.read_text())
            self.get(meta['url'])  # Recompute every cached byte hash before scoring.
            records.append(meta)
        return sorted(records, key=lambda r: r['url'])


def xml(raw):
    if b'<!ENTITY' in raw.upper():
        raise ValueError('XML entities are not accepted')
    return ET.fromstring(raw)


def provenance(mods_raw, premis_raw, package):
    mods, premis = xml(mods_raw), xml(premis_raw)
    if mods.findtext('m:recordInfo/m:recordIdentifier', namespaces=M) != package:
        raise ValueError('MODS package identity mismatch')
    ingested = mods.findtext('m:extension/m:dateIngested', namespaces=M)
    issued = mods.findtext('m:originInfo/m:dateIssued', namespaces=M)
    if not ingested or not issued:
        raise ValueError('Missing issuance/ingestion date')
    events = {}
    for event in premis.findall('p:event', P):
        kind = event.findtext('p:eventType', namespaces=P)
        success = event.findtext('p:eventOutcomeInformation/p:eventOutcome', namespaces=P)
        if kind in ('Ingestion', 'ACP Creation', 'Parsing') and success == 'Success':
            when = timestamp(event.findtext('p:eventDateTime', namespaces=P))
            events[kind] = min(events.get(kind, when), when)
    if len(events) != 3:
        raise ValueError('Missing successful ingestion/access/parsing preservation events')
    # Date precision is never treated as a midnight release.
    latest = max([timestamp(ingested), timestamp(issued)] + [timestamp(v[:10]) for v in events.values()])
    available = (date(latest) + timedelta(days=1)).isoformat().replace('+00:00', 'Z')
    return {'package': package, 'issued_at': timestamp(issued), 'available_at': available,
            'ingested_date': ingested, 'preservation_events': events,
            'basis': 'Official package preservation metadata, plus one-day access margin; not byte-identical archived rendition proof'}


def package_audit(sources, package):
    base = 'https://www.govinfo.gov/metadata/pkg/' + package
    mods, mr = sources.get(base + '/mods.xml')
    premis, pr = sources.get(base + '/premis.xml')
    proof = provenance(mods, premis, package)
    proof['sources'] = [mr, pr]
    return xml(mods), proof


def parse_law_list(raw, congress):
    try: text = raw.decode('utf-8-sig')
    except UnicodeDecodeError: text = raw.decode('cp1252')
    text = text.replace('\r', '')
    if 'FINAL' not in text.upper():
        raise ValueError('Law list is not marked final')
    pattern = re.compile(r'(?m)^([A-Z][A-Za-z. ]*?)\s+(\d+)\s*/\s*Public Law\s+' + str(congress) + r'-(\d+)\s*\n')
    matches = list(pattern.finditer(text)); result = []
    for i, match in enumerate(matches):
        body = text[match.end(): matches[i + 1].start() if i + 1 < len(matches) else len(text)]
        when = re.search(r'(?:^|\n)\(?([A-Za-z]+)\.?\s+(\d{1,2}),\s+(\d{4});', body)
        if not when:
            raise ValueError('Missing law enactment date: ' + match.group(0))
        month = when.group(1)[:3].title()
        enacted = datetime.strptime(f'{month} {when.group(2)} {when.group(3)}', '%b %d %Y').date().isoformat()
        kind = re.sub('[^a-z]', '', match.group(1).lower())
        result.append({'law': int(match.group(3)), 'bill_id': f'{congress}-{kind}{int(match.group(2))}', 'enacted': enacted})
    if not result:
        raise ValueError('Could not parse complete law list')
    return result


class LawTable(HTMLParser):
    def __init__(self):
        super().__init__(); self.rows=[]; self.row=None; self.cell=None
    def handle_starttag(self, tag, attrs):
        if tag=='tr': self.row=[]
        if tag in ('td','th') and self.row is not None: self.cell=[]
    def handle_data(self, data):
        if self.cell is not None:self.cell.append(data)
    def handle_endtag(self, tag):
        if tag in ('td','th') and self.cell is not None:
            self.row.append(' '.join(''.join(self.cell).split()));self.cell=None
        if tag=='tr' and self.row is not None:self.rows.append(self.row);self.row=None


def parse_law_table(raw, congress):
    parser=LawTable();parser.feed(raw.decode('utf-8'));rows=[]
    for cells in parser.rows:
        if len(cells)<4 or not re.fullmatch(str(congress)+r'-\d+',cells[0]):continue
        bill=re.fullmatch(r'([A-Za-z. ]+)\s+(\d+)',cells[1])
        if not bill:raise ValueError('Unrecognized bill in NARA table')
        when=re.fullmatch(r'([A-Za-z]+)\.?\s+(\d+),\s*(\d{4})',cells[3])
        if not when:raise ValueError('Unrecognized NARA enactment date')
        enacted=datetime.strptime(f'{when[1][:3]} {when[2]} {when[3]}','%b %d %Y').date().isoformat()
        rows.append({'law':int(cells[0].split('-')[1]),'bill_id':f"{congress}-{re.sub('[^a-z]','',bill[1].lower())}{int(bill[2])}",'enacted':enacted})
    return rows


def law_census(sources, congress, expected):
    rows, proofs = [], []
    for session in ('first', 'second'):
        url = (f'https://www.archives.gov/files/federal-register/laws/{congress}-{session}-session.txt' if congress==114 else f'https://www.archives.gov/federal-register/laws/{congress}-{session}-session')
        raw, proof = sources.get(url)
        rows += (parse_law_list(raw, congress) if congress==114 else parse_law_table(raw, congress)); proofs.append(proof)
    if len(rows) != expected or {r['law'] for r in rows} != set(range(1, expected + 1)):
        raise ValueError(f'Incomplete/duplicate law census for {congress}: {len(rows)} entries')
    if len({r['bill_id'] for r in rows}) != len(rows):
        raise ValueError('Duplicate bill in law census')
    return rows, proofs


def training_census(sources, nara):
    statutes, proofs = {}, []
    for volume in (129, 130):
        mods, proof = package_audit(sources, f'STATUTE-{volume}')
        proofs.append(proof)
        for item in mods.findall('m:relatedItem', M):
            ext = item.find('m:extension', M)
            if ext is None or ext.findtext('m:granuleClass', namespaces=M) != 'PUBLICLAW':
                continue
            number = int(ext.findtext('m:number', namespaces=M))
            bills = [b for b in ext.findall('.//m:bill', M) if b.get('priority') == 'primary']
            if len(bills) != 1 or bills[0].get('congress') != '114':
                raise ValueError('Ambiguous Statutes primary bill linkage')
            b = bills[0]
            statutes[number] = {'law': number, 'bill_id': '114-' + b.get('type').lower() + b.get('number'),
                                'enacted': ext.findtext('m:granuleDate', namespaces=M)}
    if sorted(statutes.values(), key=lambda r:r['law']) != sorted(nara, key=lambda r:r['law']):
        raise ValueError('Statutes and National Archives law censuses disagree')
    return {'complete_laws': len(statutes), 'available_at': max(p['available_at'] for p in proofs), 'volumes': proofs}


def excluded_slot(identity, congress, kind, reason, source, title='No introduced publication'):
    return {'bill_id':identity,'congress':congress,'type':kind,'title':title,'related':[],
            'versions':[],'eligible_packages':[],'source':source,'exclusion':reason}


def sample_bill(sources, congress, kind, number, spec, labels, directories=None):
    identity = f'{congress}-{kind}{number}'
    if directories and number not in directories[(congress,kind)][0]:
        return excluded_slot(identity,congress,kind,'No BILLSTATUS entry in complete official chamber directory; no historical introduction audited',directories[(congress,kind)][1])
    raw, source = sources.get(f'https://www.govinfo.gov/bulkdata/BILLSTATUS/{congress}/{kind}/BILLSTATUS-{congress}{kind}{number}.xml')
    bill = xml(raw).find('bill')
    if bill is None or int(bill.findtext('congress')) != congress or bill.findtext('type').lower() != kind or int(bill.findtext('number')) != number:
        raise ValueError('BILLSTATUS identifier mismatch: ' + identity)
    intro = timestamp(bill.findtext('introducedDate'))
    cutoff = (date(intro) + timedelta(days=spec['age_days'])).isoformat().replace('+00:00', 'Z')
    law = labels.get(identity)
    reported = {int(x.findtext('number').split('-')[-1]) for x in bill.findall('laws/item') if x.findtext('type', '').lower() in ('public','public law')}
    expected = {law['law']} if law else set()
    if reported != expected:
        raise ValueError('BILLSTATUS / National Archives outcome mismatch: ' + identity)
    packages = set()
    for url in bill.findall('textVersions/item/formats/item/url'):
        match = re.search(r'/pkg/(BILLS-' + str(congress) + kind + str(number) + r'([a-z]+)\d*)/', url.text or '')
        if match and match.group(2) in VERSION_STAGE:
            packages.add((match.group(1), match.group(2)))
    versions = []
    for package, version in sorted(packages):
        mods, proof = package_audit(sources, package)
        proof['version'] = version
        proof['stage'] = VERSION_STAGE[version] if (version not in ('eh', 'es') or version == ('eh' if kind == 'hr' else 'es')) else 0
        proof['title'] = mods.findtext('m:titleInfo/m:title', namespaces=M)
        versions.append(proof)
    introductions = [v for v in versions if v['version'] == ('ih' if kind == 'hr' else 'is')]
    if not introductions:
        return excluded_slot(identity,congress,kind,'No introduced publication in official text-version list',source,bill.findtext('title','No title'))
    if len(introductions) != 1 or introductions[0]['issued_at'][:10] != intro[:10]:
        raise ValueError('Conflicting introduced publication: ' + identity)
    title = introductions[0]['title']
    related = []
    for item in bill.findall('relatedBills/item'):
        rc, rt, rn = item.findtext('congress'), item.findtext('type', '').lower(), item.findtext('number')
        if rc and rt and rn:
            related.append(f'{rc}-{rt}{rn}')
    exclusion = None
    if cutoff >= congress_end(congress): exclusion = 'Checkpoint at/after Congress end'
    elif law and law['enacted'] == congress_end(congress)[:10]: exclusion = 'Enactment on session-end date has insufficient time precision'
    elif law and law['enacted'] <= cutoff[:10]: exclusion = 'Already enacted by checkpoint'
    elif introductions[0]['available_at'] > cutoff: exclusion = 'Introduction publication not available by checkpoint'
    eligible = [v for v in versions if v['available_at'] <= cutoff and v['issued_at'] <= cutoff]
    stage = max([0] + [v['stage'] for v in eligible])
    last = max([intro] + [v['available_at'] for v in eligible])
    x = [stage / 4, min(spec['age_days'], 730) / 730, min(len(eligible), 30) / 30,
         min((date(cutoff)-date(last)).days, 730) / 730, int(kind == 's'),
         min(sum((date(cutoff)-date(v['available_at'])).days <= 30 for v in eligible), 10) / 10]
    return {'bill_id': identity, 'congress': congress, 'type': kind, 'title': title, 'introduced_at': intro,
            'cutoff': cutoff, 'x': x, 'y': int(bool(law and law['enacted'] < congress_end(congress)[:10])),
            'law': law, 'related': related, 'versions': versions, 'eligible_packages': [v['package'] for v in eligible],
            'source': source, 'exclusion': exclusion}


def family_groups(rows):
    parent = {}
    def find(x):
        parent.setdefault(x, x)
        if parent[x] != x: parent[x] = find(parent[x])
        return parent[x]
    def union(a, b):
        aa, bb = find(a), find(b)
        parent[max(aa, bb)] = min(aa, bb)
    titles = {}
    for row in rows:
        identity = row['bill_id']; find(identity)
        for related in row['related']: union(identity, related)
        title = re.sub(r'\W+', ' ', row['title'].lower()).strip() if row.get('versions') else ''
        if title: union(identity, titles.setdefault(title, identity))
    return {r['bill_id']: find(r['bill_id']) for r in rows}


def prepare(directory=DIRECTORY, rebuild=False, offline=False):
    frozen = frozen_spec(directory); spec = frozen['spec']; sources = Sources(directory, offline=offline)
    if (directory/'cohort.json').exists() and not rebuild:
        return json.loads((directory/'cohort.json').read_text())
    train_laws, train_sources = law_census(sources, 114, 329)
    training_proof = training_census(sources, train_laws)
    test_laws, test_sources = law_census(sources, 118, 274)
    labels = {r['bill_id']: r for r in train_laws + test_laws}
    jobs = [(c, k, n) for c in (114,118) for k in spec['bill_types'] for n in range(spec['bill_numbers'][0], spec['bill_numbers'][1]+1)]
    directories = {}
    for c in (114,118):
        for k in spec['bill_types']:
            raw, proof = sources.get(f'https://www.govinfo.gov/bulkdata/BILLSTATUS/{c}/{k}')
            numbers = {int(n) for n in re.findall(rb'BILLSTATUS-'+str(c).encode()+k.encode()+rb'(\d+)\.xml',raw)}
            if len(numbers)<1000: raise ValueError('Incomplete official chamber directory')
            directories[(c,k)] = (numbers,proof)
    rows, failures = [], []
    def collect(args):
        try: return sample_bill(sources, *args, spec, labels, directories), None
        except Exception as exc: return None, {'bill_id': f'{args[0]}-{args[1]}{args[2]}', 'error': str(exc)}
    with ThreadPoolExecutor(max_workers=4) as pool:
        for index, (row, failure) in enumerate(pool.map(collect, jobs), 1):
            (failures if failure else rows).append(failure or row)
            if not offline and index % 20 == 0: print(f'Audited {index}/{len(jobs)} source bundles; {len(failures)} failures', flush=True)
    audit = {'protocol_hash': frozen['spec_hash'], 'created_at': now(), 'selected': len(jobs), 'rows': rows,
             'failures': failures, 'training_label_provenance': training_proof,
             'law_census_sources': train_sources + test_sources, 'limitations': LIMITATIONS}
    if failures:
        write_json(directory/'audit-blocked.json', audit)
        raise ValueError(f'{len(failures)} source audits failed. Review audit-blocked.json; scoring is blocked.')
    groups = family_groups(rows)
    for row in rows: row['family_id'] = groups[row['bill_id']]
    test_families = {r['family_id'] for r in rows if r['congress'] == 118}
    used = set()
    for row in sorted(rows, key=lambda r:r['bill_id']):
        if row['congress'] == 114 and not row['exclusion']:
            if row['family_id'] in test_families: row['exclusion'] = 'Identified family overlaps test cohort'
            elif row['family_id'] in used: row['exclusion'] = 'Duplicate training family'
            else: used.add(row['family_id'])
    test = [r for r in rows if r['congress'] == 118 and not r['exclusion']]
    if test and training_proof['available_at'] > min(r['cutoff'] for r in test):
        raise ValueError('Complete training labels were not archived before earliest test checkpoint')
    manifest = sources.manifest()
    if not rebuild: write_json(directory/'source-manifest.json', manifest)
    audit['source_hash'] = digest(manifest)
    audit['cohort_hash'] = digest(rows)
    if not rebuild: write_json(directory/'cohort.json', audit)
    return audit


def bootstrap(pairs, count=2000):
    groups = {}
    for row in pairs: groups.setdefault(row['family_id'], []).append(row)
    ids = sorted(groups); rng = random.Random(20261024); values = []
    for _ in range(count):
        draw = [r for _ in ids for r in groups[rng.choice(ids)]]
        values.append(sum((r['probability']-r['outcome'])**2-(r['baseline_probability']-r['outcome'])**2 for r in draw)/len(draw))
    values.sort()
    return {'method': 'Test-family cluster percentile bootstrap; conditional on fitted model and test Congress',
            'replicates': count, 'seed': 20261024, 'families': len(ids),
            'lower_95': values[int(.025*count)], 'upper_95': values[int(.975*count)]}


def compute(directory=DIRECTORY):
    frozen = frozen_spec(directory)
    audit = json.loads((directory/'cohort.json').read_text())
    reconstructed = prepare(directory, rebuild=True, offline=True)
    if reconstructed['cohort_hash'] != audit['cohort_hash'] or reconstructed['source_hash'] != audit['source_hash']:
        raise ValueError('Offline reconstruction disagrees with frozen cohort')
    manifest = Sources(directory, offline=True).manifest()
    if digest(manifest) != audit['source_hash'] or digest(audit['rows']) != audit['cohort_hash'] or frozen['spec_hash'] != audit['protocol_hash']:
        raise ValueError('Frozen cohort/protocol/source manifest changed')
    train = [r for r in audit['rows'] if r['congress'] == 114 and not r['exclusion']]
    test = [r for r in audit['rows'] if r['congress'] == 118 and not r['exclusion']]
    if len(train) < 20 or {r['y'] for r in train} != {0,1} or not test:
        raise ValueError('Insufficient eligible training families/classes or test rows')
    if {r['family_id'] for r in train} & {r['family_id'] for r in test}:
        raise ValueError('Training/test family overlap')
    if audit['training_label_provenance']['available_at'] > min(r['cutoff'] for r in test):
        raise ValueError('Training label availability violates forward split')
    # Fitting receives exclusively training features and training labels.
    model = fit([{'x': r['x'], 'y': r['y']} for r in train])
    rate = (sum(r['y'] for r in train)+1)/(len(train)+2)
    predictions = [{'bill_id':r['bill_id'], 'title':r['title'], 'family_id':r['family_id'], 'cutoff':r['cutoff'],
                    'status':'available', 'probability':predict(model,r['x']), 'baseline_probability':rate,
                    'feature_hash':digest({'x':r['x'],'packages':r['eligible_packages']}), 'outcome':r['y']}
                   for r in test]
    metrics = score([r['probability'] for r in predictions],[r['outcome'] for r in predictions])
    baseline = score([rate for r in predictions],[r['outcome'] for r in predictions])
    difference = metrics['brier']-baseline['brier']; interval=bootstrap(predictions)
    conclusion = ('No added value in this pilot: candidate Brier loss exceeds or equals the baseline.' if difference >= 0 else
                  'Candidate has lower Brier loss in this pilot, but the interval includes no improvement.' if interval['upper_95'] >= 0 else
                  'Provisional improvement in this pilot; one Congress and limited audit scope cannot establish generalization.')
    result = {'title':'Audited real-data historical pilot', 'kind':'audited_cohort', 'candidate':'document-stage-l2-v1',
              'config':{'dataset':'official','congress':118,'age_days':180}, 'status':'completed',
              'design_status':frozen['spec']['design_status'], 'protocol_hash':frozen['spec_hash'],
              'source_hash':audit['source_hash'], 'cohort_hash':audit['cohort_hash'],
              'preflight':{'status':'passed bounded source audit; limitations retained'}, 'input_hash':audit['cohort_hash'],
              'training_count':len(train),'training_positives':sum(r['y'] for r in train),
              'selected':len(audit['rows']), 'attempted':sum(r['congress']==118 for r in audit['rows']),
              'available':len(test), 'metrics':metrics,'baseline':baseline,'brier_difference':difference,
              'brier_difference_interval':interval, 'results':predictions,'model_artifact':model,
              'training_ids':[r['bill_id'] for r in train], 'training_label_provenance':audit['training_label_provenance'],
              'exclusions':[{'bill_id':r['bill_id'],'reason':r['exclusion']} for r in audit['rows'] if r['exclusion']],
              'conclusion':conclusion, 'limitations':LIMITATIONS, 'release_eligible':False,
              'protocol':'114th-Congress training → 118th-Congress test; frozen publication-version cohort.',
              'note':conclusion+f" Paired Brier difference {difference:+.4f}; 95% test-family bootstrap interval [{interval['lower_95']:+.4f}, {interval['upper_95']:+.4f}]. "+'Document-version features, not the action-history model. '+LIMITATIONS[0],
              'rerun_note':'Offline rerun checks all frozen source hashes and reproduces the same fitted model and predictions.'}
    code = {name:hashlib.sha256((ROOT/'engine'/name).read_bytes()).hexdigest() for name in ('cohort.py','model.py','store.py','ingest.py')}
    result['code_hash'] = digest(code)
    result['code_files'] = code
    result['reproducibility_hash'] = digest(result)
    return result


def run(directory=DIRECTORY, publish=True, parent_id=None):
    result = compute(directory)
    locked = directory/'result.json'
    if locked.exists():
        previous = json.loads(locked.read_text())
        if result['reproducibility_hash'] != previous['reproducibility_hash']:
            raise ValueError('Reproduction differs from locked result; original preserved')
    else:
        write_json(locked,result)
        for name in result['code_files']:
            code_path=directory/'code'/name;code_path.parent.mkdir(exist_ok=True);code_path.write_bytes((ROOT/'engine'/name).read_bytes())
        (directory/'predictions.jsonl').write_text(''.join(json.dumps(r,sort_keys=True)+'\n' for r in result['results']))
    if publish:
        from . import workspace, rigor
        store=Store();workspace.initialize(store)
        try:
            from .ingest import import_xml
            frozen_sources=Sources(directory,offline=True)
            audit=json.loads((directory/'cohort.json').read_text())
            for row in audit['rows']:
                source=row['source']
                if source['url'].endswith('.xml'):
                    raw,_=frozen_sources.get(source['url'])
                    import_xml(store,raw,source['url'],observed=source['retrieved_at'])
            result.update(id=str(uuid.uuid4()),created_at=now(),completed_at=now(),parent_id=parent_id)
            workspace.save_experiment(store,result)
            report=rigor.store_report(store,'historical_cohort',{k:v for k,v in result.items() if k not in ('results','model_artifact')})
            chat=workspace.new_chat(store)
            content=(f"Real-data pilot completed: {result['training_count']} training bills and {result['available']} test bills. "
                     f"Brier: model {result['metrics']['brier']:.4f}, baseline {result['baseline']['brier']:.4f}. "
                     +result['conclusion']+' Open the audit report for exclusions, provenance and limitations.')
            artifacts=[workspace.experiment_artifact(result),workspace.report_artifact(report)]
            with store.db:
                store.db.execute('UPDATE chats SET title=? WHERE id=?',('Audited real-data pilot · 114 → 118',chat['id']))
                store.db.execute('INSERT INTO messages VALUES (?,?,?,?,?,?,?,?)',(str(uuid.uuid4()),chat['id'],'assistant',content,'completed',json.dumps(artifacts),now(),None))
            result['chat_id']=chat['id'];result['audit_report_id']=report['id']
            write_json(directory/'workspace-links.json',{k:result[k] for k in ('id','chat_id','audit_report_id')})
        finally:store.close()
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=['prepare','run','reproduce'])
    args=parser.parse_args()
    if args.action=='prepare':
        r=prepare();print(json.dumps({'selected':r['selected'],'cohort_hash':r['cohort_hash'],'failures':r['failures']}))
    else:
        r=run(publish=args.action=='run');print(json.dumps({k:r[k] for k in ('training_count','available','metrics','baseline','brier_difference','brier_difference_interval','conclusion','reproducibility_hash')},indent=2))

if __name__=='__main__':main()
