"""Public chat adapter parity and evidence boundaries, using isolated local stores."""
import tempfile
import unittest
from pathlib import Path
from engine import intelligence, intelligence_tools, firm_workspace, product_tools
from engine.store import Store


class IntelligenceIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.store = Store(Path(self.tmp.name) / 'db')
        self.store.add('bill', dict(bill_id='119-hr1', dataset='official', family_id='119-hr1', source_url='https://www.govinfo.gov/example', source_name='GovInfo', effective_at='2025-01-03', observed_at='2025-01-04', introduced_at='2025-01-03', title='Energy Research Act', topic='Energy', congress=119, type='hr', source_key='119-hr1'))

    def tearDown(self):
        self.store.close()
        self.tmp.cleanup()

    def call(self, name, args):
        return product_tools.execute(self.store, name, args)

    def test_all_tools_registered_once_and_capabilities_match(self):
        names = [t['function']['name'] for t in product_tools.TOOLS]
        for name in intelligence_tools.NAMES:
            self.assertEqual(names.count(name), 1)
        result, artifact = self.call('inspect_intelligence_capabilities', {})
        self.assertEqual(result, intelligence.capabilities(self.store))
        self.assertEqual(artifact['view'], 'intelligence')
        self.assertIn('causal election scenarios', result['unsupported'])

    def test_saved_analysis_chat_and_direct_reads_agree(self):
        args = dict(dataset='official', cutoff='2025-02-01T00:00:00Z', groups=[dict(name='Energy', filters={'topics':['Energy']})])
        direct = intelligence.analyze(self.store, args)
        result, artifact = self.call('analyze_bill_groups', args)
        self.assertEqual(result['id'], direct['id'])
        self.assertEqual(result['summary'], direct['summary'])
        self.assertEqual(result['summary']['unknown'], 1)
        self.assertIsNone(result['summary']['observed_rate'])
        self.assertNotIn('frozen_rows', result)
        self.assertEqual(artifact['id'], direct['id'])
        read, _ = self.call('inspect_intelligence_report', {'id':direct['id']})
        self.assertEqual(read, result)
        with self.assertRaises(ValueError):
            self.call('analyze_bill_groups', dict(args, filters={'party':'Democratic'}))

    def test_no_receipts_or_scenario_assumptions_create_predictions(self):
        ranking, _ = self.call('rank_saved_forecasts', {'cutoff':'2025-02-01T00:00:00Z'})
        self.assertEqual(ranking['status'], 'unavailable')
        self.assertEqual(ranking['eligible'], 0)
        self.assertEqual(ranking['excluded']['no_saved_receipt'], 1)
        result, _ = self.call('record_legislative_scenario', {'cutoff':'2025-02-01T00:00:00Z', 'question':'Would this pass after a political wave?', 'assumptions':['A party gains congressional seats']})
        self.assertEqual(result['status'], 'unsupported_for_numeric_forecast')
        self.assertIsNone(result['probability'])
        self.assertIsNone(result['probability_shift'])
        self.assertEqual(self.store.db.execute('SELECT COUNT(*) FROM prospective_receipts').fetchone()[0], 0)

    def test_organization_assignment_brief_and_version_guards_through_chat(self):
        profile, artifact = self.call('save_organization_profile', {'name':'Energy client', 'issues':['Energy']})
        self.assertEqual(artifact['view'], 'firm')
        self.assertEqual(artifact['profile_id'], profile['id'])
        workspace, _ = self.call('inspect_organization_workspace', {'profile_id':profile['id']})
        self.assertEqual(workspace['matches'][0]['bill_id'], '119-hr1')
        work_args = {'profile_id':profile['id'], 'bill_id':'119-hr1', 'owner':'Analyst', 'impact':'high'}
        work, _ = self.call('save_bill_assignment', work_args)
        self.assertEqual(work['impact'], 'high')
        with self.assertRaises(ValueError):
            self.call('save_bill_assignment', work_args)
        work2, _ = self.call('save_bill_assignment', dict(work_args, expected_version=work['version'], next_action='Review text'))
        self.assertEqual(work2['version'], 2)
        brief, link = self.call('create_organization_brief', {'profile_id':profile['id']})
        self.assertEqual(brief, firm_workspace.get_brief(self.store, brief['id']))
        self.assertEqual(link['brief_id'], brief['id'])
        self.assertIn('not a passage estimate', brief['snapshot']['work_items'][0]['assessment'])
        listed, _ = self.call('list_organization_profiles', {})
        self.assertEqual(listed['profiles'], [profile])

    def test_stakeholder_record_remains_unverified_and_not_outcome(self):
        profile, _ = self.call('save_organization_profile', {'name':'Client'})
        args = dict(profile_id=profile['id'], bill_id='119-hr1', organization='Association', position='support', statement='We support this legislation.', source_url='https://example.org/statement', published_at='2025-01-05')
        position, _ = self.call('record_stakeholder_position', args)
        self.assertEqual(position['verification_status'], 'user_recorded_unverified')
        self.assertEqual(self.store.records('resolution', 'official'), [])
        with self.assertRaises(ValueError):
            self.call('record_stakeholder_position', dict(args, source_url='javascript:alert(1)'))
