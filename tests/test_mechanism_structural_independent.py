"""Independent synthetic boundary audit; no real design/quality corpus accessed."""
import copy
import hashlib
import unittest
from unittest.mock import patch

from engine.paper_evaluation import seal
from scripts.bill_context_design_text_v2 import render
from scripts.bill_structural_input_v1 import build
from scripts.mechanism_design_extractor_v5 import extract as baseline
from scripts.mechanism_structural_extractor_v1 import extract


class IndependentStructuralExtractorTests(unittest.TestCase):
    def fixture(self, fragment):
        raw = ('<bill><form><congress>113th CONGRESS</congress><legis-num>H. R. 1</legis-num>'
               '</form><legis-body><section><text>' + fragment + '</text></section></legis-body></bill>').encode()
        view = render(raw, '113-hr1')
        view['source'] = {'sha256': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw)}
        h = seal(view)['hash']
        sidecar = build(raw, '113-hr1', view, h)
        view['view_hash'] = h
        return view, sidecar

    def probe(self, view, sidecar, a, b):
        raw = {'candidates': [{'candidate_id': 'probe', 'mechanism': 'require',
            'start': 0, 'end': len(view['text']), 'quote': view['text'],
            'hits': [{'start': a, 'end': b, 'quote': view['text'][a:b]}]}]}
        with patch('scripts.mechanism_structural_extractor_v1.extract_baseline', return_value=raw):
            result = extract(view, sidecar)
        self.assertEqual(result['raw_output'], raw)
        self.assertEqual(result['full_context_text'], view['text'])
        return result['boundary_decisions'][0]

    def test_nested_outer_containment_does_not_mask_inner_crossing(self):
        view, sidecar = self.fixture('<table><row><entry>A<table><row><entry>B</entry><entry>C</entry>'
                                    '</row></table>D</entry><entry>E</entry></row></table>')
        a = view['text'].index('ABCDE') + 1
        d = self.probe(view, sidecar, a, a + 2)
        self.assertEqual(d['decision'], 'flag_cell_boundary')
        self.assertEqual(len(d['containing_cell_paths']), 1)
        self.assertEqual({b['offset'] for b in d['boundary_evidence']}, {a + 1})
        self.assertEqual(len(d['boundary_evidence']), 2)
        self.assertTrue(all(b['table_path'] == sidecar['tables'][1]['table_path'] for b in d['boundary_evidence']))

    def test_exact_half_open_touch_and_inside_cell_are_retained(self):
        view, sidecar = self.fixture('<table><row><entry>AB</entry><entry>CD</entry></row></table>')
        a = view['text'].index('ABCD')
        for start, end in [(a, a + 2), (a + 2, a + 4), (a + 1, a + 2)]:
            with self.subTest(interval=(start, end)):
                d = self.probe(view, sidecar, start, end)
                self.assertEqual(d['decision'], 'retain')
                self.assertEqual(d['boundary_evidence'], [])
        self.assertEqual(self.probe(view, sidecar, a + 1, a + 3)['decision'], 'flag_cell_boundary')

    def test_empty_and_orphan_cells_are_conservative_barriers(self):
        view, sidecar = self.fixture('A<entry/>B')
        a = view['text'].index('AB')
        d = self.probe(view, sidecar, a, a + 2)
        self.assertEqual(d['decision'], 'flag_cell_boundary')
        self.assertEqual(len(d['boundary_evidence']), 2)
        self.assertEqual(d['intersecting_cell_paths'], [])
        self.assertTrue(all(b['table_path'] is None for b in d['boundary_evidence']))
        self.assertEqual(self.probe(view, sidecar, a, a + 1)['decision'], 'retain')

    def test_fraction_and_inline_nodes_preserve_ambiguous_unicode_context(self):
        view, sidecar = self.fixture('🐈 Agency shall act after 4<fraction>1/2</fraction> hours; NW'
                                    '<fraction>1/4</fraction> section <em>café</em>.')
        a = view['text'].index('4')
        d = self.probe(view, sidecar, a, a + 4)
        self.assertEqual(d['decision'], 'retain')
        self.assertEqual(d['quote'], '41/2')
        self.assertEqual([f['text'] for f in d['fraction_context']], ['1/2', '1/4'])
        self.assertEqual([f['overlaps_hit'] for f in d['fraction_context']], [True, False])
        for f in d['fraction_context']:
            self.assertFalse(f['numeric_value_inferred'])
            self.assertEqual(f['context_text'], view['text'][f['context_start']:f['context_end']])

    def test_raw_v5_result_and_entire_inputs_unchanged(self):
        view, sidecar = self.fixture('The Secretary shall submit a report within 30 days. '
                                    '<table><row><entry>No person </entry><entry>may act.</entry></row></table>')
        original = copy.deepcopy((view, sidecar))
        result = extract(view, sidecar)
        self.assertEqual(result['raw_output'], baseline(view))
        self.assertEqual(result['full_context_text'], view['text'])
        self.assertEqual((view, sidecar), original)
        self.assertEqual(result, extract(view, sidecar))
        ids = [d['identity'] for d in result['boundary_decisions'] if d['decision'] == 'retain']
        self.assertEqual(result['usable_hits'], ids)
        self.assertFalse(result['semantic_labels_accepted'])

    def test_metric_overlap_is_half_open_and_combines_prior_retention(self):
        from scripts.run_mechanism_structural_v1 import metrics
        hits = [{'start': 10, 'end': 20, 'quote': 'x'}, {'start': 20, 'end': 30, 'quote': 'y'}]
        baseline_output = {'candidates': [{'mechanism': 'require', 'hits': hits}]}
        prior = {('require', 10, 20): {'status': 'retain'}, ('require', 20, 30): {'status': 'flagged'}}
        decisions = [{'identity': {'mechanism': 'require', 'start': 10, 'end': 20}, 'decision': 'flag_cell_boundary'},
                     {'identity': {'mechanism': 'require', 'start': 20, 'end': 30}, 'decision': 'retain'}]
        reference = {'effects': [{'mechanism': 'require', 'start': 0, 'end': 10},
                                 {'mechanism': 'require', 'start': 10, 'end': 20},
                                 {'mechanism': 'require', 'start': 20, 'end': 30},
                                 {'mechanism': 'require', 'start': 30, 'end': 40},
                                 {'mechanism': 'authorize', 'start': 10, 'end': 30}]}
        cats, effects = metrics(reference, baseline_output, prior, decisions)
        self.assertEqual(cats['require'], dict(raw_hits=2, boundary_usable=1, boundary_flagged=1,
            prior_retained=1, combined_retained=0, reference_effects=4, raw_overlap=2,
            boundary_overlap=1, prior_retained_overlap=1, combined_overlap=0))
        self.assertEqual([e['raw_overlap'] for e in effects], [False, True, True, False, False])
        self.assertEqual(cats['authorize']['reference_effects'], 1)
        self.assertEqual(cats['authorize']['raw_overlap'], 0)

    def test_stale_view_source_and_structural_bindings_rejected(self):
        view, sidecar = self.fixture('<table><row><entry>A</entry></row></table><fraction>1/2</fraction>')
        mutations = [lambda s: s['source'].update(view_hash='0' * 64),
                     lambda s: s['source'].update(raw_sha256='0' * 64),
                     lambda s: s['tables'][0]['rows'][0]['cell_paths'].clear(),
                     lambda s: s['fractions'][0].update(text='0.5'),
                     lambda s: s['nodes'].append(copy.deepcopy(s['nodes'][0])),
                     lambda s: s.update(text=s['text'] + 'x')]
        for mutate in mutations:
            changed = copy.deepcopy(sidecar)
            mutate(changed)
            with self.subTest(mutation=mutate), self.assertRaises(ValueError):
                extract(view, changed)
        changed_view = copy.deepcopy(view)
        changed_view['note'] = 'tampered full view'
        with self.assertRaises(ValueError):
            extract(changed_view, sidecar)


if __name__ == '__main__':
    unittest.main()
