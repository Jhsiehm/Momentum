import unittest
from scripts.cross_congress_evaluate import unique,make_split,probability,train_models


def row(bid,c=113,y=0,available='2015-04-01T00:00:00Z',cutoff='2017-07-01T00:00:00Z',exclusion=None):
 return dict(bill_id=bid,congress=c,y=y,label_available_at=available,cutoff=cutoff,exclusion=exclusion)


class CrossCongressTests(unittest.TestCase):
 def test_outcome_independent_family_representative(self):
  rows=[row('a',y=1),row('b'),row('c')];groups=dict(a='f',b='f',c='g')
  self.assertEqual([r['bill_id'] for r in unique(rows,groups)],['a','c'])
  for r in rows:r['y']=1-r['y']
  self.assertEqual([r['bill_id'] for r in unique(rows,groups)],['a','c'])
 def test_future_labels_excluded(self):
  rows=[row('early'),row('late',available='2018-01-01T00:00:00Z'),row('test',115)]
  train,test=make_split(rows,115,{r['bill_id']:r['bill_id'] for r in rows})
  self.assertEqual([r['bill_id'] for r in train],['early'])
 def test_eval_family_excluded_from_training(self):
  rows=[row('train'),row('test',115)]
  train,test=make_split(rows,115,dict(train='same',test='same'))
  self.assertEqual(train,[]);self.assertEqual(len(test),1)
 def test_future_congress_never_trains(self):
  rows=[row('future',116),row('test',115)]
  self.assertEqual(make_split(rows,115,dict(future='f',test='t'))[0],[])
 def test_ineligible_rows_remain_excluded(self):
  self.assertEqual(unique([row('a',exclusion='late checkpoint')],dict(a='a')),[])
 def test_no_eligible_evaluation(self):
  self.assertEqual(make_split([row('a')],115,dict(a='a')),([],[]))

class SourceAndFittingTests(unittest.TestCase):
 def test_abbreviated_law_header(self):
  from scripts.prepare_cross_congress_sources import parse_final
  raw=b'FINAL LISTING\nH.R. 41/P.L. 113-1\nTitle\n(Jan. 6, 2013; 127 Stat. 3; 1 page)\n'
  self.assertEqual(parse_final(raw,113),[dict(law=1,bill_id='113-hr41',enacted='2013-01-06')])
 def test_calibration_families_disjoint(self):
  rows=[dict(bill_id=f'113-hr{i}',congress=113,x=[(i%4)/4,.2,.1,.2,i%2,0],y=int(i%7==0)) for i in range(300)]
  result=train_models(rows)['calibrated_all_history']
  self.assertFalse(set(result['core_ids']) & set(result['calibration_ids']))
  self.assertEqual(set(result['core_ids']) | set(result['calibration_ids']),{r['bill_id'] for r in rows})
 def test_label_at_checkpoint_is_not_earlier(self):
  rows=[row('train',available='2017-07-01T00:00:00Z'),row('test',115)]
  self.assertEqual(make_split(rows,115,dict(train='a',test='b'))[0],[])

class CompatibilityTests(unittest.TestCase):
 def test_legacy_identifiers_and_preserved_raw_hash(self):
  from engine.billstatus_compat import normalize
  import hashlib,xml.etree.ElementTree as ET
  raw=b'<billStatus><bill><billType>HR</billType><billNumber>3354</billNumber></bill></billStatus>'
  converted,proof=normalize(raw)
  self.assertEqual(ET.fromstring(converted).findtext('bill/type'),'HR')
  self.assertEqual(ET.fromstring(converted).findtext('bill/number'),'3354')
  self.assertEqual(proof['original_sha256'],hashlib.sha256(raw).hexdigest())
 def test_modern_unchanged(self):
  from engine.billstatus_compat import normalize
  raw=b'<billStatus><bill><type>HR</type><number>1</number></bill></billStatus>'
  self.assertEqual(normalize(raw),(raw,None))
 def test_conflicting_alias_rejected(self):
  from engine.billstatus_compat import normalize
  with self.assertRaises(ValueError):normalize(b'<billStatus><bill><type>S</type><billType>HR</billType></bill></billStatus>')

class LegacyImportTests(unittest.TestCase):
 def test_import_retains_original_bytes_hash(self):
  import tempfile,hashlib
  from pathlib import Path
  from engine.store import Store
  from engine.ingest import import_xml
  raw=b'<billStatus><bill><congress>115</congress><billType>HR</billType><billNumber>3354</billNumber><introducedDate>2017-07-21</introducedDate><title>Fixture</title></bill></billStatus>'
  with tempfile.TemporaryDirectory() as directory:
   store=Store(Path(directory)/'test.sqlite')
   try:
    result=import_xml(store,raw,'https://www.govinfo.gov/test')
    self.assertEqual(result['bill_id'],'115-hr3354')
    self.assertEqual(result['hash'],hashlib.sha256(raw).hexdigest())
    self.assertEqual(store.bill('official','115-hr3354')['raw_hash'],result['hash'])
   finally:store.close()

class ConflictDispositionTests(unittest.TestCase):
 def source(self,first,second):
  from types import SimpleNamespace
  import xml.etree.ElementTree as ET
  raw=f'<billStatus><bill><congress>116</congress><type>S</type><number>4935</number><introducedDate>{first}</introducedDate><title>Test</title></bill></billStatus>'.encode()
  mods=ET.fromstring(f'<mods xmlns="http://www.loc.gov/mods/v3"><recordInfo><recordIdentifier>BILLS-116s4935is</recordIdentifier></recordInfo><extension><action date="{second}">Mr. X introduced the following bill</action></extension></mods>')
  return SimpleNamespace(get=lambda url:(raw,dict(url=url))),mods
 def test_both_dates_late_excludes_without_choosing(self):
  from unittest.mock import patch
  from engine.cross_congress_adjudication import late_introduction_conflict
  source,mods=self.source('2020-12-01','2020-11-30')
  with patch('engine.cross_congress_adjudication.cohort.package_audit',return_value=(mods,{})):
   result=late_introduction_conflict(source,'116-s4935')
  self.assertEqual(len(result['adjudication']['official_dates']),2)
  self.assertNotIn('y',result)
  self.assertTrue(result['exclusion'])
 def test_potentially_eligible_date_blocks(self):
  from unittest.mock import patch
  from engine.cross_congress_adjudication import late_introduction_conflict
  source,mods=self.source('2019-01-01','2020-11-30')
  with patch('engine.cross_congress_adjudication.cohort.package_audit',return_value=(mods,{})):
   with self.assertRaises(AssertionError):late_introduction_conflict(source,'116-s4935')

class QuarantineTests(unittest.TestCase):
 source=ConflictDispositionTests.source
 def test_absent_action_assigns_no_label_or_features(self):
  from unittest.mock import patch
  from engine.cross_congress_adjudication import missing_introduction_action
  from engine.cohort import M
  source,mods=self.source('2020-12-01','2020-12-01')
  ext=mods.find('m:extension',M);ext.remove(ext.find('m:action',M))
  with patch('engine.cross_congress_adjudication.cohort.package_audit',return_value=(mods,{})):
   result=missing_introduction_action(source,'116-s4935')
  self.assertNotIn('y',result);self.assertNotIn('x',result)
  self.assertFalse(result['adjudication']['resolved'])
 def test_present_action_cannot_be_quarantined_as_absent(self):
  from unittest.mock import patch
  from engine.cross_congress_adjudication import missing_introduction_action
  source,mods=self.source('2020-12-01','2020-12-01')
  with patch('engine.cross_congress_adjudication.cohort.package_audit',return_value=(mods,{})):
   with self.assertRaises(AssertionError):missing_introduction_action(source,'116-s4935')

class LegislativeDayTests(unittest.TestCase):
 def fixture(self,header):
  import xml.etree.ElementTree as ET
  from types import SimpleNamespace
  mods=ET.fromstring('<mods xmlns="http://www.loc.gov/mods/v3"><recordInfo><recordIdentifier>BILLS-114s895is</recordIdentifier></recordInfo><originInfo><dateIssued>2015-03-27</dateIssued></originInfo><extension><action date="2015-03-27">Mr. X introduced the following bill</action></extension></mods>')
  raw=('[Congressional Bills 114th Congress] [S. 895 Introduced in Senate (IS)] '+header+' A BILL').encode()
  return SimpleNamespace(get=lambda url:(raw,dict(url=url))),mods
 def test_explicit_header_corroborates_both_dates(self):
  from engine.cross_congress_adjudication import legislative_day_validator
  source,mods=self.fixture('March 27 (legislative day, March 26), 2015')
  proof=legislative_day_validator(source,mods,'BILLS-114s895is','2015-03-26')
  self.assertEqual(proof['introduced_at'],'2015-03-26')
  self.assertEqual(proof['calendar_introduction_at'],'2015-03-27')
 def test_no_parenthetical_cannot_override_conflict(self):
  from engine.cross_congress_adjudication import legislative_day_validator
  source,mods=self.fixture('March 27, 2015')
  with self.assertRaises(AssertionError):legislative_day_validator(source,mods,'BILLS-114s895is','2015-03-26')
 def test_wrong_legislative_day_rejected(self):
  from engine.cross_congress_adjudication import legislative_day_validator
  source,mods=self.fixture('March 27 (legislative day, March 25), 2015')
  with self.assertRaises(AssertionError):legislative_day_validator(source,mods,'BILLS-114s895is','2015-03-26')

class ConflictQuarantineTests(unittest.TestCase):
 source=ConflictDispositionTests.source
 def test_conflicting_date_assigns_no_prediction_inputs(self):
  from unittest.mock import patch
  from engine.cross_congress_adjudication import conflicting_introduction_quarantine
  source,mods=self.source('2019-01-01','2019-01-02')
  with patch('engine.cross_congress_adjudication.cohort.package_audit',return_value=(mods,{})):
   result=conflicting_introduction_quarantine(source,'116-s4935')
  self.assertNotIn('x',result);self.assertNotIn('y',result);self.assertNotIn('cutoff',result)
  self.assertFalse(result['adjudication']['resolved'])
 def test_agreement_is_not_quarantined(self):
  from unittest.mock import patch
  from engine.cross_congress_adjudication import conflicting_introduction_quarantine
  source,mods=self.source('2019-01-01','2019-01-01')
  with patch('engine.cross_congress_adjudication.cohort.package_audit',return_value=(mods,{})):
   with self.assertRaises(AssertionError):conflicting_introduction_quarantine(source,'116-s4935')

if __name__=='__main__':unittest.main()
