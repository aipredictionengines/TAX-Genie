import os
import sqlite3
import unittest
from tax_genie.audit_journal import AuditJournal
from tax_genie.audit_anchor import AnchorManager

class TestAuditAnchor(unittest.TestCase):
    def setUp(self):
        self.db=sqlite3.connect(":memory:")
        self.j=AuditJournal(os.urandom(32))
        self.a=AnchorManager(os.urandom(32))
        self.j.setup(self.db)
        self.j.append(self.db,"tenant-a","CASE_CREATED","fixture1")
    def tearDown(self):
        self.db.close()
    def test_checkpoint_verifies(self):
        self.assertTrue(self.a.verify(self.db,self.a.issue(self.db,"tenant-a")))
    def test_detects_row_deletion(self):
        anchor=self.a.issue(self.db,"tenant-a")
        self.db.execute("DELETE FROM audit_events")
        self.assertFalse(self.a.verify(self.db,anchor))
    def test_detects_modified_checkpoint(self):
        anchor=self.a.issue(self.db,"tenant-a")
        anchor["last_hash"]="bad"
        self.assertFalse(self.a.verify(self.db,anchor))
    def test_wrong_key(self):
        anchor=self.a.issue(self.db,"tenant-a")
        self.assertFalse(AnchorManager(os.urandom(32)).verify(self.db,anchor))
    def test_rejects_weak_key(self):
        with self.assertRaises(ValueError):AnchorManager(b"123")
if __name__=="__main__":unittest.main()
