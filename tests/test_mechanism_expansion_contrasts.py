"""Synthetic design challenges for locator expansion, not held-out accuracy.

These cases are authored from diagnosed phrase families, not sampled unseen bills.
A lexical match is allowed in misleading contexts; it must never certify an effect.
"""
import copy
import unittest
from xml.sax.saxutils import escape

from scripts.bill_context_design_text_v2 import render
from scripts.mechanism_design_extractor_v3 import extract


def fixture(text, header='Administration'):
    body = '<section><header>' + escape(header) + '</header><text>' + escape(text) + '</text></section>'
    return xml_fixture(body)


def xml_fixture(body):
    raw = ('<bill><form><congress>113th CONGRESS</congress><legis-num>H. R. 1</legis-num>'
           '</form><legis-body>' + body + '</legis-body></bill>').encode()
    return dict(render(raw, '113-hr1'), view_hash='b' * 64)


class ExpansionContrastTests(unittest.TestCase):
    def checked(self, view):
        original = copy.deepcopy(view)
        result = extract(view)
        self.assertEqual(original, view)
        self.assertEqual(result, extract(view))
        self.assertEqual(result['accepted_v2_labels_created'], 0)
        self.assertEqual({a['status'] for a in result['assessments'].values()}, {'abstain'})
        self.assertFalse(result['human_certified'])
        self.assertFalse(result['historical_feature_eligible'])
        self.assertFalse(result['trained_model'])
        self.assertTrue(result['coverage']['input_view_scanned_completely'])
        self.assertFalse(result['coverage']['truncated'])
        for candidate in result['candidates']:
            self.assertEqual(candidate['interpretation_status'], 'unreviewed_locator')
            self.assertEqual(candidate['quote'], view['text'][candidate['start']:candidate['end']])
            for hit in candidate['hits']:
                self.assertEqual(hit['quote'], view['text'][hit['start']:hit['end']])
                self.assertLessEqual(candidate['start'], hit['start'])
                self.assertGreaterEqual(candidate['end'], hit['end'])
        return result

    @staticmethod
    def rules(result, mechanism):
        return {rule for c in result['candidates'] if c['mechanism'] == mechanism
                for hit in c['hits'] for rule in hit.get('rule_ids', [])}

    def hit(self, text, mechanism, rule):
        result = self.checked(fixture(text))
        self.assertIn(rule, self.rules(result, mechanism))
        return result

    def test_varied_subject_bars_and_sentence_boundary(self):
        for text in (
            'No municipal licensing board may demand an additional bond.',
            'No newly installed barrier shall obstruct the emergency exit.',
            'No permit for commercial drone flights may be issued without review.',
        ):
            with self.subTest(text=text):
                self.hit(text, 'prohibit', 'negative_subject_modal')
        result = self.checked(fixture('No public statement was recorded. The custodian may open the archive.'))
        self.assertNotIn('negative_subject_modal', self.rules(result, 'prohibit'))

    def test_conditional_only_permissions_keep_full_context(self):
        for text in (
            'The registrar may only disclose the ledger if the applicant consents.',
            'The vessel shall be permitted only in the marked channel, except during rescue operations.',
            'A renewal may be issued only upon approval by either the board or the director.',
        ):
            with self.subTest(text=text):
                result = self.hit(text, 'prohibit', 'only_permission')
                self.assertFalse(result['proposals'])
                self.assertTrue(all(text in c['quote'] for c in result['candidates']))
        ordinary = self.checked(fixture('The only remaining copy contains a harbor diagram.'))
        self.assertNotIn('only_permission', self.rules(ordinary, 'prohibit'))

    def test_choices_and_rights_are_not_merely_shall_duties(self):
        for text in (
            'The petitioner shall have the option to request a remote hearing.',
            'Each licensee shall have the right to appeal the assessment.',
        ):
            self.hit(text, 'authorize', 'right_or_option')
        duty = self.checked(fixture('The petitioner shall deliver the application to the clerk.'))
        self.assertNotIn('right_or_option', self.rules(duty, 'authorize'))
        self.hit('The cooperative shall retain any right to use the well under State law.', 'authorize', 'retain_right')

    def test_information_transfer_vs_physical_objects(self):
        for text, rule in (
            ('The custodian shall furnish information directly to the panel upon request.', 'furnish_information'),
            ('The registrar shall file a map and legal description with the regional office.', 'file_document'),
            ('The agency shall provide address records to each municipal clerk.', 'provide_records'),
        ):
            with self.subTest(rule=rule):
                self.hit(text, 'reporting', rule)
        for text in (
            'The custodian shall furnish the empty office with desks.',
            'The technician shall repair the file cabinet.',
            'The agency shall provide chairs to each municipal clerk.',
        ):
            with self.subTest(text=text):
                result = self.checked(fixture(text))
                self.assertTrue(self.rules(result, 'reporting').isdisjoint(
                    {'furnish_information', 'file_document', 'provide_records'}))

    def test_action_recurrence_vs_salary_and_quantity(self):
        for text, rule in (
            ('The ombudsman shall submit an annual report to the board.', 'annual_report'),
            ('The auditor shall submit an account on an annual basis.', 'annual_basis'),
            ('Payments shall be made not less frequently than 2 times a year.', 'frequency_action'),
            ('The council shall conduct public meetings semiannually.', 'semiannual_action'),
        ):
            with self.subTest(rule=rule):
                self.hit(text, 'deadline', rule)
        for text in (
            'The annual salary of the custodian shall be $50,000.',
            'The annual budget for office supplies is $2,000.',
            'A package contains a seven-day supply of tablets.',
        ):
            result = self.checked(fixture(text))
            self.assertTrue(self.rules(result, 'deadline').isdisjoint(
                {'annual_report', 'annual_basis', 'frequency_action', 'semiannual_action'}))

    def test_misleading_contexts_do_not_become_effects(self):
        annual = 'The Secretary shall submit an annual report.'
        examples = [
            fixture(annual, header='Findings'),
            fixture('Nothing in this Act shall be construed to require an annual report.'),
            fixture('Section 9 is amended by striking “shall furnish information” and inserting “may inspect”.'),
            xml_fixture('<section><text>Section 9 is amended by striking:</text>'
                        '<quoted-block><section><text>' + escape(annual) +
                        '</text></section></quoted-block></section>'),
        ]
        for view in examples:
            with self.subTest(text=view['text']):
                result = self.checked(view)
                self.assertFalse(result['proposals'])
                self.assertTrue(result['candidates'])

    def test_duplicate_unicode_hits_use_selected_occurrence(self):
        text = 'The café registrar shall file a map and legal description with the clerk.'
        section = '<section><text>' + escape(text) + '</text></section>'
        result = self.checked(xml_fixture(section + section))
        hits = [h for c in result['candidates'] for h in c['hits']
                if 'file_document' in h.get('rule_ids', [])]
        self.assertEqual(len(hits), 2)
        self.assertNotEqual(hits[0]['start'], hits[1]['start'])


if __name__ == '__main__':
    unittest.main()
