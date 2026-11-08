"""Synthetic source contrasts, not quality labels or memorized design bill IDs."""
import copy
import hashlib
import unittest
from xml.sax.saxutils import escape

from scripts.bill_context_design_text_v2 import render
from scripts.mechanism_design_extractor import extract, MECHANISMS


def view(body):
    raw = ('<bill><form><congress>113th CONGRESS</congress><legis-num>H. R. 1</legis-num>'
           '</form><legis-body>' + body + '</legis-body></bill>').encode()
    return dict(render(raw, '113-hr1'), view_hash='a' * 64)


def clause(text, header='Implementation'):
    return '<section><header>' + escape(header) + '</header><text>' + escape(text) + '</text></section>'


class DesignExtractorTests(unittest.TestCase):
    def test_all_mechanisms_have_locators_but_no_accepted_status(self):
        v = view(clause('A program may receive funds; tax, prohibit, must, amend, repeal, designate, report, within, expire.'))
        result = extract(v)
        self.assertEqual({c['mechanism'] for c in result['candidates']}, set(MECHANISMS))
        self.assertEqual({x['status'] for x in result['assessments'].values()}, {'abstain'})
        self.assertEqual(result['accepted_v2_labels_created'], 0)
        self.assertFalse(result['historical_feature_eligible'])
        self.assertFalse(result['trained_model'])
        silent = extract(view(clause('Hello world.')))
        self.assertEqual(silent['candidates'], [])
        self.assertTrue(all(x['status'] == 'abstain' for x in silent['assessments'].values()))

    def test_unicode_duplicate_occurrences_determinism_and_no_mutation(self):
        sentence = 'The Secretary shall submit a report about café 🌱.'
        v = view(clause(sentence) + clause(sentence))
        before = copy.deepcopy(v)
        result = extract(v)
        self.assertEqual(result, extract(v))
        self.assertEqual(v, before)
        reports = [c for c in result['candidates'] if c['mechanism'] == 'reporting']
        self.assertEqual(len(reports), 2)
        self.assertNotEqual(reports[0]['candidate_id'], reports[1]['candidate_id'])
        for item in result['candidates'] + result['proposals']:
            self.assertEqual(item['quote'], v['text'][item['start']:item['end']])
        for candidate in result['candidates']:
            for hit in candidate['hits']:
                self.assertEqual(hit['quote'], v['text'][hit['start']:hit['end']])
                self.assertLessEqual(candidate['start'], hit['start'])
                self.assertGreaterEqual(candidate['end'], hit['end'])
        self.assertEqual(len([p for p in result['proposals'] if p['mechanism'] == 'reporting']), 2)

    def test_full_view_tail_is_scanned_without_truncation(self):
        v = view(clause('x ' * 60000) + clause('The authority shall expire on January 1, 2030.'))
        result = extract(v)
        self.assertEqual(result['coverage']['scan_ranges'], [[0, len(v['text'])]])
        self.assertTrue(result['coverage']['input_view_scanned_completely'])
        self.assertFalse(result['coverage']['source_document_completeness_verified'])
        self.assertGreater(next(c for c in result['candidates'] if c['mechanism'] == 'sunset')['hits'][0]['start'], 120000)

    def test_appropriation_and_authorization_are_distinct_suggestions(self):
        auth = extract(view(clause('There are authorized to be appropriated $100 for the program.')))
        direct = extract(view(clause('There are appropriated $100 for the program.')))
        self.assertEqual([p['mechanism'] for p in auth['proposals']], ['authorize'])
        self.assertEqual([p['mechanism'] for p in direct['proposals']], ['appropriate'])
        self.assertIn('appropriate', {c['mechanism'] for c in auth['candidates']})

    def test_nonoperative_and_quoted_context_never_promoted(self):
        for header in ('Findings', 'Sense of Congress', 'Definitions', 'Short title'):
            result = extract(view(clause('The Secretary shall submit a report.', header)))
            self.assertTrue(result['candidates'])
            self.assertFalse(result['proposals'])
            self.assertTrue(result['suppressed_proposals'])
        result = extract(view('<section><text>Section 2 is amended by inserting:</text><quoted-block>'
                              '<section><text>The Secretary shall submit a report.</text></section>'
                              '</quoted-block></section>'))
        self.assertFalse(result['proposals'])
        report = next(c for c in result['candidates'] if c['mechanism'] == 'reporting')
        self.assertIn('is amended by inserting', report['quote'])

    def test_parent_negation_list_and_full_quote_sufficiency(self):
        v = view('<section><text>The Secretary shall not be required to do the following:</text>'
                 '<paragraph><text>Submit a report.</text></paragraph>'
                 '<paragraph><text>Establish a program.</text></paragraph></section>')
        result = extract(v)
        self.assertFalse(result['proposals'])
        for c in result['candidates']:
            self.assertIn('shall not be required', c['quote'])
            self.assertIn('Submit a report.', c['quote'])
            self.assertIn('Establish a program.', c['quote'])

    def test_struck_text_and_repeal_vs_replacement(self):
        replacement = extract(view(clause('Section 2 is amended by striking “shall submit a report” and inserting “may submit a report”.')))
        self.assertFalse(replacement['proposals'])
        self.assertIn('repeal', {c['mechanism'] for c in replacement['candidates']})
        repeal = extract(view(clause('Section 2 is repealed.')))
        self.assertEqual([(p['mechanism'], p['suggested_operation']) for p in repeal['proposals']], [('repeal', 'remove')])

    def test_exception_nonconstruction_and_cross_block_scope(self):
        for text in ('The Secretary shall submit a report unless funds are unavailable.',
                     'Nothing in this Act shall be construed to prohibit reporting.',
                     'The Secretary shall submit a report. This duty does not apply to emergencies.'):
            result = extract(view(clause(text)))
            self.assertFalse(result['proposals'])
        result = extract(view('<section><text>The Secretary shall submit a report.</text>'
                              '<subsection><text>This section does not apply to emergencies.</text></subsection></section>'))
        self.assertFalse(result['proposals'])

    def test_action_deadline_vs_effective_date_or_medication_duration(self):
        for text in ('This Act takes effect after 30 days.', 'No person may dispense more than a seven-day supply within a month.'):
            result = extract(view(clause(text)))
            self.assertNotIn('deadline', {p['mechanism'] for p in result['proposals']})
        result = extract(view(clause('Not later than 30 days after enactment, the Secretary shall submit a report.')))
        p = next(p for p in result['proposals'] if p['mechanism'] == 'deadline')
        self.assertEqual(p['suggested_dimension'], 'duration')
        self.assertEqual(p['quote'], 'Not later than 30 days after enactment, the Secretary shall submit a report.')

    def test_sunset_creation_and_unknown_prior_law_abstention(self):
        result = extract(view(clause('The authority under this section shall expire on January 1, 2030.')))
        p = next(p for p in result['proposals'] if p['mechanism'] == 'sunset')
        self.assertEqual((p['suggested_operation'], p['suggested_dimension']), ('create', 'duration'))
        unknown = extract(view(clause('Section 2 is amended by striking “2029” and inserting “2030”.')))
        self.assertFalse(unknown['proposals'])
        rate = extract(view(clause('The rate of tax shall be 5 percent.')))
        self.assertFalse(rate['proposals'])
        imposed = extract(view(clause('There is hereby imposed a tax of 5 percent on sales.')))
        self.assertEqual(imposed['proposals'][0]['suggested_operation'], 'create')

    def test_invalid_source_spans_fail_closed(self):
        v = view(clause('The Secretary shall submit a report.'))
        for mutate in (lambda x: x['spans'][0].update(start=-1),
                       lambda x: x['spans'][0].update(text_sha256='bad'),
                       lambda x: x.update(view_hash='invalid'),
                       lambda x: x['spans'].append(copy.deepcopy(x['spans'][0]))):
            broken = copy.deepcopy(v)
            mutate(broken)
            with self.assertRaises(ValueError):
                extract(broken)
        broken = copy.deepcopy(v)
        section = next(s for s in broken['spans'] if s['tag'] == 'section')
        section['end'] = section['start']
        section['text_sha256'] = hashlib.sha256(b'').hexdigest()
        with self.assertRaisesRegex(ValueError, 'ancestor'):
            extract(broken)


if __name__ == '__main__':
    unittest.main()
