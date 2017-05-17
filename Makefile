PYTHON_MODULES := main.py test_main.py

DEFAULT_PYTHON := python2
VIRTUALENV := virtualenv -q --python=$(DEFAULT_PYTHON) --no-download

VENV := .venv
PIP := $(VENV)/bin/pip
PEP8 := $(VENV)/bin/pep8
PYLINT := $(VENV)/bin/pylint
PYTEST := $(VENV)/bin/pytest
PYTHON := $(VENV)/bin/python

REQUIREMENTS := -r requirements.txt
DEV_REQUIREMENTS := -r requirements-dev.txt

default: test
shell:
	$(PYTHON) -i
check: test
venv:
	test -d $(VENV) || $(VIRTUALENV) $(VENV)
requirements:
	$(PIP) install -q -i https://pypi.tuna.tsinghua.edu.cn/simple $(REQUIREMENTS) $(DEV_REQUIREMENTS)
bootstrap: venv requirements
test: bootstrap
	$(PEP8) --repeat --ignore=E202,E501,E402 --exclude="*_pb2.py" $(PYTHON_MODULES)
	$(PYLINT) -E --ignore-patterns=".*_pb2.py" $(PYTHON_MODULES)
	$(PYTEST)  $(PYTHON_MODULES)
pipfreeze:
	$(PIP) freeze

# project specific
build:
	protoc -I=. --python_out=. obj.proto
run:
	env PYTHONPATH=. DEBUG=1 $(PYTHON) main.py
.PHONY: default shell check venv requirements bootstrap test build run client
