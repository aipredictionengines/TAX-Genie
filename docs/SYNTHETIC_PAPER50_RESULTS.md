# Synthetic PAPER 50 — expected reference and reporting rules

The frozen 50-case synthetic fixture exercises 5 repeated formatting scenarios (10 examples each):
- Exact supported labels
- VAT label absent (legitimate missing)
- Identical VAT label repeated
- Contradictory VAT amounts (withhold candidate)
- Unsupported **Tax VAT Amount** label (false negative against true VAT)

This is a **synthetic parser regression evaluation**, not validation of real invoice extraction, OCR, or any tax recovery conclusion. The synthetic labels and values come from a deterministic specification, not from model output.

Run: `python -m unittest discover -s tests -v`, then `python -m scripts.run_synthetic_paper50`.

The benchmark's VAT expected TP=30, FN=10, FP=0, TN=10, precision=1.0 and recall=0.75 (threshold 0.90 **NOT met**). This is intentionally a failing quality metric; do not misrepresent CI success as meeting the product quality gate.

The fixture is generated at runtime and has no private data. Real PAPER 50 is **NOT RUN** and must be a distinct, consented, independently labeled cohort outside this public repo.
