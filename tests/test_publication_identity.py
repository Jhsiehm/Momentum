import unittest
from engine.publication_identity import validate_introduction


def mods(intro='2023-10-11', issue='2023-10-25', package='BILLS-118hr5925ih', extra=''):
    return (f'<mods xmlns="http://www.loc.gov/mods/v3"><recordInfo><recordIdentifier>{package}</recordIdentifier></recordInfo>'
            f'<originInfo><dateIssued>{issue}</dateIssued></originInfo><extension>'
            f'<action date="{intro}">Mr. Example introduced the following bill</action>{extra}</extension></mods>').encode()


class PublicationIdentityTests(unittest.TestCase):
    def test_distinct_issue_date_preserved(self):
        result = validate_introduction(mods(), 'BILLS-118hr5925ih', '2023-10-11T00:00:00Z')
        self.assertEqual(result['issued_at'], '2023-10-25')
        self.assertTrue(result['issue_date_differs'])
        self.assertFalse(result['human_audit_satisfied'])

    def test_same_day_valid(self):
        self.assertFalse(validate_introduction(mods(issue='2023-10-11'), 'BILLS-118hr5925ih', '2023-10-11')['issue_date_differs'])

    def test_conflicts_fail_closed(self):
        examples = [mods(intro='2023-10-12'), mods(issue='2023-10-10'), mods(issue=''),
                    mods(package='BILLS-118hr5926ih'),
                    mods(extra='<action date="2023-10-12">Another member introduced the following bill</action>'),
                    mods().replace(b'introduced the following bill', b'Referred to committee')]
        for raw in examples:
            with self.subTest(raw=raw), self.assertRaises(ValueError):
                validate_introduction(raw, 'BILLS-118hr5925ih', '2023-10-11')

    def test_non_introduced_package_rejected(self):
        with self.assertRaises(ValueError):
            validate_introduction(mods(package='BILLS-118hr5925eh'), 'BILLS-118hr5925eh', '2023-10-11')


if __name__ == '__main__':
    unittest.main()
