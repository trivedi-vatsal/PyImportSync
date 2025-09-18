# Pre-commit Hooks Documentation

This document provides detailed information about using PyImportSync as a pre-commit hook.

## Quick Start

### Option 1: One-Line Installation

```bash
# Using curl
curl -sSL https://raw.githubusercontent.com/trivedi-vatsal/PyImportSync/main/scripts/install_dep_check.sh | bash

# Using Python
python -c "import urllib.request; exec(urllib.request.urlopen('https://raw.githubusercontent.com/trivedi-vatsal/PyImportSync/main/scripts/install_dep_check.py').read())"
```

### Option 2: Manual Setup

1. Add to your `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/trivedi-vatsal/PyImportSync
    rev: main  # Use a specific tag for production
    hooks:
      - id: check-python-dependencies
```

2. Install the hooks:

```bash
pre-commit install
```

## Available Hooks

### check-python-dependencies

The main dependency checking hook with quiet output.

```yaml
- id: check-python-dependencies
  name: Check Python Dependencies
  args: ['--quiet']
```

### check-python-dependencies-verbose

Detailed dependency analysis with full output.

```yaml
- id: check-python-dependencies-verbose
  name: Check Python Dependencies (Verbose)
```

### check-python-dependencies-fail-fast

Exits immediately on first missing dependency.

```yaml
- id: check-python-dependencies-fail-fast
  name: Check Python Dependencies (Fail Fast)
  args: ['--quiet']
```

## Configuration Examples

### Basic Configuration

```yaml
repos:
  - repo: https://github.com/trivedi-vatsal/PyImportSync
    rev: v1.0.0
    hooks:
      - id: check-python-dependencies
```

### Custom Arguments

```yaml
repos:
  - repo: https://github.com/trivedi-vatsal/PyImportSync
    rev: v1.0.0
    hooks:
      - id: check-python-dependencies
        args: [
          '--ignore-dirs', 'tests,docs',
          '--requirements-file', 'requirements/prod.txt'
        ]
```

### Multiple Hook Variants

```yaml
repos:
  - repo: https://github.com/trivedi-vatsal/PyImportSync
    rev: v1.0.0
    hooks:
      # Quick check for all commits
      - id: check-python-dependencies
        name: Quick Dependency Check
        args: ['--quiet']
      
      # Detailed check for manual runs
      - id: check-python-dependencies-verbose
        name: Detailed Dependency Analysis
        stages: [manual]
```

### Combined with Other Tools

```yaml
repos:
  # Code formatting
  - repo: https://github.com/psf/black
    rev: 23.12.1
    hooks:
      - id: black

  # Import sorting
  - repo: https://github.com/pycqa/isort
    rev: 5.13.2
    hooks:
      - id: isort
        args: ["--profile", "black"]

  # Dependency checking
  - repo: https://github.com/trivedi-vatsal/PyImportSync
    rev: v1.0.0
    hooks:
      - id: check-python-dependencies
        args: ['--quiet']

  # Linting
  - repo: https://github.com/pycqa/flake8
    rev: 7.0.0
    hooks:
      - id: flake8
```

## Commands

### Installation

```bash
# Install pre-commit
pip install pre-commit

# Install hooks defined in .pre-commit-config.yaml
pre-commit install
```

### Running Hooks

```bash
# Run all hooks on all files
pre-commit run --all-files

# Run only dependency check
pre-commit run check-python-dependencies

# Run dependency check on specific files
pre-commit run check-python-dependencies --files src/main.py src/utils.py

# Run verbose check manually
pre-commit run --hook-stage manual check-python-dependencies-verbose
```

### Maintenance

```bash
# Update hook versions
pre-commit autoupdate

# Temporarily skip hooks
git commit --no-verify

# Clean hook cache
pre-commit clean
```

## Troubleshooting

### Common Issues

1. **Hook not running**: Make sure pre-commit is installed with `pre-commit install`
2. **Permission denied**: Ensure scripts have execute permissions
3. **Python not found**: Verify Python is in your PATH
4. **Requirements file not found**: Check the `requirements-file` argument

### Debugging

```bash
# Run with verbose output
pre-commit run check-python-dependencies-verbose --all-files

# Check hook configuration
pre-commit run --verbose check-python-dependencies
```
