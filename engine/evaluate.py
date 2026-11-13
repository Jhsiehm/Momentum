"""Separate scoring entrypoint: the experiment worker need not receive labels."""
import json
import math
from pathlib import Path
from .model import score
from .store import digest, timestamp


def evaluate(predictions_path, labels_path):
    predictions = [json.loads(line) for line in Path(predictions_path).read_text().splitlines() if line.strip()]
    label_rows = [json.loads(line) for line in Path(labels_path).read_text().splitlines() if line.strip()]
    for row in predictions + label_rows:
        if not isinstance(row, dict) or not isinstance(row.get('bill_id'), str) or not row['bill_id']:
            raise ValueError('Every prediction and label requires a bill identity')
    if len({r['bill_id'] for r in label_rows}) != len(label_rows):
        raise ValueError('Duplicate outcome labels are not permitted')
    for row in label_rows:
        if type(row.get('value')) is not int or row['value'] not in (0, 1):
            raise ValueError('Labels require explicit integer zero or one')
        timestamp(row['resolved_at'])
    for row in predictions:
        probability = row.get('probability')
        if type(probability) not in (int, float) or not math.isfinite(probability) or not 0 <= probability <= 1:
            raise ValueError('Probability must be a finite number between zero and one')
        if not isinstance(row.get('family_id'), str) or not row['family_id']:
            raise ValueError('Prediction requires a family identity')
        timestamp(row['cutoff'])
        if row.get('track') == 'prospective shadow':
            timestamp(row['issued_at'])
    labels = {r['bill_id']: r for r in label_rows}
    if len({r['bill_id'] for r in predictions}) != len(predictions):
        raise ValueError('One prespecified snapshot per bill is required')
    pairs = [(p, labels[p['bill_id']]) for p in predictions if p['bill_id'] in labels]
    for p, y in pairs:
        if timestamp(p['cutoff']) >= timestamp(y['resolved_at']):
            raise ValueError('A prediction cutoff is not before resolution')
        if p.get('track') == 'prospective shadow' and timestamp(p['issued_at']) >= timestamp(y['resolved_at']):
            raise ValueError('Prospective forecast was issued after resolution')
    result = score([p['probability'] for p, _ in pairs], [y['value'] for _, y in pairs])
    result.update({'prediction_hash': digest(predictions), 'label_hash': digest(labels),
                   'unresolved': len(predictions) - len(pairs),
                   'families': len({p['family_id'] for p, _ in pairs}),
                   'note': 'No independence-based confidence interval. Protect label file permissions externally.'})
    return result
