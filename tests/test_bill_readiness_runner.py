import unittest
from scripts.run_bill_readiness_audit import authenticate_source,population,sha,CODE

class ReadinessRunnerTests(unittest.TestCase):
    def test_wrong_bytes_and_boolean_size_fail(self):
        raw=b'xml';good=dict(bytes=3,sha256=sha(raw));authenticate_source(good,raw)
        for bad in (dict(good,bytes=True),dict(good,bytes=4),dict(good,sha256='0'*64)):
            with self.assertRaises(ValueError):authenticate_source(bad,raw)
    def test_quality_firewall_and_fixed_population(self):
        rows=[dict(bill_id='113-hr'+str(i)) for i in range(1,41)]
        pilot=dict(selection=[dict(x,partition='design') for x in rows])
        self.assertEqual(len(population(rows,pilot)),40)
        with self.assertRaises(ValueError):population(rows[:-1],pilot)
        with self.assertRaises(ValueError):population(rows[:-1]+rows[:1],pilot)
        pilot['selection'][0]['partition']='quality'
        with self.assertRaises(ValueError):population(rows,pilot)
    def test_manifest_unique(self):
        self.assertEqual(len(CODE),len(set(CODE)))
        self.assertIn('tests/test_readiness_independent.py',CODE)

if __name__=='__main__':unittest.main()
