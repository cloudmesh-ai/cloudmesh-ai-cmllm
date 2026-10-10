# Project Makefile

.PHONY: all install test clean lint docs

all: install test

install:
	pip install -e ".[test]"

test:
	PYTHONPATH=. pytest tests/

lint:
	# Placeholder for linting (e.g., flake8 or black)
	echo "Linting not configured yet"

docs:
	pip install -e ".[docs]"
	mkdocs serve

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .pytest_cache .coverage
