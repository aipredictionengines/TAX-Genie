// BUILD-018: cloud-only bootstrap. No case processing, document ingestion or data access.
export default {
  async fetch(request) {
    const url = new URL(request.url);
    if (url.pathname === "/health" && request.method === "GET") {
      return new Response(JSON.stringify({service:"tax-genie-api", status:"bootstrap", production_ready:false}), {
        status: 200,
        headers: {"content-type":"application/json; charset=utf-8","cache-control":"no-store","x-content-type-options":"nosniff"}
      });
    }
    return new Response(JSON.stringify({error:"service_unavailable",message:"Tax Genie API has not been enabled"}), {
      status: 503,
      headers: {"content-type":"application/json; charset=utf-8","cache-control":"no-store","x-content-type-options":"nosniff"}
    });
  }
};
