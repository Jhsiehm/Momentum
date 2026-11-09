"""Independent v2 compatibility/security contrasts after frozen v1 failure."""
import unittest
import xml.etree.ElementTree as ET
from scripts.bill_context_design_text_v2 import render
from scripts.bill_render_coverage_audit_v2 import audit

BODY = '<bill><form><congress>113th CONGRESS</congress><legis-num>H. R. 1</legis-num></form><legis-body><section><text>A &amp; B.</text></section></legis-body></bill>'


class IndependentV2CompatibilityTests(unittest.TestCase):
    def check(self, raw):
        return audit(raw, '113-hr1', render(raw, '113-hr1'))

    def test_runner_wiring_does_not_patch_frozen_runner(self):
        from scripts import run_bill_readiness_audit as old_runner
        from scripts import run_bill_readiness_audit_v2 as new_runner
        from scripts import bill_render_coverage_audit as old_module
        self.assertIs(old_runner.audit, old_module.audit)
        self.assertIs(new_runner.audit, audit)
        self.assertIsNot(old_runner.audit, new_runner.audit)

    def test_malformed_xml_uses_registered_failure_boundary(self):
        with self.assertRaises((ValueError, ET.ParseError)):
            audit(b'<bill><broken></bill>', '113-hr1', dict(bill_id='113-hr1'))

    def test_external_declaration_needs_no_resource(self):
        for declaration in (
            '<!DOCTYPE bill SYSTEM "file:///absolutely/nonexistent/dtd.dtd">',
            '<!DOCTYPE bill PUBLIC "-//Impossible//DTD Bill//EN" "https://invalid.invalid/bill.dtd">',
        ):
            with self.subTest(declaration=declaration):
                result = self.check((declaration + BODY).encode())
                self.assertTrue(result['parser_text_segments_accounted'])
                self.assertFalse(result['source_document_completeness'])

    def test_utf16_external_declaration_allowed(self):
        raw = ('<?xml version="1.0" encoding="utf-16"?>'
               '<!DOCTYPE bill SYSTEM "https://invalid.invalid/bill.dtd">' + BODY).encode('utf-16')
        self.assertTrue(self.check(raw)['parser_text_segments_accounted'])

    def test_internal_subset_even_without_entities_rejected(self):
        for declaration in ('<!DOCTYPE bill []>', '<!DOCTYPE bill [<!ELEMENT bill ANY>]>'):
            raw = (declaration + BODY).encode()
            with self.subTest(declaration=declaration), self.assertRaises(ValueError):
                audit(raw, '113-hr1', dict(bill_id='113-hr1'))

    def test_utf16_entity_definition_rejected_before_expansion(self):
        for entity in ('<!ENTITY e "expanded">', '<!ENTITY e SYSTEM "file:///etc/passwd">',
                       '<!ENTITY % e SYSTEM "https://invalid.invalid/entity">%e;'):
            raw = ('<?xml version="1.0" encoding="utf-16"?><!DOCTYPE bill [' + entity + ']>' + BODY).encode('utf-16')
            with self.subTest(entity=entity), self.assertRaises(ValueError):
                audit(raw, '113-hr1', dict(bill_id='113-hr1'))

    def test_external_entity_use_not_silently_dropped(self):
        raw = ('<!DOCTYPE bill SYSTEM "https://invalid.invalid/bill.dtd">' + BODY.replace('A &amp; B.', '&unknown;')).encode()
        with self.assertRaises((ValueError, ET.ParseError)):
            audit(raw, '113-hr1', dict(bill_id='113-hr1'))


if __name__ == '__main__':
    unittest.main()
