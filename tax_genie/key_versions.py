"""Versioned key references; no hardcoded secrets and no production KMS.

Explicit caller-managed, offline keyring used for tests and future KMS adapter.
"""
from __future__ import annotations
from dataclasses import dataclass
from .audit_anchor import AnchorManager

@dataclass(frozen=True)
class KeyVersion:
    key_id: str
    material: bytes

class VersionedAnchorKeys:
    def __init__(self, versions: list[KeyVersion], active_id: str):
        ids=[v.key_id for v in versions]
        if not versions or len(set(ids))!=len(ids) or any(not x for x in ids):
            raise ValueError("Unique nonempty key identifiers required")
        if any(not isinstance(v.material,bytes) or len(v.material)<32 for v in versions):
            raise ValueError("Keys must contain at least 32 bytes")
        if active_id not in ids:
            raise ValueError("Active key missing")
        self._keys={v.key_id:v.material for v in versions}
        self.active_id=active_id

    def rotate(self, next_active: str):
        if next_active not in self._keys:
            raise ValueError("Unknown rotation key")
        self.active_id=next_active

    def issue(self, db, tenant: str) -> dict:
        checkpoint=AnchorManager(self._keys[self.active_id]).issue(db,tenant)
        return {"key_id":self.active_id,"checkpoint":checkpoint}

    def verify(self, db, wrapped: dict) -> bool:
        if not isinstance(wrapped,dict) or set(wrapped)!={"key_id","checkpoint"}:
            return False
        secret=self._keys.get(wrapped["key_id"])
        return bool(secret and AnchorManager(secret).verify(db,wrapped["checkpoint"]))
