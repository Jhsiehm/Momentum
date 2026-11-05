import unittest
from engine.model import predict
from scripts.diagnose_transfer import raw, artifact, blend, summarize


class TransferDiagnosisTests(unittest.TestCase):
    def setUp(self):
        self.a = dict(weights=[-.7,.2,-.1,.3,.5,-.4,.2],means=[.1]*6,scales=[.2,.3,.4,.5,.6,.7])
        self.b = dict(weights=[-.9,-.2,.4,.1,.6,-.1,.3],means=[.2]*6,scales=[.7,.6,.5,.4,.3,.2])
        self.x = [.1,.2,.3,.4,.5,.6]

    def test_raw_conversion_preserves_probability(self):
        self.assertAlmostEqual(predict(self.a,self.x),predict(artifact(raw(self.a)),self.x),places=14)

    def test_blend_endpoints_and_logit_interpolation(self):
        import math
        self.assertAlmostEqual(predict(blend(self.a,self.b,0),self.x),predict(self.a,self.x),places=14)
        self.assertAlmostEqual(predict(blend(self.a,self.b,1),self.x),predict(self.b,self.x),places=14)
        logit=lambda p: math.log(p/(1-p))
        self.assertAlmostEqual(logit(predict(blend(self.a,self.b,.25),self.x)),.75*logit(predict(self.a,self.x))+.25*logit(predict(self.b,self.x)),places=14)

    def test_invalid_blend_rejected(self):
        with self.assertRaises(ValueError):blend(self.a,self.b,1.1)

    def test_class_error_contributions_reconcile(self):
        rows=[dict(outcome=0,original=.1,challenger=.05),dict(outcome=1,original=.2,challenger=.15)]
        all_rows=summarize(rows,['original','challenger'])
        difference=sum(summarize([r],['original','challenger'])['brier_difference_sum']['challenger'] for r in rows)
        self.assertAlmostEqual(difference,2*(all_rows['metrics']['challenger']['brier']-all_rows['metrics']['original']['brier']))
