# BUILD-007 — Two synthetic cohorts, unchanged ground truth

**Original frozen cohort** from BUILD-006 stays unchanged. Parser updated solely to accept explicit "Tax VAT Amount" labels. Expected VAT results: 30 TP, 0 FP, 0 FN, 20 TN; precision 1.0 and recall 1.0.

**Independent synthetic holdout** uses 50 new examples with different wording and several intentionally unsupported formats. Expected VAT results: 20 TP, 0 FP, 20 FN, 10 TN; precision 1.0 and recall 0.5. This **fails** the 0.90 recall target.

Both results are code-defined regression expectations, not verified standalone GitHub benchmark artifacts until run. Holdout cases are synthetic, and may not represent real-world layouts. The improvement on the first cohort is not evidence of generalization.

Next step is enhanced label coverage validated on a new holdout, and a hardened security/privacy environment before consented real invoices.
