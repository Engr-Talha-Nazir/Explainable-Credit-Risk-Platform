# Contributing to Explainable-Credit-Risk-Platform

Thanks for your interest in contributing! This project aims to be a professional, reproducible reference for explainable and fair ML in credit risk.

## Getting Started

1. Fork the repo and clone your fork:
   `ash
   git clone https://github.com/YOUR-USERNAME/Explainable-Credit-Risk-Platform.git
   cd Explainable-Credit-Risk-Platform
   `

2. Set up environment:
   `ash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   pip install -e .
   pip install -r requirements-dev.txt
   pre-commit install
   `

3. Create a feature branch: git checkout -b feature/your-feature

## Development Guidelines

- **Code style**: Black, isort, Ruff. Run lack . && isort . && ruff check . --fix.
- **Type hints**: Use type hints; mypy src must pass.
- **Tests**: Add/modify tests in 	ests/. Run pytest -v.
- **Commits**: Use clear, concise messages (conventional style preferred: eat:, ix:, docs:, 	est:, efactor:, chore:).
- **Reproducibility**: Set seeds via src/utils/seed.py; avoid non-determinism.
- **Ethics**: Never add code that logs secrets; avoid training with protected attributes as predictors.

## Pull Request Process

1. Ensure all checks pass (lint, typecheck, tests).
2. Update docs if behavior/API changes.
3. Include a clear description of changes and rationale.
4. Link related issues.

## Reporting Issues

Use GitHub Issues. Include: environment, steps to reproduce, expected/actual behavior, logs/screenshots if relevant.

## Code of Conduct

Be respectful, inclusive, and professional.
