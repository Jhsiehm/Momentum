"""Read-only alternative label-evidence investigation; never scores or changes studies."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import json
from . import cohort, sample_publication
from .store import ROOT, digest

DIRECTORY = ROOT / 'data/investigations/earlier-labels'


def law_identity(mods, congress, number):
    extensions = [e for e in mods.findall('m:extension', cohort.M) if e.find('m:congress', cohort.M) is not None]
    congresses = {e.findtext('m:congress', namespaces=cohort.M) for e in extensions}
    numbers = {e.findtext('m:number', namespaces=cohort.M) for e in extensions}
    if congresses != {str(congress)} or numbers != {str(number)}:
        raise ValueError('Public law identity mismatch')
    bills = {(b.get('congress'), b.get('type'), b.get('number'))
             for e in extensions for b in e.findall('m:bill', cohort.M)
             if b.get('priority') == 'primary'}
    if len(bills) != 1:
        raise ValueError('Ambiguous primary bill linkage')
    c, kind, n = next(iter(bills))
    if c != str(congress) or not kind or not n or not n.isdigit():
        raise ValueError('Invalid primary bill linkage')
    issued = mods.findtext('m:originInfo/m:dateIssued', namespaces=cohort.M)
    return {'law': number, 'bill_id': f'{c}-{kind.lower()}{int(n)}', 'enacted': issued}


def investigate(directory=DIRECTORY, offline=False):
    sources = sample_publication.Sources(directory, offline)
    census, census_sources = sample_publication.law_census(sources, 116, 344)
    def collect(expected):
        package = f"PLAW-116publ{expected['law']}"
        try:
            mods, proof = cohort.package_audit(sources, package)
            actual = law_identity(mods, 116, expected['law'])
            if actual != expected:
                raise ValueError(f'Individual-law / final NARA census disagreement: {actual}')
            return {**actual, 'proof': proof}, None
        except Exception as exc:
            return None, {'package': package, 'error': str(exc)}
    rows, failures = [], []
    with ThreadPoolExecutor(max_workers=4) as pool:
        for i, (row, error) in enumerate(pool.map(collect, census), 1):
            if row: rows.append(row)
            if error: failures.append(error)
            if not offline and i % 25 == 0:
                print(f'Individual laws audited {i}/344; failures {len(failures)}', flush=True)
    manifest = sources.manifest()
    result = {
        'kind': 'earlier_training_label_evidence_investigation',
        'congress': 116, 'expected_laws': 344, 'verified_laws': len(rows),
        'status': 'complete' if len(rows) == 344 and not failures else 'blocked',
        'available_at': max((r['proof']['available_at'] for r in rows), default=None),
        'rows': rows, 'failures': failures, 'census_sources': census_sources,
        'source_hash': digest(manifest), 'sources_count': len(manifest),
        'limitations': [
            'Investigation only; no forecasts, scores, changed frozen study, or human audit signoff.',
            'The final NARA census fetched now establishes retrospective completeness, not that this exact census file was archived before evaluation.',
            'Each law uses the existing bounded publication-availability rule: official issuance, ingestion and first successful preservation events plus one day.',
            'Current metadata and preservation histories do not prove byte-identical historical law renditions or historical linkage fields.',
            'Using individual public laws instead of bound Statutes volumes requires a separately registered protocol; the original study stays blocked.',
        ],
    }
    result['evidence_hash'] = digest(result)
    return result, manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--offline', action='store_true')
    args = parser.parse_args()
    result, manifest = investigate(offline=args.offline)
    if args.offline:
        saved = json.loads((DIRECTORY / 'report.json').read_text())
        if result != saved: raise ValueError('Investigation reconstruction mismatch')
    else:
        cohort.write_json(DIRECTORY / 'report.json', result)
        cohort.write_json(DIRECTORY / 'source-manifest.json', manifest)
    print(json.dumps({k: result[k] for k in ('status', 'verified_laws', 'available_at', 'failures', 'evidence_hash')}, indent=2))

if __name__ == '__main__': main()
