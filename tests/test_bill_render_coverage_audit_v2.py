import hashlib
import unittest

from scripts.bill_context_design_text_v2 import render
from scripts.bill_render_coverage_audit_v2 import audit


class RenderCoverageAuditV2Tests(unittest.TestCase):
    def xml(self, body='', namespace=''):
        return (f'<bill{namespace}><form><congress>113th CONGRESS</congress><legis-num>H. R. 1</legis-num>'
                f'</form><legis-body>{body}</legis-body></bill>').encode()

    def run_audit(self, body='', namespace=''):
        raw = self.xml(body, namespace)
        return audit(raw, '113-hr1', render(raw, '113-hr1'))

    def test_table_cells_and_rows_preserved_in_inventory_not_spans(self):
        result = self.run_audit('<table><tbody><tr><td>A</td><td>B</td></tr><tr><td>C</td><td>D</td></tr></tbody></table>')
        self.assertEqual(result['counts']['cells'], 4)
        self.assertEqual(result['counts']['rows'], 2)
        self.assertEqual(len(result['cell_boundaries']), 2)
        self.assertTrue(all(b['no_whitespace_boundary'] for b in result['cell_boundaries']))
        self.assertIn('unrepresented_table_structure', [w['code'] for w in result['warnings']])
        self.assertFalse(result['source_document_completeness'])

    def test_nested_wrappers_inline_tails_unicode_and_entities(self):
        result = self.run_audit('<section><wrapper><text>A<em>caf&#233; 🐈</em> &amp; Z</text></wrapper></section>')
        segments = [s['text'] for s in result['segments']]
        self.assertIn('café 🐈', segments)
        self.assertIn(' & Z', segments)
        self.assertEqual(result['counts']['source_text_characters'] + result['counts']['inserted_separator_characters'], result['counts']['rendered_characters'])
        self.assertEqual(len({n['path'] for n in result['nodes']}), result['counts']['nodes'])
        self.assertIn('wrapper', result['unrepresented_tags'])

    def test_default_namespace_and_qualified_names_retained(self):
        result = self.run_audit('<section><text>Content</text></section>', ' xmlns="urn:bill"')
        self.assertTrue(all(n['qualified_tag'].startswith('{urn:bill}') for n in result['nodes']))
        self.assertIn('namespace_identity_collapsed', [w['code'] for w in result['warnings']])

    def test_distinct_namespaces_same_local_name_unique_paths(self):
        result = self.run_audit('<a:text xmlns:a="urn:a">A</a:text><b:text xmlns:b="urn:b">B</b:text>')
        nodes = [n for n in result['nodes'] if n['tag'] == 'text']
        self.assertEqual([n['path'].rsplit('/', 1)[-1] for n in nodes], ['text[1]', 'text[2]'])
        self.assertNotEqual(nodes[0]['qualified_tag'], nodes[1]['qualified_tag'])

    def test_empty_and_attributes_nontext(self):
        result = self.run_audit('<section id="s"><text/><table><row><entry colspan="2"/></row></table><graphic href="x"/><formula alt="x"/></section>')
        self.assertEqual(result['counts']['possible_nontext_nodes'], 2)
        self.assertEqual(result['counts']['attribute_nodes'], 4)
        self.assertFalse(result['semantic_structure_complete'])
        self.assertEqual(next(n for n in result['nodes'] if n['tag'] == 'entry')['attributes'], {'colspan': '2'})

    def test_dtd_entity_external_and_utf16_rejected(self):
        for declaration in ('<!DOCTYPE bill [<!ENTITY x "test">]>', '<!DOCTYPE bill []>', '<!DOCTYPE bill [<!ENTITY % x SYSTEM "file:///missing"> %x;]>'):
            for encoding in ('utf-8', 'utf-16'):
                raw = (declaration + self.xml().decode()).encode(encoding)
                with self.assertRaises(ValueError):
                    audit(raw, '113-hr1', {'bill_id': '113-hr1'})

    def test_external_doctype_records_identifiers_without_network(self):
        from unittest.mock import patch
        for declaration, public, system in (
            ('<!DOCTYPE bill PUBLIC "-//US Congress//DTD Bill//EN" "https://example.invalid/bill.dtd">', '-//US Congress//DTD Bill//EN', 'https://example.invalid/bill.dtd'),
            ('<!DOCTYPE bill SYSTEM "file:///definitely-missing.dtd">', None, 'file:///definitely-missing.dtd'),
            ('<!DOCTYPE bill>', None, None),
        ):
            for encoding in ('utf-8', 'utf-16'):
                raw = (declaration + self.xml('<text>Safe &amp; café</text>').decode()).encode(encoding)
                with patch('socket.socket', side_effect=AssertionError('Network access forbidden')):
                    result = audit(raw, '113-hr1', render(raw, '113-hr1'))
                self.assertEqual(result['doctype_declarations'], [dict(name='bill', public_id=public,
                    system_id=system, internal_subset=False, external_resource_resolved=False)])
                self.assertFalse(result['external_resources_resolved'])
                self.assertFalse(result['source_document_completeness'])

    def test_external_undefined_entity_not_silently_dropped(self):
        raw = b'<!DOCTYPE bill SYSTEM "https://example.invalid/bill.dtd">' + self.xml('<text>&unknown;</text>')
        with self.assertRaises(ValueError) as caught:
            audit(raw, '113-hr1', {'bill_id': '113-hr1'})
        self.assertIn('undefined entity', str(caught.exception))

    def test_malformed_xml_error_is_value_error(self):
        for raw in (b'<bill>', b'<bill><x></bill>', b'not xml'):
            with self.assertRaises(ValueError):
                audit(raw, '113-hr1', {'bill_id': '113-hr1'})

    def test_forged_view_text_span_renderer_identity(self):
        raw = self.xml('<section><text>A</text></section>')
        for kind in ('text', 'spans', 'renderer', 'bill_id'):
            view = render(raw, '113-hr1')
            if kind == 'spans':
                view['spans'][0]['start'] += 1
            else:
                view[kind] += 'X'
            with self.assertRaises(ValueError):
                audit(raw, '113-hr1', view)

    def test_exact_byte_binding(self):
        raw = self.xml()
        view = render(raw, '113-hr1')
        view['source'] = {'sha256': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw)}
        self.assertEqual(audit(raw, '113-hr1', view)['raw_bytes'], len(raw))
        for field, wrong in [('sha256', '0' * 64), ('bytes', True), ('bytes', len(raw) + 1)]:
            altered = dict(view, source=dict(view['source'], **{field: wrong}))
            with self.assertRaises(ValueError):
                audit(raw, '113-hr1', altered)

    def test_whitespace_cell_boundaries_not_conflated(self):
        result = self.run_audit('<table><row><entry>A </entry><entry>B</entry></row></table>')
        self.assertFalse(result['cell_boundaries'][0]['no_whitespace_boundary'])


if __name__ == '__main__':
    unittest.main()
