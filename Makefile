SHELL := /bin/bash

.PHONY: setup test lint plates notebooks

setup:
	python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt && pip install -e .

test:
	pytest -q

plates:
	python scripts/make_plate.py --dry-run

notebooks:
	papermill notebooks/01_horizons_intro.ipynb artifacts/01_horizons_executed.ipynb
