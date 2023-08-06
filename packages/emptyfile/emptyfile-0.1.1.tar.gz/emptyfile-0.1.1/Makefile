.PHONY: clean docs help push release dist install lint
.DEFAULT_GOAL := help

define BROWSER_PYSCRIPT
import os, webbrowser, sys

from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT


BROWSER := python -c "$$BROWSER_PYSCRIPT"
PROJECTNAME = emptyfile
help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean: clean-build ## remove all build, test, coverage and Python artifacts

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	rm -fr *.egg-info
	rm -fr *.egg
	rm -f **.pyc
	rm -f **.pyo
	rm -f **~
	rm -fr **/__pycache__
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache
	rm -f corbertura.xml
	rm -f coverage.xml
	rm -fr .codacy-coverage

lint: ## check style with flake8
	black ${PROJECTNAME}
	black tests
	isort ${PROJECTNAME}
	isort tests
	pylint ${PROJECTNAME} tests
	pycodestyle ${PROJECTNAME} tests
	pydocstyle ${PROJECTNAME} tests
	pyroma .
	bandit ${PROJECTNAME}/*

test: ## run tests quickly with the default Python
	tox

push: lint clean test ## push to remote github repo
	git add .
	git commit -m "generic message"
	git push

release: clean lint test ## package and upload a release
	twine upload dist/*
