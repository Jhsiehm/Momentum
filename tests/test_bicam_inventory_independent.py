"""Independent adversarial cases; no network or actual outcome inspection."""
import csv
import hashlib
import io
import struct
import json
import pathlib
import tempfile
from unittest import mock
import unittest
import zlib
from scripts import bicam_inventory_audit_v1 as m


class IndependentInventoryTests(unittest.TestCase):
    def data(self, rows):
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['bill_id', 'bill_type', 'bill_number', 'congress', 'introduced_at', 'is_law'])
        writer.writerows(rows)
        return output.getvalue().encode()

    def row(self, n=1):
        return [f'hr{n}-113', 'hr', str(n), '113', '2013-01-03', 'OUTCOME_SENTINEL']

    def test_case_equivalent_duplicate_blocks_sample(self):
        a, b = self.row(), self.row()
        b[0] = b[0].upper()
        result = m.inventory(self.data([a, b]))
        self.assertFalse(result['complete_identity_census'])
        self.assertEqual(result['sample'], [])

    def test_unknown_bill_type_blocks_sample(self):
        row = self.row()
        row[1] = 'hr_typo'
        result = m.inventory(self.data([row]))
        self.assertTrue(result['issues'])
        self.assertEqual(result['sample'], [])

    def test_identity_disagreement_cannot_hide_outside_scope(self):
        row = self.row()
        row[1] = 'hres'
        self.assertTrue(m.inventory(self.data([row]))['issues'])

    def test_exact_sample_and_no_outcome_values(self):
        rows = [self.row(n) for n in range(1, 122)]
        result = m.inventory(self.data(rows))
        expected = sorted([row[0] for row in rows], key=lambda bid: hashlib.sha256((m.VERSION+'\n'+bid).encode()).hexdigest())[:100]
        self.assertEqual([r['bill_id'] for r in result['sample']], expected)
        self.assertNotIn('OUTCOME_SENTINEL', str(result))
        self.assertNotIn('is_law', str(result))
        self.assertEqual(result['counts']['113-hr'], 121)

    def test_boundaries_and_non_midnight_rejected(self):
        for date in ['2013-01-02', '2015-01-03', '2013-01-03 12:00:00', '2013-02-30']:
            row = self.row()
            row[4] = date
            with self.subTest(date=date):
                self.assertTrue(m.inventory(self.data([row]))['issues'])

    def test_known_non_bill_type_is_outside_scope(self):
        row = self.row()
        row[0], row[1] = 'hres1-113', 'hres'
        result = m.inventory(self.data([row]))
        self.assertEqual(result['counts']['outside_scope'], 1)
        self.assertEqual(result['rows'], [])

    def test_trailing_deflate_payload_rejected(self):
        value = b'x'*100
        compressor = zlib.compressobj(wbits=-15)
        raw = compressor.compress(value)+compressor.flush()+b'trailing'
        entry = dict(compressed=len(raw), uncompressed=len(value), crc=zlib.crc32(value))
        with self.assertRaises(ValueError):
            m.inflate(raw, entry)

    def test_encrypted_local_header_rejected(self):
        entry = dict(flags=1, crc=1, compressed=2, uncompressed=3)
        raw = struct.pack('<IHHHHHIIIHH', 0x04034b50, 20, 1, 8, 0, 0, 1, 2, 3, 9, 0)
        with self.assertRaises(ValueError):
            m.local_header(raw, entry)

    def test_http_identity_failures_are_retained_and_stop(self):
        prior = json.loads((m.PRIOR / 'zip-result.json').read_text())[0]['headers']
        size = prior['Content-Length']
        base = {'ETag': prior['ETag'], 'x-amz-version-id': prior['x-amz-version-id'],
                'Content-Range': f'bytes 0-29/{size}', 'Content-Length': '30'}
        cases = [('ETag', '"wrong"'), ('x-amz-version-id', 'wrong'),
                 ('Content-Range', f'bytes 1-30/{size}'), ('Content-Length', '31'), ('status', 200)]
        for key, value in cases:
            with self.subTest(key=key), tempfile.TemporaryDirectory() as temp:
                response = mock.MagicMock()
                response.__enter__.return_value = response
                response.headers = dict(base)
                response.status = 206
                if key == 'status':
                    response.status = value
                else:
                    response.headers[key] = value
                opener = mock.Mock()
                opener.open.return_value = response
                output = pathlib.Path(temp) / 'run'
                with mock.patch.object(m.urllib.request, 'build_opener', return_value=opener):
                    with self.assertRaisesRegex(ValueError, 'HTTP range identity mismatch'):
                        m.run(output)
                self.assertEqual(opener.open.call_count, 1)
                response.read.assert_not_called()
                self.assertTrue((output / 'request-01-intent.json').exists())
                self.assertTrue((output / 'request-01.json').exists())
                self.assertTrue((output / 'failure.json').exists())
                self.assertFalse((output / 'result.json').exists())

    def test_redirect_handler_disallows_redirect(self):
        self.assertIsNone(m.NoRedirect().redirect_request(None, None, 302, 'redirect', {}, 'https://example.com'))

if __name__ == '__main__':
    unittest.main()
