import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from engine import cohort as c


class CohortTests(unittest.TestCase):
    def test_preservation_requires_success_and_conservative_date(self):
        mods=b'<mods xmlns="http://www.loc.gov/mods/v3"><recordInfo><recordIdentifier>BILLS-114hr2ih</recordIdentifier></recordInfo><extension><dateIngested>2015-01-03</dateIngested></extension><originInfo><dateIssued>2015-01-01</dateIssued></originInfo></mods>'
        events=''.join(f'<event><eventType>{t}</eventType><eventDateTime>2015-01-02T23:00:00-05:00</eventDateTime><eventOutcomeInformation><eventOutcome>Success</eventOutcome></eventOutcomeInformation></event>' for t in ('Ingestion','ACP Creation','Parsing'))
        premis=('<premis xmlns="info:lc/xmlns/premis-v2">'+events+'</premis>').encode()
        self.assertEqual(c.provenance(mods,premis,'BILLS-114hr2ih')['available_at'],'2015-01-04T23:59:59Z')
        with self.assertRaises(ValueError):c.provenance(mods,premis.replace(b'Success',b'Failure'),'BILLS-114hr2ih')
        with self.assertRaises(ValueError):c.provenance(mods,premis,'BILLS-114hr3ih')

    def test_law_lists_handle_original_missing_parenthesis_and_joint_resolutions(self):
        raw=b'FINAL LISTING\nH.R. 2 / Public Law 114-1\nTitle\nJune 29, 2015; 129 Stat. 319; 43 pages)\nS.J. Res. 3 / Public Law 114-2\nTitle\n(July 1, 2015; 129 Stat. 320; 1 page)'
        rows=c.parse_law_list(raw,114)
        self.assertEqual(rows[0]['enacted'],'2015-06-29')
        self.assertEqual(rows[1]['bill_id'],'114-sjres3')
        with self.assertRaises(ValueError):c.parse_law_list(b'partial list',114)

    def test_html_law_table_exact_bill_and_date(self):
        raw=b'<table><tr><td>118-8</td><td>S. 30</td><td>Title</td><td>July 18, 2023</td></tr></table>'
        self.assertEqual(c.parse_law_table(raw,118),[{'law':8,'bill_id':'118-s30','enacted':'2023-07-18'}])

    def test_offline_cache_rejects_missing_or_changed_bytes(self):
        with tempfile.TemporaryDirectory() as directory:
            cache=c.Sources(Path(directory),offline=True)
            with self.assertRaises(ValueError):cache.get('https://example.test/source')
            cache.offline=False
            with patch.object(c,'fetch',return_value=b'original'):cache.get('https://example.test/source')
            cache.offline=True
            self.assertEqual(cache.get('https://example.test/source')[0],b'original')
            next(cache.directory.glob('*.raw')).write_bytes(b'changed')
            with self.assertRaises(ValueError):cache.get('https://example.test/source')

    def test_family_graph_transitive_across_external_related_ids(self):
        rows=[{'bill_id':'114-hr2','title':'A','versions':[1],'related':['114-s9']},
              {'bill_id':'118-s4','title':'B','versions':[1],'related':['114-s9']},
              {'bill_id':'118-hr5','title':'A','versions':[1],'related':[]}]
        groups=c.family_groups(rows)
        self.assertEqual(len(set(groups.values())),1)

    def test_cluster_bootstrap_is_deterministic_and_paired(self):
        pairs=[{'family_id':'a','probability':.2,'baseline_probability':.2,'outcome':0},
               {'family_id':'b','probability':.2,'baseline_probability':.2,'outcome':1}]
        first=c.bootstrap(pairs,100)
        self.assertEqual(first,c.bootstrap(pairs,100))
        self.assertEqual((first['lower_95'],first['upper_95']),(0,0))

    def test_rerun_routes_saved_pilot_without_generic_substitution(self):
        from engine import workspace as w
        parent={'kind':'audited_cohort'}
        with patch.object(w,'get_experiment',return_value=parent),patch.object(w,'rerun_cohort',return_value={'status':'completed'}) as rerun,patch.object(w,'create_experiment') as generic:
            result=w.start_experiment(None,{},'saved-pilot')
            self.assertEqual(result['status'],'completed');rerun.assert_called_once_with(None,'saved-pilot');generic.assert_not_called()
