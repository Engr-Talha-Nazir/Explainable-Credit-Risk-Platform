# Data Guide

This guide covers recommended datasets, sources, preprocessing notes, ethical considerations, and how data is organized in this repo.

## Data Directory Structure

`
data/
├── raw/        # Original datasets (downloaded locally; typically NOT tracked in git for large files)
├── processed/  # Cleaned, encoded, split datasets ready for modeling
└── external/   # Supplementary artifacts (mappings, metadata)
`

> Note: aw/, processed/, external/ contents are git-ignored except for .gitkeep files to preserve structure.

## Recommended Public Credit Datasets

### 1) German Credit (UCI) – Recommended for Reproducibility
- **Source**: [UCI Machine Learning Repository - German Credit Data](https://archive.ics.uci.edu/ml/datasets/statlog+(german+credit+data))
- **Format**: .data (tabular), 1000 samples, 20 features + target.
- **Target**: Credit risk (good/bad). Common mapping: 1=good, 0=bad (or vice versa; document mapping).
- **Protected/sensitive**: Includes Age and Sex/personal status features — useful for fairness auditing (never used as predictors).
- **Pros**: Small, well-documented, widely used in XAI/fairness literature; easy to include/run without large downloads.
- **Cons**: Legacy dataset (1970s), limited size/modern representation.

**Suggested default**: Use German Credit for instant end-to-end runs and for the comparison/disagreement + fairness audit in this portfolio project.

### 2) Give Me Some Credit (Kaggle)
- **Source**: [Kaggle - Give Me Some Credit](https://www.kaggle.com/competitions/GiveMeSomeCredit)
- **Size**: ~150k samples, 10 features.
- **Target**: SeriousDlqin2yrs (1 = serious delinquency in 2+ years).
- **Pros**: Large, modern structure, clean columns.
- **Cons**: Kaggle download requires account; no explicit gender field in core features (limits some fairness axes). Age present.

### 3) Home Credit Default Risk (Kaggle)
- **Source**: [Kaggle - Home Credit Default Risk](https://www.kaggle.com/competitions/home-credit-default-risk)
- **Size**: Large (train ~300k), many relational tables.
- **Target**: Default indicator.
- **Pros**: Real-world, rich features.
- **Cons**: Larger setup; multiple files; some features need domain care.

### 4) LendingClub (Historical Loan Data)
- **Source**: [LendingClub Data](https://www.lendingclub.com/info/download-data.action) (historical; terms vary by year)
- **Size**: Large (millions historically).
- **Notes**: Review data use/terms, licensing, and PII. Filter to relevant periods; be careful with post-issuance info/leakage.
- **Cons**: Can include information not available at application time (leakage risk). Requires careful preprocessing.

## Download & Setup

### Option A: German Credit (automatic-friendly, no auth hurdles)
Provide loader in src/data/load_german.py (or general loader) with clear mapping. Can also download via UCI URL if desired; include fallback instructions.

### Option B: Kaggle datasets
Use kaggle CLI (pip install kaggle). Place API key in ~/.kaggle/kaggle.json. Download to data/raw/ via script or documented commands.

See preprocessing configs in configs/ for dataset selection/paths.

## Preprocessing Guidelines

1. **Target definition**: Document exact mapping and class balance.
2. **Missing data**: Impute with justified strategy (mean/median/mode, grouped) or flag; avoid target-based imputation leakage.
3. **Feature selection/engineering**: Keep interpretable features where possible for cleaner explanations.
4. **Categorical encoding**: Use consistent encoding (one-hot for nominal; ordinal maps for ordered). Preserve mapping for interpretability.
5. **Scaling**: Not required for XGBoost; if using other models or LIME preprocessing assumptions, document.
6. **Train/test split**: Stratified, time-aware if temporal (LendingClub) to avoid lookahead; fixed andom_state.
7. **Leakage prevention**: Exclude features derived after decision point, IDs, exact duplicates revealing target, or fields that would not exist at application time.
8. **Protected attributes**: Extract to separate columns (ge_group, sex/gender) for fairness; exclude from predictor feature matrix.

## Data Quality & Validation

- **Schema checks**: Column names, dtypes, ranges.
- **Class imbalance**: Report (may affect metrics; consider stratification, PR-AUC).
- **Distributions**: Check for outliers, unexpected values.
- **Correlation audit**: Quick scan for suspicious high correlations (potential proxies/leaks).

## Ethical, Legal & Licensing Considerations

- **Public only**: Use publicly available datasets with permissible research use. Check Kaggle/UCI terms of use per dataset.
- **No PII**: Public datasets are typically de-identified; still verify no direct identifiers remain.
- **Bias awareness**: Historical credit data encodes systemic biases. We measure and report disparities; do not treat data as neutral.
- **Attribution**: Cite dataset sources in README/docs and any derivative reports.
- **Responsible use**: This repo is educational. Real lending requires regulatory compliance, model risk management, human oversight, and local legal review.

## Reproducibility Notes

- Raw data files are not committed by default (large). Provide download scripts/instructions and small sample if useful.
- Processed data can be regenerated from configs + raw; alternatively include small processed sample for CI/tests if feasible.
- Document dataset version/date of download in data/README.md (this file).
