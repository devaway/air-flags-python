SHELL := /bin/bash
.DEFAULT_GOAL := help
VENV_PATH := venv

# Colors
GREEN  := $(shell tput -Txterm setaf 2)
YELLOW := $(shell tput -Txterm setaf 3)
WHITE  := $(shell tput -Txterm setaf 7)
RESET  := $(shell tput -Txterm sgr0)
TARGET_MAX_CHAR_NUM=10


.PHONY: venv
## Create virtual environment
venv:
	python3 -m $(VENV_PATH) $(VENV_PATH)

.PHONY: install
## Run the package installation for development.
install:
	$(VENV_PATH)/bin/pip install -e .
	$(VENV_PATH)/bin/pip install -r requirements-test.txt

.PHONY: dist
## Build the package.
dist:
	rm -rf dist build
	$(VENV_PATH)/bin/python setup.py sdist

.PHONY: test
## Run the tests.
test:
	$(VENV_PATH)/bin/python -m pytest

.PHONY: coverage
## Run the tests with coverage.
coverage:
	$(VENV_PATH)/bin/python -m pytest --cov=air_flags

.PHONY: lint
## Run all linter checks.
lint:
	$(VENV_PATH)/bin/isort . --check
	$(VENV_PATH)/bin/black . --check --line-length 79
	$(VENV_PATH)/bin/flake8 .
	find air_flags -iname '*.py' | xargs $(VENV_PATH)/bin/mypy
	find tests -iname '*.py' | xargs $(VENV_PATH)/bin/mypy

.PHONY: fmt
## Apply linter format.
fmt:
	$(VENV_PATH)/bin/isort .
	$(VENV_PATH)/bin/black . --line-length 79

help:
	@echo "Thanks for your interest in Air flags!"
	@echo
	@echo "Usage:"
	@echo "  ${YELLOW}make${RESET} ${GREEN}<target>${RESET}"
	@echo
	@echo 'Targets:'
	@awk '/^[a-zA-Z\-\_0-9]+:/ { \
		helpMessage = match(lastLine, /^## (.*)/); \
		if (helpMessage) { \
			helpCommand = substr($$1, 0, index($$1, ":")); \
			helpMessage = substr(lastLine, RSTART + 3, RLENGTH); \
			printf "  ${YELLOW}%-$(TARGET_MAX_CHAR_NUM)s${RESET} ${GREEN}%s${RESET}\n", helpCommand, helpMessage; \
		} \
	} \
	{ lastLine = $$0 }' $(MAKEFILE_LIST)
	@echo
	@echo "Also make sure to read ./CONTRIBUTING.md"
