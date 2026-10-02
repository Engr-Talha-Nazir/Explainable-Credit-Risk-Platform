# Domain Rationale: Why Credit (Loan Approval)?

This project focuses on **credit risk (loan approval)** as the high-stakes domain for explainable and fair AI. The rationale below justifies this choice against alternatives (hiring, healthcare).

## Comparison of Domains

| Criterion | Credit (Loan Approval) | Hiring | Healthcare Risk |
|---|---|---|---|
| **Real need for recourse** | High. Rejected applicants need actionable reasons to improve eligibility ("what would change the outcome"). | Medium. Candidates benefit from feedback, but recourse is less structured and data is limited. | High patient impact, but "recourse" differs (clinical intervention vs. applicant actionability). |
| **Explainability fit** | Excellent. Counterfactuals map directly to financial levers (income, debt, credit history, utilization). Canonical XAI showcase. | Good for bias, weaker for counterfactual actionability with synthetic/public data. | Strong need, but requires clinician-facing explanations and uncertainty. |
| **Data availability** | Strong public datasets (German Credit UCI, Give Me Some Credit Kaggle, Home Credit, LendingClub). Includes plausible features/age/gender in some sets. | Scarce, often proprietary/synthetic; difficult for reproducible real audits. | Restricted (PHI/IRB). Hard to include/share full reproducible data without approvals. |
| **Fairness audit feasibility** | Feasible. Protected attributes (age, sex/gender) exist in standard sets; measurable disparities with fair lending lens. | Feasible conceptually, but dataset constraints limit realism. | Important, but subgroup definitions and clinical confounders complicate naive fairness metrics. |
| **Regulatory relevance** | Strong: GDPR (right to explanation), ECOA/Fair Lending (US), responsible lending norms. Ties directly to compliance concerns. | Relevant (EEOC, AI hiring regulations), less directly tied to "right to explanation with recourse" in public datasets. | Strong (FDA/HTA, medical device AI, explainability for clinicians/patients), but complex. |
| **Ethical risk profile** | Moderate-high stakes but lower direct physical harm. Portfolio-level mistakes are measurable; educational scope is appropriate. | High reputational/fairness stakes; data realism issues. | Very high (patient safety). Credible work needs uncertainty, calibration, limitations, clinician validation beyond scope of a portfolio demo. |
| **Reproducibility** | High. Can run end-to-end with small public data (German Credit) without special access. | Lower due to data realism. | Limited without data access agreements. |

## Chosen Approach

We adopt **credit (loan approval)** because it best balances:

1. **Actionable explainability**: DiCE counterfactuals provide realistic, minimal changes applicants could act on.
2. **Meaningful fairness audit**: We can report before/after disparities (demographic parity, equalized odds, disparate impact) with explicit accuracy trade-offs.
3. **Regulatory alignment**: Demonstrates transparency consistent with right-to-explanation and fair lending principles.
4. **Portfolio-readiness + safety**: High-stakes enough to be professional, but contained for an educational/research project.

## Limitations & Guardrails

- **Not production lending**: This is a research/demo system. Do not deploy for real credit decisions without compliance, validation, and human-in-the-loop review.
- **Historical bias**: Training data reflects past lending patterns; disparities found are documented, not excused.
- **Protected attributes**: Audited but never used as predictors. We emphasize trade-offs and uncertainty.
- **Dataset caveats**: Public datasets are cleaned/legacy (German Credit is older). Results illustrate methods, not current market performance.
