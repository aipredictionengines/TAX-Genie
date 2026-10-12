import os
import sqlite3
import unittest
from tax_genie.audit_journal import AuditJournal
from tax_genie.audit_anchor import AnchorManager
from tax_genie.audit_custody import DisabledCustody,CustodyUnavailable,TestOnlyMemoryCustody,publish_verified,verify_retained
from tax_genie.key_versions import KeyVersion, VersionedAnchorKeys

class TestAuditCustody(unittest.TestCase):
    def setUp(self):
        self.db=sqlite3.connect(":memory:")
        self.j=AuditJournal(os.urandom(32));self.j.setup(self.db)
        self.j.append(self.db,"a","CASE_CREATED","one")
        self.anchor=AnchorManager(os.urandom(32))
    def tearDown(self):self.db.close()
    def test_disabled_external_custody(self):
        with self.assertRaises(CustodyUnavailable):
            publish_verified(self.anchor,self.db,"a")
    def test_synthetic_receipt_and_row_integrity(self):
        store=TestOnlyMemoryCustody({})
        receipt=publish_verified(self.anchor,self.db,"a",store)
        self.assertTrue(verify_retained(self.anchor,self.db,receipt,store))
        self.db.execute("UPDATE audit_events SET record_hash='bad' WHERE tenant='a'")
        self.assertFalse(verify_retained(self.anchor,self.db,receipt,store))
    def test_old_key_valid_after_rotation(self):
        ring=VersionedAnchorKeys([KeyVersion("v1",os.urandom(32)),KeyVersion("v2",os.urandom(32))],"v1")
        old=ring.issue(self.db,"a")
        ring.rotate("v2")
        new=ring.issue(self.db,"a")
        self.assertTrue(ring.verify(self.db,old))
        self.assertTrue(ring.verify(self.db,new))
        self.assertFalse(VersionedAnchorKeys([KeyVersion("v2",os.urandom(32))],"v2").verify(self.db,old))
    def test_reject_weak_key(self):
        with self.assertRaises(ValueError):VersionedAnchorKeys([KeyVersion("weak",b"x"*8)],"weak")
if __name__=="__main__":unittest.main()
