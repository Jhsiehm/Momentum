import copy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from engine.paper_evaluation import seal
from engine.store import digest
from scripts.bill_context_design_text_v2 import render
from scripts.mechanism_training_expansion_v2 import AcquisitionDeadline, cycle_specs, select_expansion, validate_current_record


class ExpansionTests(unittest.TestCase):
    def test_global_deadline_is_not_a_retryable_transport_timeout(self):
        from engine.ingest import fetch
        with patch('urllib.request.urlopen',side_effect=AcquisitionDeadline('cap')) as request:
            with self.assertRaises(AcquisitionDeadline):fetch('https://www.govinfo.gov/test')
            self.assertEqual(request.call_count,1)

    def test_cycles_cover_fixed_selection_once_without_exceeding_100(self):
        selected=[dict(bill_id=f'113-hr{i}') for i in range(1,1001)]
        cycles=cycle_specs(selected)
        self.assertEqual(len(cycles),10)
        self.assertTrue(all(len(c['bill_ids'])==100 and c['acquisition_cap']==100 for c in cycles))
        self.assertEqual([b for c in cycles for b in c['bill_ids']],[s['bill_id'] for s in selected])
        self.assertEqual([len(c['bill_ids']) for c in cycle_specs(selected[:251])],[100,100,51])
        with self.assertRaisesRegex(ValueError,'Duplicate'):cycle_specs(selected[:2]+selected[:1])
        with self.assertRaisesRegex(ValueError,'cap'):cycle_specs(selected+[dict(bill_id='113-hr1001')])

    def fixture(self,n=310):
        rows=[dict(bill_id=f'{c}-hr{i}',congress=c,cutoff=f'{1787+2*c}-09-01T23:59:59Z',label_available_at='2023-01-01T00:00:00Z',exclusion=None,y=i%2) for c in (113,114,115,116) for i in range(1,n+1)]
        groups={r['bill_id']:r['bill_id'] for r in rows};ids=[r['bill_id'] for r in rows]
        parts={'117':dict(core_ids=ids[::2],calibration_ids=ids[1::2],first_evaluation_cutoff='2024-01-01T00:00:00Z')}
        excluded=[dict(bill_id=f'{c}-hr{i}',family_id=f'{c}-hr{i}') for c in (113,114,115,116) for i in range(1,51)]
        return rows,groups,parts,excluded

    def test_fixed_1000_selection_excludes_prior_and_ignores_outcomes(self):
        rows,groups,parts,excluded=self.fixture();selected,ledger=select_expansion(rows,groups,parts,excluded)
        self.assertEqual(len(selected),1000)
        self.assertFalse({s['bill_id'] for s in selected}&{s['bill_id'] for s in excluded})
        changed=copy.deepcopy(rows)
        for r in changed:r['y']=1-r['y']
        self.assertEqual((selected,ledger),select_expansion(changed,groups,parts,excluded))
        for c in (113,114,115,116):
            ids=[s['bill_id'] for s in selected if s['congress']==c]
            self.assertEqual(len(ids),250);self.assertEqual(ids,sorted(ids,key=lambda bid:(digest(bid),bid)))

    def test_prior_families_excluded_not_only_exact_id(self):
        rows,groups,parts,excluded=self.fixture();groups['114-hr51']=groups['113-hr1']
        selected,ledger=select_expansion(rows,groups,parts,excluded)
        self.assertNotIn('114-hr51',{s['bill_id'] for s in selected})
        self.assertEqual(next(x for x in ledger if x['bill_id']=='114-hr51')['disposition'],'prior_selected_identity_or_family')

    def test_insufficient_stratum_not_filled_from_other_congress(self):
        rows,groups,parts,excluded=self.fixture(52)
        selected,_=select_expansion(rows,groups,parts,excluded)
        self.assertEqual(len(selected),8)
        self.assertTrue(all(sum(s['congress']==c for s in selected)==2 for c in (113,114,115,116)))

    def test_bad_membership_label_date_and_exclusion_binding_rejected(self):
        rows,groups,parts,excluded=self.fixture(52)
        bad=copy.deepcopy(parts);bad['117']['calibration_ids'].append(bad['117']['core_ids'][0])
        with self.assertRaisesRegex(ValueError,'overlap'):select_expansion(rows,groups,bad,excluded)
        excluded[0]['family_id']='wrong'
        with self.assertRaisesRegex(ValueError,'family changed'):select_expansion(rows,groups,parts,excluded)
        excluded[0]['family_id']=excluded[0]['bill_id'];rows[0]['label_available_at']='2024-01-01T00:00:00Z'
        with self.assertRaisesRegex(ValueError,'timing'):select_expansion(rows,groups,parts,excluded)

    def make_record(self,p):
        selected=dict(bill_id='113-hr1',congress=113,family_id='f',cutoff='2013-06-01T00:00:00Z',label_available_at='2015-01-01T00:00:00Z',memberships=[])
        raw=b'<bill><form><congress>113th CONGRESS</congress><legis-num>H. R. 1</legis-num></form><legis-body><section><text>Test.</text></section></legis-body></bill>'
        url='https://www.govinfo.gov/content/pkg/BILLS-113hr1ih/xml/BILLS-113hr1ih.xml';key=hashlib.sha256(url.encode()).hexdigest()
        receipt=dict(url=url,sha256=hashlib.sha256(raw).hexdigest(),bytes=len(raw),retrieved_at='2026-11-08T12:00:00Z')
        proof={'available_at':'2013-01-02T23:59:59Z'}
        view=seal(dict(**render(raw,'113-hr1'),source=receipt,registration_hash='reg',historical_feature_eligible=False))
        record=dict(**selected,registration_hash='reg',human_certified=False,historical_feature_eligible=False,status='metadata_dated_current_xml',package='BILLS-113hr1ih',publication_metadata=proof,source=receipt,source_view_hash=view['hash'])
        for sub in ('records','sources','views','packets'):(p/sub).mkdir()
        (p/'sources'/(key+'.raw')).write_bytes(raw);(p/'sources'/(key+'.json')).write_text(json.dumps(receipt))
        (p/'records/113-hr1.json').write_text(json.dumps(seal(record)));(p/'views/113-hr1.json').write_text(json.dumps(view))
        (p/'packets/113-hr1.json').write_text(json.dumps(seal(dict(bill_id='113-hr1',cutoff=selected['cutoff'],family_id='f'))))
        return selected,record,('BILLS-113hr1ih',url,proof)

    def test_completed_record_replay_checks_bytes_view_and_certification(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d);selected,record,proof=self.make_record(p)
            with patch('scripts.mechanism_training_expansion_v2.introduced_evidence',return_value=proof):
                self.assertTrue(validate_current_record(p,selected,'reg','2026-11-08T00:00:00Z'))
                record['historical_feature_eligible']=True;(p/'records/113-hr1.json').write_text(json.dumps(seal(record)))
                with self.assertRaisesRegex(ValueError,'certification'):validate_current_record(p,selected,'reg','2026-11-08T00:00:00Z')
                record['historical_feature_eligible']=False;(p/'records/113-hr1.json').write_text(json.dumps(seal(record)))
                path=next((p/'sources').glob('*.raw'));path.write_bytes(path.read_bytes()+b' ')
                with self.assertRaisesRegex(ValueError,'receipt changed'):validate_current_record(p,selected,'reg','2026-11-08T00:00:00Z')

    def test_blocked_record_requires_error_and_is_not_counted_usable(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d);selected,record,proof=self.make_record(p);record['status']='blocked';record['error']='HTTP404'
            (p/'records/113-hr1.json').write_text(json.dumps(seal(record)))
            self.assertFalse(validate_current_record(p,selected,'reg','2026-11-08T00:00:00Z'))
            record.pop('error');(p/'records/113-hr1.json').write_text(json.dumps(seal(record)))
            with self.assertRaisesRegex(ValueError,'Unexplained'):validate_current_record(p,selected,'reg','2026-11-08T00:00:00Z')


if __name__=='__main__':unittest.main()
