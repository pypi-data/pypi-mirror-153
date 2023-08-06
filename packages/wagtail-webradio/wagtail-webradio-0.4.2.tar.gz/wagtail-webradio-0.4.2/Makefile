.PHONY: clean lint format help
.DEFAULT_GOAL := help

PYTHON := venv/bin/python

help:
	@echo "Please use 'make <target>' where <target> is one of"
	@echo ""
	@grep '^[^.#]\+:\s\+.*#' Makefile | \
	  sed "s/\(.\+\):\s*\(.*\) #\s*\(.*\)/`printf "\033[93m"`  \1`printf "\033[0m"`	\3 [\2]/" | \
	  expand -35
	@echo ""
	@echo "Check the Makefile to know exactly what each target is doing."

clean: # Remove all builds and Python artifacts
	find wagtail_webradio \
	  \( -name '*.py[co]' -o -name '__pycache__' \) -exec rm -rf {} +
	rm -rf build dist .eggs *.egg-info

test: # Run tests quickly with the current Python
	$(PYTHON) -m pytest

test-wip: # Run tests marked as wip with the current Python
	$(PYTHON) -m pytest -vv -m 'wip' --pdb

coverage: # Check code coverage quickly with the current Python
	$(PYTHON) -m coverage run -m pytest
	$(PYTHON) -m coverage report -m
	$(PYTHON) -m coverage html
	@echo open htmlcov/index.html

lint: # Check the Python code syntax and style
	$(PYTHON) -m flake8 wagtail_webradio tests

format: # Fix the Python code syntax and imports order
	$(PYTHON) -m isort wagtail_webradio tests
	$(PYTHON) -m black wagtail_webradio tests

release: dist # Package and upload a release
	$(PYTHON) -m twine upload dist/*

dist: clean # Build source and wheel package
	$(PYTHON) -m build
	ls -l dist
