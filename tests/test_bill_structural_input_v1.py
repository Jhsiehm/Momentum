import copy
import unittest

from engine.paper_evaluation import seal
from scripts.bill_context_design_text_v2 import render
from scripts.bill_structural_input_v1 import build, validate


class StructuralInputTests(unittest.TestCase):
    def fixture(self, body, attributes=''):
        raw = (f'<bill{attributes}><form><congress>113th CONGRESS</congress><legis-num>H. R. 1</legis-num>'
               f'</form><legis-body>{body}</legis-body></bill>').encode()
        view = render(raw, '113-hr1')
        return raw, view, seal(view)['hash']

    def make(self, body, attributes=''):
        raw, view, view_hash = self.fixture(body, attributes)
        before = copy.deepcopy(view)
        result = build(raw, '113-hr1', view, view_hash)
        self.assertEqual(before, view)
        self.assertTrue(validate(result, raw, '113-hr1', view, view_hash))
        return result

    def test_tables_empty_cells_spans_and_nested_ownership(self):
        result = self.make('<table><tgroup><colspec colname="c1"/><tbody><row><entry namest="c1" nameend="c2" morerows="1"/>'
                           '<entry>A<table><tr><td>inner</td></tr></table>Z</entry></row>'
                           '<row><entry colspan="2">B</entry></row></tbody></tgroup></table>')
        outer, inner = result['tables']
        self.assertEqual([len(t['rows']) for t in result['tables']], [2, 1])
        self.assertEqual([len(t['cells']) for t in result['tables']], [3, 1])
        self.assertEqual(inner['parent_table_path'], outer['table_path'])
        self.assertEqual(outer['cells'][0]['start'], outer['cells'][0]['end'])
        self.assertEqual(outer['cells'][0]['attributes'], {'namest': 'c1', 'nameend': 'c2', 'morerows': '1'})
        self.assertEqual(outer['cells'][1]['text'], 'AinnerZ')
        self.assertFalse(outer['grid_coordinates_inferred'])
        self.assertFalse(outer['span_attributes_interpreted'])

    def test_unicode_entities_inline_tails_partition(self):
        result = self.make('<section><text>🐈 café<em>é</em> &amp; e&#769;</text></section>')
        parts = result['segments'] + result['inserted_separators']
        parts.sort(key=lambda s: (s['start'], s['end']))
        self.assertEqual(''.join(s['text'] for s in parts), result['text'])
        for node in result['nodes']:
            for child in node['children_paths']:
                self.assertEqual(next(n for n in result['nodes'] if n['path'] == child)['parent_path'], node['path'])
        for part in parts:
            self.assertEqual(result['text'][part['start']:part['end']], part['text'])
        self.assertFalse(result['raw_byte_offsets_available'])

    def test_namespace_collisions_and_qualified_attributes(self):
        result = self.make('<a:text a:unit="x" unit="y">A</a:text><b:text b:unit="z">B</b:text>',
                           ' xmlns="urn:bill" xmlns:a="urn:a" xmlns:b="urn:b"')
        nodes = [n for n in result['nodes'] if n['tag'] == 'text']
        self.assertEqual([n['qualified_tag'] for n in nodes], ['{urn:a}text', '{urn:b}text'])
        self.assertEqual(nodes[0]['attributes'], {'{urn:a}unit': 'x', 'unit': 'y'})
        self.assertNotEqual(nodes[0]['path'], nodes[1]['path'])
        self.assertEqual(result['counts']['attributes'], 3)

    def test_fraction_context_not_numeric_normalization(self):
        result = self.make('<text>4<fraction style="stacked">1/2</fraction> hours. NW<fraction>1/4</fraction> sec.21 '
                           '<m:mfrac xmlns:m="urn:math"><m:mi>a</m:mi><m:mn>2</m:mn></m:mfrac></text>')
        self.assertEqual([f['text'] for f in result['fractions']], ['1/2', '1/4', 'a2'])
        self.assertIn('41/2 hours', result['text'])
        self.assertIn('NW1/4 sec.21', result['text'])
        for fraction in result['fractions']:
            self.assertFalse(fraction['numeric_value_inferred'])
            self.assertEqual(result['text'][fraction['context_start']:fraction['context_end']], fraction['context_text'])
        self.assertEqual(len(result['fractions'][2]['children_paths']), 2)

    def test_orphan_rows_cells_and_cells_without_row(self):
        result = self.make('<row><entry>A</entry></row><entry>B</entry><table><entry>C</entry><row/></table>')
        self.assertEqual(len(result['orphan_row_paths']), 1)
        self.assertEqual(len(result['orphan_cell_paths']), 2)
        self.assertEqual(len(result['tables'][0]['orphan_cell_paths']), 1)
        self.assertIsNone(result['tables'][0]['cells'][0]['row_path'])

    def test_authentication_rejects_forgery_and_identity(self):
        raw, view, view_hash = self.fixture('<text>A</text>')
        for identity in ('113-hr2', '0-hr1', None):
            with self.assertRaises(ValueError):
                build(raw, identity, view, view_hash)
        with self.assertRaises(ValueError):
            build(raw, '113-hr1', view, '0' * 64)
        forged = copy.deepcopy(view)
        forged['text'] += 'X'
        with self.assertRaises(ValueError):
            build(raw, '113-hr1', forged, seal(forged)['hash'])
        with self.assertRaises(ValueError):
            build(raw.replace(b'>A<', b'>B<'), '113-hr1', view, view_hash)

    def test_canonical_validation_detects_every_component_change(self):
        raw, view, view_hash = self.fixture('<table><row><entry x="1">A</entry></row></table><fraction>1/2</fraction>')
        result = build(raw, '113-hr1', view, view_hash)
        for key in result:
            altered = copy.deepcopy(result)
            del altered[key]
            with self.assertRaises(ValueError, msg=key):
                validate(altered, raw, '113-hr1', view, view_hash)
        altered = copy.deepcopy(result)
        altered['tables'][0]['cells'][0]['attributes']['x'] = '2'
        with self.assertRaises(ValueError):
            validate(altered, raw, '113-hr1', view, view_hash)
        altered = copy.deepcopy(result)
        altered['raw_byte_offsets_available'] = 0
        with self.assertRaises(ValueError):
            validate(altered, raw, '113-hr1', view, view_hash)

    def test_external_doctype_offline_and_internal_subset_rejection(self):
        raw, view, view_hash = self.fixture('<text>A</text>')
        external = b'<!DOCTYPE bill SYSTEM "file:///not-present.dtd">' + raw
        sidecar = build(external, '113-hr1', view, view_hash)
        self.assertFalse(sidecar['external_resources_resolved'])
        self.assertEqual(len(sidecar['doctype_declarations']), 1)
        with self.assertRaises(ValueError):
            build(b'<!DOCTYPE bill []>' + raw, '113-hr1', view, view_hash)


if __name__ == '__main__':
    unittest.main()
