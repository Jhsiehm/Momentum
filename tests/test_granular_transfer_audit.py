import math
import unittest
from scripts.granular_transfer_audit import metrics, collisions, objective_gradient
from engine.model import predict


class GranularAuditTests(unittest.TestCase):
    def test_error_reconciliation(self):
        rows=[dict(outcome=y,anchor=a,full_update=b,delta=(b-y)**2-(a-y)**2) for y,a,b in [(0,.1,.2),(1,.3,.4)]]
        result=metrics(rows)
        self.assertAlmostEqual(result['delta_mean'],result['update']['brier']-result['anchor']['brier'])
        self.assertEqual(result['positives'],1)

    def test_mixed_feature_vectors(self):
        rows=[dict(bill_id=str(i),features=[i//2],outcome=y) for i,y in enumerate([0,1,0,0])]
        result=collisions(rows)
        self.assertEqual(result['unique_vectors'],2)
        self.assertEqual(result['mixed_rows'],2)
        self.assertEqual(result['positives_in_mixed_cells'],1)

    def test_objective_gradient_matches_finite_difference(self):
        model=dict(weights=[-.8,.2],means=[.1],scales=[.3],l2=.2,iterations=300)
        rows=[dict(x=[.2],y=0),dict(x=[.7],y=1)]
        grad=objective_gradient(model,rows)['objective_gradient']
        def objective():
            loss=sum(-r['y']*math.log(predict(model,r['x']))-(1-r['y'])*math.log(1-predict(model,r['x'])) for r in rows)/len(rows)
            return loss+.5*model['l2']*sum(w*w for w in model['weights'][1:])
        for i in range(2):
            old=model['weights'][i];step=1e-6
            model['weights'][i]=old+step;plus=objective()
            model['weights'][i]=old-step;minus=objective()
            model['weights'][i]=old
            self.assertAlmostEqual(grad[i],(plus-minus)/(2*step),places=8)
