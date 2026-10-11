"""Conservative pilot ingress controls; not a production security certification."""
import hashlib
import hmac
import time
from collections import defaultdict
from threading import Lock

class RateLimiter:
    def __init__(self, limit=30, window=60):
        self.limit=limit
        self.window=window
        self.events=defaultdict(list)
        self.lock=Lock()
    def allow(self, subject):
        now=time.monotonic()
        with self.lock:
            history=[t for t in self.events[subject] if now-t<self.window]
            if len(history)>=self.limit:
                self.events[subject]=history
                return False
            history.append(now)
            self.events[subject]=history
            return True

class ScannerUnavailable(RuntimeError):
    pass

class Scanner:
    """Fail-closed scanner protocol: no client-facing uploads until wired."""
    def scan(self, data: bytes) -> bool:
        raise ScannerUnavailable("Malware scanner is not configured")

def verified_scan(scanner, content):
    try:
        return scanner.scan(content) is True
    except Exception:
        return False

def audit_digest(tenant, case_id, event, secret):
    """Opaque integrity tag, not a complete append-only audit system."""
    message=f"{tenant}:{case_id}:{event}".encode()
    return hmac.new(secret,message,hashlib.sha256).hexdigest()
