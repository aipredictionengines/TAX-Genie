"""Fail-closed custody adapter for independently retained audit checkpoints.

The default backend is disabled. In-memory backend is TEST-ONLY; it offers no
external durability or independence. Production custody needs an independently
controlled immutable store and its own authentication.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Protocol

class CustodyUnavailable(RuntimeError):
    pass

class AuditCustody(Protocol):
    def publish(self, checkpoint: dict) -> str: ...
    def retrieve(self, receipt: str) -> dict: ...

class DisabledCustody:
    def publish(self, checkpoint: dict) -> str:
        raise CustodyUnavailable("External audit custody is not configured")
    def retrieve(self, receipt: str) -> dict:
        raise CustodyUnavailable("External audit custody is not configured")

@dataclass
class TestOnlyMemoryCustody:
    """Synthetic tests only. MUST NOT be used as external audit storage."""
    records: dict
    def publish(self, checkpoint: dict) -> str:
        from copy import deepcopy
        import hashlib, json
        receipt=hashlib.sha256(json.dumps(checkpoint,sort_keys=True).encode()).hexdigest()
        if receipt in self.records:
            raise ValueError("Duplicate receipt")
        self.records[receipt]=deepcopy(checkpoint)
        return receipt
    def retrieve(self, receipt: str) -> dict:
        from copy import deepcopy
        return deepcopy(self.records[receipt])

def publish_verified(anchor_manager, db, tenant: str, custody=None) -> str:
    custody=custody if custody is not None else DisabledCustody()
    checkpoint=anchor_manager.issue(db,tenant)
    if not anchor_manager.verify(db,checkpoint):
        raise ValueError("Checkpoint cannot be verified")
    return custody.publish(checkpoint)

def verify_retained(anchor_manager, db, receipt: str, custody=None) -> bool:
    custody=custody if custody is not None else DisabledCustody()
    return anchor_manager.verify(db,custody.retrieve(receipt))
