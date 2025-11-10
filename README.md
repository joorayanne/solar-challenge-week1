# Solar Data Discovery — Week 1

Starter repository scaffold generated 2025-11-10.

## Quickstart

```bash
# 1) Create repo locally
git clone <YOUR-REPO-URL> solar-challenge-week1
cd solar-challenge-week1

# 2) Create & activate venv
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# 3) Install deps
pip install -r requirements.txt

# 4) Start Jupyter
jupyter notebook
```

## Branching model

- `setup-task` — environment & CI scaffolding
- `eda-<country>` — EDA per country (e.g., `eda-benin`, `eda-sierra_leone`, `eda-togo`)

Open a PR to merge into `main` when a task is complete.

## Data layout

- Keep raw and cleaned CSVs in `data/` (already `.gitignore`d).
- Do **not** commit CSVs to the repo.

## Notebooks

- Country EDA notebooks live in `notebooks/` and are pre-filled templates:
- `sierra_leone_eda.ipynb`

## CI

GitHub Actions installs dependencies and prints Python version on each push or PR.