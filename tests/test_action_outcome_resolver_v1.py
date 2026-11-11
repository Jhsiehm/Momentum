import unittest
from scripts import action_outcome_resolver_v1 as m
from scripts import official_context_features_v2 as old
from tests import test_action_label_contract_v1 as f
from tests import test_official_context_v1 as fixtures
CASE=fixtures.CASE
CUTOFF='2013-07-02'

class ResolverTests(unittest.TestCase):
    def resolve(self,actions,law='113-1'):
        return m.resolve_outcome(f.raw(actions,law),CASE,CUTOFF)
    def test_exact_annotation_with_independent_concordance(self):
        actions=f.action('Became Public Law No: 113-1.')+f.action('Signed by President.')
        self.assertIsNone(old.resolve_outcome(f.raw(actions),CASE,CUTOFF)['y'])
        answer=self.resolve(actions);self.assertEqual(answer['y'],1);self.assertEqual(answer['enacted_at'],'2014-01-01')
    def test_signature_alone_unknown_with_or_without_list(self):
        self.assertIsNone(self.resolve(f.action('Signed by President.'))['y'])
        raw=fixtures.ContextTests().raw(actions=f.action('Signed by President.'))
        self.assertIsNone(m.resolve_outcome(raw,CASE,CUTOFF)['y'])
    def test_all_annotation_dates_must_agree(self):
        acts=f.action('Became Public Law No: 113-1.')+f.action('Signed by President.')+f.action('Signed by President.',when='2014-01-02')
        r=self.resolve(acts);self.assertIsNone(r['y']);self.assertEqual(r['reason'],'Signing annotation/enactment date disagreement')
    def test_no_broader_code_source_or_text_exception(self):
        concord=f.action('Became Public Law No: 113-1.')
        for signature in (f.action('Signed by President.',source='2'),f.action('Signed by President.',code='E40000'),f.action('Signed by President'),f.action('signed by President.'),f.action('Signed by President. Additional statement')):
            self.assertIsNone(self.resolve(concord+signature)['y'])
    def test_wrong_law_and_multiple_dates_stay_unknown(self):
        signature=f.action('Signed by President.')
        for events in (f.action('Became Public Law No: 113-2.'),f.action('Became Public Law No: 113-1.')+f.action('Became Public Law No: 113-1.',when='2014-01-02')):
            self.assertIsNone(self.resolve(events+signature)['y'])
    def test_risk_boundaries_unchanged(self):
        for when in ('2013-07-02','2013-06-01','2015-01-03'):
            self.assertIsNone(self.resolve(f.action('Became Public Law No: 113-1.',when=when)+f.action('Signed by President.',when=when))['y'])
    def test_ordinary_negative_identical(self):
        raw=fixtures.ContextTests().raw()
        self.assertEqual(m.resolve_outcome(raw,CASE,CUTOFF),old.resolve_outcome(raw,CASE,CUTOFF))
    def test_valid_positive_without_annotation_identical(self):
        raw=f.raw(f.action('Became Public Law No: 113-1.'))
        self.assertEqual(m.resolve_outcome(raw,CASE,CUTOFF),old.resolve_outcome(raw,CASE,CUTOFF))

if __name__=='__main__':unittest.main()
