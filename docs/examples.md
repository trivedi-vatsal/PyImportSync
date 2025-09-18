# Example configurations for using the Python Dependency Checker

## As a GitHub Action

### .github/workflows/dependency-check.yml

```yaml
name: Dependency Check
on: [push, pull_request]

jobs:
  check-dependencies:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Check Python Dependencies
        uses: trivedi-vatsal/PyImportSync@v1
        with:
          fail-on-missing: true
```

## As a Pre-commit Hook

### .pre-commit-config.yaml (Minimal)

```yaml
repos:
  - repo: https://github.com/trivedi-vatsal/PyImportSync
    rev: main
    hooks:
      - id: check-python-dependencies
```

### .pre-commit-config.yaml (Complete Example)

```yaml
repos:
  # Python dependency checking
  - repo: https://github.com/trivedi-vatsal/PyImportSync
    rev: main
    hooks:
      - id: check-python-dependencies
        name: Check Python Dependencies
        args: ['--quiet']

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

  # Linting
  - repo: https://github.com/pycqa/flake8
    rev: 7.0.0
    hooks:
      - id: flake8
        args: ['--max-line-length=88', '--extend-ignore=E203,W503']
```

## Local Usage

### Command Line

```bash
# Basic check
python src/check_dependencies.py

# Custom requirements file
python src/check_dependencies.py --requirements-file requirements-dev.txt

# Ignore specific directories
python src/check_dependencies.py --ignore-dirs "tests,docs,examples"

# Save missing dependencies to file
python src/check_dependencies.py --output missing-deps.txt --quiet
```

### As a Git Hook (without pre-commit)

```bash
# Copy the dependency checker to your .git/hooks/ directory
cp check_dependencies.py .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit

# Or create a simple wrapper
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/sh
python check_dependencies.py --quiet
EOF
chmod +x .git/hooks/pre-commit
```
