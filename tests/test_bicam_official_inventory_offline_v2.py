import unittest
from scripts.bicam_official_inventory_offline_v2 import parse

class OfflineTests(unittest.TestCase):
    def test_exact_zip_is_separate(self):
        raw=b'<html><a href="BILLSTATUS-118s1.xml">x</a><a href="BILLSTATUS-118-s.zip">z</a></html>'
        got=parse(raw,118,'s','https://www.govinfo.gov/bulkdata/BILLSTATUS/118/s')
        self.assertTrue(got['accepted_index'])
        self.assertEqual(got['directory_zip_resources'],['BILLSTATUS-118-s.zip'])
        self.assertEqual(got['ids'],['s1-118'])
    def test_other_zip_still_rejected(self):
        for href in ['BILLSTATUS-117-s.zip','https://bad.test/BILLSTATUS-118-s.zip','BILLSTATUS-118-s.zip?x=1']:
            raw=f'<html><a href="BILLSTATUS-118s1.xml">x</a><a href="{href}">z</a></html>'.encode()
            self.assertFalse(parse(raw,118,'s','https://www.govinfo.gov/bulkdata/BILLSTATUS/118/s')['accepted_index'])
    def test_empty_zip_only_is_not_inventory(self):
        raw=b'<html><a href="BILLSTATUS-118-s.zip">z</a></html>'
        self.assertFalse(parse(raw,118,'s','https://www.govinfo.gov/bulkdata/BILLSTATUS/118/s')['accepted_index'])
