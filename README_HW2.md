# CPS 310 Homework 2 — Inventory Manager Automated Testing

This project refactors the original Homework 1 program by moving important logic into testable helper functions, without removing the interactive menu.

## Run on macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install pytest
python -m pytest -v
python inventory_manager.py
```

Tests use `tmp_path` for every file I/O check so `inventory.txt` is not changed. The fixture returns fresh data. Parametrized tests have readable ids.

## GitHub workflow

Preserve your original Homework 1 `main` commit. Create an issue and feature branch `feature/automated-testing`, make at least five meaningful commits as the tests/refactors are developed, push the branch, open a PR that includes `Closes #<actual issue number>`, and merge it to main. Use your own GitHub account/repo URL. Finally capture pytest, git status, and git log screenshots.

## AI use

If using AI, append an accurate description of the assistance and what you personally verified to your existing `AI_USAGE.md`.
