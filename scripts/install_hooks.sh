#!/bin/bash
# Script to install pre-commit hooks for dependency checking

echo "Installing pre-commit hooks for dependency checking..."

# Install pre-commit if not already installed
if ! command -v pre-commit &> /dev/null; then
    echo "Installing pre-commit..."
    pip install pre-commit
else
    echo "pre-commit is already installed"
fi

# Install the pre-commit hooks
pre-commit install

echo "Pre-commit hooks installed successfully!"
echo ""
echo "The following hooks will now run before each commit:"
echo "  - Code formatting (black, isort)"
echo "  - Code quality checks"
echo "  - Dependency validation"
echo ""
echo "To run hooks manually: pre-commit run --all-files"
echo "To skip hooks temporarily: git commit --no-verify"
