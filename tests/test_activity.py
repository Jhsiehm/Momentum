import tempfile
import unittest
from pathlib import Path
from engine.store import Store,now
from engine import workspace as w

class ActivityTests(unittest.TestCase):
    def test_latest_event_per_step_is_returned_without_arguments(self):
        with tempfile.TemporaryDirectory() as folder:
            store=Store(Path(folder)/'activity.sqlite');w.initialize(store);chat=w.new_chat(store)
            with store.db:store.db.execute('INSERT INTO messages VALUES (?,?,?,?,?,?,?,?)',('message',chat['id'],'assistant','Working','running','[]',now(),None))
            w.record_activity(store,'message','tool1','read','Read sources','running')
            w.record_activity(store,'message','tool1','read','Read sources','completed')
            w.record_activity(store,'message','tool2','audit','Check evidence','blocked')
            events=w.get_chat(store,chat['id'])['messages'][0]['activity']
            self.assertEqual([e['status'] for e in events],['completed','blocked'])
            self.assertEqual(store.db.execute('SELECT COUNT(*) FROM message_activity').fetchone()[0],3)
            self.assertNotIn('arguments',events[0])
            with self.assertRaises(ValueError):w.record_activity(store,'message','bad','invented','Fake','completed')
            store.close()
