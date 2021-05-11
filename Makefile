VENV_DIR ?= .venv
TEST_PATH ?= ./tests
PIP_CMD ?= pip
NOSE_LOG_LEVEL ?= WARNING

ifeq ($(OS), Windows_NT)
	VENV_RUN = . $(VENV_DIR)/Scripts/activate
else
	VENV_RUN = . $(VENV_DIR)/bin/activate
endif

setup-venv:
	(test `which virtualenv` || $(PIP_CMD) install --user virtualenv) && \
		(test -e $(VENV_DIR) || virtualenv $(VENV_OPTS) $(VENV_DIR))

install-venv:
	make setup-venv && \
		test ! -e requirements.txt || ($(VENV_RUN); $(PIP_CMD) -q install -r requirements.txt)

test:
	($(VENV_RUN); DEBUG=$(DEBUG) PYTHONPATH=`pwd` nosetests $(NOSE_ARGS) --with-timer --with-coverage --logging-level=$(NOSE_LOG_LEVEL) --nocapture --no-skip --exe --cover-erase --cover-tests --cover-inclusive --cover-package=localstack --with-xunit --exclude='$(VENV_DIR).*' --ignore-files='lambda_python3.py' $(TEST_PATH))