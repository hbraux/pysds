PYTHON = python3

.DEFAULT_GOAL := help


help:
	@echo $$(fgrep -h "## " $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/^\([a-z][a-z_\-]*\): ##/\\nmake \\\e[1;34m\1\\\e[0m\t:/g')


install: ## install module
	$(PYTHON) setup.py install

develop: ## install module in development mode
	 $(PYTHON) setup.py develop 


test: ## run unit tests
	PYTHONDONTWRITEBYTECODE=1 pytest -v .

clitest: ## run cli tests
	sds init
