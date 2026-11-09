"""Independent adversarial tests: inventory evidence never releases history gates."""
import io
import unittest
import zipfile
from scripts import historical_source_feasibility_v1 as h


def premis(extra=''):
    return ('<premis xmlns="urn:test"><object><objectIdentifier><objectIdentifierValue>old-a</objectIdentifierValue></objectIdentifier>' + extra + '</object></premis>').encode()


def archive(files):
    stream=io.BytesIO()
    with zipfile.ZipFile(stream,'w') as z:
        for name,data in files:z.writestr(name,data)
    return stream.getvalue()


class IndependentHistoricalFeasibility(unittest.TestCase):
    def record(self):
        return dict(bill_id='113-hr1',package='BILLS-113hr1ih',cutoff='2013-07-01',
                    xml_objects=[{'id':'old-a','digest':None},{'id':'old-b','digest':None}],
                    current_source={'sha256':'a'*64})

    def test_utf16_entity_not_accepted(self):
        raw='<?xml version="1.0" encoding="UTF-16"?><!DOCTYPE premis [<!ENTITY x "expanded">]><premis><object><objectIdentifierValue>&x;</objectIdentifierValue></object></premis>'.encode('utf-16')
        with self.assertRaises(ValueError):h.objects(raw)

    def test_duplicate_objects_rejected(self):
        raw=b'<premis><object><objectIdentifierValue>x</objectIdentifierValue></object><object><objectIdentifierValue>x</objectIdentifierValue></object></premis>'
        with self.assertRaises(ValueError):h.objects(raw)

    def test_missing_object_id_rejected(self):
        with self.assertRaises(ValueError):h.objects(b'<premis><object/></premis>')

    def test_digest_and_size_remain_untrusted_strings(self):
        result=h.objects(premis('<objectCharacteristics><fixity><messageDigestAlgorithm>SHA-256</messageDigestAlgorithm><messageDigest>not hexadecimal</messageDigest></fixity><size>-42</size></objectCharacteristics>'))
        self.assertEqual(result[0]['sizes'],['-42'])
        assessed=h.assess(self.record(),result,{})
        self.assertFalse(assessed['recovered_digest_records'][0]['supported_valid_digest'])
        self.assertFalse(assessed['historical_feature_eligible'])

    def test_matching_old_digest_does_not_establish_access(self):
        obj=dict(id='old-a',digests=[dict(algorithm='SHA-256',digest='A'*64)])
        result=h.assess(self.record(),[obj],dict(members=[dict(name='BILLS-113hr1ih/xml.xml',sha256='a'*64)]))
        self.assertEqual(len(result['old_digest_member_matches']),1)
        self.assertEqual(result['disposition'],'unresolved_public_access_chain')
        self.assertFalse(result['historical_feature_eligible'])
        self.assertFalse(result['historical_public_access_proven'])

    def test_other_object_digest_is_not_old_object_evidence(self):
        obj=dict(id='unrelated',digests=[dict(algorithm='SHA-256',digest='a'*64)])
        result=h.assess(self.record(),[obj],{})
        self.assertEqual(result['recovered_digest_records'],[])

    def test_ancient_date_cannot_upgrade_current_bytes(self):
        raw=premis('<objectCharacteristics><dateCreatedByApplication>1900-01-01</dateCreatedByApplication></objectCharacteristics>')
        result=h.assess(self.record(),h.objects(raw),dict(members=[dict(name='BILLS-113hr1ih/xml.xml',sha256='a'*64)]))
        self.assertEqual(len(result['current_xml_matching_members']),1)
        self.assertFalse(result['historical_feature_eligible'])

    def test_traversal_never_extracted(self):
        with self.assertRaises(ValueError):h.inspect_zip(archive([('BILLS-113hr1ih/../escape','x')]),'BILLS-113hr1ih')

    def test_zip_member_limit(self):
        with self.assertRaises(ValueError):h.inspect_zip(archive([(f'BILLS-113hr1ih/{i}','x') for i in range(257)]),'BILLS-113hr1ih')

    def test_missing_package_identity(self):
        with self.assertRaises(ValueError):h.inspect_zip(archive([('another/file.xml','x')]),'BILLS-113hr1ih')

    def test_malformed_xml_error_normalized(self):
        with self.assertRaises(ValueError):h.objects(b'<premis>')


if __name__=='__main__':unittest.main()
