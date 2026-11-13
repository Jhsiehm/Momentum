import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from engine import prospective
from engine.store import Store


class CaptureClockAudit(unittest.TestCase):
    def test_clock_rollback_rejected_before_receipt_write(self):
        with tempfile.TemporaryDirectory() as directory:
            store = Store(Path(directory)/'db')
            try:
                with patch('engine.prospective.now', side_effect=['2026-11-12T12:00:00Z', '2026-11-12T11:59:59Z']):
                    with self.assertRaisesRegex(ValueError, 'Clock moved backward'):
                        prospective.capture(store, 'official', '119-hr999')
                self.assertEqual(prospective.list_receipts(store), [])
                with patch('engine.prospective.now', return_value='2026-11-12T12:00:00Z'):
                    receipt = prospective.capture(store, 'official', '119-hr999')
                self.assertEqual(receipt['status'], 'unavailable')
                self.assertEqual(len(prospective.list_receipts(store)), 1)
            finally:
                store.close()
