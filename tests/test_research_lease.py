import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from engine.store import Store
from engine.research_lease import lease

class LeaseTests(unittest.TestCase):
    def test_owner_exclusion_expiration_and_recovery(self):
        with tempfile.TemporaryDirectory() as d:
            a=Store(Path(d)/'lease.sqlite');b=Store(Path(d)/'lease.sqlite')
            try:
                with patch('engine.research_lease.time.time',return_value=100):
                    self.assertTrue(lease(a,'acquire','a',60)['granted'])
                    self.assertFalse(lease(b,'acquire','b',60)['granted'])
                    self.assertFalse(lease(b,'release','b')['granted'])
                    self.assertTrue(lease(a,'renew','a',60)['granted'])
                with patch('engine.research_lease.time.time',return_value=161):
                    self.assertFalse(lease(a,'renew','a',60)['granted'])
                    self.assertTrue(lease(b,'acquire','b',60)['granted'])
                    self.assertFalse(lease(a,'release','a')['granted'])
                    self.assertTrue(lease(b,'release','b')['granted'])
                    self.assertFalse(lease(a,'status','a')['active'])
            finally:a.close();b.close()
