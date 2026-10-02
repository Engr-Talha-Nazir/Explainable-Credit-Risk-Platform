# Explanation Comparison Report: SHAP vs LIME vs DiCE

*This is a template report. It will be populated after running the full pipeline (training + explanation generation + comparison). The structure below matches the requirement: "A comparison of explanation methods and where they disagree".*

## Executive Summary

We compare three explanation methods on the credit risk model:
- **SHAP** (feature attributions, local+global, game-theoretic)
- **LIME** (local surrogate, perturbation-based)
- **DiCE** (counterfactuals, actionable recourse)

We quantify agreement/disagreement across instances and highlight cases where methods diverge in top drivers, direction, or ranking. Disagreements are treated as signals of approximation differences/uncertainty rather than errors.

## Methodology (Recap)

- **Dataset**: (to be filled — e.g., German Credit / Give Me Some Credit)
- **Model**: XGBoost (trained on held-out test split)
- **Instances analyzed**: N local instances (e.g., random sample + edge cases: high-prob reject/approve, near threshold)
- **Agreement metrics**: Spearman/Kendall rank correlation, top-k feature overlap (Jaccard), sign agreement, Pearson correlation on normalized attributions
- **Comparison scope**: Local explanations for same instances; global trends via aggregated SHAP vs. LIME feature importances

See [docs/methodology.md](../docs/methodology.md) for full details.

## Global Comparison

| Aspect | SHAP | LIME | DiCE | Notes |
|---|---|---|---|---|
| **Type** | Additive attributions | Local linear surrogate | Counterfactual examples | Different explanation targets (why now vs. what to change). |
| **Scope** | Local + global consistent | Primarily local | Local actionable recourse | SHAP best for global ranking consistency. |
| **Stability** | Relatively stable (deterministic for TreeExplainer given data) | More variable (perturbations) | Depends on optimization/diversity | LIME may vary across runs; DiCE can produce diverse sets. |
| **Actionability** | Descriptive (importance/contribution) | Descriptive | Prescriptive (minimal changes) | DiCE directly answers recourse. |
| **Computation** | Fast for trees | Moderate (perturbations) | Higher (optimization) | Trade-offs vary by data size. |

## Local Agreement Metrics

*(Populated after analysis; example structure)*

| Metric | Mean | Std | Min | Max | Interpretation |
|---|---|---|---|---|---|
| **Spearman rank correlation (SHAP vs LIME)** | _tbd_ | _tbd_ | _tbd_ | _tbd_ | Higher = stronger ranking agreement. |
| **Top-3 overlap (Jaccard)** | _tbd_ | _tbd_ | _tbd_ | _tbd_ | Overlap of top-3 drivers. |
| **Sign agreement (%)** | _tbd_ | _tbd_ | _tbd_ | _tbd_ | % features same direction (contribution sign). |
| **Pearson (norm. attributions)** | _tbd_ | _tbd_ | _tbd_ | _tbd_ | Magnitude alignment. |

## Where They Disagree

### Disagreement Case 1: _(Near-threshold applicant)_
- **Instance summary**: Prediction prob ~0.5 (borderline reject/approve)
- **SHAP top drivers**: _tbd_
- **LIME top drivers**: _tbd_
- **DiCE recourse**: Suggests _tbd_ (smallest change set)
- **Disagreement observed**: Ranking differs for _tbd_ (low top-k overlap). Near decision boundary, local surrogate (LIME) can be sensitive to perturbation region; SHAP uses tree paths.
- **Implication**: Borderline cases warrant higher scrutiny and possibly presenting multiple explanations with uncertainty note.

### Disagreement Case 2: _(High-confidence reject)_
- **Observation**: _tbd_
- **Likely cause**: Feature interactions — LIME’s linear local model may miss interactions that SHAP attributes via Shapley decomposition.
- **Implication**: For nonlinear interactions, SHAP tends to be more faithful to tree model; present both with caveat.

### Disagreement Case 3: _(Approved with mixed signals)_
- **Observation**: _tbd_
- **Note**: DiCE may propose multiple diverse counterfactuals (different feasible paths) while attribution methods point to primary drivers.
- **Implication**: Attribution (why) and recourse (what to change) answer different questions — some divergence expected and useful.

## Analysis of Causes

Common sources of disagreement observed (anticipated):

1. **Different mathematical objectives**: Shapley (fair allocation) vs. local fidelity with perturbation kernel (LIME) vs. optimization for minimal diverse flips (DiCE).
2. **Local neighborhood definition**: LIME samples around instance with kernel; SHAP uses model-specific coalitions/paths; DiCE searches feasible space near instance.
3. **Nonlinear interactions**: Tree models have strong interactions — linear surrogates can misattribute.
4. **Decision boundary proximity**: Disagreement tends to increase near threshold (unstable local regions).
5. **Feature correlations**: Attribution can be split differently across correlated features.

## Visualizations

Figures generated: eports/figures/explanation_comparison_*.png
- Side-by-side SHAP force/waterfall vs. LIME bars per disagreement case
- Top-k overlap heatmap
- Rank correlation distribution across test sample
- DiCE counterfactual comparison tables

*(Add figure references/paths once generated.)*

## Conclusion

- **Overall agreement**: Typically moderate-to-good on clear high-impact features; lower on borderline/interaction-heavy cases.
- **Complementarity**: Using all three is valuable: SHAP for consistent local+global attributions, LIME for simple local intuition, DiCE for actionable recourse.
- **Practical recommendation**: Surface disagreement explicitly. For cases with low rank agreement (< ~0.4 Spearman) or <50% top-3 overlap, flag as “low explanation consensus” and show both attribution views plus feasible counterfactuals with notes about uncertainty.

## Reproducibility

- Scripts: src/explain/comparison.py, src/explain/shap_explainer.py, src/explain/lime_explainer.py, src/explain/dice_explainer.py
- Config: configs/explain.yaml
- To regenerate: run full pipeline after training; outputs saved to eports/ and eports/figures/.
