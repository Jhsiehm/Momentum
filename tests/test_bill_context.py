import hashlib
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from engine.store import Store
from engine.bill_context import context


class BillContextTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.root=Path(self.tmp.name)
        (self.root/'data'/'raw').mkdir(parents=True)
        self.store=Store(self.root/'db.sqlite')
        self.patcher=patch('engine.bill_context.ROOT',self.root); self.patcher.start()
    def tearDown(self):
        self.patcher.stop(); self.store.close(); self.tmp.cleanup()
    def add(self,title='First',observed='2025-02-01',extra='',prefix='',namespace=''):
        raw=(prefix+f'<billStatus {namespace}><bill><congress>119</congress><type>HR</type><number>1</number>{extra}</bill></billStatus>').encode()
        sha=hashlib.sha256(raw).hexdigest(); (self.root/'data'/'raw'/sha).write_bytes(raw)
        self.store.checkpoint('raw:119-hr1:'+sha,{'retrieved_at':observed,'hash':sha})
        self.store.add('bill',dict(dataset='official',bill_id='119-hr1',family_id='119-hr1',source_url='https://www.govinfo.gov',
            source_name='fixture',observed_at=observed,effective_at='2025-01-01',introduced_at='2025-01-01',
            type='hr',congress=119,title=title,topic='Topic',sponsor='Person',source_key='119-hr1',raw_hash=sha))
        return sha
    def test_relationship_and_text_sources_not_family_inference(self):
        self.add(extra='''<relatedBills><item><congress>119</congress><type>S</type><number>2</number><title>Related</title>
        <relationshipDetails><item><type>Procedurally related</type></item></relationshipDetails></item></relatedBills>
        <textVersions><item><date>2025-01-01</date><type>Introduced</type><formats><item><url>https://www.govinfo.gov/content/bill.xml</url></item></formats></item></textVersions>''',namespace='xmlns="urn:test"')
        result=context(self.store,'official','119-hr1','2025-02-02')
        self.assertEqual(result['related_bills'][0]['relationship'],'Procedurally related')
        self.assertFalse(result['related_bills'][0]['imported'])
        self.assertEqual(len(result['text_versions']),1)
        self.assertEqual(result['changes'],[])
        self.assertNotIn('family_id',result['related_bills'][0])
    def test_cutoff_excludes_future_retrieval_and_future_versions(self):
        self.add(extra='<textVersions><item><date>2025-03-01</date><formats><item><url>https://www.govinfo.gov/future</url></item></formats></item></textVersions>')
        self.assertEqual(context(self.store,'official','119-hr1','2025-01-15')['text_versions'],[])
        self.assertEqual(context(self.store,'official','119-hr1','2025-02-02')['text_versions'],[])
        self.add(title='Changed',observed='2025-04-01',extra='<title>Different raw</title>')
        self.assertEqual(context(self.store,'official','119-hr1','2025-03-01')['changes'],[])
        changes=context(self.store,'official','119-hr1','2025-05-01')['changes']
        self.assertEqual(changes[0]['before'],'First'); self.assertEqual(changes[0]['after'],'Changed')
    def test_unsafe_urls_and_doctypes_rejected(self):
        urls=['javascript:alert(1)','https://evil.example/file','https://www.govinfo.gov.evil.example/a','http://www.govinfo.gov/file','https://user@www.govinfo.gov/file']
        formats=''.join(f'<item><url>{u}</url></item>' for u in urls)
        self.add(extra=f'<textVersions><item><formats>{formats}</formats></item></textVersions>')
        self.assertEqual(context(self.store,'official','119-hr1','2025-03-01')['text_versions'],[])
        self.add(observed='2025-04-01',prefix='<!DOCTYPE billStatus>',extra='<relatedBills><item><type>S</type><number>2</number><congress>119</congress></item></relatedBills>')
        self.assertEqual(context(self.store,'official','119-hr1','2025-05-01')['related_bills'],[])
    def test_missing_raw_no_invented_relationship(self):
        sha=self.add(); (self.root/'data'/'raw'/sha).unlink()
        result=context(self.store,'official','119-hr1','2025-03-01')
        self.assertEqual(result['related_bills'],[]); self.assertEqual(result['text_versions'],[])
    def test_summary_changes_plain_text_not_full_bill_diff(self):
        self.add(extra='<summaries><summary><actionDate>2025-01-01</actionDate><text>&lt;p&gt;Before&lt;/p&gt;</text></summary></summaries>')
        self.add(observed='2025-04-01',extra='<summaries><summary><actionDate>2025-03-01</actionDate><text>&lt;p&gt;After&lt;/p&gt;</text></summary></summaries>')
        result=context(self.store,'official','119-hr1','2025-05-01')
        self.assertEqual(result['changes'][0]['field'],'summary')
        self.assertEqual(result['changes'][0]['after'],'After')
        self.assertIn('not full legislative text',' '.join(result['notes']))


if __name__=='__main__': unittest.main()
