import unittest
from scripts.bicam_inventory_compare_v1 import compare

class CompareTests(unittest.TestCase):
    def official(self):
        return {'all_indexes_accepted':True,'results':[{'congress':c,'bill_type':t,'ids':[f'{t}1-{c}']} for c in range(113,119) for t in ('hr','s')]}
    def test_differences_and_errors_are_distinct(self):
        result=compare(self.official(),[{'bill_id':'hr1-113'},{'bill_id':'hr2-113'}],[{'original':{'bill_id':'s1-113'},'issue':'date'},{'original':{'bill_id':'bad'},'issue':'identity'}])
        self.assertEqual(result['intersection'],1)
        self.assertEqual(result['candidate_not_official'],['hr2-113'])
        self.assertEqual(len(result['official_not_candidate']),11)
        self.assertTrue(result['all_corpus_errors'][0]['official_directory_present'])
        self.assertIsNone(result['all_corpus_errors'][1]['official_directory_present'])
        self.assertFalse(result['candidate_census_complete'])
    def test_reject_duplicate_candidate(self):
        with self.assertRaises(ValueError):
            compare(self.official(),[{'bill_id':'hr1-113'}]*2,[])
    def test_reject_incomplete_official(self):
        official=self.official();official['results'].pop()
        with self.assertRaises(ValueError):
            compare(official,[],[])
