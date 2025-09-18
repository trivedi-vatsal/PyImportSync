#!/bin/bash
# Quick installer for Python Dependency Checker pre-commit hook

set -e

echo "🔧 Installing PyImportSync for pre-commit..."
echo

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "✗ This directory is not a git repository"
    echo "  Please run this script from the root of your git repository"
    exit 1
fi

# Install pre-commit if not already installed
if ! command -v pre-commit &> /dev/null; then
    echo "Installing pre-commit..."
    pip install pre-commit
    echo "✓ pre-commit installed"
else
    echo "✓ pre-commit is already installed"
fi

# Create or update .pre-commit-config.yaml
CONFIG_FILE=".pre-commit-config.yaml"
REPO_URL="https://github.com/trivedi-vatsal/PyImportSync"  # Replace with your repo URL

if [ -f "$CONFIG_FILE" ]; then
    echo "Found existing $CONFIG_FILE"
    
    # Check if our hook is already present
    if grep -q "check-python-dependencies" "$CONFIG_FILE" && grep -q "$REPO_URL" "$CONFIG_FILE"; then
        echo "✓ Dependency checker is already configured"
    else
        echo "  - repo: $REPO_URL" >> "$CONFIG_FILE"
        echo "    rev: main" >> "$CONFIG_FILE"
        echo "    hooks:" >> "$CONFIG_FILE"
        echo "      - id: check-python-dependencies" >> "$CONFIG_FILE"
        echo "        name: Check Python Dependencies" >> "$CONFIG_FILE"
        echo "        args: ['--quiet']" >> "$CONFIG_FILE"
        echo "✓ Added dependency checker to existing config"
    fi
else
    echo "Creating new $CONFIG_FILE"
    cat > "$CONFIG_FILE" << EOF
repos:
  - repo: $REPO_URL
    rev: main
    hooks:
      - id: check-python-dependencies
        name: Check Python Dependencies
        args: ['--quiet']
EOF
    echo "✓ Created $CONFIG_FILE"
fi

# Install the hooks
echo "Installing pre-commit hooks..."
pre-commit install
echo "✓ Pre-commit hooks installed"

echo
echo "🎉 Installation complete!"
echo
echo "The dependency checker will now run before each commit."
echo
echo "Commands you can use:"
echo "  • Run all hooks manually: pre-commit run --all-files"
echo "  • Run only dependency check: pre-commit run check-python-dependencies"
echo "  • Skip hooks for one commit: git commit --no-verify"
echo "  • Update hook versions: pre-commit autoupdate"