# Project Structure

This document outlines the organization and structure of the PyImportSync repository.

## Repository Layout

```text
PyImportSync/
├── README.md                           # Main documentation
├── LICENSE                             # License file
├── action.yml                          # GitHub Action definition
├── Dockerfile                          # Docker setup for GitHub Action
├── entrypoint.sh                       # Docker entrypoint
├── requirements.txt                    # Python dependencies
├── .pre-commit-hooks.yaml             # Pre-commit hook definitions
├── src/                               # Main source code
│   ├── check_dependencies.py         # Main dependency checker script
│   ├── pre_commit_hook.py            # Pre-commit wrapper
│   └── pyimportsync/                 # Core library modules
│       ├── __init__.py
│       ├── analyzer.py               # Import analysis logic
│       ├── cache.py                  # File caching system
│       ├── checker.py                # Main checking logic
│       ├── gitignore.py              # Gitignore pattern handling
│       ├── reporter.py               # Output formatting
│       ├── scanner.py                # File scanning
│       └── utils.py                  # Utility functions
├── scripts/                           # Installation and utility scripts
│   ├── install_dep_check.py          # Python installer
│   ├── install_dep_check.sh          # Shell installer
│   ├── install_hooks.ps1             # PowerShell hook installer
│   ├── install_hooks.sh              # Shell hook installer
│   ├── check_deps.ps1                # PowerShell check script
│   └── check_deps.sh                 # Shell check script
├── docs/                              # Documentation
│   ├── quick-start.md                 # Getting started guide
│   ├── configuration.md               # Configuration options
│   ├── examples.md                    # Usage examples
│   ├── github-action.md              # GitHub Action documentation
│   ├── pre-commit-hooks.md           # Pre-commit hooks documentation
│   ├── advanced-usage.md             # Advanced features and troubleshooting
│   └── project-structure.md          # This file
├── examples/                          # Configuration examples
│   ├── pyimportsync-config.json      # Example configuration file
│   ├── minimal-precommit-config.yaml # Minimal pre-commit setup
│   ├── complete-precommit-config.yaml # Complete pre-commit setup
│   ├── github-workflows/             # GitHub workflow examples
│   │   ├── dependency-check.yml      # Basic workflow
│   │   └── advanced-dependency-check.yml # Advanced workflow
│   └── local-usage/                  # Local usage examples
│       ├── README.md
│       └── sample-project/           # Sample project for testing
└── tests/                            # Test files
    └── test_dependencies.py          # Unit tests
```

## Core Components

### Source Code (`src/`)

- **`check_dependencies.py`**: Main entry point for dependency checking
- **`pre_commit_hook.py`**: Wrapper for pre-commit hook integration
- **`pyimportsync/`**: Core library with modular components

### Scripts (`scripts/`)

Installation and utility scripts for different platforms and use cases:

- **Installation scripts**: Automated setup for different environments
- **Check scripts**: Platform-specific dependency checking scripts

### Documentation (`docs/`)

Comprehensive documentation covering all aspects of PyImportSync:

- **User guides**: Quick start and configuration
- **Reference**: API documentation and examples
- **Advanced topics**: Troubleshooting and technical details

### Examples (`examples/`)

Real-world configuration examples and sample projects:

- **Configuration files**: JSON configs for different scenarios
- **Workflow files**: GitHub Actions workflow examples
- **Sample projects**: Test projects for validation

## Module Architecture

### Core Library (`src/pyimportsync/`)

The core functionality is organized into specialized modules:

- **`analyzer.py`**: Handles Python AST parsing and import extraction
- **`cache.py`**: Implements file content caching for performance
- **`checker.py`**: Main logic for dependency checking
- **`gitignore.py`**: Gitignore pattern parsing and file filtering
- **`reporter.py`**: Output formatting and reporting
- **`scanner.py`**: File system scanning and discovery
- **`utils.py`**: Common utility functions and helpers

This modular design ensures:

- **Separation of concerns**: Each module has a specific responsibility
- **Testability**: Individual components can be tested in isolation
- **Maintainability**: Changes to one area don't affect others
- **Extensibility**: New features can be added without major refactoring
