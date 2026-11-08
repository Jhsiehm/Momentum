import unittest
from scripts.bill_context_design_text_v2 import render


class DesignTextV2Tests(unittest.TestCase):
    def xml(self, congress='113th CONGRESS', body='<section id="s"><header>Short title</header><text>This Act shall not auth<em>or</em>ize caf\u00e9.</text><subsection><text>Except as provided.</text></subsection></section>'):
        return f'<bill><form><congress>{congress}</congress><legis-num>H. R. 1</legis-num></form><legis-body>{body}</legis-body></bill>'.encode()

    def test_strict_identity(self):
        for congress in ('1130th CONGRESS','113th CONGRESS extra','113','114th CONGRESS'):
            with self.assertRaises(ValueError):render(self.xml(congress),'113-hr1')
        with self.assertRaises(ValueError):render(self.xml(),'113-hr2')
        self.assertEqual(render(self.xml(),'113-hr1')['bill_id'],'113-hr1')

    def test_block_boundaries_and_inline_continuity(self):
        value=render(self.xml(),'113-hr1')
        self.assertIn('Short title\n\nThis Act',value['text'])
        self.assertIn('shall not authorize caf\u00e9.',value['text'])
        section=next(s for s in value['spans'] if s['xml_id']=='s')
        self.assertIn('Except as provided.',value['text'][section['start']:section['end']])
        paths=[s['path'] for s in value['spans']]
        self.assertEqual(len(paths),len(set(paths)))

    def test_entities_rejected(self):
        with self.assertRaises(ValueError):render(b'<!ENTITY x "unsafe">'+self.xml(),'113-hr1')


if __name__=='__main__':unittest.main()
