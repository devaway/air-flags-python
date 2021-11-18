SHELL := /bin/bash
.DEFAULT_GOAL := help

# Colors
GREEN  := $(shell tput -Txterm setaf 2)
YELLOW := $(shell tput -Txterm setaf 3)
WHITE  := $(shell tput -Txterm setaf 7)
RESET  := $(shell tput -Txterm sgr0)
TARGET_MAX_CHAR_NUM=10

.PHONY: install
## Run the package installation for development.
install:
	pip install -e .
	pip install -r requirements-test.txt

.PHONY: test
## Run the tests.
test:
	python3 -m pytest

.PHONY: coverage
## Run the tests with coverage.
coverage:
	python -m pytest --cov=air_flags

.PHONY: lint
## Run all linter checks.
lint:
	isort . --check
	black . --check --line-length 79
	flake8 .
	find air_flags -iname '*.py' | xargs mypy
	find tests -iname '*.py' | xargs mypy

.PHONY: fmt
## Apply linter format.
fmt:
	isort .
	black . --line-length 79

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
