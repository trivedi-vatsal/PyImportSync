# Project Manifest

This file documents the reorganized structure of PyImportSync.

## Core Files (Root Level)

- `README.md` - Main project documentation
- `LICENSE` - Project license
- `action.yml` - GitHub Action definition
- `Dockerfile` - Container setup for GitHub Action
- `entrypoint.sh` - Container entrypoint script
- `requirements.txt` - Python dependencies
- `.pre-commit-hooks.yaml` - Pre-commit hook definitions
- `.gitignore` - Git ignore patterns

## Source Code (`src/`)

- `check_dependencies.py` - Main CLI entry point
- `pre_commit_hook.py` - Pre-commit hook wrapper
- `pyimportsync/` - Core library
  - `__init__.py`
  - `analyzer.py`
  - `cache.py`
  - `checker.py`
  - `gitignore.py`
  - `reporter.py`
  - `scanner.py`
  - `utils.py`

## Installation Scripts (`scripts/`)

- `install_dep_check.py` - Python-based installer
- `install_dep_check.sh` - Shell-based installer
- `install_hooks.ps1` - PowerShell pre-commit installer
- `install_hooks.sh` - Shell pre-commit installer

## Documentation (`docs/`)

- `configuration.md` - Configuration system documentation
- `examples.md` - Comprehensive usage examples
- `github-action.md` - GitHub Action specific documentation
- `pre-commit-hooks.md` - Pre-commit hooks specific documentation

## Examples (`examples/`)

- `minimal-precommit-config.yaml` - Minimal pre-commit configuration
- `complete-precommit-config.yaml` - Complete pre-commit configuration with multiple tools
- `github-workflows/` - GitHub workflow examples
  - `dependency-check.yml` - Basic workflow
  - `advanced-dependency-check.yml` - Advanced workflow with matrix strategy
- `local-usage/` - Local usage examples
  - `README.md` - Local usage documentation
  - `sample-project/` - Sample project for testing

## Tests (`tests/`)

- `test_dependencies.py` - Unit tests for PyImportSync

## Key Changes Made

1. **Organized source code** into `src/` directory
2. **Centralized scripts** in `scripts/` directory
3. **Separated documentation** into `docs/` directory
4. **Provided comprehensive examples** in `examples/` directory
5. **Added test structure** in `tests/` directory
6. **Updated all file references** to use new paths
7. **Maintained backward compatibility** for GitHub Action and pre-commit hooks
