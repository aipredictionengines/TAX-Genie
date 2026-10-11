import os
import sqlite3
import tempfile
import unittest
from tax_genie.audit_journal import AuditJournal

class TestAuditJournal(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.con=sqlite3.connect(self.temp.name+"/audit.db")
        self.audit=AuditJournal(os.urandom(32))
        self.audit.setup(self.con)
    def tearDown(self):
        self.con.close()
        self.temp.cleanup()
    def test_tenant_chains_separate(self):
        self.audit.append(self.con,"a","CASE_CREATED","case-a")
        self.audit.append(self.con,"b","CASE_CREATED","case-b")
        self.audit.append(self.con,"a","CASE_DELETED","case-a")
        self.assertTrue(self.audit.verify(self.con,"a"))
        self.assertTrue(self.audit.verify(self.con,"b"))
    def test_tampering_detected(self):
        self.audit.append(self.con,"a","CASE_CREATED","case-a")
        self.con.execute("UPDATE audit_events SET event='CASE_DELETED' WHERE tenant='a'")
        self.assertFalse(self.audit.verify(self.con,"a"))
    def test_no_raw_identifier_persisted(self):
        self.audit.append(self.con,"a","CASE_CREATED","my-secret-case-id")
        row=self.con.execute("SELECT entity_digest FROM audit_events").fetchone()[0]
        self.assertNotIn("my-secret-case-id",row)
    def test_reject_invalid_events(self):
        with self.assertRaises(ValueError): self.audit.append(self.con,"a","SENSITIVE_INVOICE","id")
if __name__=="__main__": unittest.main()
