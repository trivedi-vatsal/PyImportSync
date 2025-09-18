# GitHub Action Documentation

This document provides detailed information about using PyImportSync as a GitHub Action.

## Basic Setup

Add this action to your workflow file (`.github/workflows/dependency-check.yml`):

```yaml
name: Check Dependencies
on: [push, pull_request]

jobs:
  dependency-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Check Python Dependencies
        uses: trivedi-vatsal/PyImportSync@v1
        with:
          project-path: '.'
          fail-on-missing: true
```

## Configuration Options

### Inputs

| Input | Description | Required | Default |
|-------|-------------|----------|---------|
| `project-path` | Path to the Python project directory | No | `.` |
| `requirements-file` | Path to requirements.txt file | No | `requirements.txt` |
| `ignore-dirs` | Comma-separated list of directories to ignore | No | `''` |
| `fail-on-missing` | Whether to fail if missing dependencies are found | No | `true` |
| `output-file` | Output file to save missing dependencies | No | `''` |
| `use-pipreqs` | Whether to use pipreqs for additional detection | No | `true` |
| `respect-gitignore` | Whether to respect .gitignore patterns | No | `true` |

### Outputs

| Output | Description |
|--------|-------------|
| `missing-dependencies` | List of missing dependencies (newline-separated) |
| `missing-count` | Number of missing dependencies found |
| `status` | Status of the check (`success`, `missing-deps`, or `error`) |

## Advanced Examples

### Multiple Requirements Files

```yaml
- name: Check Production Dependencies
  uses: trivedi-vatsal/PyImportSync@v1
  with:
    requirements-file: 'requirements/production.txt'

- name: Check Development Dependencies
  uses: trivedi-vatsal/PyImportSync@v1
  with:
    requirements-file: 'requirements/development.txt'
    fail-on-missing: false
```

### Matrix Strategy

```yaml
strategy:
  matrix:
    requirements: ['requirements.txt', 'requirements-dev.txt', 'requirements-test.txt']

steps:
  - uses: actions/checkout@v4
  - name: Check Dependencies - ${{ matrix.requirements }}
    uses: trivedi-vatsal/PyImportSync@v1
    with:
      requirements-file: ${{ matrix.requirements }}
```

### Conditional Execution

```yaml
- name: Check Dependencies
  uses: trivedi-vatsal/PyImportSync@v1
  if: contains(github.event.head_commit.modified, 'requirements.txt')
```
