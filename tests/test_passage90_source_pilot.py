import unittest
import io
import json
from pathlib import Path
import re
import tempfile
from unittest.mock import Mock, patch
from scripts.passage90_source_pilot import inspect, select, run


class PilotTest(unittest.TestCase):
    case = dict(bill_id='hr1-118', congress=118, bill_type='hr', bill_number=1)

    def xml(self, dates=(), intro='2023-01-03', number=1, extra=''):
        actions = ''.join('<item><actionCode>8000</actionCode><sourceSystem><code>9</code></sourceSystem>'
                          '<actionDate>' + day + '</actionDate><text>Passed/agreed to in House: test</text></item>' for day in dates)
        return (f'<billStatus><bill><congress>118</congress><type>HR</type><number>{number}</number>'
                f'<introducedDate>{intro}</introducedDate><actions>{actions}{extra}</actions></bill></billStatus>').encode()

    def test_absence_is_unresolved(self):
        row = inspect(self.xml(), self.case)
        self.assertEqual(row['disposition'], 'unresolved_no_recognized_passage')
        self.assertIsNone(row['certified_label'])

    def test_passage_candidate_never_certifies(self):
        row = inspect(self.xml(['2023-03-01']), self.case)
        self.assertEqual(row['disposition'], 'candidate_within_window_passage')
        self.assertIsNone(row['certified_label'])

    def test_first_passage_prevents_repassage_rescue(self):
        row = inspect(self.xml(['2023-03-01', '2023-01-10']), self.case)
        self.assertEqual(row['disposition'], 'excluded_already_passed')

    def test_boundaries_and_late_window(self):
        for day in ('2023-02-02', '2023-05-03'):
            self.assertEqual(inspect(self.xml([day]), self.case)['disposition'], 'unresolved_boundary_day')
        self.assertEqual(inspect(self.xml(intro='2024-12-01'), self.case)['disposition'], 'excluded_incomplete_congress_window')

    def test_wrong_identity_and_ambiguous_action(self):
        with self.assertRaises(ValueError):
            inspect(self.xml(number=2), self.case)
        bad = '<item><actionCode>8000</actionCode><actionDate>2023-03-01</actionDate></item>'
        self.assertEqual(inspect(self.xml(extra=bad), self.case)['disposition'], 'unresolved_action_semantics')

    def test_frozen_selection_independent_of_input_order(self):
        ids = [f'hr{n}-118' for n in range(1, 30)]
        self.assertEqual(select(ids, 'hr'), select(list(reversed(ids)), 'hr'))
        with self.assertRaises(ValueError):
            select(ids + [ids[0]], 'hr')
        with self.assertRaises(ValueError):
            select(ids, 's')

    def test_full_collector_pipeline_with_mocked_transport(self):
        class Response(io.BytesIO):
            def __init__(self, url, raw, kind):
                super().__init__(raw)
                self.url, self.status = url, 200
                self.headers = {'Content-Type': kind, 'Content-Length': str(len(raw))}
            def geturl(self):
                return self.url
        requested = []
        def open_request(request, timeout):
            url = request.full_url
            requested.append(url)
            match = re.search(r'BILLSTATUS-118(hr|s)([0-9]+)\.xml$', url)
            if match:
                kind, number = match.groups()
                raw = (f'<billStatus><bill><congress>118</congress><type>{kind.upper()}</type>'
                       f'<number>{number}</number><introducedDate>2023-01-03</introducedDate>'
                       '<actions></actions></bill></billStatus>').encode()
                return Response(url, raw, 'application/xml')
            kind = url.rsplit('/', 1)[-1]
            raw = ('<html>' + ''.join(f'<a href="/bulkdata/BILLSTATUS/118/{kind}/BILLSTATUS-118{kind}{n}.xml">Bill</a>'
                                      for n in range(1, 12)) + '</html>').encode()
            return Response(url, raw, 'text/html')
        with tempfile.TemporaryDirectory() as temporary, patch('engine.forecast_ledger.urllib.request.build_opener',
                return_value=Mock(open=Mock(side_effect=open_request))):
            output = Path(temporary) / 'pilot'
            result = run(output)
            self.assertEqual(result['requests'], 22)
            self.assertEqual(result['captured'], 20)
            self.assertEqual(result['inspected'], 20)
            self.assertEqual(result['dispositions'], {'unresolved_no_recognized_passage': 20})
            self.assertEqual(result['certified_negative_labels'], 0)
            self.assertEqual(len(requested), 22)
            self.assertTrue(all('BILLSTATUS-118' not in url for url in requested[:2]))
            self.assertEqual(json.loads((output / 'result.json').read_text())['verification']['sources'], 22)

    def test_failed_inventory_stops_without_replacement(self):
        with tempfile.TemporaryDirectory() as temporary, patch('engine.forecast_ledger.urllib.request.build_opener',
                return_value=Mock(open=Mock(side_effect=TimeoutError))) as opener:
            output = Path(temporary) / 'pilot'
            result = run(output)
            self.assertEqual(result['status'], 'blocked')
            self.assertTrue((output / 'blocked.json').is_file())
            self.assertFalse((output / 'sample.json').exists())
            self.assertEqual(opener.return_value.open.call_count, 1)


if __name__ == '__main__':
    unittest.main()
