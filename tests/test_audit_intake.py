import os
import tempfile
import unittest
from tax_genie.intake import IntakeStore

class TestAuditIntake(unittest.TestCase):
    def test_create_and_delete_are_journaled(self):
        with tempfile.TemporaryDirectory() as folder:
            store=IntakeStore(folder+"/pilot.sqlite",os.urandom(32))
            case=store.new_case("tenant-a")
            with store._db() as con:
                self.assertTrue(store.audit.verify(con,"tenant-a"))
                self.assertEqual(con.execute("SELECT COUNT(*) FROM audit_events WHERE tenant='tenant-a'").fetchone()[0],1)
            self.assertTrue(store.delete_case("tenant-a",case["id"]))
            with store._db() as con:
                self.assertTrue(store.audit.verify(con,"tenant-a"))
                self.assertEqual(con.execute("SELECT COUNT(*) FROM audit_events WHERE tenant='tenant-a'").fetchone()[0],2)
    def test_wrong_tenant_cannot_emit_delete(self):
        with tempfile.TemporaryDirectory() as folder:
            store=IntakeStore(folder+"/pilot.sqlite",os.urandom(32))
            case=store.new_case("tenant-a")
            self.assertFalse(store.delete_case("tenant-b",case["id"]))
            with store._db() as con:
                self.assertEqual(con.execute("SELECT COUNT(*) FROM audit_events WHERE tenant='tenant-b'").fetchone()[0],0)
if __name__=="__main__": unittest.main()
