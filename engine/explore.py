"""Collection evidence landscape; no fitted probabilities or hindsight metadata."""
from datetime import timedelta
from .collections import get_collection
from .model import date, snapshot
from .store import digest, now, timestamp


def _event_key(event):
    # Retained source identifiers survive refreshes. Legacy records without one
    # use semantic fields, deliberately excluding observation IDs and hashes.
    return event.get('source_key') or digest({k: event.get(k) for k in
        ('bill_id', 'effective_at', 'stage', 'text', 'description', 'source_url', 'action_code')})


def collection_view(store, collection_id, cutoff=None, window_days=90, collection_version=None):
    if collection_version is not None and (type(collection_version) is not int or collection_version < 1):
        raise ValueError('Collection version must be a positive integer.')
    collection = get_collection(store, collection_id, collection_version)
    if isinstance(window_days, bool):
        raise ValueError('Comparison window must be an integer from 1 to 730 days.')
    try:
        parsed_window = int(window_days)
    except (ValueError, TypeError):
        raise ValueError('Comparison window must be an integer from 1 to 730 days.')
    if str(parsed_window) != str(window_days) or not 1 <= parsed_window <= 730:
        raise ValueError('Comparison window must be an integer from 1 to 730 days.')
    current = now()
    requested = cutoff or ('2023-07-01' if collection['dataset'] == 'demo' else current)
    try:
        as_of = min(timestamp(requested), current)
    except (ValueError, TypeError, AttributeError):
        raise ValueError('Supply an ISO date or timestamp with a timezone.')
    previous_as_of = timestamp((date(as_of) - timedelta(days=parsed_window)).isoformat())
    dataset = collection['dataset']
    watched = set(store.watched(dataset))
    rows, starts = [], []
    for bill_id in collection['bill_ids']:
        # Bounds describe retained coverage, never the substantive future record.
        bounds = store.db.execute(
            'SELECT MIN(MAX(available_at,effective_at)) FROM records WHERE dataset=? AND bill_id=?',
            (dataset, bill_id)).fetchone()[0]
        if bounds:
            starts.append(min(bounds, current))
        snap = snapshot(store, dataset, bill_id, as_of)
        previous = snapshot(store, dataset, bill_id, previous_as_of)
        row = dict(bill_id=bill_id, watched=bill_id in watched, available=bool(snap),
                   title='Metadata unavailable at cutoff', topic='Unavailable', type=None,
                   reason='No bill metadata demonstrably available at this cutoff.', stage=None,
                   stage_name='Unavailable', event_count=0, new_event_count=0,
                   effective_event_count=0, stage_change=None, latest_action_at=None,
                   observed_at=None, newly_available=False)
        if snap:
            bill = snap['bill']
            # Compare events independently of metadata availability: first seeing
            # metadata must not manufacture changes to already retained events.
            prior_events = store.records('event', dataset, bill_id, previous_as_of)
            old_keys = {_event_key(e) for e in prior_events}
            new_events = {_event_key(e): e for e in snap['events'] if _event_key(e) not in old_keys}
            row.update(title=bill['title'], topic=bill.get('topic') or 'Unclassified', type=bill['type'],
                       reason=None, stage=snap['stage'], stage_name=snap['stage_name'],
                       event_count=len({_event_key(e) for e in snap['events']}),
                       new_event_count=len(new_events),
                       effective_event_count=sum(e['effective_at'] > previous_as_of for e in new_events.values()),
                       stage_change=snap['stage'] - previous['stage'] if previous else None,
                       latest_action_at=max((e['effective_at'] for e in snap['events']), default=None),
                       observed_at=bill['observed_at'], newly_available=previous is None)
        rows.append(row)
    total_available = sum(r['available'] for r in rows)
    # Do not pass get_collection's present-day import coverage into a replay.
    collection = dict(collection, coverage=dict(total=len(rows), imported=total_available,
        missing=len(rows)-total_available, note='Metadata eligible at the selected cutoff; not experiment eligibility.'))
    return dict(collection=collection, as_of=as_of, previous_as_of=previous_as_of,
                window_days=parsed_window, date_bounds=dict(min=min(starts or [as_of])[:10], max=current[:10]),
                rows=rows, summary=dict(total=len(rows), available=total_available,
                    unavailable=len(rows)-total_available,
                    changed=sum(bool(r['new_event_count'] or r['stage_change'] or r['newly_available']) for r in rows),
                    new_events=sum(r['new_event_count'] for r in rows),
                    newly_available=sum(r['newly_available'] for r in rows)))
