import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from engine import sample_publication as p
from engine.store import digest

class SamplePublicationTests(unittest.TestCase):
    def test_protocol_immutable(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); spec=root/'spec.json';spec.write_text('{"age_days":180}')
            with patch.object(p,'SPEC',spec):
                self.assertEqual(p.frozen_spec(root)['spec_hash'],digest({'age_days':180}))
                spec.write_text('{"age_days":90}')
                with self.assertRaisesRegex(ValueError,'Protocol changed'):p.frozen_spec(root)
    def test_automated_family_screen_excludes_train_overlap_and_duplicates(self):
        def row(bid,congress,title,related=[]):return dict(bill_id=bid,congress=congress,title=title,related=related,versions=[{}],exclusion=None)
        rows=[row('114-hr1',114,'Same title'),row('118-s1',118,'Same title'),row('114-hr2',114,'Other'),row('116-s2',116,'Other'),row('116-hr3',116,'Distinct')]
        p.assign_families(rows)
        self.assertEqual(rows[0]['exclusion'],'Identified family overlaps evaluation cohort')
        self.assertEqual(rows[3]['exclusion'],'Duplicate training family')
        self.assertIsNone(rows[4]['exclusion'])
    def test_116_census_requires_complete_unique_laws(self):
        class Source:
            def get(self,url):return b'ignored',{'url':url}
        with patch.object(p.cohort,'parse_law_list',side_effect=[[{'law':1,'bill_id':'116-hr1'}],[{'law':2,'bill_id':'116-s2'}]]):
            rows,proofs=p.law_census(Source(),116,2)
            self.assertEqual(len(rows),2);self.assertTrue(all('.txt' in x['url'] for x in proofs))
        with patch.object(p.cohort,'parse_law_list',return_value=[{'law':1,'bill_id':'116-hr1'}]):
            with self.assertRaisesRegex(ValueError,'Incomplete/duplicate'):p.law_census(Source(),116,2)
    def test_offline_cache_detects_tampering(self):
        with tempfile.TemporaryDirectory() as d:
            s=p.Sources(Path(d));url='https://example.org/official.xml'
            with patch.object(p.cohort,'fetch',return_value=b'original'):s.get(url)
            next(s.directory.glob('*.raw')).write_bytes(b'changed');s.offline=True
            with self.assertRaisesRegex(ValueError,'checksum mismatch'):s.get(url)
    def test_late_training_labels_block_fitting(self):
        rows=[dict(bill_id=f'114-hr{i}',congress=114,family_id=f'f{i}',exclusion=None,y=i%2) for i in range(20)]
        rows.append(dict(bill_id='118-s1',congress=118,family_id='test',exclusion=None,y=0,cutoff='2023-08-01T00:00:00Z'))
        audit=dict(rows=rows,failures=[],source_hash='s',cohort_hash='c',protocol_hash='p',training_label_provenance=[dict(available_at='2025-02-13T23:59:59Z')])
        spec=dict(spec_hash='p',spec=dict(bill_ids=[r['bill_id'] for r in rows],design_status='development',sample_id='sample'))
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);(root/'cohort.json').write_text(json.dumps(audit))
            with patch.object(p,'frozen_spec',return_value=spec),patch.object(p,'prepare',return_value=audit),patch.object(p,'fit') as fitting:
                result=p.compute(root)
                self.assertEqual(result['status'],'blocked');self.assertIn('Complete training labels',result['conclusion']);self.assertEqual(result['results'],[]);fitting.assert_not_called()
    def test_workspace_publication_and_both_rerun_routes(self):
        from engine import workspace
        from engine.store import Store
        frozen=dict(status='blocked',available=32,results=[],blockers=['source audit'],preflight={},cohort_hash='c',reproducibility_hash='r',conclusion='Blocked',config={'dataset':'official','congress':118,'age_days':180},attempted=40)
        with tempfile.TemporaryDirectory() as d:
            store=Store(Path(d)/'test.sqlite');workspace.initialize(store)
            with patch.object(p,'run',side_effect=lambda:json.loads(json.dumps(frozen))):
                first=workspace.publish_sample_publication(store)
                self.assertEqual(first['available'],0);self.assertEqual(first['publication_eligible_count'],32)
                with patch.object(workspace,'create_experiment',side_effect=AssertionError('Wrong action-history fallback')):
                    second=workspace.start_experiment(store,first['config'],first['id'])
                    brief,_=workspace.execute_tool(store,'rerun_experiment',{'experiment_id':first['id']})
                self.assertEqual(second['kind'],'sample_publication_study');self.assertEqual(brief['available'],0)
                self.assertEqual(second['parent_id'],first['id']);self.assertEqual(second['status'],'blocked')
            store.close()
