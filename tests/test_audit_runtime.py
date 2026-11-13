"""Exercise the real evaluation CLI with isolated files and database location."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class EvaluationCLIIntegrityTests(unittest.TestCase):
    def run_cli(self, predictions=None, labels=None):
        if predictions is None:
            predictions = [dict(bill_id='119-hr1', family_id='f1', cutoff='2025-01-01T00:00:00Z', probability=0.2)]
        if labels is None:
            labels = [dict(bill_id='119-hr1', resolved_at='2025-02-01T00:00:00Z', value=1)]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)
            for name, rows in [('predictions', predictions), ('labels', labels)]:
                (path/name).write_text(''.join(json.dumps(row)+'\n' for row in rows))
            # Call the actual CLI, but redirect its default Store into this temp root.
            code = "import pathlib; import engine.store; engine.store.ROOT=pathlib.Path('.'); from engine.__main__ import main; main()"
            return subprocess.run([sys.executable, *(['-O'] if sys.flags.optimize else []), '-c', code, 'evaluate', 'predictions', 'labels'], cwd=path,
                                  env={**os.environ, 'PYTHONPATH':str(ROOT)}, text=True, capture_output=True, timeout=20)

    def test_valid_control(self):
        result=self.run_cli();self.assertEqual(result.returncode,0,result.stderr)
        self.assertAlmostEqual(json.loads(result.stdout)['brier'],0.64)

    def test_duplicate_labels_rejected(self):
        rows=[dict(bill_id='119-hr1',resolved_at='2025-02-01T00:00:00Z',value=v) for v in [1,0]]
        self.assertNotEqual(self.run_cli(labels=rows).returncode,0)

    def test_timestamp_offsets_cannot_hide_post_resolution_prediction(self):
        p=[dict(bill_id='119-hr1',family_id='f1',cutoff='2025-01-01T01:00:00Z',probability=0.2)]
        y=[dict(bill_id='119-hr1',resolved_at='2025-01-01T02:00:00+05:00',value=1)]
        self.assertNotEqual(self.run_cli(p,y).returncode,0)

    def test_boolean_probability_or_label_rejected(self):
        p=[dict(bill_id='119-hr1',family_id='f1',cutoff='2025-01-01',probability=True)]
        self.assertNotEqual(self.run_cli(predictions=p).returncode,0)
        y=[dict(bill_id='119-hr1',resolved_at='2025-02-01',value=True)]
        self.assertNotEqual(self.run_cli(labels=y).returncode,0)

    def test_nonfinite_and_wrong_range_probabilities_rejected(self):
        for value in [float('nan'),float('inf'),-0.1,1.1]:
            p=[dict(bill_id='119-hr1',family_id='f1',cutoff='2025-01-01',probability=value)]
            self.assertNotEqual(self.run_cli(predictions=p).returncode,0)

    def test_valid_unresolved_prediction_remains_unresolved(self):
        p=[dict(bill_id='119-hr1',family_id='f1',cutoff='2025-01-01',probability=0.2),
           dict(bill_id='119-hr2',family_id='f2',cutoff='2025-01-01',probability=0.3)]
        result=self.run_cli(predictions=p);self.assertEqual(result.returncode,0,result.stderr)
        self.assertEqual(json.loads(result.stdout)['unresolved'],1)
