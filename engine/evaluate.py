"""Separate scoring entrypoint: the experiment worker need not receive labels."""
import json
from pathlib import Path
from .model import score
from .store import digest


def evaluate(predictions_path, labels_path):
    predictions = [json.loads(line) for line in Path(predictions_path).read_text().splitlines() if line.strip()]
    labels = {r['bill_id']: r for r in (json.loads(line) for line in Path(labels_path).read_text().splitlines() if line.strip())}
    if len({r['bill_id'] for r in predictions}) != len(predictions):
        raise ValueError('One prespecified snapshot per bill is required')
    pairs = [(p, labels[p['bill_id']]) for p in predictions if p['bill_id'] in labels]
    for p, y in pairs:
        if p['cutoff'] >= y['resolved_at']:
            raise ValueError('A prediction cutoff is not before resolution')
        if p.get('track') == 'prospective shadow' and p['issued_at'] >= y['resolved_at']:
            raise ValueError('Prospective forecast was issued after resolution')
    result = score([p['probability'] for p, _ in pairs], [y['value'] for _, y in pairs])
    result.update({'prediction_hash': digest(predictions), 'label_hash': digest(labels),
                   'unresolved': len(predictions) - len(pairs),
                   'families': len({p['family_id'] for p, _ in pairs}),
                   'note': 'No independence-based confidence interval. Protect label file permissions externally.'})
    return result
