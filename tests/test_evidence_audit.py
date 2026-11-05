import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from engine import evidence_audit
from engine.store import digest


class AssistedAuditTests(unittest.TestCase):
    def test_findings_hash_verified_and_sample_bound(self):
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)
            report=dict(sample_id='a',sample_hash='frozen',rows=[dict(bill_id='114-hr1',human_review='pending')])
            report['findings_hash']=digest(report['rows'])
            (path/'assisted-audit.json').write_text(json.dumps(report))
            with patch.object(evidence_audit,'DIRECTORY',path), patch.object(evidence_audit.sampling,'get_sample',return_value={'hash':'frozen'}):
                self.assertEqual(evidence_audit.get_audit(None,'a'),report)
                self.assertIsNone(evidence_audit.get_audit(None,'other'))
                report['rows'][0]['human_review']='passed'
                (path/'assisted-audit.json').write_text(json.dumps(report))
                with self.assertRaisesRegex(ValueError,'checksum'):
                    evidence_audit.get_audit(None,'a')

    def test_audit_export_formula_safe_and_human_pending(self):
        csv=evidence_audit.export_audit_csv({'rows':[dict(bill_id='114-hr1',title='=HYPERLINK("unsafe")',human_review='pending',notes=['No human receipt'])]})
        self.assertIn("'=HYPERLINK",csv)
        self.assertIn('pending',csv)
        self.assertIn('No human receipt',csv)
