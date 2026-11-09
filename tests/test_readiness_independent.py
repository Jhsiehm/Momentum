"""Independent adversarial readiness fixtures; never quality or outcome data."""
import hashlib
import unittest
from scripts import bill_provenance_preflight as provenance
from scripts.bill_context_design_text_v2 import render


def xml(body):
    return ('<bill><form><congress>113th CONGRESS</congress><legis-num>H. R. 1</legis-num>'
            '</form><legis-body>' + body + '</legis-body></bill>').encode()


class IndependentProvenanceTests(unittest.TestCase):
    def test_every_identity_component_is_binding(self):
        identity = dict(congress=113, type='hr', number=1, version='ih',
                        raw_sha256='a'*64, view_sha256='b'*64)
        for key, value in dict(congress=114, type='s', number=2, version='rh',
                               raw_sha256='c'*64, view_sha256='d'*64).items():
            changed = dict(identity, **{key: value})
            with self.subTest(key=key), self.assertRaises(ValueError):
                provenance.validate_identity(changed, identity)
        with self.assertRaises(ValueError):
            provenance.validate_identity(dict(identity, number=True), identity)

    def test_byte_proof_is_separate_from_claimed_identity(self):
        identity = dict(congress=113, type='hr', number=1, version='ih',
                        raw_sha256=hashlib.sha256(b'raw').hexdigest(),
                        view_sha256=hashlib.sha256(b'view').hexdigest())
        self.assertTrue(provenance.verify_bytes(identity, b'raw', b'view'))
        for raw, view in ((b'RAW', b'view'), (b'raw', b'VIEW')):
            with self.assertRaises(ValueError):
                provenance.verify_bytes(identity, raw, view)

    def event(self):
        return dict(event_id='hearing-1', kind='scheduled_event',
                    known_at='2020-01-01T10:00:00-05:00',
                    source_available_at='2020-01-01T15:00:00Z',
                    version_available_at='2020-01-01T15:00:00Z',
                    event_at='2020-02-01T15:00:00Z')

    def test_cutoff_equality_and_independent_availability_clocks(self):
        cutoff = '2020-01-01T15:00:00Z'
        event = self.event()
        self.assertEqual(provenance.feature_eligibility(event, cutoff),
                         dict(eligible=True, reasons=[], historical_source_certified=False))
        for clock in ('known_at', 'source_available_at', 'version_available_at'):
            future = dict(event, **{clock: '2020-01-01T15:00:00.000001Z'})
            self.assertFalse(provenance.feature_eligibility(future, cutoff)['eligible'])
            missing = dict(event); del missing[clock]
            with self.assertRaises(ValueError):
                provenance.feature_eligibility(missing, cutoff)
        with self.assertRaises(ValueError):
            provenance.utc('2020-01-01T15:00:00')

    def test_timezone_equivalent_schedule_versions_are_ambiguous(self):
        first = self.event()
        second = dict(first, known_at='2020-01-01T15:00:00Z')
        with self.assertRaises(ValueError):
            provenance.select_schedule_vintage([first, second], '2020-01-02T00:00:00Z')

    def test_future_revision_never_overwrites_known_announcement(self):
        first = self.event()
        future = dict(first, known_at='2020-01-03T00:00:00Z',
                      source_available_at='2020-01-03T00:00:00Z',
                      version_available_at='2020-01-03T00:00:00Z',
                      kind='cancellation', event_at='2020-01-03T00:00:00Z')
        result = provenance.select_schedule_vintage([future, first], '2020-01-02T00:00:00Z')
        self.assertEqual(result['selected'], first)
        self.assertEqual(result['excluded_count'], 1)
        self.assertEqual(result['status'], 'announced')

    def test_elapsed_day180_not_calendar_midnight(self):
        self.assertEqual(provenance.day180_cutoff('2020-01-01T12:00:00-05:00',
                         '2020-06-29T17:00:00Z', '2021-01-03T17:00:00Z').hour, 17)
        with self.assertRaises(ValueError):
            provenance.day180_cutoff('2020-01-01T12:00:00-05:00',
                                    '2020-06-29T00:00:00Z', '2021-01-03T17:00:00Z')


class FrozenRendererCounterexamples(unittest.TestCase):
    def test_table_cell_join_is_real_counterexample(self):
        value = render(xml('<section><table><tr><td>No person</td><td> may act</td>'
                           '</tr></table></section>'), '113-hr1')
        self.assertIn('No person may act', value['text'])
        self.assertFalse(any(s['tag'] == 'td' for s in value['spans']))

    def test_inline_and_tail_content_preserved_but_attributes_not_rendered(self):
        value = render(xml('<section><text>Pre<em>fix</em> tail &amp; end.</text>'
                           '<graphic alt="Important chart"/></section>'), '113-hr1')
        self.assertIn('Prefix tail & end.', value['text'])
        self.assertNotIn('Important chart', value['text'])


class IndependentCoverageTests(unittest.TestCase):
    def audit(self, raw):
        from scripts.bill_render_coverage_audit import audit
        return audit(raw, '113-hr1', render(raw, '113-hr1'))

    def test_mixed_content_segments_exactly_partition_render(self):
        raw = xml('<section><text>A<em>B</em>C<em>D</em>E &#x1F600; &amp; F.</text></section>')
        result = self.audit(raw)
        view = render(raw, '113-hr1')
        pieces = result['segments'] + result['inserted_separators']
        pieces.sort(key=lambda s: (s['start'], s['end']))
        self.assertEqual(''.join(s['text'] for s in pieces), view['text'])
        cursor = 0
        for segment in pieces:
            self.assertEqual(segment['start'], cursor)
            self.assertEqual(view['text'][segment['start']:segment['end']], segment['text'])
            cursor = segment['end']
        self.assertEqual(cursor, len(view['text']))
        self.assertEqual([s['text'] for s in result['segments'] if s['kind'] == 'tail'], ['C', 'E 😀 & F.'])
        self.assertFalse(result['source_document_completeness'])
        self.assertFalse(result['semantic_structure_complete'])

    def test_namespace_collisions_attributes_and_empty_graphics_accounted(self):
        raw = xml('<section xmlns:a="urn:a" xmlns:b="urn:b"><a:text>A</a:text>'
                  '<b:text>B</b:text><graphic alt="chart"/><wrapper meaning="exemption"/></section>')
        result = self.audit(raw)
        texts = [n for n in result['nodes'] if n['tag'] == 'text']
        self.assertEqual([n['qualified_tag'] for n in texts], ['{urn:a}text', '{urn:b}text'])
        self.assertEqual(len(set(n['path'] for n in result['nodes'])), len(result['nodes']))
        self.assertEqual(result['counts']['attribute_nodes'], 2)
        self.assertEqual(result['counts']['possible_nontext_nodes'], 1)
        codes = {w['code'] for w in result['warnings']}
        self.assertTrue({'namespace_identity_collapsed', 'attributes_not_rendered',
                         'nontext_content_requires_review'} <= codes)

    def test_table_risk_survives_even_when_cells_have_whitespace(self):
        for separator in ('', ' '):
            raw = xml('<section><table><tr><td>No person</td>' + separator +
                      '<td>may act</td></tr></table></section>')
            result = self.audit(raw)
            self.assertEqual(result['counts']['cells'], 2)
            self.assertEqual(len(result['cell_boundaries']), 1)
            self.assertEqual(result['cell_boundaries'][0]['no_whitespace_boundary'], not bool(separator))
            self.assertIn('unrepresented_table_structure', {w['code'] for w in result['warnings']})
            self.assertFalse(result['semantic_structure_complete'])

    def test_utf16_dtd_rejected_not_bypassed_by_ascii_scanner(self):
        from scripts.bill_render_coverage_audit import audit
        raw = ('<?xml version="1.0" encoding="utf-16"?><!DOCTYPE bill ['
               '<!ENTITY hidden "content">]><bill/>').encode('utf-16')
        with self.assertRaises(ValueError):
            audit(raw, '113-hr1', dict(bill_id='113-hr1'))


if __name__ == '__main__':
    unittest.main()
