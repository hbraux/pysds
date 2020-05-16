PYTHON = python3
SDS_CONFIG_PATH = $(CURDIR)/target
TEST_UUID = f6f8f779-e2f9-4fb5-8021-eabfa9248ade
TEST_PUBKEY = MEgCQQCm0wfw5h/TYrRJwk0L4UPR7ZgGpswAxMS3V86vhzLA69WRnZzNJ24Wphw5/Yseb4E60Vzp0dW4elkuFR5N+R8TAgMBAAE=

export SDS_CONFIG_PATH

.DEFAULT_GOAL := help

help:
	@echo $$(fgrep -h "## " $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/^\([a-z][a-z_\-]*\): ##/\\nmake \\\e[1;34m\1\\\e[0m\t:/g')


install: ## install module
	$(PYTHON) setup.py install

develop: ## install module in development mode
	 $(PYTHON) setup.py develop 


test: ## run unit tests
	PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=tests coverage run --source=pysds -m pytest -v
	coverage report

testcli:  ## run cli tests
	rm -fr $(SDS_CONFIG_PATH)
	pysds init
	pysds register testuser test@email.org $(TEST_UUID) $(TEST_PUBKEY)
	pysds users
	pysds import -i ork.mymank.wires tests/wires.csv
	pysds load tests/wires.sds_

