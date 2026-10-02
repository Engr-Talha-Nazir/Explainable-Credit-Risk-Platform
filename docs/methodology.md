# Methodology

This document outlines the methods used for prediction, explainability (SHAP, LIME, DiCE), fairness auditing (Fairlearn), leakage detection, and evaluation.

## 1) Problem Formulation

We frame credit risk as a **binary classification** task: predict loan default/approval risk (approve vs. reject) based on applicant features. The exact target definition depends on dataset:

- **German Credit (UCI)**: Target indicates "good" vs. "bad" credit risk.
- **Give Me Some Credit (Kaggle)**: SeriousDlqin2yrs (serious delinquency in 2 years).
- **Home Credit**: Default indicator on repayment.
- **LendingClub**: Loan status (charged off/default vs. fully paid).

We prioritize **explainability + fairness** alongside predictive performance (ROC-AUC, F1, precision/recall, accuracy, balanced accuracy).

## 2) Data Preprocessing

- **Cleaning**: Handle missing values, outliers, data types.
- **Encoding**: One-hot/ordinal for categorical; numeric scaling as appropriate (tree-based models like XGBoost do not require strict normalization).
- **Feature engineering**: Domain-relevant aggregates; avoid leakage.
- **Train/val/test split**: Stratified split (e.g., 70/15/15) with fixed random seed.
- **Data leakage checks**: See Section 5.
- **Reproducibility**: All steps config-driven (configs/*.yaml), seeded (src/utils/seed.py).

Sensitive/protected attributes (age bands, gender/sex where present) are **held out from model features used for prediction** in training inputs, but preserved in evaluation data for fairness auditing. They are never treated as predictors.

## 3) Modeling

- **Algorithm**: XGBoost (gradient boosted trees) — strong baseline for tabular credit data, efficient, handles nonlinearities and interactions; compatible with SHAP TreeExplainer.
- **Training**: Configurable hyperparameters (learning rate, depth, estimators, subsample, regularization). Can extend to LightGBM/CatBoost if desired.
- **Validation**: Early stopping on validation set, cross-validation optional.
- **Calibration** (optional): Platt/Isotonic if probability calibration matters for thresholding.
- **Metrics**: ROC-AUC, PR-AUC, accuracy, balanced accuracy, F1, precision, recall, confusion matrices.

## 4) Explainability Methods

We use three complementary methods and analyze **agreement/disagreement**.

### SHAP (SHapley Additive exPlanations)

- **Type**: Game-theoretic, additive feature attributions (local + global).
- **Explainer**: TreeExplainer for XGBoost (fast, exact for trees).
- **Outputs**: Force/waterfall plots, summary plots (beeswarm/bar), dependence plots, SHAP values per instance/feature.
- **Strengths**: Theoretically grounded (Shapley values), consistent, supports global interpretability.
- **Limitations**: Can be expensive in some cases; assumptions about feature independence in certain settings; tree-path dependence nuances.

### LIME (Local Interpretable Model-Agnostic Explanations)

- **Type**: Local surrogate (sparse linear) around instance via perturbations.
- **Explainer**: lime.lime_tabular.LimeTabularExplainer.
- **Outputs**: Local feature weights (positive/negative contribution), explanation objects per instance.
- **Strengths**: Model-agnostic, intuitive, simple local fidelity.
- **Limitations**: Instability (random perturbations), choice of kernel/num_samples affects results, lacks global consistency guarantees.

### DiCE (Diverse Counterfactual Explanations)

- **Type**: Actionable counterfactuals ("what would change the outcome?").
- **Explainer**: dice_ml.Dice with RandomSampling/genetic/optimization methods; supports feasibility constraints.
- **Outputs**: Minimal, diverse sets of feature changes that flip prediction to desired class (e.g., reject → approve).
- **Strengths**: Actionable recourse, supports immutable/feasible ranges, diversity avoids single-path bias.
- **Limitations**: Depends on data distribution/feasibility constraints; can generate unrealistic examples if unconstrained; optimization cost.

### Explanation Comparison & Disagreement

We quantify where methods disagree (src/explain/comparison.py):

- **Feature ranking agreement**: Spearman/Kendall rank correlation of top features (local), Jaccard/top-k overlap.
- **Sign agreement**: Fraction of features with same direction of contribution (where comparable).
- **Magnitude correlation**: Pearson/Spearman on attribution vectors (normalized).
- **Local disagreement cases**: Identify instances with low rank overlap or conflicting top drivers.
- **Stability**: Optional resampling for LIME/DiCE sensitivity.
- **Reporting**: Tables, bar/heatmap visualizations, example cases with side-by-side explanations in eports/explanation_comparison.md.

Rationale: Disagreement is informative (uncertainty, approximation differences) — we report it explicitly rather than forcing consensus.

## 5) Leakage & Proxy Feature Detection

Explanation-driven inspection helps catch leaks/proxies (src/preprocessing/leakage.py):

- **Target leakage**: Unintended features that reveal target (post-outcome, future info, derived directly from target). Check high importance + suspicious timing/derivation.
- **Train-test leakage**: Look for features with unrealistically perfect separation or computed using full dataset.
- **Proxy detection**: Correlation between features and protected attributes (Phi/Cramér’s V, point-biserial, Pearson) combined with high predictive power. Flag potential proxies even if not explicit.
- **Singleton dominance**: Single feature with disproportionate SHAP importance across many instances.
- **Distributional artifacts**: ID-like, leaky encodings, or aggregation bugs.
- **Documentation**: Evidence (correlations, SHAP, examples), impact assessment, remediation (drop/transform/document) in eports/leakage_issue_report.md.

## 6) Fairness Audit

Using Fairlearn, we evaluate group fairness with protected attributes (dataset-dependent: age bands, gender/sex). Attributes are **not predictors**.

### Fairness Metrics

- **Demographic Parity Difference (DPD)**: |P(Ŷ=1 | A=a) - P(Ŷ=1 | A=b)| — equal selection rates across groups.
- **Demographic Parity Ratio / Disparate Impact (DI)**: P(Ŷ=1|A=a)/P(Ŷ=1|A=b) (approximate 4/5ths rule context).
- **Equalized Odds Difference (EOD)**: Max over y of |P(Ŷ=1|A=a,Y=y) - P(Ŷ=1|A=b,Y=y)| — equal TPR/FPR.
- **Equal Opportunity Difference (EOpD)**: |TPR(A=a)-TPR(A=b)| (focus on positive class).
- **Error rate gaps**: FPR/accuracy gaps, balanced accuracy by group.
- **Performance by group**: ROC-AUC, F1, precision/recall disaggregated.

### Mitigation Strategies

We explore practical mitigations and report **before/after + accuracy trade-off** (src/fairness/mitigation.py):

- **Pre-processing**: Reweighing (sample weights to reduce disparity).
- **In-processing**: Fairness-constrained training (where supported) or regularization — context-dependent.
- **Post-processing**: Threshold optimization (e.g., equalized odds post-processing, or group-specific thresholds with constraints) to adjust decision thresholds per group while tracking accuracy.

Trade-offs are visualized (fairness metric vs. accuracy) and tabulated. We document whether disparities are reduced, at what accuracy cost, and any residual gaps.

### Reporting

Results saved to eports/fairness_audit.md with:
- Baseline metrics table (overall + by group)
- Before/after comparison table
- Trade-off plots (eports/figures/fairness_tradeoff_*.png)
- Disparity visualizations (bar charts, confusion matrices by group)
- Discussion of assumptions/limitations.

## 7) Evaluation & Validation

- **Predictive**: Hold-out test set; report uncertainty-aware summaries where appropriate.
- **Explainability**: Sanity checks (remove important feature → performance drops), local fidelity intuition, disagreement analysis.
- **Fairness**: Multiple metrics (no single metric captures all); report trade-offs transparently.
- **Robustness**: Optional small perturbation tests on key features.
- **Reproducibility**: Fixed seeds, config files, versioned deps (equirements*.txt, pyproject.toml).

## 8) Limitations

- **Explanations approximate**: SHAP/LIME/DiCE are approximations of model behavior; disagreement indicates approximation/definition differences.
- **Data representativeness**: Public credit datasets may not reflect current lending distributions or practices.
- **Causal vs. correlational**: Counterfactuals suggest plausible changes but are not guaranteed causal interventions.
- **Group definitions**: Age bins/gender categories are simplified; real audits require careful subgroup construction and legal review.
- **No automatic guarantee**: Reducing one disparity can affect others; accuracy-fairness trade-offs are explicit and case-dependent.
