"""Synthetic identity/time preflight. No historical certification or production adapter."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path

IDENTITY_FIELDS = ('congress', 'type', 'number', 'version', 'raw_sha256', 'view_sha256')
BILL_TYPES = {'hr', 's', 'hjres', 'sjres', 'hconres', 'sconres', 'hres', 'sres'}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def utc(value):
    """Require an explicitly zoned instant; normalize before any comparison."""
    require(isinstance(value, str), 'timestamp must be text')
    try:
        stamp = datetime.fromisoformat(value.replace('Z', '+00:00'))
    except ValueError as exc:
        raise ValueError('invalid timestamp') from exc
    require(stamp.tzinfo is not None and stamp.utcoffset() is not None, 'naive timestamp')
    return stamp.astimezone(timezone.utc)


def validate_identity(actual, expected):
    """Compare against caller-trusted expected identity; not a version-code registry.

    Version syntax is checked, not official vocabulary/chamber compatibility.
    Matching self-asserted objects never establishes bill or historical identity."""
    for obj in (actual, expected):
        require(isinstance(obj, dict), 'identity must be an object')
        require(set(IDENTITY_FIELDS) <= set(obj), 'incomplete identity')
        for key in ('congress', 'number'):
            require(type(obj[key]) is int and obj[key] > 0, 'invalid identity integer')
        require(obj['type'] in BILL_TYPES, 'invalid bill type')
        require(isinstance(obj['version'], str) and re.fullmatch(r'[a-z][a-z0-9]*', obj['version']), 'invalid version')
        for key in ('raw_sha256', 'view_sha256'):
            require(isinstance(obj[key], str) and re.fullmatch(r'[0-9a-f]{64}', obj[key]), 'invalid digest')
    require(all(actual[k] == expected[k] for k in IDENTITY_FIELDS), 'identity/version/digest mismatch')
    return True


def verify_bytes(identity, raw, rendered):
    """Optional actual byte binding; this still does not prove historical availability."""
    validate_identity(identity, identity)
    require(isinstance(raw, bytes) and isinstance(rendered, bytes), 'byte inputs required')
    require(hashlib.sha256(raw).hexdigest() == identity['raw_sha256'], 'raw byte mismatch')
    require(hashlib.sha256(rendered).hexdigest() == identity['view_sha256'], 'rendered byte mismatch')
    return True


def day180_cutoff(introduced_at, cutoff, congress_end):
    """180 elapsed UTC days; inclusion exactly at cutoff, horizon strictly positive."""
    start, checkpoint, end = map(utc, (introduced_at, cutoff, congress_end))
    require(checkpoint == start + timedelta(days=180), 'cutoff is not introduction plus 180 days')
    require(end > checkpoint, 'nonpositive prediction horizon')
    return checkpoint


def feature_eligibility(record, cutoff):
    """Return explicit exclusion reasons; malformed/missing timestamps fail closed.

    scheduled_event.event_at may be future: only the known announcement is used.
    actual_event/realized_adjournment/cancellation require occurrence by cutoff.
    Family records are screening-only, never granted historical feature eligibility.
    """
    limit = utc(cutoff)
    require(isinstance(record, dict), 'feature must be an object')
    kind = record.get('kind')
    require(kind in {'text_version', 'scheduled_event', 'actual_event', 'realized_adjournment', 'cancellation', 'family_screening'}, 'unknown feature kind')
    clocks = {k: utc(record[k]) for k in ('known_at', 'source_available_at', 'version_available_at') if k in record}
    require(len(clocks) == 3, 'missing availability clock')
    reasons = [key + '_after_cutoff' for key, val in clocks.items() if val > limit]
    if kind in {'scheduled_event', 'actual_event', 'realized_adjournment', 'cancellation'}:
        require('event_at' in record, 'missing event clock')
        event = utc(record['event_at'])
        if kind != 'scheduled_event' and event > limit:
            reasons.append('realized_event_after_cutoff')
    if kind == 'family_screening':
        reasons.append('family_screening_only')
    return {'eligible': not reasons, 'reasons': reasons, 'historical_source_certified': False}


def select_schedule_vintage(records, cutoff):
    """Select latest eligible announcement/revision, retaining future exclusions.

    One event identity only. Equal known-at vintages are ambiguous, never resolved
    by input order. A known cancellation may supersede an announcement.
    """
    require(isinstance(records, list) and records, 'empty schedule history')
    require(all(isinstance(r, dict) for r in records), 'invalid schedule record')
    event_id = records[0].get('event_id')
    require(isinstance(event_id, str) and event_id.strip(), 'missing event identity')
    require(all(r.get('event_id') == event_id for r in records), 'mixed event identities')
    eligible, excluded = [], []
    for record in records:
        require(record.get('kind') in {'scheduled_event', 'cancellation'}, 'invalid schedule kind')
        result = feature_eligibility(record, cutoff)
        (eligible if result['eligible'] else excluded).append(record)
    if not eligible:
        return {'selected': None, 'excluded_count': len(excluded), 'status': 'unknown', 'historical_source_certified': False}
    newest = max(utc(r['known_at']) for r in eligible)
    chosen = [r for r in eligible if utc(r['known_at']) == newest]
    require(len(chosen) == 1, 'ambiguous same-time schedule vintages')
    return {'selected': chosen[0], 'excluded_count': len(excluded), 'status': 'cancelled' if chosen[0]['kind'] == 'cancellation' else 'announced', 'historical_source_certified': False}


def run_manifest(manifest):
    require(manifest.get('synthetic_only') is True, 'synthetic manifest required')
    results = []
    dispatch = {'identity': validate_identity, 'day180': day180_cutoff, 'feature': feature_eligibility, 'schedule': select_schedule_vintage}
    seen = set()
    for case in manifest['cases']:
        require(case['id'] not in seen, 'duplicate case id')
        seen.add(case['id'])
        require(case['operation'] in dispatch, 'unknown operation')
        try:
            result = dispatch[case['operation']](*case['args'])
            if isinstance(result, datetime):
                result = result.isoformat()
            observed = {'result': result}
        except ValueError as exc:
            observed = {'error': str(exc)}
        passed = observed == case['expected']
        results.append({'id': case['id'], 'passed': passed, 'observed': observed})
    return {'synthetic_only': True, 'historical_source_certified': False, 'predictive_test': False, 'cases': results, 'passed': all(r['passed'] for r in results)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('manifest', type=Path)
    args = parser.parse_args()
    result = run_manifest(json.loads(args.manifest.read_text()))
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result['passed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
