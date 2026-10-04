# One short word does one whole job. Run `make` alone to see them.
.DEFAULT_GOAL := help
PY ?= python

help:      ## Show every command
	@grep -E '^[a-z-]+:.*##' Makefile | sed 's/:.*##/ -/'

setup:     ## Install everything (first time only)
	$(PY) -m pip install -r requirements.txt
	@test -f .env || cp .env.example .env

check:     ## Lint + all tests (same as CI)
	$(PY) -m flake8 backend/ tests/ scripts/ auto_task_sync.py --max-line-length=100
	$(PY) -m pytest tests/ -q

verify:    ## Quant verification (math checks on the models)
	$(PY) scripts/quant_verify.py

run:       ## Start the API on http://127.0.0.1:5000
	$(PY) backend/app.py

apo:       ## Start APO on http://127.0.0.1:8000
	$(PY) apo/apo.py

status:    ## Where things stand and what to do next
	$(PY) scripts/status.py

all: check verify status ## Check, verify, then show status
