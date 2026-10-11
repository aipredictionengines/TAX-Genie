"""Tenant-scoped chained HMAC audit records for private pilot use.

SQLite is mutable: this provides tamper detection against changes without the
key, NOT immutability, rollback protection or an external trusted audit sink.
"""
from __future__ import annotations
import hashlib
import hmac
import json
import sqlite3
from datetime import datetime, timezone

ALLOWED_EVENTS = frozenset({"CASE_CREATED","CASE_DELETED","DOCUMENT_ACCEPTED"})

class AuditJournal:
    def __init__(self, key: bytes):
        if not isinstance(key, bytes) or len(key) < 32:
            raise ValueError("Audit HMAC key requires 32+ bytes")
        self.key = hmac.new(key, b"tax-genie:audit:v1", hashlib.sha256).digest()

    @staticmethod
    def setup(con: sqlite3.Connection) -> None:
        con.execute("""CREATE TABLE IF NOT EXISTS audit_events(
          seq INTEGER PRIMARY KEY AUTOINCREMENT,
          tenant TEXT NOT NULL,
          event TEXT NOT NULL,
          entity_digest TEXT NOT NULL,
          occurred TEXT NOT NULL,
          prev_hash TEXT NOT NULL,
          record_hash TEXT NOT NULL
        )""")
        con.execute("CREATE INDEX IF NOT EXISTS audit_tenant_seq ON audit_events(tenant,seq)")

    def _tag(self, values: list[str]) -> str:
        canonical = json.dumps(values, separators=(",",":"), ensure_ascii=True).encode()
        return hmac.new(self.key,canonical,hashlib.sha256).hexdigest()

    def append(self, con: sqlite3.Connection, tenant: str, event: str, entity_id: str) -> None:
        if not tenant or event not in ALLOWED_EVENTS or not entity_id:
            raise ValueError("Invalid audit input")
        digest=self._tag(["entity",tenant,entity_id])
        previous=con.execute("SELECT record_hash FROM audit_events WHERE tenant=? ORDER BY seq DESC LIMIT 1",(tenant,)).fetchone()
        prev=previous[0] if previous else "GENESIS"
        occurred=datetime.now(timezone.utc).isoformat()
        tag=self._tag(["record",tenant,event,digest,occurred,prev])
        con.execute("INSERT INTO audit_events(tenant,event,entity_digest,occurred,prev_hash,record_hash) VALUES(?,?,?,?,?,?)",
                    (tenant,event,digest,occurred,prev,tag))

    def verify(self, con: sqlite3.Connection, tenant: str) -> bool:
        rows=con.execute("SELECT event,entity_digest,occurred,prev_hash,record_hash FROM audit_events WHERE tenant=? ORDER BY seq",(tenant,)).fetchall()
        prev="GENESIS"
        for event,digest,occurred,linked,tag in rows:
            expected=self._tag(["record",tenant,event,digest,occurred,prev])
            if linked != prev or not hmac.compare_digest(tag,expected):
                return False
            prev=tag
        return True
