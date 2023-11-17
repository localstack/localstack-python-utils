VENV_BIN ?= python3 -m venv
VENV_DIR ?= .venv
PIP_CMD ?= pip3

ifeq ($(OS), Windows_NT)
	VENV_ACTIVATE = $(VENV_DIR)/Scripts/activate
else
	VENV_ACTIVATE = $(VENV_DIR)/bin/activate
endif

VENV_RUN = . $(VENV_ACTIVATE)

venv: $(VENV_ACTIVATE)

format: venv           		  ## Run ruff and black to format the whole codebase
	($(VENV_RUN); python -m ruff check --show-source --fix .; python -m black .)

lint: venv      		  ## Run code linter to check code style and check if formatter would make changes
	($(VENV_RUN); python -m ruff check --show-source . && python -m black --check .)

install: venv
	$(VENV_RUN); $(PIP_CMD) install -e .

test: venv              	  ## Run tests
	($(VENV_RUN); python -m pytest -v --cov=plux --cov-report=term-missing --cov-report=xml tests)

