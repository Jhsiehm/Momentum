import unittest
from scripts.chronological_weight_updates import partitions, effective
from engine.model import predict
from engine.three_model_experiment import calibrate


class ChronologicalWeightTests(unittest.TestCase):
    def fixture(self):
        train=[dict(congress=113,family_id=str(i),y=int(i<5),label_available_at='2015-01-01') for i in range(200)]
        train.append(dict(congress=114,family_id='new',y=1,label_available_at='2017-01-01'))
        test=[dict(congress=115,family_id='test',cutoff='2017-07-01')]
        return train,test

    def test_anchor_excludes_latest_congress(self):
        train,test=self.fixture()
        self.assertEqual(len(partitions(train,test)),200)
        self.assertEqual({r['congress'] for r in partitions(train,test)},{113})

    def test_future_labels_rejected(self):
        train,test=self.fixture();train[-1]['label_available_at']='2018-01-01'
        with self.assertRaises(AssertionError):partitions(train,test)

    def test_family_overlap_rejected(self):
        train,test=self.fixture();test[0]['family_id']='0'
        with self.assertRaises(AssertionError):partitions(train,test)

    def test_calibration_conversion(self):
        base=dict(weights=[-2,.2,.1,.3,.4,.1,.2],means=[.1]*6,scales=[.5]*6)
        model=dict(base=base,calibration=dict(intercept=.2,slope=1.1));x=[.2]*6
        self.assertAlmostEqual(predict(effective(model),x),calibrate(model['calibration'],predict(base,x)),places=14)
