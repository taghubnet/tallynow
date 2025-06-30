# TallyNow Makefile
# Automated Oil & Gas Upper Completion Tally System

.PHONY: help well tests install clean lint

# Default target
help:
	@echo "TallyNow - Automated Upper Completion Tally System"
	@echo ""
	@echo "Available targets:"
	@echo "  well      - Run the completion tally calculation (main.py)"
	@echo "  tests     - Run all tests"
	@echo "  install   - Install dependencies"
	@echo "  clean     - Clean up temporary files"
	@echo "  lint      - Run code quality checks (if available)"
	@echo "  help      - Show this help message"

# Run the main well completion calculation
well:
	@echo "Running TallyNow completion calculation..."
	@if [ -f bin/activate ]; then \
		. bin/activate && python main.py; \
	else \
		python main.py; \
	fi

# Run all tests
tests:
	@echo "Running TallyNow test suite..."
	@if [ -f bin/activate ]; then \
		. bin/activate && pytest tests/test_basic.py tests/test_utils.py -v; \
	else \
		pytest tests/test_basic.py tests/test_utils.py -v; \
	fi

# Install dependencies
install:
	@echo "Installing TallyNow dependencies..."
	pip install -r requirements.txt

# Clean temporary files
clean:
	@echo "Cleaning temporary files..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.tmp" -delete

# Run linting (optional - add flake8 or black if desired)
lint:
	@echo "Code linting not configured. Consider adding flake8 or black to requirements.txt"
	@echo "Example: pip install flake8 && flake8 *.py"