"""Local report with deterministic synthetic figures only."""
import json
from tax_genie.holdout_v2 import run_holdout_v2
from tax_genie.release_gates import release_readiness

if __name__=="__main__":
    print(json.dumps({"benchmark":run_holdout_v2(),"release":release_readiness()},indent=2,sort_keys=True))
