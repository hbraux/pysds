PYTHON = python3
PYSYD_CONFIG_PATH = $(CURDIR)/target
export PYSYD_CONFIG_PATH

.DEFAULT_GOAL := help

help:
	@echo $$(fgrep -h "## " $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/^\([a-z][a-z_\-]*\): ##/\\nmake \\\e[1;34m\1\\\e[0m\t:/g')


install: ## install module
	$(PYTHON) setup.py install

develop: ## install module in development mode
	 $(PYTHON) setup.py develop 


test: ## run unit tests
	PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=tests/ pytest -v .

testcli:  ## run cli tests
	rm -fr $(PYSYD_CONFIG_PATH)
	pysds init
	pysds register testuser test@email.org 8a88e12a-98d6-4c1c-9850-d3cf5b31ca8a MEgCQQChLLM582ZAE+rSsDimhXbln+8jCY5gDeyNGdgIK5crhIU3kiRJWr6V711Or2AmtMBHHoFf1rz1Mbjw+YOn4x5JAgMBAAE=
	pysds users
	pysds add tests/wires.csv

