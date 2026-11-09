import csv
import io
import struct
import unittest
import zlib
from scripts import bicam_inventory_audit_v1 as m

class InventoryTests(unittest.TestCase):
    def data(self, rows):
        out=io.StringIO(); w=csv.writer(out)
        w.writerow(['bill_id','bill_type','bill_number','congress','introduced_at','is_law'])
        w.writerows(rows)
        return out.getvalue().encode()
    def row(self, number=1):
        return [f'hr{number}-113','hr',str(number),'113','2013-01-03','FORBIDDEN']
    def test_identity_only(self):
        result=m.inventory(self.data([self.row()]))
        self.assertEqual(result['rows'][0]['bill_id'],'hr1-113')
        self.assertNotIn('is_law',str(result))
        self.assertNotIn('FORBIDDEN',str(result))
    def test_duplicate_blocks_sample(self):
        r=m.inventory(self.data([self.row(),self.row()]))
        self.assertFalse(r['complete_identity_census']); self.assertEqual(r['sample'],[])
    def test_date_outside_congress(self):
        row=self.row(); row[4]='2015-01-03'
        self.assertEqual(m.inventory(self.data([row]))['issues'][0]['issue'],'invalid_introduction_date')
    def test_identity_mismatch(self):
        row=self.row(); row[0]='s1-113'
        self.assertEqual(m.inventory(self.data([row]))['issues'][0]['issue'],'identity_disagreement')
    def test_sample_order_independent(self):
        rows=[self.row(n) for n in range(1,121)]
        a=m.inventory(self.data(rows)); b=m.inventory(self.data(rows[::-1]))
        self.assertEqual(a['sample'],b['sample']); self.assertEqual(len(a['sample']),100)
    def test_bad_columns(self):
        with self.assertRaises(ValueError):m.inventory(b'bill_id,bill_id\nx,x\n')
    def compressed(self):
        raw=b'sample contents'*20; c=zlib.compressobj(wbits=-15); compressed=c.compress(raw)+c.flush()
        return raw,compressed,dict(compressed=len(compressed),uncompressed=len(raw),crc=zlib.crc32(raw))
    def test_inflate(self):
        raw,c,e=self.compressed();self.assertEqual(m.inflate(c,e),raw)
    def test_bad_crc(self):
        raw,c,e=self.compressed();e['crc']^=1
        with self.assertRaises(ValueError):m.inflate(c,e)
    def test_inflate_bomb_cap(self):
        raw,c,e=self.compressed();e['uncompressed']=10
        with self.assertRaises(ValueError):m.inflate(c,e)
    def test_truncated(self):
        raw,c,e=self.compressed();e['compressed']-=1
        with self.assertRaises(ValueError):m.inflate(c[:-1],e)
    def test_header_mismatch(self):
        e=dict(flags=0,crc=1,compressed=2,uncompressed=3)
        h=struct.pack('<IHHHHHIIIHH',0x04034b50,20,0,8,0,0,1,2,3,9,0)
        self.assertEqual(m.local_header(h,e),(9,0));e['crc']=2
        with self.assertRaises(ValueError):m.local_header(h,e)
    def test_tail_hash(self):
        with self.assertRaises(ValueError):m.directory(b'bad',100)

if __name__=='__main__': unittest.main()
