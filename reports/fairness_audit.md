# Fairness Audit Report: Before vs After with Accuracy Trade-off

*Template report — populated after running fairness audit (src/fairness/audit.py, src/fairness/mitigation.py). Covers before/after fairness metrics and accuracy trade-off as requested.*

## Executive Summary

We audit fairness for the credit risk model with respect to protected groups (e.g., **age bands**, **gender/sex** depending on dataset). We report baseline disparities, apply mitigation (e.g., reweighing or post-processing threshold adjustment), and present **before/after metrics alongside accuracy trade-offs**.

Key principle: disparities are measured and documented transparently; mitigation involves trade-offs that are explicit (not hidden).

## Dataset & Groups

- **Dataset**: _tbd_ (German Credit / Give Me Some Credit / Home Credit)
- **Protected attributes**: _tbd_ (age_group, sex/gender). Note: never used as predictors.
- **Group definitions**: Age binned reasonably (e.g., <25, 25-40, 40-60, >60) to have sufficient sample sizes; document binning rationale.
- **Split**: Test set used for audit (held-out).

## Metrics

Definitions (see [docs/methodology.md](../docs/methodology.md)):

| Metric | What it measures | Fairness goal (lower difference = fairer) |
|---|---|---|
| **Demographic Parity Difference (DPD)** | Difference in positive prediction rates across groups | 0 |
| **Disparate Impact (DI)** | Ratio of positive rates (group_a / group_b) | ~1.0 (4/5ths rule heuristic ~0.8–1.25) |
| **Equalized Odds Difference (EOD)** | Max difference in TPR/FPR across groups (conditional on Y) | 0 |
| **Equal Opportunity Difference (EOpD)** | Difference in TPR (true positive rates) | 0 |
| **FPR Difference** | False positive rate gaps | 0 |
| **Accuracy Difference** | Accuracy gaps by group | Smaller preferred (contextual) |
| **Balanced Accuracy** | By-group balanced accuracy | Track alongside overall |

## Baseline (Before Mitigation)

### Overall Performance
| Metric | Value |
|---|---|
| **Accuracy** | _tbd_ |
| **Balanced Accuracy** | _tbd_ |
| **ROC-AUC** | _tbd_ |
| **F1** | _tbd_ |
| **Precision/Recall** | _tbd_ |

### Group-wise Rates (Positive Prediction Rate, TPR, FPR)

| Group | n | P(Ŷ=1) (Selection Rate) | TPR | FPR | Accuracy | Balanced Acc |
|---|---|---|---|---|---|---|
| Group A (_tbd_) | _tbd_ | _tbd_ | _tbd_ | _tbd_ | _tbd_ | _tbd_ |
| Group B (_tbd_) | _tbd_ | _tbd_ | _tbd_ | _tbd_ | _tbd_ | _tbd_ |

### Fairness Differences (Before)
| Metric | Difference (max across groups) | Notes |
|---|---|---|
| **DPD** | _tbd_ | Selection rate disparity |
| **DI (min/max ratio)** | _tbd_ | Disparate impact ratio |
| **EOD** | _tbd_ | Equalized odds (TPR/FPR) |
| **EOpD** | _tbd_ | Equal opportunity (TPR) |
| **FPR Diff** | _tbd_ | Error type disparity |
| **Accuracy Gap (max)** | _tbd_ | Performance disparity |

## Mitigation (After)

**Mitigation strategy applied**: _tbd_ (e.g., Fairlearn Reweighing / Post-processing for Equalized Odds / Threshold optimization). Rationale and constraints documented.

### Group-wise Rates (After Mitigation)
| Group | n | P(Ŷ=1) | TPR | FPR | Accuracy | Balanced Acc |
|---|---|---|---|---|---|---|
| Group A | _tbd_ | _tbd_ | _tbd_ | _tbd_ | _tbd_ | _tbd_ |
| Group B | _tbd_ | _tbd_ | _tbd_ | _tbd_ | _tbd_ | _tbd_ |

### Fairness Differences (After)
| Metric | Difference (max) | Δ vs Before | Notes |
|---|---|---|---|
| **DPD** | _tbd_ | _tbd_ | _tbd_ |
| **DI** | _tbd_ | _tbd_ | _tbd_ |
| **EOD** | _tbd_ | _tbd_ | _tbd_ |
| **EOpD** | _tbd_ | _tbd_ | _tbd_ |
| **FPR Diff** | _tbd_ | _tbd_ | _tbd_ |
| **Accuracy Gap** | _tbd_ | _tbd_ | _tbd_ |

## Accuracy Trade-off (Before vs After)

| Metric | Before | After | Δ (After - Before) | Trade-off Assessment |
|---|---|---|---|---|
| **Overall Accuracy** | _tbd_ | _tbd_ | _tbd_ | Change in overall accuracy. |
| **Balanced Accuracy** | _tbd_ | _tbd_ | _tbd_ | Better for imbalanced classes. |
| **ROC-AUC** | _tbd_ | _tbd_ | _tbd_ | Ranking quality. |
| **F1** | _tbd_ | _tbd_ | _tbd_ | Precision/recall balance. |

**Trade-off plot**: eports/figures/fairness_tradeoff_accuracy_vs_fairness.png

## Interpretation

- **What improved**: _tbd_
- **Cost**: _tbd_
- **Residual disparities**: _tbd_
- **Practical choice**: _tbd_

## Assumptions & Limitations

- **Multiple metrics conflict**: Report several.
- **Group size**: Uncertainty not fully quantified.
- **Binning**: Documented.
- **Causal vs. observational**: Disparities indicate potential concerns.
- **Mitigation scope**: Harm-reduction, not complete fix.
- **Dataset limitations**: Historical structural bias.

## Visualizations

Saved figures in eports/figures/.

## Reproducibility

- Scripts: src/fairness/audit.py, src/fairness/mitigation.py
- Config: configs/fairness.yaml
- Outputs: tables + figures in eports/

