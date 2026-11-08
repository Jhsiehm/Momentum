import tempfile
import unittest
from pathlib import Path
from scripts.run_mechanism_design_extractor import locator_diagnostic, persist


class DesignRunnerTests(unittest.TestCase):
    def test_context_overlap_does_not_count_as_trigger_hit(self):
        out = {'candidates': [{'mechanism': 'require', 'start': 0, 'end': 12,
                              'hits': [{'start': 0, 'end': 2}]}]}
        ref = {'effects': [{'mechanism': 'require', 'start': 4, 'end': 8, 'quote': 'must'}]}
        result = locator_diagnostic(out, ref, 'xxxxmustxxxx')
        self.assertEqual(result['require'], {'reference_effects': 1, 'effects_with_trigger_overlap': 0})
        out['candidates'][0]['hits'] = [{'start': 4, 'end': 8}]
        self.assertEqual(locator_diagnostic(out, ref, 'xxxxmustxxxx')['require']['effects_with_trigger_overlap'], 1)
        out['candidates'][0]['mechanism'] = 'authorize'
        self.assertEqual(locator_diagnostic(out, ref, 'xxxxmustxxxx')['require']['effects_with_trigger_overlap'], 0)

    def test_quote_mismatch_rejected(self):
        with self.assertRaises(Exception):
            locator_diagnostic({'candidates': []}, {'effects': [{'mechanism': 'require', 'start': 0, 'end': 1, 'quote': 'y'}]}, 'x')

    def test_immutable_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp)/'record.json'
            self.assertEqual(persist(p, {'x': 1}), persist(p, {'x': 1}))
            with self.assertRaises(Exception):
                persist(p, {'x': 2})
