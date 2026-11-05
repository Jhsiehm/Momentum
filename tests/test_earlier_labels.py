import unittest
from engine.earlier_labels import parse_calendar
from engine.label_investigation import law_identity
from engine.cohort import xml


class EarlierLabelsTests(unittest.TestCase):
    def test_complete_calendar_maps_bills_and_joint_resolutions(self):
        text = 'PUBLIC LAWS 116–1 ....S. 24 116–2 ....H.R. 251 116–3 ....H.J. Res. 28'
        self.assertEqual(parse_calendar(text, expected=3), [
            {'law': 1, 'bill_id': '116-s24'}, {'law': 2, 'bill_id': '116-hr251'},
            {'law': 3, 'bill_id': '116-hjres28'}])

    def test_missing_or_duplicate_calendar_rows_rejected(self):
        for text in ('PUBLIC LAWS 116-1 ....S. 24',
                     'PUBLIC LAWS 116-1 ....S. 24 116-1 ....H.R. 251',
                     'PUBLIC LAWS 116-1 ....S. 24 116-2 ....S. 24'):
            with self.assertRaises(ValueError): parse_calendar(text, expected=2)

    def test_primary_context_duplicates_allowed_but_conflicts_rejected(self):
        prefix = '<mods xmlns="http://www.loc.gov/mods/v3"><extension><unrelated>metadata</unrelated></extension><extension><congress>116</congress><number>1</number>'
        bill = '<bill congress="116" type="S" number="24" priority="primary" />'
        suffix = '</extension><originInfo><dateIssued>2019-01-16</dateIssued></originInfo></mods>'
        self.assertEqual(law_identity(xml((prefix+bill+bill+suffix).encode()),116,1)['bill_id'],'116-s24')
        with self.assertRaises(ValueError):
            law_identity(xml((prefix+bill+bill.replace('24','25')+suffix).encode()),116,1)

if __name__ == '__main__': unittest.main()
