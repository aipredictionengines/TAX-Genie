import assert from "node:assert/strict";
import test from "node:test";
import {RESOURCE_NAMES,BINDINGS,documentKey,assertTenantScopedKey,validateBindings} from "../src/storage-contracts.mjs";

test("fixed isolated resource and binding names",()=>{
  assert.deepEqual(RESOURCE_NAMES,{database:"tax-genie-db",documents:"tax-genie-documents"});
  assert.equal(BINDINGS.database,"TAX_GENIE_DB");
  assert.equal(BINDINGS.documents,"TAX_GENIE_DOCUMENTS");
});
test("tenant scoped object keys",()=>{
  const key=documentKey("tenant-A","case-001","doc-001");
  assert.equal(key,"tenants/tenant-A/cases/case-001/documents/doc-001");
  assert.equal(assertTenantScopedKey("tenant-A",key),true);
  assert.throws(()=>assertTenantScopedKey("tenant-B",key),/cross_tenant/);
});
test("rejects traversal, slashes and malformed keys",()=>{
  for (const bad of ["../evil","a/b","", ".",".hidden","é"]) {
    assert.throws(()=>documentKey(bad,"case","file"));
  }
  assert.throws(()=>assertTenantScopedKey("tenant-A","tenants/tenant-A/cases/../documents/doc"),/invalid_object_key/);
  assert.throws(()=>assertTenantScopedKey("tenant-A","tenants/tenant-A/cases/x/documents/doc/extra"),/invalid_object_key/);
});
test("bindings fail closed until explicitly configured",()=>{
  assert.deepEqual(validateBindings({}),{ready:false,missing:["TAX_GENIE_DB","TAX_GENIE_DOCUMENTS"]});
  assert.deepEqual(validateBindings({TAX_GENIE_DB:{}}),{ready:false,missing:["TAX_GENIE_DOCUMENTS"]});
  assert.deepEqual(validateBindings({TAX_GENIE_DB:{},TAX_GENIE_DOCUMENTS:{}}),{ready:true,missing:[]});
});

test("rejects invalid case IDs and object IDs independently",()=>{
  for (const bad of ["../x","a/b","",".hidden","é"]) {
    assert.throws(()=>documentKey("tenant-A",bad,"doc-001"));
    assert.throws(()=>documentKey("tenant-A","case-001",bad));
  }
});
test("rejects tenant-prefix confusion and malformed object layouts",()=>{
  const valid=documentKey("tenant-A","case-001","doc-001");
  assert.throws(()=>assertTenantScopedKey("tenant",valid),/cross_tenant/);
  assert.throws(()=>assertTenantScopedKey("tenant-A","tenants/tenant-A/cases/case-001/other/doc-001"),/invalid_object_key/);
  assert.throws(()=>assertTenantScopedKey("tenant-A","tenants/tenant-A/cases/case-001/documents/../doc-001"),/invalid_object_key/);
});
