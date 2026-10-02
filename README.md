# Explainable-Credit-Risk-Platform
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://pre-commit.com/)

A production-grade, explainable and fair credit risk prediction system. It provides transparent loan approval decisions with plain-language explanations, counterfactual "what-if" recommendations, and a rigorous fairness audit — built for high-stakes decision-making with regulatory considerations (GDPR right to explanation, fair lending).

## Key Features

- **End-to-end ML pipeline**: Data ingestion, preprocessing, XGBoost training with reproducible configuration.
- **Multi-method explainability**: SHAP (global + local), LIME (local), and DiCE (actionable counterfactuals) to compare explanations and identify disagreements.
- **Actionable recourse**: Counterfactual suggestions showing what minimal changes could flip an adverse decision.
- **Bias audit & mitigation**: Fairlearn-based evaluation across protected groups (age, gender where available) with before/after fairness metrics and accuracy trade-offs.
- **Comparison & disagreement analysis**: Quantifies where explanation methods diverge to surface reliability concerns.
- **Leakage detection**: Systematic checks to catch leaked/proxy features and document findings.
- **API-first**: FastAPI service for real-time predictions and explanations.
- **Interactive dashboard**: Streamlit app for exploring decisions, explanations, counterfactuals, and fairness reports.
- **Reproducible & professional**: Config-driven, tested, containerized (Docker), linted, type-checked, with CI-ready structure and comprehensive documentation.

## Project Scope (Domain Choice Rationale)

This project uses **credit (loan approval)** because:

- **Real recourse need**: Rejected applicants deserve clear reasons and actionable steps.
- **Strong XAI fit**: Credit is the canonical domain for explainability/counterfactuals.
- **Feasible fairness**: Public datasets include plausible protected attributes for audit.
- **Regulatory relevance**: Aligns with GDPR's right to explanation and fair lending principles.
- **Practical & ethical**: Lower direct patient risk than healthcare while still high-stakes; avoids hiring data scarcity/synthetic issues.

See [Domain Rationale](docs/domain_rationale.md) for detailed justification.

## Quick Start

### Prerequisites

- Python 3.10+
- Git
- (Optional) Docker

### Installation

`ash
# Clone repo
git clone https://github.com/Engr-Talha-Nazir/Explainable-Credit-Risk-Platform.git
cd Explainable-Credit-Risk-Platform

# Create virtual environment
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/macOS
# source .venv/bin/activate

# Install dependencies
pip install -e .
pip install -r requirements-dev.txt
`

### Dataset

Recommended public datasets (credit):

- **German Credit (UCI)**: Small, well-known, easy to include for reproducibility. Includes age/sex features useful for fairness auditing.
- **Give Me Some Credit (Kaggle)**: Larger, practical for default risk.
- **Home Credit Default Risk (Kaggle)**: Comprehensive real-world structure.
- **LendingClub (historical)**: Large-scale; use carefully per terms.

**Default approach:** Include German Credit preprocessing for instant reproducibility (no large downloads required). Provide download instructions/scripts for larger datasets in [data/README.md](data/README.md).

### Train Model

`ash
# Train with default config (German Credit)
python -m src.train --config configs/train_german.yaml
`

### Run API

`ash
# Start FastAPI server
uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload
`

API docs: [http://localhost:8000/docs](http://localhost:8000/docs)

### Run Streamlit Dashboard

`ash
streamlit run src/dashboard/app.py
`

Dashboard: [http://localhost:8501](http://localhost:8501)

### Run Tests

`ash
pytest tests/ -v
`

### Lint & Format

`ash
black .
isort .
ruff check .
mypy src
`

### Docker

`ash
docker compose up --build
`

## Repo Structure

`
Explainable-Credit-Risk-Platform/
├── configs/              # YAML configs for data, train, explain, fairness
├── data/
│   ├── raw/              # Raw data (downloaded; not tracked if large)
│   ├── processed/        # Cleaned/engineered features
│   └── external/         # External artifacts
├── docs/                 # Detailed docs (methods, report, rationale)
├── notebooks/            # Exploratory analysis & demos
├── reports/              # Generated reports, figures, comparison results
├── src/
│   ├── data/             # Data loaders
│   ├── preprocessing/    # Cleaning, encoding, splitting
│   ├── models/           # Model training/evaluation
│   ├── explain/          # SHAP, LIME, DiCE wrappers
│   ├── fairness/         # Fairlearn audit/mitigation
│   ├── utils/            # Helpers, logging, seeding
│   ├── api/              # FastAPI app
│   └── dashboard/        # Streamlit app
├── tests/                # Unit/integration tests
├── .github/workflows/    # CI (lint/test)
├── Dockerfile            # Container image
├── docker-compose.yml    # API + dashboard
├── .gitignore            # Git ignore rules
├── .pre-commit-config.yaml
├── LICENSE               # MIT License
├── README.md             # This file
├── pyproject.toml        # Build, deps, tooling config
├── requirements.txt      # Runtime deps
└── requirements-dev.txt  # Dev/test deps
`

## Core Capabilities

### 1) Explainability Comparison (SHAP vs LIME vs DiCE)

We compute and compare feature attributions/counterfactuals across methods to identify **where they disagree**:

- **Agreement metrics**: Rank correlation (Spearman/Kendall), top-k feature overlap, sign agreement.
- **Local disagreement analysis**: Per-instance cases where methods rank features differently or suggest conflicting drivers.
- **Stability checks**: Sensitivity to perturbations/sampling where applicable.
- **Visualization**: Side-by-side force plots, bar charts, and disagreement heatmaps saved in eports/figures/ and summarized in [reports/explanation_comparison.md](reports/explanation_comparison.md).

Key script: src/explain/comparison.py

### 2) Fairness Audit with Accuracy Trade-off

Using [Fairlearn](https://fairlearn.org/), we evaluate:

- **Sensitive attributes**: Age bands, gender (dataset-dependent; handled carefully, never as predictors).
- **Metrics (before/after)**: Demographic parity difference, equalized odds difference, disparate impact, TPR/FPR gaps, accuracy, balanced accuracy.
- **Trade-offs**: Plot fairness metric vs. accuracy under baseline and post-mitigation (e.g., threshold optimization, post-processing, or reweighing where appropriate).
- **Reporting**: Tables + charts in [reports/fairness_audit.md](reports/fairness_audit.md).

Key modules: src/fairness/audit.py, src/fairness/mitigation.py

### 3) Leakage/Proxy Feature Detection & Issue Report

We explicitly look for problematic features:

- **Correlation leaks**: Target leakage via high train-test leakage signals, time-based leaks, or proxy variables.
- **Proxy detection**: Correlation to protected attributes + predictive power (red flags).
- **Stability/importance**: Unrealistically high SHAP importance, single-feature dominance.
- **Documentation**: Findings, evidence, impact, and remediation captured in [reports/leakage_issue_report.md](reports/leakage_issue_report.md) (as requested: "a short report on one issue the explanations helped you catch, such as a leaked or proxy feature").

Key checks: src/preprocessing/leakage.py, notebooks, and explanation-driven inspection.

## Documentation

- [Domain Rationale](docs/domain_rationale.md) – why credit domain chosen
- [Methodology](docs/methodology.md) – XAI methods, fairness, evaluation
- [Data Guide](data/README.md) – datasets, sources, preprocessing, licenses/ethics
- [API Reference](docs/api.md) – endpoints, request/response schemas
- [Explanation Comparison Report](reports/explanation_comparison.md) – SHAP/LIME/DiCE agreement/disagreement
- [Fairness Audit Report](reports/fairness_audit.md) – before/after metrics + trade-offs
- [Leakage Issue Report](reports/leakage_issue_report.md) – issue caught via explanations

## Ethical, Legal & Responsible AI

- **No misuse**: This is an educational/research tool. Not intended as unreviewed production lending automation without compliance review.
- **Avoid protected attributes as predictors**: We audit them but do not train to exploit them; we report disparities responsibly.
- **Right to explanation**: Local explanations + counterfactual recourse align with transparency goals.
- **Bias awareness**: Disparities are measured and documented; mitigation trade-offs are explicit (not hidden).
- **Data provenance & licensing**: Public datasets only; document sources/terms. Remove PII; use features as-is responsibly.
- **Limitations**: Explanations are approximations; disagreement signals uncertainty. Models can reflect historical bias in data.

## Contributing

Contributions welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines (issues, PRs, code style, testing).

## License

MIT License – see [LICENSE](LICENSE).

## Acknowledgments

- [SHAP](https://shap.readthedocs.io/)
- [LIME](https://lime-ml.readthedocs.io/)
- [DiCE](https://interpret.ml/DiCE/)
- [Fairlearn](https://fairlearn.org/)
- [XGBoost](https://xgboost.readthedocs.io/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Streamlit](https://streamlit.io/)
- Public datasets: UCI German Credit, Kaggle Give Me Some Credit/Home Credit, LendingClub (references in docs).
