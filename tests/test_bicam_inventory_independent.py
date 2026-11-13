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
import zipfile
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

    def synthetic_archive(self, root):
        """Synthetic ZIP/prior envelope; never reconstruct a historical receipt."""
        members = {
            'bills.csv': self.data([self.row(1), self.row(2)]),
            'ref_bill_version_codes.csv': b'code,description\nIH,Introduced in House\nIS,Introduced in Senate\n',
        }
        stream = io.BytesIO()
        with zipfile.ZipFile(stream, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
            for name, value in members.items():
                archive.writestr(name, value)
        raw = stream.getvalue()
        prior = root / 'synthetic-prior'
        prior.mkdir()
        headers = {'Content-Length': str(len(raw)), 'ETag': '"synthetic-archive"',
                   'x-amz-version-id': 'synthetic-v1'}
        (prior / 'zip-result.json').write_text(json.dumps([{'headers': headers}]))
        # The complete small ZIP is also a valid tail; its offset adjustment is zero.
        (prior / 'zip-tail.bin').write_bytes(raw)
        return raw, prior, headers, members

    def test_http_identity_failures_are_retained_and_stop(self):
        cases = [('ETag', '"wrong"'), ('x-amz-version-id', 'wrong'),
                 ('Content-Range', 'wrong range'), ('Content-Length', '31'), ('status', 200)]
        for key, value in cases:
            with self.subTest(key=key), tempfile.TemporaryDirectory() as temp:
                root = pathlib.Path(temp)
                raw, prior, source_headers, _ = self.synthetic_archive(root)
                size = len(raw)
                response = mock.MagicMock()
                response.__enter__.return_value = response
                response.headers = dict(source_headers, **{
                    'Content-Range': f'bytes 0-29/{size}', 'Content-Length': '30'})
                response.status = 206
                if key == 'status':
                    response.status = value
                else:
                    response.headers[key] = value
                opener = mock.Mock()
                opener.open.return_value = response
                output = root / 'run'
                with mock.patch.object(m, 'PRIOR', prior), \
                     mock.patch.object(m, 'TAIL_HASH', hashlib.sha256(raw).hexdigest()), \
                     mock.patch.object(m.urllib.request, 'build_opener', return_value=opener):
                    with self.assertRaisesRegex(ValueError, 'HTTP range identity mismatch'):
                        m.run(output)
                self.assertEqual(opener.open.call_count, 1)
                response.read.assert_not_called()
                self.assertTrue((output / 'request-01-intent.json').exists())
                self.assertTrue((output / 'request-01.json').exists())
                self.assertTrue((output / 'failure.json').exists())
                self.assertFalse((output / 'result.json').exists())
                failure = json.loads((output / 'failure.json').read_text())
                self.assertEqual(failure['request_count'], 1)
                self.assertEqual(failure['error'], 'HTTP range identity mismatch')

    def test_valid_synthetic_range_archive_completes_all_six_requests(self):
        with tempfile.TemporaryDirectory() as temp:
            root = pathlib.Path(temp)
            raw, prior, source_headers, members = self.synthetic_archive(root)
            observed_ranges = []

            def respond(request, timeout):
                self.assertEqual(request.full_url, m.URL)
                self.assertEqual(request.get_header('If-match'), source_headers['ETag'])
                self.assertGreater(timeout, 0)
                unit, interval = request.get_header('Range').split('=')
                self.assertEqual(unit, 'bytes')
                lo, hi = map(int, interval.split('-'))
                self.assertGreaterEqual(lo, 0)
                self.assertLess(hi, len(raw))
                observed_ranges.append((lo, hi))
                payload = io.BytesIO(raw[lo:hi + 1])
                response = mock.MagicMock()
                response.__enter__.return_value = response
                response.status = 206
                response.headers = dict(source_headers, **{
                    'Content-Range': f'bytes {lo}-{hi}/{len(raw)}',
                    'Content-Length': str(hi - lo + 1)})
                response.read.side_effect = payload.read
                return response

            opener = mock.Mock()
            opener.open.side_effect = respond
            output = root / 'run'
            with mock.patch.object(m, 'PRIOR', prior), \
                 mock.patch.object(m, 'TAIL_HASH', hashlib.sha256(raw).hexdigest()), \
                 mock.patch.object(m.urllib.request, 'build_opener', return_value=opener):
                m.run(output)
            self.assertEqual(opener.open.call_count, 6)
            self.assertEqual(len(observed_ranges), 6)
            self.assertFalse((output / 'failure.json').exists())
            result = json.loads((output / 'result.json').read_text())
            self.assertEqual(result['disposition'], 'inventory_complete')
            self.assertEqual(result['request_count'], 6)
            self.assertEqual(result['sampled'], 2)
            self.assertEqual(result['reference_rows'], 2)
            self.assertEqual(result['model_fits'], 0)
            self.assertFalse(result['historical_eligibility_established'])
            self.assertEqual(result['downloaded_bytes'], sum(hi - lo + 1 for lo, hi in observed_ranges))
            for index in range(1, 7):
                self.assertTrue((output / f'request-{index:02d}-intent.json').exists())
                self.assertTrue((output / f'request-{index:02d}.json').exists())
            for name, expected in members.items():
                self.assertEqual((output / name).read_bytes(), expected)
                self.assertEqual(result['member_sha256'][name], hashlib.sha256(expected).hexdigest())
            census = json.loads((output / 'identity-census.json').read_text())
            self.assertNotIn('OUTCOME_SENTINEL', str(census))
            self.assertEqual(census['sample_shortfall'], 98)

    def test_redirect_handler_disallows_redirect(self):
        self.assertIsNone(m.NoRedirect().redirect_request(None, None, 302, 'redirect', {}, 'https://example.com'))

if __name__ == '__main__':
    unittest.main()
