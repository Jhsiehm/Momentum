import copy
import unittest
from scripts.mechanism_design_extractor_v2 import extract
from scripts.run_mechanism_context_v2 import check_context,invariant_signature
from scripts.mechanism_design_extractor import extract as extract_v1
from tests.test_mechanism_design_extractor import view


class ContextRunnerTests(unittest.TestCase):
    def fixture(self):
        v=view('<section><header>Authority</header><text>The Secretary shall do the following:</text><quoted-block><section><text>Report annually.</text></section></quoted-block></section>')
        return v,extract(v)

    def test_structure_and_behavior(self):
        v,out=self.fixture();counts=check_context(out,v)
        self.assertGreater(counts['relations']['quoted_block_boundary'],0)
        self.assertEqual(invariant_signature(out),invariant_signature(extract_v1(v)))

    def test_tampered_span_boundary_and_relationship_rejected(self):
        for mode in ('pool','boundary','ancestor','missing'):
            v,out=self.fixture()
            if mode=='pool':out['structural_spans'][0]['tag']='invented'
            if mode=='boundary':
                hit=next(h for c in out['candidates'] for h in c['hits'] if h['structural_boundaries'])
                hit['structural_boundaries'][0]['ancestor_path']='/unrelated'
            if mode=='ancestor':
                link=next(r for c in out['candidates'] for h in c['hits'] for r in h['structural_context'] if r['relation']=='ancestor_preceding_direct_text')
                link['ancestor_path']='/unrelated'
            if mode=='missing':
                hit=next(h for c in out['candidates'] for h in c['hits'] if h['structural_boundaries'])
                hit['structural_boundaries'][0]['span_id']='unknown'
            with self.assertRaises(ValueError):check_context(out,v)
