"""Execute bill-context evidence preparation and fail-closed stage preflight.

This runner never fits models or certifies human reviews. Downloaded current
renditions remain ineligible for historical prediction pending source review.
"""
import argparse
import hashlib
import json
import math
import re
import time
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

from engine.cohort import Sources, family_groups
from engine.paper_evaluation import seal, unseal
from engine.research_lease import lease
from engine.store import ROOT, Store, congress_end, digest, now, timestamp
from scripts.cross_congress_evaluate import D, load_rows, make_split
from scripts.paper_readiness_audit import audit
from scripts.paper_review_packet import packet, persist_or_compare

PLAN = ROOT/'docs/research/BILL_CONTEXT_EXPERIMENT_PLAN_V1.md'
MECHANISMS = {
    'create_programme': r'\bestablish(?:ed|es)?\b',
    'authorize': r'\bauthoriz(?:e|es|ed|ation)\b',
    'appropriate': r'\bappropriat(?:e|es|ed|ion|ions)\b',
    'tax': r'\btax(?:es|ation)?\b', 'prohibit': r'\bprohibit(?:ed|ion|s)?\b',
    'require': r'\b(?:shall|require[ds]?)\b', 'amend': r'\bamend(?:ed|s|ment)?\b',
    'repeal': r'\brepeal(?:ed|s)?\b', 'rename_designate': r'\b(?:designat(?:e|ed|ion)|rename[ds]?)\b',
    'reporting': r'\breport(?:s|ing)?\b', 'deadline': r'\bnot later than\b',
    'sunset': r'\b(?:sunset|terminat(?:e|es|ion)|expire[ds]?)\b',
}


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def select_pilot(rows, groups):
    """Deterministic global-family exclusion, Congress order 113 through 117."""
    if len({r['bill_id'] for r in rows}) != len(rows):
        raise ValueError('Duplicate bill identity')
    selected, used, disposition = [], set(), []
    for c in range(113, 118):
        n = 0
        for row in sorted((r for r in rows if r['congress'] == c),
                          key=lambda r:(digest(r['bill_id']), r['bill_id'])):
            family = groups[row['bill_id']]
            reason = row.get('exclusion')
            if not reason and family in used:
                reason = 'Family already selected in pilot'
            if not reason and n >= 20:
                reason = 'Outside fixed stratum quota'
            item = dict(bill_id=row['bill_id'], congress=c, family_id=family,
                        disposition=reason or 'selected')
            if not reason:
                used.add(family)
                item['partition'] = 'design' if n < 10 else 'quality'
                selected.append(dict(row, family_id=family, partition=item['partition']))
                n += 1
            disposition.append(item)
        if n != 20:
            raise ValueError(f'Congress {c}: only {n}/20 eligible distinct families')
    return selected, disposition


def calendar_features(row, arm):
    x = row['x']
    if (len(x) != 6 or any(type(v) not in (int, float) or not math.isfinite(v) for v in x)
            or x[0] not in (0, .25, .5, .75)):
        raise ValueError('Invalid legacy features')
    cutoff = datetime.fromisoformat(timestamp(row['cutoff']).replace('Z', '+00:00'))
    end = datetime.fromisoformat(congress_end(row['congress']).replace('Z', '+00:00'))
    r = (end-cutoff).total_seconds()/(86400*730)
    if not 0 < r <= 1:
        raise ValueError('Checkpoint outside remaining-time range')
    if arm == 'control': return list(x)
    if arm == 'time': return list(x)+[r]
    if arm == 'interaction': return list(x)+[r, x[0]*r]
    raise ValueError('Unknown arm')


def xml_url(record, root):
    candidates = []
    for version in record['versions']:
        if not version['used_as_feature'] or not re.fullmatch(r'BILLS-\d+(?:hr|s)\d+(?:ih|is)', version['package']):
            continue
        expected = f"https://www.govinfo.gov/content/pkg/{version['package']}/xml/{version['package']}.xml"
        for source in version['sources']:
            if not source['url'].endswith('/mods.xml'): continue
            raw = (root/source['retained_matches'][0]['raw_path']).read_bytes()
            if b'<!ENTITY' in raw.upper(): raise ValueError('XML entities forbidden')
            tree = ET.fromstring(raw)
            if any(e.tag.rsplit('}', 1)[-1] == 'url' and (e.text or '').strip() == expected for e in tree.iter()):
                candidates.append((version['package'], expected))
    if len(set(candidates)) != 1:
        raise ValueError('No unique introduced XML rendition linked by retained MODS')
    return candidates[0]


def parse_design(raw, bill_id):
    if b'<!ENTITY' in raw.upper(): raise ValueError('XML entities forbidden')
    tree = ET.fromstring(raw)
    for e in tree.iter(): e.tag = e.tag.rsplit('}', 1)[-1]
    if tree.tag != 'bill': raise ValueError('Not bill XML')
    c, suffix = bill_id.split('-', 1)
    kind, number = re.fullmatch(r'(hr|s)(\d+)', suffix).groups()
    metadata = tree.find('form')
    if metadata is None: raise ValueError('Missing bill form')
    congress = metadata.findtext('congress', '')
    number_text = metadata.findtext('legis-num', '')
    if not congress.startswith(c) or re.sub(r'[^a-z0-9]', '', number_text.lower()) != kind+number:
        raise ValueError('Bill XML identity mismatch')
    text = ''.join(tree.itertext())
    sections = []
    for i, e in enumerate(tree.iter('section')):
        section = ''.join(e.itertext())
        sections.append(dict(index=i, xml_id=e.get('id'), text=section,
                             text_sha256=hashlib.sha256(section.encode()).hexdigest()))
    candidates = {name:[dict(start=m.start(), end=m.end(), quote=m.group())
                        for m in re.finditer(pattern, text, re.IGNORECASE)]
                  for name, pattern in MECHANISMS.items()}
    return dict(text=text, sections=sections, lexical_candidates=candidates,
                mechanism_labels={k:None for k in MECHANISMS},
                status='unreviewed_design_only',
                warning='Lexical hits are review pointers, not assertions of legal effect; negation and cross-references require review.')


def stage_status(fold_checks, acquired):
    shared = ['Required subject-bound human source/family/outcome reviews and methods population signoff are absent from the legacy inputs.']
    return {
        'E0':dict(status='partial', completed='100-case registration, source packet, design-only text extraction and pending annotation queue',
                  acquired_texts=acquired, blockers=['Two qualified independent reviewers and adjudicator not assigned; quality annotations absent; no fields certified.']),
        'E1':dict(status='blocked', blockers=shared, folds=fold_checks),
        'E2':dict(status='blocked', blockers=shared+['E0 accepted mechanism/policy fields unavailable.']),
        'E3':dict(status='blocked', blockers=shared+['Text historical availability uncertified; sparse solver/dependency verification not executed.']),
        'E4':dict(status='blocked', blockers=shared+['No registered reviewed point-in-time support/procedural feature matrix.']),
        'E5':dict(status='blocked', blockers=shared+['No registered reviewed announcement-vintage schedule/relationship matrix.']),
        'E6':dict(status='blocked', blockers=['E1 anchor and qualifying E2–E5 results unavailable.']),
        'E7':dict(status='blocked', blockers=['E6 representation unavailable; tree implementation not registered/verified.']),
        'E8':dict(status='blocked', blockers=shared+['Fixed selected encoding and reviewed initial training population unavailable.']),
        'E9':dict(status='blocked', blockers=['No qualifying successor, joint preregistration or independent custodian; future Congress 120/121 outcomes cannot be observed now.']),
    }


def run(directory, acquire=False):
    directory = Path(directory)
    if directory.resolve() == ROOT or ROOT/'data' not in directory.resolve().parents:
        raise ValueError('Output must be a new directory beneath ignored data/')
    directory.mkdir(parents=True, exist_ok=False)
    store = Store(); owner = 'bill-context-'+directory.name
    if not lease(store, 'acquire', owner)['granted']:
        store.close(); raise RuntimeError('Research lease unavailable')
    try:
        before = audit(); rows = load_rows(); groups = family_groups(rows)
        selected, dispositions = select_pilot(rows, groups)
        spec = dict(plan_sha256=sha(PLAN), code_sha256=sha(__file__),
                    dependencies={p:sha(ROOT/p) for p in ('engine/cohort.py','engine/store.py','engine/paper_evaluation.py','engine/ingest.py','scripts/paper_review_packet.py','scripts/cross_congress_evaluate.py')},
                    frozen_audit=before, selection=[dict(bill_id=r['bill_id'],family_id=r['family_id'],partition=r['partition']) for r in selected],
                    population_sha256=digest(rows), family_graph_sha256=digest(groups),
                    selection_rule='Congress ascending 113–117; canonical digest(bill_id) then ID; global family exclusion; first 10 design, next 10 quality per Congress',
                    acquisition_limit=100, acquire=acquire, mechanisms=MECHANISMS,
                    mode='evidence preparation and gate assessment only; no fit or score', registered_at=now())
        protocol = seal(spec); persist_or_compare(directory/'registration.json', protocol)
        persist_or_compare(directory/'disposition.json', seal(dispositions))
        caches = [D/'sources', ROOT/'data/research-runs/cross-congress-reserve-20261105/sources']
        evidence = packet(selected, caches, ROOT)
        persist_or_compare(directory/'source-packet.json', seal(evidence))
        sources = Sources(directory, offline=not acquire)
        records, failures, acquired = [], [], 0
        for row, record in zip(selected, evidence['records']):
            if not lease(store, 'renew', owner)['granted']: raise RuntimeError('Lost lease')
            item = dict(bill_id=row['bill_id'], family_id=row['family_id'], congress=row['congress'],
                        partition=row['partition'], cutoff=row['cutoff'],
                        historical_feature_eligible=False, human_review='pending', attributes={k:dict(value=None,status='unknown') for k in MECHANISMS})
            try:
                package, url = xml_url(record, ROOT)
                raw, source = sources.get(url); acquired += 1
                item.update(package=package, source=source, original_availability='unverified',
                            parser_sha256=sha(__file__))
                if row['partition'] == 'design':
                    item['design_extraction'] = parse_design(raw, row['bill_id'])
                else:
                    item['quality_content'] = 'Retained raw only; extraction and annotations unopened until design freeze'
            except Exception as error:
                item['blocked_reason'] = str(error)
                failures.append(dict(bill_id=row['bill_id'], error=str(error)))
            records.append(item)
            persist_or_compare(directory/'records'/(row['bill_id']+'.json'), seal(item))
            if acquire: time.sleep(.15)
            print(json.dumps(dict(processed=len(records), total=100, acquired=acquired, failures=len(failures))), flush=True)
        folds, encoding = {}, {}
        for c in (115,116,117):
            train, test = make_split(rows, c, groups)
            saved = json.loads((D/f'fold-{c}.json').read_text())
            models = json.loads((D/f'fold-{c}-models.json').read_text())
            if digest(models) != saved['models_hash']: raise ValueError('Legacy model hash mismatch')
            membership_ok = ([r['bill_id'] for r in train] == saved['training_ids'] and
                             [r['bill_id'] for r in test] == [r['bill_id'] for r in saved['predictions']])
            if not membership_ok: raise ValueError('Legacy fold membership changed')
            old = models['calibrated_all_history']
            lookup = {r['bill_id']:r for r in train}
            if set(old['core_ids']) & set(old['calibration_ids']) or set(old['core_ids']) | set(old['calibration_ids']) != set(lookup):
                raise ValueError('Invalid legacy calibration split')
            scope = train+test
            pending = sum(any(not v.get('introduction_validation',{}).get('human_audit_satisfied',False)
                              for v in r['versions'] if v['package'] in r['eligible_packages']) for r in scope)
            folds[str(c)] = dict(training=len(train), evaluation=len(test),
                                pending_introduction_review_rows=pending,
                                subject_bound_review_rows=sum(bool(r.get('review')) for r in scope),
                                membership_matches=True,
                                temporal_order=max(r['label_available_at'] for r in train)<min(r['cutoff'] for r in test),
                                family_disjoint=not bool({r['family_id'] for r in train}&{r['family_id'] for r in test}),
                                reviewed_positive_family_gate='not established; methods signoff required')
            encoding[str(c)] = dict(core_ids=old['core_ids'], calibration_ids=old['calibration_ids'],
                evaluation_ids=[r['bill_id'] for r in test],
                rows=[dict(bill_id=r['bill_id'],cutoff=r['cutoff'],
                           features={a:calendar_features(r,a) for a in ('control','time','interaction')}) for r in scope])
        persist_or_compare(directory/'e1-unapproved-inputs.json', seal(encoding))
        queue = [dict(bill_id=r['bill_id'], partition=r['partition'], annotator_1=None, annotator_2=None,
                      adjudicator=None, status='pending', labels={k:None for k in MECHANISMS}) for r in selected]
        persist_or_compare(directory/'annotation-queue.json', seal(queue))
        if audit() != before: raise ValueError('Frozen artifacts changed')
        result = seal(dict(protocol_hash=protocol['hash'], selected=100, design=50, quality=50,
                           source_references=evidence['source_references'], acquired_texts=acquired,
                           design_parsed=sum('design_extraction' in r for r in records), failures=failures,
                           stages=stage_status(folds, acquired), frozen_artifacts_unchanged=True,
                           models_fitted=0, outcomes_scored=0, forecasts_issued=0,
                           release_eligible=False, independent_validation=False))
        persist_or_compare(directory/'result.json', result)
        return result
    except Exception as error:
        persist_or_compare(directory/'failure.json', seal(dict(error=str(error), release_eligible=False)))
        raise
    finally:
        lease(store, 'release', owner); store.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--acquire', action='store_true', help='Fetch at most one introduced XML rendition per selected bill')
    args = parser.parse_args()
    result = run(args.output, args.acquire)
    print(json.dumps(dict(hash=result['hash'], **{k:v for k,v in unseal(result).items() if k not in ('stages','failures')}), indent=2))
