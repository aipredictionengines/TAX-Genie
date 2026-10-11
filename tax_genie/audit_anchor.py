"""Exportable signed audit checkpoints; external anchoring is NOT implemented.

The checkpoint must be stored outside the database under independent custody
to detect rollback/truncation. Do not log or commit live checkpoints containing
tenant identifiers.
"""
from __future__ import annotations
import hashlib
import hmac
import json
import sqlite3
from datetime import datetime, timezone

class AnchorManager:
    def __init__(self, secret: bytes):
        if not isinstance(secret, bytes) or len(secret)<32:
            raise ValueError("Independent anchor secret requires >=32 bytes")
        self._secret=hmac.new(secret,b"tax-genie:external-anchor:v1",hashlib.sha256).digest()

    def _sign(self, payload: dict) -> str:
        encoded=json.dumps(payload,sort_keys=True,separators=(",",":"),ensure_ascii=True).encode()
        return hmac.new(self._secret,encoded,hashlib.sha256).hexdigest()

    def issue(self, db: sqlite3.Connection, tenant: str) -> dict:
        if not tenant:
            raise ValueError("Tenant required")
        row=db.execute("SELECT seq,record_hash FROM audit_events WHERE tenant=? ORDER BY seq DESC LIMIT 1",(tenant,)).fetchone()
        if row is None:
            raise ValueError("No audit events")
        payload={"version":1,"tenant":tenant,"last_seq":row[0],
                 "last_hash":row[1],"issued_at":datetime.now(timezone.utc).isoformat()}
        return {**payload,"signature":self._sign(payload)}

    def verify(self, db: sqlite3.Connection, anchor: dict) -> bool:
        if not isinstance(anchor,dict) or set(anchor)!={"version","tenant","last_seq","last_hash","issued_at","signature"}:
            return False
        payload={k:v for k,v in anchor.items() if k!="signature"}
        try:
            if payload["version"] != 1 or not isinstance(payload["tenant"],str) or not payload["tenant"]:
                return False
            if type(payload["last_seq"]) is not int or payload["last_seq"]<1:
                return False
            if not isinstance(anchor["signature"],str) or not hmac.compare_digest(self._sign(payload),anchor["signature"]):
                return False
            from .audit_journal import AuditJournal
            # Without the journal HMAC key, this verifies only the anchored row,
            # not the whole intervening chain.
            row=db.execute("SELECT record_hash FROM audit_events WHERE tenant=? AND seq=?",
                           (payload["tenant"],payload["last_seq"])).fetchone()
            return row is not None and hmac.compare_digest(row[0],payload["last_hash"])
        except (TypeError,ValueError,sqlite3.Error):
            return False
