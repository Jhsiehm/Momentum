"""Executable research contract, immutable protocols and evidence-backed audit reports."""
import json
import re
import uuid
from collections import Counter
from .store import ROOT, available, digest, now, timestamp
from .model import snapshot, resolution

VERSION = 'research-contract-v1'
DOCUMENTS = {'plan': 'docs/IMPLEMENTATION_BRIEF.md', 'architecture': 'docs/ARCHITECTURE.md',
             'protocol': 'docs/PROTOCOL.md', 'roadmap': 'docs/ROADMAP.md'}
CAPABILITIES = [
    ('recognition', 'Policy recognition and bill linking', 'not_implemented', 'Specific bill IDs can be imported; independent policy-event detection and vehicle-linking benchmarks are not implemented.', 'import_bill'),
    ('scenarios', 'Conditional scenarios', 'not_implemented', 'No validated scenario model or causal intervention estimator; hypothetical assumptions must not rewrite saved forecasts.', None),
    ('protocol', 'Protocol and definitions', 'partial', 'Saved immutable fixed-age development protocols; broader designs are recorded as blocked.', 'register_protocol, run_registered_protocol'),
    ('ingestion', 'Evidence backbone', 'partial', 'GovInfo targeted imports, raw hashes, append-only metadata/actions. Census backfills and adjudication remain pending.', 'import_bill, list_sources, audit_data'),
    ('temporal', 'Point-in-time reconstruction', 'implemented', 'Effective and available timestamps filter evidence. Archive proof is an operator assertion, not independently verified.', 'inspect_bill, audit_forecast'),
    ('coverage', 'Historical coverage and missingness', 'partial', 'Imported-subset counts and missingness; no 50-year coverage claim.', 'audit_data'),
    ('baseline', 'A/B baselines and analogs', 'partial', 'Prior-Congress global/reference rates and structured L2 logistic regression for enactment; no trained calibration.', 'run_experiment, run_registered_protocol'),
    ('milestones', 'Milestone and timing models', 'not_implemented', 'Committee/chamber/bicameral and competing-risk timing forecasts need audited targets and models.', None),
    ('context', 'Economic, public and institutional context', 'not_implemented', 'ALFRED vintages, elections, polls, hearings, news and markets require source/licensing audits and paired ablations.', None),
    ('evaluation', 'Forward evaluation and uncertainty', 'partial', 'Fixed-age prior-only development scores and paired descriptive comparisons. No clustered intervals or protected untouched holdout.', 'compare_experiments, inspect_experiment'),
    ('ai', 'AI candidates and extraction', 'partial', 'Exact-span extraction with retained failures; no human-reviewed benchmark or validated C/D/E ensemble.', 'extract_evidence'),
    ('interface', 'Replay, monitoring and research workspace', 'implemented', 'Chat tools, versioned saved collections, frozen research sessions, reproducible exports, reports and sourced bill pages.', 'open_view'),
    ('prospective', 'Prospective shadow evaluation', 'partial', 'Timestamped forecast ledger plus opt-in local source refresh and change feed while server runs. Automatic forecast issuance and prospective validation remain pending.', 'save_forecast, audit_forecast, inspect_watching, configure_monitoring'),
    ('advanced', 'HybridAgent, states and provision tracking', 'not_implemented', 'Separate research extensions; never infer federal transfer or faithful architecture implementation.', None),
    ('release', 'Customer-facing promotion gates', 'not_passed', 'No validated real-data skill, calibrated subgroups, registered protected holdout or prospective reliability.', 'research_readiness')
]
SCHEMA = '''
CREATE TABLE IF NOT EXISTS research_protocols(id TEXT PRIMARY KEY,created_at TEXT,body TEXT);
CREATE TRIGGER IF NOT EXISTS protocols_no_update BEFORE UPDATE ON research_protocols BEGIN SELECT RAISE(ABORT,'Protocols are immutable'); END;
CREATE TRIGGER IF NOT EXISTS protocols_no_delete BEFORE DELETE ON research_protocols BEGIN SELECT RAISE(ABORT,'Protocols are immutable'); END;
CREATE TABLE IF NOT EXISTS research_reports(id TEXT PRIMARY KEY,created_at TEXT,body TEXT);
'''


def initialize(store):
    store.db.executescript(SCHEMA)


def capabilities():
    return [{'id': i, 'name': n, 'status': s, 'scope': scope, 'tools': tools} for i, n, s, scope, tools in CAPABILITIES]


def read_document(document='plan', section=None):
    if document not in DOCUMENTS:
        raise ValueError('Choose plan, architecture, protocol or roadmap')
    text = (ROOT / DOCUMENTS[document]).read_text()
    lines = text.splitlines()
    headings = [{'line': index + 1, 'heading': line.lstrip('# ').strip()} for index, line in enumerate(lines) if line.startswith('#')]
    result = {'document': document, 'path': DOCUMENTS[document], 'hash': digest(text), 'sections': headings,
              'note': 'Design specification; statements of intended capability are not evidence of implementation.'}
    if section:
        matches = [index for index, line in enumerate(lines) if line.startswith('#') and line.lstrip('# ').strip().lower() == section.lower()]
        if not matches:
            raise ValueError('Use an exact heading from the document index')
        start = matches[0]; level = len(lines[start]) - len(lines[start].lstrip('#'))
        end = next((index for index in range(start + 1, len(lines)) if lines[index].startswith('#') and len(lines[index]) - len(lines[index].lstrip('#')) <= level), len(lines))
        result['content'] = '\n'.join(lines[start:end])
        result['start_line'] = start + 1
    elif document != 'plan':
        result['content'] = text
    return result


def store_report(store, kind, body):
    initialize(store)
    report = {**body, 'id': str(uuid.uuid4()), 'kind': kind, 'created_at': now(), 'contract_version': VERSION}
    with store.db:
        store.db.execute('INSERT INTO research_reports VALUES (?,?,?)', (report['id'], report['created_at'], json.dumps(report)))
    return report


def get_report(store, identity):
    row = store.db.execute('SELECT body FROM research_reports WHERE id=?', (identity,)).fetchone()
    if not row:
        raise ValueError('Research report not found')
    return json.loads(row[0])


def audit_data(store, dataset, congress=None):
    if dataset not in ('demo', 'official'):
        raise ValueError('Unknown dataset')
    bills = [b for b in store.bills(dataset) if congress is None or b['congress'] == int(congress)]
    counts = Counter(); groups = {}; issues = []
    for bill in bills:
        counts['bills'] += 1
        group = groups.setdefault(str(bill['congress']), {'congress': bill['congress'], 'bills': 0, 'events': 0, 'resolved': 0})
        group['bills'] += 1
        events = store.records('event', dataset, bill['bill_id'])
        counts['events'] += len(events); group['events'] += len(events)
        if bill.get('family_status', '').startswith('unadjudicated') or (dataset == 'official' and not bill.get('family_proof')):
            counts['family_links_unverified'] += 1
        for record in [bill] + events:
            if record.get('published_at') is None:
                counts['publication_unknown'] += 1
            if record.get('archive_proof'):
                counts['archive_assertions'] += 1
            if available(record) > timestamp(record['effective_at']):
                counts['availability_after_event'] += 1
            raw = record.get('raw_hash')
            if dataset == 'official' and (not raw or not (ROOT / 'data' / 'raw' / raw).is_file()):
                counts['raw_snapshot_missing'] += 1
        outcome = resolution(store, dataset, bill['bill_id'])
        if outcome:
            counts['resolved'] += 1; group['resolved'] += 1
            counts['enacted' if outcome['value'] else 'not_enacted'] += 1
        else:
            counts['unresolved_or_unadjudicated'] += 1
    for key in ('bills', 'events', 'resolved', 'enacted', 'not_enacted', 'unresolved_or_unadjudicated', 'publication_unknown', 'archive_assertions', 'family_links_unverified', 'availability_after_event', 'raw_snapshot_missing'):
        counts.setdefault(key, 0)
    if dataset == 'demo':
        issues.append('Synthetic records only; no real-world source or performance validation.')
    if not bills:
        issues.append('No records in this selection.')
    if counts['publication_unknown']:
        issues.append('Unknown publication dates cannot establish historical public availability.')
    if counts['family_links_unverified']:
        issues.append('Family relationships need adjudication before credible family-sensitive evaluation.')
    if counts['unresolved_or_unadjudicated']:
        issues.append('Missing resolutions remain unknown, never negative outcomes.')
    return {'title': 'Source and temporal audit', 'dataset': dataset, 'congress': congress, 'counts': dict(counts),
            'by_congress': sorted(groups.values(), key=lambda r: r['congress']), 'findings': issues,
            'status': 'demonstration' if dataset == 'demo' else 'audit_required',
            'limitations': ['Imported subset is not a census.', 'Archive assertions have not been independently verified by this audit.', 'Counts describe stored records, not source coverage completeness.']}


def cohort_pilots(store, dataset):
    if dataset != 'official' or not store.db.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='experiments'").fetchone():
        return []
    rows=[json.loads(r[0]) for r in store.db.execute('SELECT body FROM experiments ORDER BY created_at DESC')]
    return [{k:r.get(k) for k in ('id','candidate','training_count','available','metrics','baseline','brier_difference_interval','conclusion','reproducibility_hash')} for r in rows if r.get('kind')=='audited_cohort'][:3]


def readiness(store, dataset):
    return {'title': 'Research readiness', 'dataset': dataset, 'capabilities': capabilities(),
            'source_audit': audit_data(store, dataset), 'completed_cohort_pilots': cohort_pilots(store,dataset), 'release_eligible': False,
            'release_blockers': ['Real-data forward skill versus baselines has not been established.',
                                 'Calibration and family/Congress-dependent uncertainty are not validated.',
                                 'No permission-protected untouched final holdout is integrated with chat.',
                                 'Prospective system reliability is not established.'],
            'next_step': 'Audit temporal availability, family links and resolved outcomes, then register a development protocol before testing.',
            'tracks': ['structured historical development', 'AI-assisted retrospective extraction (contamination possible)', 'prospective shadow logging (validation pending)']}


def preflight(store, config):
    dataset, congress, age = config['dataset'], config['congress'], config['age_days']
    from datetime import timedelta
    from .model import date, training_rows
    bills = [b for b in store.bills(dataset) if b['congress'] == congress]
    blocked = []; warnings = []; eligible = 0; reasons = Counter()
    if not bills:
        blocked.append('No bills in the selected Congress and collection.')
    if len(bills) > 500:
        blocked.append('Interactive limit is 500 bills; use a bounded audited cohort or the CLI.')
    for bill in bills[:500]:
        cutoff = (date(bill['introduced_at']) + timedelta(days=age)).isoformat()
        if date(cutoff) > date(now()):
            reasons['future_checkpoint'] += 1; continue
        snap = snapshot(store, dataset, bill['bill_id'], cutoff)
        if not snap:
            reasons['no_point_in_time_metadata'] += 1; continue
        if resolution(store, dataset, bill['bill_id'], cutoff):
            reasons['already_resolved_at_checkpoint'] += 1; continue
        training = training_rows(store, snap)
        if len(training) < 20 or len({r['y'] for r in training}) < 2:
            reasons['insufficient_prior_resolved_families'] += 1; continue
        eligible += 1
    if bills and not eligible:
        blocked.append('No target has both an eligible historical snapshot and sufficient prior resolved training data.')
    if dataset == 'demo':
        warnings.append('Fictional data: execution tests pipeline behavior only.')
    else:
        warnings += ['Official subset: coverage, archive claims and family links require human audit.', 'Development only; execution does not authorize performance claims.']
    return {'status': 'blocked' if blocked else 'ready_for_development', 'target_count': len(bills),
            'eligible_count': eligible, 'exclusion_counts': dict(reasons), 'blockers': blocked, 'warnings': warnings,
            'target': 'own-bill enactment by Congress end', 'candidate': 'structured-l2-v1',
            'split': 'Earlier Congresses; labels observable at each target cutoff', 'release_eligible': False}


def data_fingerprint(store, dataset):
    return digest([row[0] for row in store.db.execute('SELECT id FROM records WHERE dataset=? ORDER BY id', (dataset,))])


def register_protocol(store, args):
    initialize(store)
    allowed = {'title', 'hypothesis', 'dataset', 'congress', 'age_days', 'target', 'track', 'candidate', 'feature_families', 'supersedes'}
    if set(args) - allowed:
        raise ValueError('Unknown protocol fields: ' + ', '.join(sorted(set(args) - allowed)))
    title, hypothesis = args.get('title', '').strip(), args.get('hypothesis', '').strip()
    if not 3 <= len(title) <= 160 or not 10 <= len(hypothesis) <= 3000:
        raise ValueError('A protocol needs a title and an explicit hypothesis of 10–3,000 characters.')
    from .workspace import validate_experiment
    config = validate_experiment({k: args[k] for k in ('dataset', 'congress', 'age_days') if k in args})
    target = args.get('target', 'enactment_by_congress_end')
    track = args.get('track', 'structured_development')
    candidate = args.get('candidate', 'B')
    families = args.get('feature_families', ['structured'])
    if not isinstance(families, list) or not all(isinstance(v, str) for v in families):
        raise ValueError('Feature families must be a list of names')
    unsupported = []
    if target != 'enactment_by_congress_end': unsupported.append('Requested outcome/timing model is not implemented.')
    if track != 'structured_development': unsupported.append('This runner supports structured development only; protected holdout, AI challengers and prospective evaluation require separate infrastructure.')
    if candidate != 'B': unsupported.append('Runner compares candidate B with the historical-rate baseline; requested candidate is not implemented as a selectable experiment.')
    if set(families) != {'structured'}: unsupported.append('Requested feature family/ablation is not implemented or temporally audited.')
    supersedes = args.get('supersedes')
    if supersedes: get_protocol(store, supersedes)
    prior = preflight(store, config)
    # Existing scored work means a later protocol cannot be called preregistered.
    seen = store.db.execute('SELECT body FROM experiments').fetchall()
    prior_matching = [json.loads(row[0])['id'] for row in seen if json.loads(row[0]).get('config') == config]
    record = {'id': str(uuid.uuid4()), 'created_at': now(), 'title': title, 'hypothesis': hypothesis,
              'config': config, 'target': target, 'track': track, 'candidate': candidate, 'feature_families': families,
              'supersedes': supersedes, 'status': 'blocked' if unsupported or prior['blockers'] else 'registered_development',
              'unsupported': unsupported, 'preflight_at_registration': prior, 'prior_matching_runs': prior_matching,
              'registration_note': 'This configuration has already been run; registration is post hoc.' if prior_matching else 'No matching run recorded locally at registration. External prior inspection cannot be ruled out.',
              'split_rules': 'Strictly earlier Congresses; resolved/observable labels; unique training families; fixed age; no random split.',
              'metrics': ['Brier', 'log loss', 'reliability counts', 'historical-rate baseline'],
              'uncertainty': 'No clustered confidence interval or calibrated individual interval implemented.',
              'promotion': 'Never automatically eligible for customer-facing claims.',
              'data_fingerprint': data_fingerprint(store, config['dataset']),
              'document_hashes': {key: read_document(key)['hash'] for key in DOCUMENTS}, 'contract_version': VERSION}
    archive = ROOT / 'data' / 'research_documents'
    archive.mkdir(parents=True, exist_ok=True)
    for name, fingerprint in record['document_hashes'].items():
        destination = archive / (fingerprint + '.md')
        if not destination.exists(): destination.write_text((ROOT / DOCUMENTS[name]).read_text())
    record['fingerprint'] = digest(record)
    with store.db:
        store.db.execute('INSERT INTO research_protocols VALUES (?,?,?)', (record['id'], record['created_at'], json.dumps(record)))
    return record


def get_protocol(store, identity):
    row = store.db.execute('SELECT body FROM research_protocols WHERE id=?', (identity,)).fetchone()
    if not row: raise ValueError('Protocol not found')
    return json.loads(row[0])


def list_protocols(store):
    return [json.loads(row[0]) for row in store.db.execute('SELECT body FROM research_protocols ORDER BY created_at DESC,rowid DESC LIMIT 30')]


def compare_runs(store, left_id, right_id):
    from .workspace import get_experiment
    left, right = get_experiment(store, left_id), get_experiment(store, right_id)
    result = {'title': 'Paired experiment comparison', 'left_id': left_id, 'right_id': right_id,
              'left_config': left['config'], 'right_config': right['config'], 'release_eligible': False,
              'uncertainty': 'Descriptive paired scores only; no family/Congress-clustered confidence interval.'}
    if left['status'] != 'completed' or right['status'] != 'completed' or left['config'] != right['config']:
        return dict(result, status='not_comparable', reason='Both runs must be completed with identical collection, Congress and checkpoint definitions.')
    key = lambda r: (r['bill_id'], timestamp(r['cutoff']))
    a = {key(r): r for r in left.get('results', []) if r.get('probability') is not None and r.get('outcome') is not None}
    b = {key(r): r for r in right.get('results', []) if r.get('probability') is not None and r.get('outcome') is not None}
    shared = sorted(set(a) & set(b))
    valid = [k for k in shared if a[k]['outcome'] == b[k]['outcome']]
    if not valid:
        return dict(result, status='not_comparable', reason='No identical resolved bill/cutoff pairs with agreeing labels.')
    from .model import score
    labels = [a[k]['outcome'] for k in valid]
    ls, rs = score([a[k]['probability'] for k in valid], labels), score([b[k]['probability'] for k in valid], labels)
    return dict(result, status='descriptive_comparison', pairs=len(valid), left_only=len(set(a)-set(b)), right_only=len(set(b)-set(a)),
                label_disagreements=len(shared)-len(valid), left_scores=ls, right_scores=rs,
                brier_difference_right_minus_left=rs['brier']-ls['brier'],
                same_locked_forecasts=bool(left.get('reproducibility_hash') and left.get('reproducibility_hash') == right.get('reproducibility_hash')) or all(a[k].get('forecast_id') and a[k].get('forecast_id') == b[k].get('forecast_id') for k in valid),
                explanation='Identical locked forecasts are replication, not independent evidence of improvement.')


def audit_forecast(store, identity):
    row = store.db.execute('SELECT body FROM forecasts WHERE id=?', (identity,)).fetchone()
    if not row: raise ValueError('Saved forecast not found')
    f = json.loads(row[0]); problems = []; checked = 0
    for evidence_id in f['evidence_ids']:
        row = store.db.execute('SELECT body FROM records WHERE id=?', (evidence_id,)).fetchone()
        if not row:
            problems.append('Missing input record: ' + evidence_id); continue
        record = json.loads(row[0]); checked += 1
        if record['dataset'] != f['dataset'] or available(record) > f['cutoff'] or timestamp(record['effective_at']) > f['cutoff']:
            problems.append('Input outside dataset/temporal contract: ' + evidence_id)
    for train in f['training_manifest']:
        row = store.db.execute('SELECT body FROM records WHERE id=?', (train['resolution_id'],)).fetchone()
        if not row:
            problems.append('Missing training resolution: ' + train['bill_id']); continue
        record = json.loads(row[0])
        if available(record) > f['cutoff'] or timestamp(record['effective_at']) > f['cutoff']:
            problems.append('Training label was unavailable at origin: ' + train['bill_id'])
    return {'title': 'Saved forecast audit', 'forecast_id': identity, 'bill_id': f['bill_id'], 'dataset': f['dataset'],
            'cutoff': f['cutoff'], 'issued_at': f['issued_at'], 'track': f['track'], 'inputs_checked': checked,
            'training_labels_checked': len(f['training_manifest']), 'findings': problems,
            'status': 'violations_found' if problems else 'checked_rules_pass', 'snapshot_hash': f['snapshot_hash'],
            'limitations': ['Checks stored timestamps and namespace only; does not independently authenticate source provenance.',
                            'Does not certify archive assertions, historic model-weight cleanliness, training-feature reconstruction, calibration or release readiness.']}


def context_manifest(store, dataset):
    return {'contract_version': VERSION, 'documents': {key: {'path': path, 'hash': read_document(key)['hash']} for key, path in DOCUMENTS.items()},
            'capabilities': capabilities(), 'active_dataset': dataset, 'release_eligible': False,
            'completed_cohort_pilots': cohort_pilots(store,dataset),
            'recent_protocols': [{k: p[k] for k in ('id', 'title', 'status', 'config', 'hypothesis')} for p in list_protocols(store)[:5]],
            'rules': ['The full plan is a specification, not evidence that its features exist.',
                      'Read exact plan sections for methodological questions; cite document and heading.',
                      'Audit source timing, label maturity, family links and coverage before real-data experiments.',
                      'Register explicit hypothesis/target/split/features before confirmatory work; post-hoc registration stays labeled.',
                      'No outcome rewriting, backdated forecasts, fabricated archive proof, random temporal splits or missing-to-zero conversion.',
                      'Separate structured historical, contaminated AI retrospective and prospective tracks.',
                      'No calibrated intervals, causal scenario claims or customer-facing promotion without validated methods.',
                      'For unsupported features explain the missing implementation/evidence; do not silently substitute the available baseline.',
                      'Use paired same-case comparisons; reruns of saved forecasts are replication, not independent validation.']}
