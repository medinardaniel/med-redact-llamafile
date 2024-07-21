# Makefile for the Medical Note Redaction Service

# Variables
VENV_DIR=venv
PYTHON=$(VENV_DIR)/bin/python
PIP=$(VENV_DIR)/bin/pip

# Commands
INSTALL_CMD=$(PIP) install -r requirements.txt
FORMAT_CMD=$(PYTHON) -m black .
LINT_CMD=$(PYTHON) -m flake8
TEST_CMD=$(PYTHON) -m pytest

# Targets
.PHONY: install format lint test

install: $(VENV_DIR)
	$(INSTALL_CMD)

format:
	$(FORMAT_CMD)

lint:
	$(LINT_CMD)

test:
	$(TEST_CMD)

$(VENV_DIR):
	python3 -m venv $(VENV_DIR)