"""Mutation regressions against the retained pilot when locally available.

The runtime corpus is deliberately not committed; these integration cases skip
explicitly in clean checkouts without it. No originals are edited.
"""
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from engine.paper_evaluation import seal, unseal
from engine.store import ROOT
from scripts.verify_bill_context_execution import verify


class ContextReplayMutationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        source = ROOT/'data/research-runs/bill-context-20261108-v1'
        if not (source/'result.json').exists():
            raise unittest.SkipTest('Retained local pilot required for replay integration tests')
        cls.temp = tempfile.TemporaryDirectory(prefix='momentum-replay-test-')
        cls.directory = Path(cls.temp.name)/'pilot'
        shutil.copytree(source, cls.directory)

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def reject(self, name, change, message):
        path = self.directory/name
        original = path.read_bytes()
        body = unseal(json.loads(original))
        change(body)
        path.write_text(json.dumps(seal(body)))
        try:
            with self.assertRaisesRegex(ValueError, message):
                verify(self.directory)
        finally:
            path.write_bytes(original)

    def test_original_replays(self):
        self.assertFalse(verify(self.directory)['scientific_validation'])

    def test_record_identity_rejected(self):
        self.reject('records/113-hr4401.json', lambda b:b.update(bill_id='117-hr999999'), 'identity/cutoff')

    def test_core_calibration_swap_rejected(self):
        def swap(body):
            fold=body['115']
            fold['core_ids'][0],fold['calibration_ids'][0]=fold['calibration_ids'][0],fold['core_ids'][0]
        self.reject('e1-unapproved-inputs.json',swap,'authoritative fold/feature')

    def test_consistent_changed_control_rejected(self):
        def change(body):
            for arm in ('control','time','interaction'):
                body['115']['rows'][0]['features'][arm][2]=.123456
        self.reject('e1-unapproved-inputs.json',change,'authoritative fold/feature')

    def test_section_coordinates_rejected(self):
        self.reject('records/113-hr4401.json',lambda b:b['design_extraction']['sections'][0].update(xml_id='false-coordinate'),'Section coordinates')

    def test_release_claim_rejected(self):
        self.reject('result.json',lambda b:b.update(release_eligible=True),'eligibility')

    def test_annotation_label_rejected(self):
        self.reject('annotation-queue.json',lambda b:b[0]['labels'].update(tax=True),'Annotation queue')

    def test_optimized_python_rejects_false_fit_count(self):
        path=self.directory/'result.json';original=path.read_bytes()
        body=unseal(json.loads(original));body['models_fitted']=123
        path.write_text(json.dumps(seal(body)))
        try:
            script='from scripts.verify_bill_context_execution import verify; import sys; verify(sys.argv[1])'
            process=subprocess.run([sys.executable,'-O','-c',script,str(self.directory)],cwd=ROOT,capture_output=True,text=True)
            self.assertNotEqual(process.returncode,0)
            self.assertIn('ValueError',process.stderr)
            self.assertIn('models_fitted',process.stderr)
        finally:
            path.write_bytes(original)


if __name__=='__main__':unittest.main()
