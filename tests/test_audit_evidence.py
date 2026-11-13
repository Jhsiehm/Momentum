"""Independent subprocess checks: optimized Python must retain source guards."""
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROBE = '''
from engine.passage_evidence import audit_bill
class Sources:
    def get(self, url):
        return b'<billStatus><bill><congress>118</congress><type>hr</type><number>NUMBER</number><introducedDate>2023-02-01</introducedDate></bill></billStatus>', {'url':url,'sha256':'fixture'}
try:
    result = audit_bill(Sources(), '118-hr1')
    print('accepted:' + result['bill_id'])
except ValueError as error:
    print('rejected:' + str(error))
'''


class EvidenceGuardAudit(unittest.TestCase):
    def test_identity_rejection_and_valid_control_normal_and_optimized(self):
        for options in ([], ['-O']):
            for number, expected in [('1', 'accepted:118-hr1'), ('2', 'rejected:Bill identity mismatch')]:
                with self.subTest(options=options, number=number):
                    result = subprocess.run([sys.executable, *options, '-c', PROBE.replace('NUMBER', number)],
                                            cwd=ROOT, capture_output=True, text=True, timeout=20)
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertEqual(result.stdout.strip(), expected)
