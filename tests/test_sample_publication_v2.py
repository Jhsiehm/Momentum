"""Portable regression fixtures for the introduction/issue-date distinction."""
import copy
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET

from engine import cohort, sample_publication_v2 as v2


class FixtureSources:
    def get(self, url):
        return b'''<billStatus><bill><congress>118</congress><type>HR</type><number>5925</number>
        <introducedDate>2023-10-11</introducedDate><title>Example bill</title>
        <textVersions><item><formats><item><url>https://www.govinfo.gov/content/pkg/BILLS-118hr5925ih/xml/BILLS-118hr5925ih.xml</url></item></formats></item></textVersions>
        </bill></billStatus>''', {'url': url, 'sha256': 'fixture'}


def audit(intro='2023-10-11', issued='2023-10-25', available='2023-11-07T00:00:00Z'):
    mods = ET.fromstring(f'''<mods xmlns="http://www.loc.gov/mods/v3">
    <recordInfo><recordIdentifier>BILLS-118hr5925ih</recordIdentifier></recordInfo>
    <titleInfo><title>Example bill</title></titleInfo><originInfo><dateIssued>{issued}</dateIssued></originInfo>
    <extension><action date="{intro}">Mr. Example introduced the following bill</action>
    <action date="2023-10-25">Referred to committee</action></extension></mods>''')
    return mods, {'package': 'BILLS-118hr5925ih', 'issued_at': issued + 'T00:00:00Z', 'available_at': available}


class RevisedPublicationTests(unittest.TestCase):
    def row(self):
        return v2.sample_bill(FixtureSources(), 118, 'hr', 5925, {'age_days': 180}, {})

    def test_issue_date_does_not_shift_introduction_checkpoint(self):
        with patch.object(v2, 'package_audit', return_value=audit()):
            row = self.row()
        self.assertEqual(row['introduced_at'], '2023-10-11T23:59:59Z')
        self.assertEqual(row['cutoff'], '2024-04-08T23:59:59Z')
        self.assertEqual(row['versions'][0]['issued_at'], '2023-10-25T00:00:00Z')
        self.assertEqual(row['versions'][0]['available_at'], '2023-11-07T00:00:00Z')
        self.assertIsNone(row['exclusion'])
        self.assertEqual(row['y'], 0)
        self.assertEqual(row['x'], [0, 180/730, 1/30, 153/730, 0, 0])

    def test_contradictory_introduction_fails(self):
        with patch.object(v2, 'package_audit', return_value=audit(intro='2023-10-12')):
            with self.assertRaisesRegex(ValueError, 'Conflicting introduction'):
                self.row()

    def test_late_availability_still_excludes(self):
        with patch.object(v2, 'package_audit', return_value=audit(available='2024-05-01T00:00:00Z')):
            row = self.row()
        self.assertEqual(row['exclusion'], 'Introduction publication not available by checkpoint')
        self.assertEqual(row['eligible_packages'], [])

    def test_original_math_unchanged_for_same_day_publication(self):
        fixture = audit(issued='2023-10-11')
        with patch.object(cohort, 'package_audit', return_value=copy.deepcopy(fixture)):
            original = cohort.sample_bill(FixtureSources(), 118, 'hr', 5925, {'age_days': 180}, {})
        with patch.object(v2, 'package_audit', return_value=copy.deepcopy(fixture)):
            revised = self.row()
        revised['versions'][0].pop('introduction_validation')
        self.assertEqual(revised, original)


if __name__ == '__main__':
    unittest.main()

class V2WorkspaceRoutingTests(unittest.TestCase):
    def test_v2_reruns_keep_version_and_original_result(self):
        import tempfile
        from pathlib import Path
        from unittest.mock import patch
        from engine import workspace, sample_publication_v2
        from engine.store import Store
        def result():
            return dict(status='completed',available=33,publication_eligible_count=33,results=[{}]*33,blockers=[],preflight={},cohort_hash='c',reproducibility_hash='v2',config={'dataset':'official','congress':118,'age_days':180},attempted=40)
        with tempfile.TemporaryDirectory() as directory:
            store=Store(Path(directory)/'test.sqlite'); workspace.initialize(store)
            with patch.object(sample_publication_v2,'run',side_effect=result), patch('engine.sample_publication.run',side_effect=AssertionError('Wrong v1 route')):
                first=workspace.publish_sample_publication(store,version=2)
                second=workspace.start_experiment(store,first['config'],first['id'])
                brief,_=workspace.execute_tool(store,'rerun_experiment',{'experiment_id':first['id']})
                self.assertEqual(second['kind'],'sample_publication_study_v2')
                self.assertEqual(second['parent_id'],first['id'])
                self.assertEqual(brief['available'],33)
                self.assertEqual(workspace.get_experiment(store,first['id'])['reproducibility_hash'],'v2')
            store.close()
