import copy
import hashlib
from pathlib import Path
import tempfile
import unittest

from engine.store import digest
from scripts.mechanism_training_coverage import coverage, introduced_evidence, population_snapshot, select_training


class TrainingCoverageTests(unittest.TestCase):
    def test_excluded_checkpoint_missing_snapshot_preserved_without_outcomes(self):
        row=dict(bill_id='113-hr1',congress=113,label_available_at='2015-01-01T00:00:00Z',exclusion='No checkpoint',y=1)
        snapshot=population_snapshot([row],{'113-hr1':'family'})
        self.assertIsNone(snapshot[0]['cutoff'])
        self.assertEqual(snapshot[0]['exclusion'],'No checkpoint')
        self.assertNotIn('y',snapshot[0])

    def fixture(self, n=55):
        rows=[]
        for c in (113,114,115,116):
            rows += [dict(bill_id=f'{c}-hr{i}',congress=c,cutoff=f'{1787+2*c}-10-01T23:59:59Z',
                          label_available_at='2023-01-01T00:00:00Z',exclusion=None,y=i%2) for i in range(1,n+1)]
        rows += [dict(bill_id='117-hr1',congress=117,cutoff='2022-01-01T00:00:00Z',
                      label_available_at='2023-01-01T00:00:00Z',exclusion=None,y=1)]
        groups={r['bill_id']:r['bill_id'] for r in rows}
        train=[r['bill_id'] for r in rows if r['congress']<117]
        memberships={'117':dict(core_ids=train[::2],calibration_ids=train[1::2],first_evaluation_cutoff='2024-01-01T00:00:00Z')}
        return rows,groups,memberships

    def test_fixed_cap_training_only_and_outcome_invariance(self):
        rows,groups,parts=self.fixture()
        selected,ledger=select_training(rows,groups,parts,[])
        self.assertEqual(len(selected),200)
        self.assertTrue(all(s['congress']<117 for s in selected))
        self.assertEqual([s['congress'] for s in selected],sorted(s['congress'] for s in selected))
        changed=copy.deepcopy(rows)
        for r in changed:r['y']=1-r['y']
        self.assertEqual((selected,ledger),select_training(changed,groups,parts,[]))
        for c in (113,114,115,116):
            ids=[s['bill_id'] for s in selected if s['congress']==c]
            self.assertEqual(ids,sorted(ids,key=lambda bid:(digest(bid),bid)))

    def test_pilot_family_firewall_and_no_surplus_replacement(self):
        rows,groups,parts=self.fixture(4)
        groups['114-hr1']=groups['113-hr1']
        pilot=[dict(bill_id='113-hr1',family_id=groups['113-hr1'],partition='quality')]
        selected,_=select_training(rows,groups,parts,pilot,quota=4)
        self.assertNotIn('113-hr1',{s['bill_id'] for s in selected})
        self.assertNotIn('114-hr1',{s['bill_id'] for s in selected})
        self.assertEqual(len(selected),14)
        # Acquisition outcomes are not an argument to selection: no backfilling.
        self.assertEqual(selected,select_training(rows,groups,parts,pilot,quota=4)[0])

    def test_late_training_labels_and_bad_quotas_fail_closed(self):
        rows,groups,parts=self.fixture(2)
        rows[0]['label_available_at']='2024-01-01T00:00:00Z'
        with self.assertRaisesRegex(ValueError,'timing'):select_training(rows,groups,parts,[])
        for q in (0,51,True):
            with self.assertRaisesRegex(ValueError,'Quota'):select_training(rows,groups,parts,[],q)

    def test_duplicate_identity_and_pilot_family_mutation_rejected(self):
        rows,groups,parts=self.fixture(2)
        with self.assertRaisesRegex(ValueError,'Duplicate'):select_training(rows+[rows[0]],groups,parts,[])
        with self.assertRaisesRegex(ValueError,'family changed'):
            select_training(rows,groups,parts,[dict(bill_id=rows[0]['bill_id'],family_id='wrong')])

    def test_coverage_counts_never_certify_and_do_not_mix_roles(self):
        p={'117':dict(core_ids=['a','b'],calibration_ids=['c'],first_evaluation_cutoff='2020-01-01T00:00:00Z')}
        result=coverage(p,{'b','c','not-in-partition'})['117']
        self.assertEqual(result['core'],dict(total=2,metadata_dated_xml=1,certified_historical=0))
        self.assertEqual(result['calibration'],dict(total=1,metadata_dated_xml=1,certified_historical=0))

    def test_introduced_metadata_link_identity_and_cutoff_replay(self):
        package='BILLS-113hr1ih';url=f'https://www.govinfo.gov/content/pkg/{package}/xml/{package}.xml'
        mods=f'<mods xmlns="http://www.loc.gov/mods/v3"><recordInfo><recordIdentifier>{package}</recordIdentifier></recordInfo><extension><dateIngested>2013-01-02</dateIngested></extension><originInfo><dateIssued>2013-01-01</dateIssued></originInfo><location><url>{url}</url></location></mods>'.encode()
        events=''.join(f'<event><eventType>{kind}</eventType><eventDateTime>2013-01-02T12:00:00Z</eventDateTime><eventOutcomeInformation><eventOutcome>Success</eventOutcome></eventOutcomeInformation></event>' for kind in ['Ingestion','ACP Creation','Parsing'])
        premis=('<premis xmlns="info:lc/xmlns/premis-v2">'+events+'</premis>').encode()
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);sources=[]
            for name,raw in [('mods',mods),('premis',premis)]:
                (root/name).write_bytes(raw)
                sources.append(dict(url=f'https://www.govinfo.gov/metadata/pkg/{package}/{name}.xml',sha256=hashlib.sha256(raw).hexdigest(),bytes=len(raw),retained_matches=[dict(raw_path=name)]))
            v=dict(package=package,used_as_feature=True,issued_at='2013-01-01T23:59:59Z',available_at='2013-01-03T23:59:59Z',sources=sources)
            r=dict(bill_id='113-hr1',cutoff='2013-06-01T23:59:59Z',versions=[v])
            self.assertEqual(introduced_evidence(r,root)[:2],(package,url))
            r['cutoff']='2013-01-02T23:59:59Z'
            with self.assertRaisesRegex(ValueError,'later than cutoff'):introduced_evidence(r,root)
            r['cutoff']='2013-06-01T23:59:59Z';r['bill_id']='113-hr2'
            with self.assertRaisesRegex(ValueError,'identity mismatch'):introduced_evidence(r,root)
            r['bill_id']='113-hr1';(root/'mods').write_bytes(mods+b' ')
            with self.assertRaisesRegex(ValueError,'metadata changed'):introduced_evidence(r,root)


if __name__=='__main__':unittest.main()
