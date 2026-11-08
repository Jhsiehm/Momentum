"""Synthetic context challenges informed by exposed design diagnostics.

Not a blinded or held-out sample. Retention is lack of a structural flag, not
semantic support. Every locator must remain represented in a separate decision.
"""
import copy
import unittest
from xml.sax.saxutils import escape

from scripts.bill_context_design_text_v2 import render
from scripts.mechanism_design_extractor_v3 import extract
from scripts.mechanism_context_filter import classify


def make_view(body, title='Synthetic locator context challenge'):
    raw = ('<bill><form><congress>113th CONGRESS</congress><legis-num>H. R. 1</legis-num>'
           '<official-title>' + escape(title) + '</official-title></form><legis-body>' +
           body + '</legis-body></bill>').encode()
    return dict(render(raw, '113-hr1'), view_hash='c' * 64)


def section(text, header='Administration'):
    return '<section><header>' + escape(header) + '</header><text>' + escape(text) + '</text></section>'


class ContextFilterContrastTests(unittest.TestCase):
    def checked(self, view):
        locator = extract(view)
        original_view, original_locator = copy.deepcopy(view), copy.deepcopy(locator)
        result = classify(view, locator)
        self.assertEqual(result, classify(view, locator))
        self.assertEqual(view, original_view)
        self.assertEqual(locator, original_locator)
        self.assertFalse(result['human_certified'])
        self.assertFalse(result['historical_feature_eligible'])
        self.assertFalse(result['semantic_accuracy_verified'])
        expected = {(c['mechanism'], h['start'], h['end'])
                    for c in locator['candidates'] for h in c['hits']}
        decisions = result['decisions']
        identities = [(d['mechanism'], d['start'], d['end']) for d in decisions]
        self.assertEqual(len(identities), len(set(identities)))
        self.assertEqual(set(identities), expected)
        self.assertEqual(locator['accepted_v2_labels_created'], 0)
        self.assertEqual({a['status'] for a in locator['assessments'].values()}, {'abstain'})
        for d in decisions:
            self.assertIn(d['status'], {'flagged', 'retain'})
            self.assertEqual(d['quote'], view['text'][d['start']:d['end']])
            for e in d['evidence']:
                self.assertEqual(e['quote'], view['text'][e['start']:e['end']])
        return result

    def annual(self, result):
        return sorted((d for d in result['decisions'] if d['mechanism'] == 'deadline'
                       and d['quote'].lower() == 'annual report'), key=lambda d: d['start'])

    def test_heading_and_identical_operative_body_are_separate(self):
        result = self.checked(make_view(section('The archivist shall submit an annual report.', 'Annual report')))
        heading, body = self.annual(result)
        self.assertEqual(heading['status'], 'flagged')
        self.assertIn('heading_only', heading['reasons'])
        self.assertEqual(body['status'], 'retain')

    def test_purpose_title_is_not_the_body_duty(self):
        result = self.checked(make_view(section('The archivist shall submit an annual report.'),
                                        title='To require the submission of an annual report.'))
        title, body = self.annual(result)
        self.assertEqual(title['status'], 'flagged')
        self.assertTrue({'official_title', 'outside_legis_body'} & set(title['reasons']))
        self.assertEqual(body['status'], 'retain')

    def test_findings_and_sense_scope_vs_normative_section(self):
        for header in ('Findings', 'Sense of Congress'):
            with self.subTest(header=header):
                result = self.checked(make_view(
                    section('The archivist shall submit an annual report.', header) +
                    section('The inspector shall submit an annual report.')))
                finding, body = self.annual(result)
                self.assertEqual(finding['status'], 'flagged')
                self.assertIn('findings_or_sense_context', finding['reasons'])
                self.assertEqual(body['status'], 'retain')

    def test_same_amendment_old_operand_vs_inserted_operand(self):
        for old, new in (('“annual report”', '“annual report on grants”'),
                         ('annual report', 'annual report on grants')):
            with self.subTest(old=old):
                result = self.checked(make_view(section(
                    'Section 8 is amended by striking ' + old + ' and inserting ' + new + '.')))
                struck, inserted = self.annual(result)
                self.assertEqual(struck['status'], 'flagged')
                self.assertTrue({'struck_inline_quote', 'struck_replacement_operand'} & set(struck['reasons']))
                self.assertEqual(inserted['status'], 'retain')

    def test_quoted_block_deletion_vs_addition(self):
        for instruction, expected in (
            ('Section 8 is amended by striking the following:', 'flagged'),
            ('Section 8 is amended by inserting the following:', 'retain'),
        ):
            with self.subTest(instruction=instruction):
                body = ('<section><text>' + escape(instruction) + '</text><quoted-block>'
                        '<section><text>The registrar shall submit an annual report.</text></section>'
                        '</quoted-block></section>')
                result = self.checked(make_view(body))
                item, = self.annual(result)
                self.assertEqual(item['status'], expected)
                if expected == 'flagged':
                    self.assertIn('struck_quoted_block', item['reasons'])

    def test_incidental_striking_elsewhere_does_not_taint_body(self):
        bodies = [
            section('Section 8 is amended by striking “obsolete”. The archivist shall submit an annual report.'),
            '<section><text>Section 8 is amended by striking obsolete.</text>'
            '<subsection><text>The archivist shall submit an annual report.</text></subsection></section>',
            section('Section 8 is amended by striking obsolete.') +
            section('The archivist shall submit an annual report.'),
        ]
        for body in bodies:
            with self.subTest(body=body):
                result = self.checked(make_view(body))
                item, = self.annual(result)
                self.assertEqual(item['status'], 'retain')

    def test_retain_is_not_semantic_certification(self):
        result = self.checked(make_view(section(
            'Nothing in this Act requires the archivist to submit an annual report.')))
        item, = self.annual(result)
        # No nonconstruction classifier is promised. Even an unflagged hit must
        # remain a locator, never an inferred affirmative reporting obligation.
        self.assertEqual(item['status'], 'retain')
        self.assertFalse(result['semantic_accuracy_verified'])


if __name__ == '__main__':
    unittest.main()
