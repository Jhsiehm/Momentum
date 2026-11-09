import hashlib
import io
import unittest
import zipfile
from unittest.mock import patch
from scripts.historical_source_feasibility_v1 import objects,inspect_zip,assess,fetch

class FeasibilityTests(unittest.TestCase):
    def record(self):
        return dict(bill_id='113-hr1',package='BILLS-113hr1ih',cutoff='2014-01-01T00:00:00Z',
            current_source={'sha256':hashlib.sha256(b'x').hexdigest()},xml_objects=[{'id':'old1','digest':None},{'id':'old2','digest':None}])
    def test_old_missing_digest_not_filled_by_current_object(self):
        raw=b'<premis><object><objectIdentifier><objectIdentifierValue>old1</objectIdentifierValue></objectIdentifier></object></premis>'
        parsed=objects(raw);self.assertEqual(parsed[0]['digests'],[])
        result=assess(self.record(),parsed,{})
        self.assertEqual(result['recovered_digest_records'],[]);self.assertFalse(result['historical_feature_eligible'])
    def test_matching_old_bytes_still_need_public_access_chain(self):
        digest=hashlib.sha256(b'x').hexdigest()
        result=assess(self.record(),[dict(id='old1',digests=[dict(algorithm='SHA-256',digest=digest)])],
            dict(members=[dict(name='BILLS-113hr1ih.xml',sha256=digest)]))
        self.assertEqual(len(result['old_digest_member_matches']),1)
        self.assertFalse(result['historical_public_access_proven'])
        self.assertEqual(result['disposition'],'unresolved_public_access_chain')
    def test_invalid_digest_is_not_recovered_bytes(self):
        r=assess(self.record(),[dict(id='old1',digests=[dict(algorithm='SHA-256',digest='bad')])],{})
        self.assertFalse(r['recovered_digest_records'][0]['supported_valid_digest']);self.assertEqual(r['old_digest_member_matches'],[])
    def test_xml_entities_and_wrong_root_rejected(self):
        for raw in [b'<!DOCTYPE premis []><premis/>',b'<html/>','<!DOCTYPE premis []><premis/>'.encode('utf-16')]:
            with self.assertRaises(ValueError):objects(raw)
    def test_zip_inventory_without_extraction(self):
        buf=io.BytesIO()
        with zipfile.ZipFile(buf,'w') as z:z.writestr('BILLS-113hr1ih/xml/BILLS-113hr1ih.xml',b'x')
        inv=inspect_zip(buf.getvalue(),'BILLS-113hr1ih')
        self.assertEqual(inv['members'][0]['sha256'],hashlib.sha256(b'x').hexdigest())
    def test_zip_traversal_and_substring_identity_rejected(self):
        for path in ['../BILLS-113hr1ih.xml','unrelated-BILLS-113hr1ih.xml']:
            buf=io.BytesIO()
            with zipfile.ZipFile(buf,'w') as z:z.writestr(path,b'x')
            with self.assertRaises(ValueError):inspect_zip(buf.getvalue(),'BILLS-113hr1ih')
    def test_partial_error_body_retained(self):
        class Reply:
            code=200;headers={}
            def __enter__(self):return self
            def __exit__(self,*args):pass
            def read(self,n):
                if not hasattr(self,'done'):self.done=True;return b'partial'
                raise TimeoutError('fixture')
        with patch('urllib.request.build_opener') as opener:
            opener.return_value.open.return_value=Reply()
            raw,r=fetch('https://www.govinfo.gov/example')
        self.assertEqual(raw,b'partial');self.assertIn('TimeoutError',r['error']);self.assertEqual(r['bytes'],7)
