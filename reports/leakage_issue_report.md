# Leakage/Proxy Feature Issue Report

*Template to document an issue caught via explanations.*

## Issue Title
_tbd_

## Summary
Document one concrete issue (target leakage / proxy / train-test leakage) found via SHAP/LIME inspection.

## How Explanations Helped
- Unusually high SHAP importance / singleton dominance
- Instance-level waterfalls pointing to same feature
- Cross-method (SHAP vs LIME) triggered deeper check
- Led to correlation/provenance audit

## Evidence
- Top features & mean |SHAP|: _tbd_
- Feature definition/provenance/timing: _tbd_
- Statistical checks (correlation with target, with protected attrs, univariate): _tbd_
- Example instances: _tbd_

## Issue Classification
- Type: target_leakage | proxy_feature | train_test_leakage | encoding_leak
- Severity: Low/Medium/High
- Status: Suspected/Confirmed

## Impact
- Model validity, fairness, explainability trust, ethical/business: _tbd_

## Remediation
- Action (drop/transform/recompute/document): _tbd_
- Validation plan: retrain, compare metrics, SHAP redistribution, re-audit

## Outcome
- Performance/fairness changes, conclusion: _tbd_

## Lessons Learned
- Explanation-driven QA effective; cross-method useful; document explicitly.

## References
- docs/methodology.md (leakage section)
- reports/figures/leakage_*.png

