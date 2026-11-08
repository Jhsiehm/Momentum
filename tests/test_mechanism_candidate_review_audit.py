import copy
import unittest
from scripts.mechanism_candidate_review_audit import validate_review


class ReviewIntegrityTests(unittest.TestCase):
    def setUp(self):
        self.packet={'records':[{'bill_id':'b','misses':[{'effect_index':2,'mechanism':'require'}],'proposals':[{'proposal_id':'p'}]}]}
        self.views={'b':{'text':'A shall act.'}}
        evidence={'start':0,'end':12,'quote':'A shall act.'}
        self.review={'human_certified':False,'historical_feature_eligible':False,'records':[{'bill_id':'b',
            'miss_reviews':[{'effect_index':2,'mechanism':'require','disposition':'vocabulary_gap','rationale':'Reason','evidence':evidence}],
            'proposal_reviews':[{'proposal_id':'p','disposition':'uncertain','rationale':'Reason','evidence':evidence}]}]}

    def test_complete_primary_and_peer(self):
        self.assertEqual(sum(validate_review(self.packet,self.review,self.views).values()),2)
        for field in ('miss_reviews','proposal_reviews'):
            self.review['records'][0][field][0]['disposition']='agree'
        self.assertEqual(sum(validate_review(self.packet,self.review,self.views,peer=True).values()),2)

    def test_missing_duplicate_and_unknown_items_rejected(self):
        for change in ('missing','duplicate','unknown'):
            review=copy.deepcopy(self.review);items=review['records'][0]['miss_reviews']
            if change=='missing':items.clear()
            if change=='duplicate':items.append(copy.deepcopy(items[0]))
            if change=='unknown':items[0]['effect_index']=999
            with self.assertRaises(ValueError):validate_review(self.packet,review,self.views)

    def test_tampered_evidence_and_flags_rejected(self):
        for change in ('quote','offset','mechanism','certification','disposition'):
            review=copy.deepcopy(self.review);item=review['records'][0]['miss_reviews'][0]
            if change=='quote':item['evidence']['quote']='wrong'
            if change=='offset':item['evidence']['start']=True
            if change=='mechanism':item['mechanism']='tax'
            if change=='certification':review['human_certified']=True
            if change=='disposition':item['disposition']='accepted'
            with self.assertRaises(ValueError):validate_review(self.packet,review,self.views)

    def test_boolean_identity_and_contradictory_view_rejected(self):
        packet=copy.deepcopy(self.packet);review=copy.deepcopy(self.review)
        packet['records'][0]['misses'][0]['effect_index']=1
        review['records'][0]['miss_reviews'][0]['effect_index']=True
        with self.assertRaises(ValueError):validate_review(packet,review,self.views)
        packet=copy.deepcopy(self.packet);packet['records'][0]['source_view_hash']='a'*64
        review=copy.deepcopy(self.review);review['records'][0]['source_view_hash']='b'*64
        with self.assertRaises(ValueError):validate_review(packet,review,self.views)
