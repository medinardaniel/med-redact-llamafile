# Define variables
DOCKER_IMAGE_NAME=llamafile-backend
SOURCE_DIR=llamafile-backend
TEST_DIR=llamafile-backend

# Define commands
PYTHON_FORMATTER=black
LINTER=flake8
TEST_RUNNER=pytest

# Install dependencies
install:
	pip install -r $(SOURCE_DIR)/requirements.txt

# Format code using black
format:
	$(PYTHON_FORMATTER) $(SOURCE_DIR)

# Lint code using flake8
lint:
	$(LINTER) $(SOURCE_DIR)

# Run tests using pytest
test:
	$(TEST_RUNNER) $(TEST_DIR)

# Build Docker image
build:
	docker build -t $(DOCKER_IMAGE_NAME) $(SOURCE_DIR)

# Run all steps: format, lint, test, and build
all: format lint test build

.PHONY: format lint test docker-build all
