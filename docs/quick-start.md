# Quick Start Guide

This guide will help you get PyImportSync up and running quickly in your project.

## As a GitHub Action

### Basic Setup

Add this step to your GitHub workflow:

```yaml
- name: Check Python Dependencies
  uses: trivedi-vatsal/PyImportSync@v1.0.0
  with:
    project-path: '.'
    fail-on-missing: true
```

### Complete Workflow Example

Create `.github/workflows/dependency-check.yml`:

```yaml
name: Check Dependencies
on: [push, pull_request]

jobs:
  dependency-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Check Python Dependencies
        uses: trivedi-vatsal/PyImportSync@v1.0.0
        with:
          project-path: '.'
          fail-on-missing: true
```

## As a Pre-commit Hook

### Option 1: Quick Install (Recommended)

Run this one-liner in your project root:

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
    rev: v1.0.0  # Use a specific tag for production
    hooks:
      - id: check-python-dependencies
        name: Check Python Dependencies
        args: ['--quiet']  # Only show missing dependencies
```

1. Install the hooks:

```bash
pre-commit install
```

### Option 3: Local Hook

If you prefer to include the script directly in your repository:

```yaml
repos:
  - repo: local
    hooks:
      - id: check-dependencies
        name: Check Python Dependencies
        entry: python src/check_dependencies.py --quiet
        language: system
        files: \.py$
```

## Command Line Usage

You can also use PyImportSync directly from the command line:

```bash
# Clone and run directly
git clone https://github.com/trivedi-vatsal/PyImportSync.git
cd PyImportSync
python src/check_dependencies.py

# Basic usage (if you already have the code)
python src/check_dependencies.py

# With verbose output
python src/check_dependencies.py --verbose

# Custom requirements file
python src/check_dependencies.py --requirements-file requirements-dev.txt

# Use configuration file
python src/check_dependencies.py --config-file examples/pyimportsync-config.json
```

## Next Steps

- [Configure PyImportSync](configuration.md) for your project
- View [usage examples](examples.md) for more complex scenarios
- Check [advanced usage](advanced-usage.md) for technical details
