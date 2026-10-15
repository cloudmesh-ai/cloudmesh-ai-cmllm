# Project Makefile for cloudmesh-ai-cmm

.PHONY: all install test clean lint docs serve chat admin view

# Default target: install dependencies and run tests
all: install test

# Install the project in editable mode with test dependencies
install:
	pip install -e ".[test]"

# Run all tests, including unit, smoke, and integration tests in tests/
test:
	pytest tests/

# Remove temporary build artifacts and caches
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .pytest_cache .coverage .mypy_cache .ruff_cache build dist *.egg-info

# Placeholder for linting
lint:
	# Linting not configured yet
	echo "Linting not configured yet"

# Generate and serve documentation using mkdocs
docs:
	pip install -e ".[docs]"
	mkdocs serve

# Start the mock server
serve:
	cmm serve

# Start the mock server in the background and open the chat interface
chat:
	nohup cmm serve > /dev/null 2>&1 & \
	until curl -s http://localhost:8888/docs > /dev/null; do sleep 0.5; done && \
	open http://localhost:8888/chat

# Start the mock server in the background and open the admin interface
admin:
	nohup cmm serve > /dev/null 2>&1 & \
	until curl -s http://localhost:8888/docs > /dev/null; do sleep 0.5; done && \
	open http://localhost:8888/admin

# Open documentation, admin, and user interface in the browser
view:
	nohup cmm serve > /dev/null 2>&1 & \
	until curl -s http://localhost:8888/docs > /dev/null; do sleep 0.5; done && \
	open http://localhost:8888/docs && \
	open http://localhost:8888/admin && \
	open http://localhost:8888/chat && \
	open https://github.com/cloudmesh-ai/cloudmesh-ai-llm-mock && \
	open https://cloudmesh-ai.github.io/cloudmesh-ai-llm-mock

