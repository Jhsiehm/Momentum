"""Independent synthetic adversarial structural-input checks; no design corpus."""
import copy
import hashlib
import unittest
from unittest.mock import patch

from engine.paper_evaluation import seal
from scripts.bill_context_design_text_v2 import render
from scripts.bill_structural_input_v1 import build, validate


class IndependentStructuralInputTests(unittest.TestCase):
    def fixture(self, body, declaration=''):
        raw = (declaration + '<bill xmlns:a="urn:a" xmlns:b="urn:b"><form>'
               '<congress>113th CONGRESS</congress><legis-num>H. R. 1</legis-num>'
               '</form><legis-body>' + body + '</legis-body></bill>').encode()
        view = render(raw, '113-hr1')
        view['source'] = dict(sha256=hashlib.sha256(raw).hexdigest(), bytes=len(raw))
        return raw, view, seal(view)['hash']

    def build_fixture(self, body, declaration=''):
        raw, view, view_hash = self.fixture(body, declaration)
        sidecar = build(raw, '113-hr1', view, view_hash)
        return raw, view, view_hash, sidecar

    def test_nested_table_membership_does_not_duplicate_inner_cells(self):
        _, _, _, result = self.build_fixture('<table><row><entry>A<table><row><entry>B</entry>'
            '<entry>C</entry></row></table>D</entry><entry>E</entry></row></table>')
        outer, inner = result['tables']
        self.assertIsNone(outer['parent_table_path'])
        self.assertEqual(inner['parent_table_path'], outer['table_path'])
        self.assertEqual(len(outer['rows']), 1)
        self.assertEqual(len(inner['rows']), 1)
        self.assertEqual([c['text'] for c in outer['cells']], ['ABCD', 'E'])
        self.assertEqual([c['text'] for c in inner['cells']], ['B', 'C'])
        outer_paths = set(c['path'] for c in outer['cells'])
        inner_paths = set(c['path'] for c in inner['cells'])
        self.assertFalse(outer_paths & inner_paths)
        self.assertEqual(set(outer['rows'][0]['cell_paths']), outer_paths)
        self.assertEqual(set(inner['rows'][0]['cell_paths']), inner_paths)

    def test_empty_cells_and_merged_cell_attributes_are_literal(self):
        _, view, _, result = self.build_fixture('<table><tgroup cols="3"><colspec colname="x"/>'
            '<spanspec spanname="wide" namest="x" nameend="z"/><tbody><row>'
            '<entry spanname="wide" morerows="2"/><entry colspan="bogus" rowspan="-1">🐈é</entry>'
            '</row><row/></tbody></tgroup></table>')
        table = result['tables'][0]
        self.assertEqual(len(table['rows']), 2)
        empty, text = table['cells']
        self.assertEqual(empty['start'], empty['end'])
        self.assertEqual(empty['text'], '')
        self.assertEqual(empty['attributes'], {'spanname': 'wide', 'morerows': '2'})
        self.assertEqual(text['attributes'], {'colspan': 'bogus', 'rowspan': '-1'})
        self.assertEqual(text['end'] - text['start'], 2)
        self.assertEqual(view['text'][text['start']:text['end']], '🐈é')
        self.assertEqual(table['rows'][1]['cell_paths'], [])

    def test_orphans_not_attached_to_inapplicable_ancestor_row(self):
        _, _, _, result = self.build_fixture('<row><entry>outside</entry><table><entry>inside orphan</entry>'
            '<row><entry>normal</entry></row></table></row><entry>alone</entry>')
        table = result['tables'][0]
        self.assertEqual(len(table['rows']), 1)
        self.assertEqual(len(table['orphan_cell_paths']), 1)
        self.assertEqual(len(result['orphan_row_paths']), 1)
        self.assertEqual(len(result['orphan_cell_paths']), 2)
        orphan = next(c for c in table['cells'] if c['text'] == 'inside orphan')
        self.assertIsNone(orphan['row_path'])

    def test_fraction_context_preserves_ambiguity_and_mathml_children(self):
        _, view, _, result = self.build_fixture('<text>4<fraction>1/2</fraction> hours; NW'
            '<fraction>1/4</fraction> sec.; <m:mfrac xmlns:m="urn:math"><m:mi>x</m:mi>'
            '<m:mn>2</m:mn></m:mfrac> &amp; café🐈</text>')
        fractions = result['fractions']
        self.assertEqual([f['text'] for f in fractions], ['1/2', '1/4', 'x2'])
        self.assertIn('41/2 hours; NW1/4 sec.; x2 & café🐈', result['text'])
        self.assertEqual(result['text'], view['text'])
        self.assertEqual(len(fractions[2]['children_paths']), 2)
        for f in fractions:
            self.assertEqual(view['text'][f['start']:f['end']], f['text'])
            self.assertEqual(view['text'][f['context_start']:f['context_end']], f['context_text'])
            self.assertLessEqual(f['context_start'], f['start'])
            self.assertGreaterEqual(f['context_end'], f['end'])

    def test_namespace_attribute_collision_retains_qualified_names(self):
        _, _, _, result = self.build_fixture('<a:thing a:x="one" b:x="two" x="three"/>'
                                             '<b:thing b:x="four"/>')
        nodes = [n for n in result['nodes'] if n['tag'] == 'thing']
        self.assertEqual([n['qualified_tag'] for n in nodes], ['{urn:a}thing', '{urn:b}thing'])
        self.assertNotEqual(nodes[0]['path'], nodes[1]['path'])
        self.assertEqual(nodes[0]['attributes'], {'{urn:a}x': 'one', '{urn:b}x': 'two', 'x': 'three'})

    def test_hash_binding_and_bill_identity_fail_closed(self):
        raw, view, h = self.fixture('<text>X</text>')
        for replacement in ('', '0' * 64, True, None):
            with self.subTest(hash=replacement), self.assertRaises(ValueError):
                build(raw, '113-hr1', view, replacement)
        with self.assertRaises(ValueError):
            build(raw, '113-hr2', view, h)
        changed = copy.deepcopy(view)
        changed['source']['bytes'] += 1
        with self.assertRaises(ValueError):
            build(raw, '113-hr1', changed, seal(changed)['hash'])

    def test_canonical_validation_rejects_tampering_without_mutation(self):
        raw, view, h, result = self.build_fixture('<table><row><entry a:x="y">X</entry></row></table>'
                                                '<fraction>1/2</fraction>')
        original = copy.deepcopy(result)
        mutations = [lambda x: x['nodes'][0].update(start=999),
                     lambda x: x['nodes'][0]['children_paths'].reverse(),
                     lambda x: x['tables'][0]['rows'][0]['cell_paths'].clear(),
                     lambda x: x['tables'][0]['cells'][0]['attributes'].clear(),
                     lambda x: x['fractions'][0].update(text='0.5'),
                     lambda x: x.update(text=x['text'] + ' '),
                     lambda x: x.update(unrecognized=True)]
        validate(result, raw, '113-hr1', view, h)
        for mutate in mutations:
            candidate = copy.deepcopy(result)
            mutate(candidate)
            with self.subTest(mutation=mutate), self.assertRaises(ValueError):
                validate(candidate, raw, '113-hr1', view, h)
        self.assertEqual(result, original)

    def test_build_is_deterministic_and_inputs_remain_unchanged(self):
        raw, view, h = self.fixture('<text>A<em>é🐈</em> &amp; B</text>')
        original = copy.deepcopy(view)
        first = build(raw, '113-hr1', view, h)
        second = build(raw, '113-hr1', view, h)
        self.assertEqual(first, second)
        self.assertEqual(view, original)

    def test_external_doctype_cannot_trigger_network(self):
        declaration = '<!DOCTYPE bill SYSTEM "https://example.invalid/unavailable.dtd">'
        with patch('socket.socket', side_effect=AssertionError('network forbidden')):
            _, _, _, result = self.build_fixture('<text>local</text>', declaration)
        self.assertEqual(result['text'].count('local'), 1)


if __name__ == '__main__':
    unittest.main()
