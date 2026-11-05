import unittest
from engine.macro_pilot import parse_csv,macro_features,vintage
class MacroPilotTests(unittest.TestCase):
    def test_strict_previous_month_vintage(self):
        self.assertEqual(vintage('2023-01-01T23:59:59Z'),'2022-12-31')
        self.assertEqual(vintage('2024-03-25T23:59:59Z'),'2024-02-29')
    def test_vintage_must_match_and_future_values_fail(self):
        raw=b'observation_date,UNRATE_20230131\n2022-12-01,3.5\n'
        self.assertEqual(parse_csv(raw,'UNRATE','2023-01-31'),{'2022-12-01':3.5})
        for content in (raw.replace(b'20230131',b'20240131'),raw.replace(b'2022-12-01',b'2023-02-01'),raw.replace(b'3.5',b'nan')):
            with self.assertRaises(ValueError):parse_csv(content,'UNRATE','2023-01-31')
    def test_inflation_computed_inside_same_vintage(self):
        data={'UNRATE':{'2022-12-01':3.5},'CPIAUCSL':{'2021-12-01':100,'2022-12-01':108}}
        x,dates=macro_features(data,'2023-01-31')
        self.assertAlmostEqual(x[1],8);self.assertEqual(x[0],3.5)
        del data['CPIAUCSL']['2021-12-01']
        with self.assertRaises(ValueError):macro_features(data,'2023-01-31')
    def test_stale_data_fails_instead_of_silent_imputation(self):
        with self.assertRaises(ValueError):macro_features({'UNRATE':{'2020-01-01':4},'CPIAUCSL':{'2020-01-01':100,'2021-01-01':103}},'2023-01-31')

class MacroRerunTests(unittest.TestCase):
    def test_chat_rerun_reproduces_macro_instead_of_different_model(self):
        import tempfile
        from pathlib import Path
        from unittest.mock import patch
        from engine.store import Store
        from engine import workspace
        with tempfile.TemporaryDirectory() as directory:
            s=Store(Path(directory)/'db');workspace.initialize(s)
            run=dict(id='macro-test',kind='macro_pilot',status='completed',created_at='2026-11-03',config=dict(dataset='official',congress=118,age_days=180),reproducibility_hash='same',metrics=None)
            workspace.save_experiment(s,run)
            with patch('engine.macro_pilot.run',return_value={'reproducibility_hash':'same'}) as reproduce:
                result,artifact=workspace.execute_tool(s,'rerun_experiment',{'experiment_id':'macro-test'})
                self.assertEqual(result['id'],'macro-test');self.assertEqual(artifact['id'],'macro-test');reproduce.assert_called_once_with(offline=True)
            with patch('engine.macro_pilot.run',return_value={'reproducibility_hash':'different'}):
                with self.assertRaises(ValueError):workspace.execute_tool(s,'rerun_experiment',{'experiment_id':'macro-test'})
            self.assertEqual(len(workspace.experiment_list(s)),1)
            s.close()
