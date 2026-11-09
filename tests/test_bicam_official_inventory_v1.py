import unittest
from scripts.bicam_official_inventory_v1 import parse


class DirectoryTests(unittest.TestCase):
    url = 'https://www.govinfo.gov/bulkdata/BILLSTATUS/118/s'
    def parse(self, links, ending='</html>'):
        raw = '<html>' + ''.join('<a href="' + link + '">bill</a>' for link in links) + ending
        return parse(raw.encode(), 118, 's', self.url)
    def test_exact_identity_and_noncontiguous(self):
        got = self.parse(['BILLSTATUS-118s1.xml', '/bulkdata/BILLSTATUS/118/s/BILLSTATUS-118s5314.xml'])
        self.assertTrue(got['accepted_index'])
        self.assertEqual(got['ids'], ['s1-118', 's5314-118'])
        self.assertFalse(got['official_completeness_certified'])
    def test_duplicate_links_count_once(self):
        got = self.parse(['BILLSTATUS-118s1.xml'] * 2)
        self.assertEqual(got['unique_count'], 1)
        self.assertEqual(got['duplicate_links'], {'s1-118': 2})
    def test_wrong_scope_and_host_rejected(self):
        for link in ['BILLSTATUS-117s1.xml', 'BILLSTATUS-118hr1.xml', 'https://example.com/BILLSTATUS-118s1.xml', 'BILLSTATUS-118s01.xml', '../BILLSTATUS-118s1.xml']:
            with self.subTest(link=link):
                got = self.parse([link, 'BILLSTATUS-118s2.xml'])
                self.assertFalse(got['accepted_index'])
                self.assertEqual(len(got['rejected_bill_links']), 1)
    def test_query_and_fragment_not_bill_sources(self):
        for suffix in ['?x=1', '#x']:
            self.assertFalse(self.parse(['BILLSTATUS-118s1.xml'+suffix])['accepted_index'])
    def test_pagination_and_truncation_fail(self):
        self.assertFalse(self.parse(['BILLSTATUS-118s1.xml', '?page=2'])['accepted_index'])
        self.assertFalse(self.parse(['BILLSTATUS-118s1.xml'], '')['accepted_index'])
    def test_empty_or_text_only_not_inventory(self):
        self.assertFalse(self.parse([])['accepted_index'])
        self.assertFalse(parse(b'<html>BILLSTATUS-118s1.xml</html>',118,'s',self.url)['accepted_index'])
    def test_invalid_encoding_and_scope_fail(self):
        with self.assertRaises(UnicodeDecodeError):
            parse(b'\xff',118,'s',self.url)
        with self.assertRaises(ValueError):
            parse(b'',119,'s',self.url)

if __name__ == '__main__':
    unittest.main()
