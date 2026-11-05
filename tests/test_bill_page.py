import tempfile
import unittest
from pathlib import Path
from engine.store import Store
from engine.fixtures import seed
from engine.bill_page import detail, PlainText, overview
from unittest.mock import patch

class BillPageTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.store=Store(Path(self.tmp.name)/'test.sqlite');seed(self.store)
    def tearDown(self):
        self.store.close();self.tmp.cleanup()
    def test_future_metadata_hidden(self):
        page=detail(self.store,'demo','demo-118-hr101','2020-01-01')
        self.assertFalse(page['available']);self.assertNotIn('bill',page)
    def test_watch_and_evidence_dates(self):
        self.store.watch('demo','demo-118-hr101',True)
        page=detail(self.store,'demo','demo-118-hr101','2023-07-01')
        self.assertTrue(page['watched']);self.assertTrue(page['available'])
        self.assertTrue(all(e['effective_at']<=page['as_of'] for e in page['events']))
        self.assertIn('Synthetic',page['overview']['label'])
    def test_ended_unknown_is_not_negative(self):
        bill=dict(self.store.bill('demo','demo-118-hr101'))
        bill.update(bill_id='demo-118-hr9999',source_key='unknown-bill')
        self.store.add('bill',bill)
        page=detail(self.store,'demo','demo-118-hr9999','2026-01-01')
        self.assertIn('not audited',page['status'])
        self.assertIsNone(page['outcome'])
        self.assertEqual(page['forecast']['status'],'unavailable')
    def test_summary_markup_is_text(self):
        parser=PlainText();parser.feed('<p>A &amp; B</p><script>hidden</script><p>Next</p>')
        self.assertEqual(''.join(parser.parts),'A & B\nNext\n')

    def test_nested_official_summary_and_retrieval_boundary(self):
        root=Path(self.tmp.name);raw=root/'data'/'raw';raw.mkdir(parents=True)
        key='a'*64
        (raw/key).write_text('<billStatus><bill><summaries><summary><actionDate>2025-07-04</actionDate><updateDate>2025-07-05T12:00:00Z</updateDate><cdata><text>&lt;p&gt;Official purpose.&lt;/p&gt;</text></cdata></summary><summary><actionDate>2025-07-01</actionDate><updateDate>2025-07-06T12:00:00Z</updateDate><text>Older version edited later</text></summary></summaries></bill></billStatus>')
        bill={'title':'Title','dataset':'official','source_url':'https://www.govinfo.gov/','raw_hash':key,'observed_at':'2026-01-01T00:00:00Z'}
        with patch('engine.bill_page.ROOT',root):
            self.assertEqual(overview(bill,'2026-02-01T00:00:00Z')['text'],'Official purpose.')
            self.assertEqual(overview(bill,'2025-02-01T00:00:00Z')['text'],'Title')
