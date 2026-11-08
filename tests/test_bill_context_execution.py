import copy
import unittest

from scripts.bill_context_execution import calendar_features, parse_design, select_pilot, stage_status


class BillContextExecutionTests(unittest.TestCase):
    def population(self):
        rows = [dict(bill_id=f'{c}-hr{i}', congress=c, exclusion=None, y=i%2)
                for c in range(113,118) for i in range(1,26)]
        return rows, {r['bill_id']:r['bill_id'] for r in rows}

    def test_selection_reproducible_blind_and_partitioned(self):
        rows, groups = self.population()
        selected, disposition = select_pilot(rows, groups)
        mutated = copy.deepcopy(rows)
        for row in mutated: row['y'] = 1-row['y']
        other, _ = select_pilot(list(reversed(mutated)), groups)
        self.assertEqual([r['bill_id'] for r in selected], [r['bill_id'] for r in other])
        self.assertEqual(len(disposition),125)
        self.assertEqual(len(selected),100)
        for c in range(113,118):
            self.assertEqual(sum(r['congress']==c and r['partition']=='design' for r in selected),10)
            self.assertEqual(sum(r['congress']==c and r['partition']=='quality' for r in selected),10)

    def test_global_families_shortfall_and_duplicate(self):
        rows, groups = self.population()
        for row in rows: groups[row['bill_id']] = 'one-family'
        with self.assertRaisesRegex(ValueError,'only 1/20'): select_pilot(rows,groups)
        with self.assertRaisesRegex(ValueError,'Duplicate'): select_pilot(rows+[rows[0]],groups)

    def test_calendar_boundary_and_timezone(self):
        row = dict(congress=117, cutoff='2023-01-02T12:00:00-05:00', x=[.5,180/730,0,0,1,0])
        values = calendar_features(row,'interaction')
        self.assertAlmostEqual(values[-2],1/730)
        self.assertAlmostEqual(values[-1],.5/730)
        self.assertEqual(calendar_features(row,'control'),row['x'])
        row['cutoff']='2023-01-03T17:00:00Z'
        with self.assertRaises(ValueError):calendar_features(row,'time')

    def test_xml_preserves_meaning_without_certifying_lexical_hits(self):
        raw = b'<bill><form><congress>117th CONGRESS</congress><legis-num>H. R. 1</legis-num></form><legis-body><section id="a"><text>Shall not authorize tax; caf\xc3\xa9.</text></section></legis-body></bill>'
        value=parse_design(raw,'117-hr1')
        self.assertIn('not authorize',value['text'])
        self.assertIn('caf\u00e9',value['sections'][0]['text'])
        self.assertIsNone(value['mechanism_labels']['authorize'])
        hit=value['lexical_candidates']['authorize'][0]
        self.assertEqual(value['text'][hit['start']:hit['end']],hit['quote'])
        with self.assertRaisesRegex(ValueError,'identity'):parse_design(raw,'117-hr2')
        with self.assertRaisesRegex(ValueError,'entities'):parse_design(b'<!ENTITY x "a">'+raw,'117-hr1')

    def test_stages_never_convert_missing_reviews_to_success(self):
        states=stage_status({},100)
        self.assertEqual(set(states),{f'E{i}' for i in range(10)})
        self.assertEqual(states['E0']['status'],'partial')
        self.assertTrue(all(states[f'E{i}']['status']=='blocked' for i in range(1,10)))


if __name__=='__main__':unittest.main()
