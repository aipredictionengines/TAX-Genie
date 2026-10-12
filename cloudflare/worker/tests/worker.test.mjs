import assert from "node:assert/strict";
import test from "node:test";
import worker from "../src/index.mjs";

test("health endpoint has explicit bootstrap status", async () => {
  const response = await worker.fetch(new Request("https://example.test/health"));
  assert.equal(response.status, 200);
  const json = await response.json();
  assert.deepEqual(json, {service:"tax-genie-api",status:"bootstrap",production_ready:false});
  assert.equal(response.headers.get("cache-control"), "no-store");
});

test("case routes fail closed without handling payloads", async () => {
  for (const method of ["GET","POST"]) {
    const response = await worker.fetch(new Request("https://example.test/v1/cases", {method}));
    assert.equal(response.status, 503);
    assert.equal((await response.json()).error,"service_unavailable");
  }
});

test("unknown endpoints fail closed", async () => {
  const response=await worker.fetch(new Request("https://example.test/anything"));
  assert.equal(response.status,503);
});
