"""Run from project root: python -m scripts.run_synthetic_paper50"""
import json
from tax_genie.synthetic50 import run

def main():
    result=run()
    print(json.dumps(result,indent=2,sort_keys=True))
    return 0
if __name__=="__main__":
    raise SystemExit(main())
