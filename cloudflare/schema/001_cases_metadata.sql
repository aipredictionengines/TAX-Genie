-- BUILD-019 D1 schema proposal. NOT applied to any database.
-- No PDFs, customer identifiers, financial data, tax IDs, invoice bytes, or credentials here.
-- Case IDs and tenant IDs are opaque application-generated identifiers.
CREATE TABLE IF NOT EXISTS tenants (
  tenant_id TEXT PRIMARY KEY NOT NULL,
  created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS cases (
  tenant_id TEXT NOT NULL,
  case_id TEXT NOT NULL,
  status TEXT NOT NULL CHECK(status IN ('DRAFT','PROCESSING','REVIEW','BLOCKED')),
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  PRIMARY KEY (tenant_id, case_id),
  FOREIGN KEY (tenant_id) REFERENCES tenants(tenant_id)
);
CREATE INDEX IF NOT EXISTS idx_cases_tenant_status ON cases(tenant_id,status);
-- Audit custody remains out of scope: D1 is NOT immutable or independent WORM storage.
