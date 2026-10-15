// BUILD-019 synthetic-only storage contracts; intentionally no live resource calls.
// Credentials, customer documents and PII must never be passed through this module.
export const RESOURCE_NAMES = Object.freeze({
  database: "tax-genie-db",
  documents: "tax-genie-documents",
});
export const BINDINGS = Object.freeze({ database: "TAX_GENIE_DB", documents: "TAX_GENIE_DOCUMENTS" });
const tenantRE = /^[a-zA-Z0-9][a-zA-Z0-9_-]{0,63}$/;
const caseRE = /^[a-zA-Z0-9][a-zA-Z0-9_-]{0,95}$/;
export function documentKey(tenantId, caseId, objectId) {
  for (const [field, value, re] of [
    ["tenantId",tenantId,tenantRE], ["caseId",caseId,caseRE], ["objectId",objectId,caseRE],
  ]) {
    if (typeof value !== "string" || !re.test(value)) throw new TypeError("Invalid " + field);
  }
  return `tenants/${tenantId}/cases/${caseId}/documents/${objectId}`;
}
export function validateBindings(env) {
  if (env === null || typeof env !== "object") return { ready: false, missing: ["TAX_GENIE_DB","TAX_GENIE_DOCUMENTS"] };
  const missing = [BINDINGS.database,BINDINGS.documents].filter(name => !env[name]);
  return { ready: missing.length === 0, missing };
}
export function assertTenantScopedKey(tenantId, key) {
  if (typeof tenantId !== "string" || !tenantRE.test(tenantId)) throw new TypeError("Invalid tenantId");
  if (typeof key !== "string" || !key.startsWith(`tenants/${tenantId}/`)) throw new Error("cross_tenant_object_access_denied");
  const parts=key.split("/");
  if (parts.length !== 6 || parts[0]!=="tenants" || parts[2]!=="cases" || parts[4]!=="documents" ||
      !caseRE.test(parts[3]) || !caseRE.test(parts[5])) throw new Error("invalid_object_key");
  return true;
}
