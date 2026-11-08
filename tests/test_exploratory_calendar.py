import unittest
try:
    import numpy
except ImportError:
    numpy = None
if numpy is not None:
    from scripts.exploratory_calendar import metrics, summarize, intervals, ARMS


@unittest.skipIf(numpy is None, 'Optional research dependency NumPy is not installed')
class ExploratoryCalendarTests(unittest.TestCase):
    def folds(self):
        folds=[]
        for c in (115,116,117):
            predictions=[dict(bill_id=f'{c}-{i}',family_id=f'f{i}',outcome=i%2,control=.3,time=.2,interaction=.25,rate=.4,stage=.35) for i in range(8)]
            m={a:dict(brier=.1,log_loss=.3) for a in list(ARMS)+[a+'_raw' for a in ARMS]+['rate','stage']}
            m['time']=dict(brier=.09,log_loss=.29);m['interaction']=dict(brier=.095,log_loss=.29)
            folds.append(dict(congress=c,metrics=m,predictions=predictions))
        return folds

    def test_all_fold_lead_and_mixed_rejection(self):
        f=self.folds();self.assertEqual(summarize(f)['exploratory_lead'],'time')
        f[0]['metrics']['time']['log_loss']=.31
        # A lower average Brier does not override any period's logloss reversal.
        self.assertEqual(summarize(f)['exploratory_lead'],'interaction')
        f[1]['metrics']['interaction']['brier']=.11
        self.assertIsNone(summarize(f)['exploratory_lead'])
        with self.assertRaises(ValueError):summarize(f[:2])

    def test_metrics_include_empty_bins_and_exact_pair_counts(self):
        m=metrics([0,.5,1],[0,1,1]);self.assertEqual(sum(x['n'] for x in m['reliability']),3)
        self.assertEqual(m['reliability'][9]['n'],1)
        self.assertAlmostEqual(m['brier'],.25/3)
        self.assertIsNone(metrics([.2],[0])['by_outcome']['1']['brier'])

    def test_bootstrap_global_family_reproducible(self):
        a=intervals(self.folds(),draws=100)
        self.assertEqual(a,intervals(self.folds(),draws=100))
        self.assertEqual(a['global_families'],8)
        self.assertEqual(a['invalid'],0)
        self.assertEqual(len(a['intervals']),8)


if __name__=='__main__':unittest.main()
