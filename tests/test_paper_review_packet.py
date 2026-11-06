import copy
import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from engine.paper_evaluation import seal
from scripts.paper_review_packet import select,resolve,packet,persist_or_compare


class ReviewPacketTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name);self.cache=self.root/'sources';self.cache.mkdir()
        self.source=dict(url='fixture://source',sha256=hashlib.sha256(b'evidence').hexdigest(),bytes=8,retrieved_at='2026-11-06T00:00:00Z')
        key=hashlib.sha256(self.source['url'].encode()).hexdigest()
        self.raw=self.cache/(key+'.raw');self.meta=self.cache/(key+'.json')
        self.raw.write_bytes(b'evidence');self.meta.write_text(json.dumps(self.source))

    def test_selection_outcome_blind_and_order_stable(self):
        rows=[dict(bill_id='117-hr'+str(i),y=i%2) for i in range(20)]
        expected=[r['bill_id'] for r in select(rows,12)]
        for r in rows:r['y']=1-r['y']
        self.assertEqual(expected,[r['bill_id'] for r in select(list(reversed(rows)),12)])
        with self.assertRaises(ValueError):select(rows+[rows[0]],12)
        with self.assertRaises(ValueError):select(rows,21)

    def test_bytes_receipts_and_missing_evidence(self):
        self.assertEqual(resolve(self.source,[self.cache],self.root)['retained_matches'][0]['raw_path'],str(self.raw.relative_to(self.root)))
        self.raw.write_bytes(b'corrupt!')
        with self.assertRaisesRegex(ValueError,'corrupt'):resolve(self.source,[self.cache],self.root)
        self.raw.write_bytes(b'evidence');self.meta.unlink()
        with self.assertRaisesRegex(ValueError,'Missing'):resolve(self.source,[self.cache],self.root)

    def test_packet_retains_pending_and_omits_outcomes(self):
        version=dict(package='example',stage=0,issued_at='2013-01-01',available_at='2013-01-02',sources=[self.source])
        row=dict(bill_id='113-hr1',congress=113,family_id='family',introduced_at='2013-01-01',cutoff='2013-07-01',x=[0]*6,
                 source=self.source,versions=[version],eligible_packages=['example'],y=1,law={'law':1})
        result=packet([row],[self.cache],self.root)
        self.assertFalse(result['human_certified']);self.assertFalse(result['release_eligible'])
        self.assertEqual(result['records'][0]['human_review']['status'],'pending')
        self.assertNotIn('y',result['records'][0]);self.assertNotIn('law',result['records'][0])
        self.assertEqual(result['source_references'],2)

    def test_replay_never_overwrites(self):
        path=self.root/'packet.json';original=seal({'value':1})
        persist_or_compare(path,original);before=path.read_bytes()
        persist_or_compare(path,original)
        with self.assertRaisesRegex(ValueError,'mismatch'):persist_or_compare(path,seal({'value':2}))
        self.assertEqual(before,path.read_bytes())


if __name__=='__main__':unittest.main()
