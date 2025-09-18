# PyImportSync - Python Import & Requirements Synchronizer

A versatile tool that automatically checks if all Python imports in your codebase are properly declared in `requirements.txt`. Works as both a GitHub Action and a pre-commit hook to help ensure your project dependencies are complete and up-to-date.

## Features

- 🔍 **Comprehensive Analysis**: Scans all Python files in your repository for import statements using AST parsing
- 📦 **Requirements Validation**: Compares imports against your `requirements.txt` file
- 🚀 **CI/CD Integration**: Seamlessly integrates with GitHub workflows
- 🪝 **Pre-commit Hook**: Can be used as a pre-commit hook for local development
- 📊 **Detailed Reporting**: Provides clear output about missing dependencies with optional rich formatting
- 🛠️ **Configurable**: Flexible configuration options for different project structures
- � **Git-aware**: Respects `.gitignore` patterns to skip irrelevant files
- ⚡ **Performance**: File content caching for faster subsequent runs
- 🧩 **Modular Architecture**: Clean, maintainable codebase with specialized modules
- � **Dynamic Detection**: Uses Python's built-in standard library detection
- 📈 **Enhanced Matching**: Advanced package metadata inspection for accurate dependency mapping

## Project Structure

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
│   └── pre_commit_hook.py            # Pre-commit wrapper
├── scripts/                           # Installation and utility scripts
│   ├── install_dep_check.py          # Python installer
│   ├── install_dep_check.sh          # Shell installer
│   ├── install_hooks.ps1             # PowerShell hook installer
│   ├── install_hooks.sh              # Shell hook installer
│   ├── check_deps.ps1                # PowerShell check script
│   └── check_deps.sh                 # Shell check script
├── docs/                              # Documentation
│   ├── examples.md                    # Usage examples
│   ├── github-action.md              # GitHub Action documentation
│   └── pre-commit-hooks.md           # Pre-commit hooks documentation
├── examples/                          # Configuration examples
│   ├── pyimportsync-config.json      # Example configuration file
│   ├── minimal-precommit-config.yaml
│   ├── complete-precommit-config.yaml
│   ├── github-workflows/
│   │   ├── dependency-check.yml
│   │   └── advanced-dependency-check.yml
│   └── local-usage/
│       ├── README.md
│       └── sample-project/
└── tests/                             # Test files
    └── test_dependencies.py
```

## Quick Start

### As a GitHub Action

Add this step to your GitHub workflow:

```yaml
- name: Check Python Dependencies
  uses: trivedi-vatsal/PyImportSync@v1
  with:
    project-path: '.'
    fail-on-missing: true
```

### As a Pre-commit Hook

#### Option 1: Quick Install (Recommended)

Run this one-liner in your project root:

```bash
# Using curl
curl -sSL https://raw.githubusercontent.com/trivedi-vatsal/PyImportSync/main/scripts/install_dep_check.sh | bash

# Using Python
python -c "import urllib.request; exec(urllib.request.urlopen('https://raw.githubusercontent.com/trivedi-vatsal/PyImportSync/main/scripts/install_dep_check.py').read())"
```

#### Option 2: Manual Setup

1. Add to your `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/trivedi-vatsal/PyImportSync
    rev: main  # Use a specific tag for production
    hooks:
      - id: check-python-dependencies
        name: Check Python Dependencies
        args: ['--quiet']  # Only show missing dependencies
```

1. Install the hooks:

```bash
pre-commit install
```

#### Option 3: Local Hook

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

## Configuration

The dependency checker can be customized using a configuration file to better fit your project's needs.

### Basic Configuration

Create a `pyimportsync-config.json` file and specify it with `--config-file`:

```json
{
  "ignore_dirs": ["tests", "docs", "examples"],
  "requirements_file": "requirements.txt",
  "enable_cache": true,
  "cache_file": ".pyimportsync_cache.json",
  "use_pathspec": true
}
```

### Configuration Options

The modern PyImportSync configuration supports:

- **`ignore_dirs`**: Directories to skip when scanning (in addition to .gitignore)
- **`requirements_file`**: Path to your requirements file
- **`enable_cache`**: Enable file content caching for performance
- **`cache_file`**: Path to cache file for storing file hashes
- **`use_pathspec`**: Use .gitignore patterns for file filtering

### Using Custom Config

```bash
# Use custom config file
python src/check_dependencies.py --config-file examples/pyimportsync-config.json

# Basic usage (no config file needed)
python src/check_dependencies.py
```

See [Configuration Guide](docs/configuration.md) for detailed documentation and examples.

## Inputs

| Input | Description | Required | Default |
|-------|-------------|----------|---------|
| `project-path` | Path to the Python project directory (relative to repository root) | No | `.` |
| `requirements-file` | Path to requirements.txt file (relative to project-path) | No | `requirements.txt` |
| `ignore-dirs` | Comma-separated list of directories to ignore (in addition to defaults) | No | `''` |
| `fail-on-missing` | Whether to fail the action if missing dependencies are found | No | `true` |
| `output-file` | Output file to save missing dependencies | No | `''` |
| `use-pipreqs` | Whether to use pipreqs for additional dependency detection | No | `true` |
| `respect-gitignore` | Whether to respect .gitignore patterns when scanning files | No | `true` |

## Outputs

| Output | Description |
|--------|-------------|
| `missing-dependencies` | List of missing dependencies (newline-separated) |
| `missing-count` | Number of missing dependencies found |
| `status` | Status of the check (`success`, `missing-deps`, or `error`) |

## Usage Examples

### GitHub Action Examples

#### Basic Usage

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
```

#### Advanced Configuration

```yaml
name: Advanced Dependency Check
on: [push, pull_request]

jobs:
  dependency-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Check Dependencies in Subdirectory
        uses: trivedi-vatsal/PyImportSync@v1
        with:
          project-path: 'src/python'
          requirements-file: 'requirements/production.txt'
          ignore-dirs: 'tests,docs,examples'
          fail-on-missing: false
          output-file: 'missing-deps.txt'
          respect-gitignore: true
```

### Pre-commit Hook Examples

#### Basic Hook Configuration

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/trivedi-vatsal/PyImportSync
    rev: v1.0.0  # Use a specific version
    hooks:
      - id: check-python-dependencies
```

#### Hook with Custom Arguments

```yaml
# .pre-commit-config.yaml
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

#### Multiple Hook Variants

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/trivedi-vatsal/PyImportSync
    rev: v1.0.0
    hooks:
      # Quick check (quiet mode)
      - id: check-python-dependencies
        name: Quick Dependency Check
        args: ['--quiet']
      
      # Detailed check (verbose mode)
      - id: check-python-dependencies-verbose
        name: Detailed Dependency Analysis
        stages: [manual]  # Only run when specifically requested
```

#### Combined with Other Hooks

```yaml
# .pre-commit-config.yaml
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
```

#### Pre-commit Commands

```bash
# Install hooks
pre-commit install

# Run all hooks on all files
pre-commit run --all-files

# Run only dependency check
pre-commit run check-python-dependencies

# Run dependency check on specific files
pre-commit run check-python-dependencies --files src/main.py src/utils.py

# Skip hooks for one commit
git commit --no-verify

# Update hook versions
pre-commit autoupdate

# Run specific hook stage
pre-commit run --hook-stage manual check-python-dependencies-verbose
```

### Disable Gitignore Respect

```yaml
name: Full Scan (Ignore .gitignore)
on: [push, pull_request]

jobs:
  dependency-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Check All Python Files
        uses: trivedi-vatsal/PyImportSync@v1
        with:
          respect-gitignore: false
          ignore-dirs: 'node_modules,vendor'
```

### Non-blocking Check with Outputs

```yaml
name: Dependency Check with Outputs
on: [push, pull_request]

jobs:
  dependency-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Check Python Dependencies
        id: dep-check
        uses: trivedi-vatsal/PyImportSync@v1
        with:
          fail-on-missing: false
          
      - name: Process Results
        run: |
          echo "Status: ${{ steps.dep-check.outputs.status }}"
          echo "Missing count: ${{ steps.dep-check.outputs.missing-count }}"
          if [ "${{ steps.dep-check.outputs.missing-count }}" -gt "0" ]; then
            echo "Missing dependencies:"
            echo "${{ steps.dep-check.outputs.missing-dependencies }}"
          fi
```

## How It Works

1. **Code Analysis**: The action scans all Python files in the specified project path
2. **Git-aware Filtering**: Respects `.gitignore` patterns to skip ignored files and directories
3. **Import Extraction**: Uses AST parsing to extract all import statements
4. **Smart Filtering**: Removes standard library modules and internal project modules
5. **Comparison**: Compares found imports with packages listed in requirements.txt
6. **Reporting**: Generates a detailed report of missing dependencies
7. **Optional pipreqs**: Uses pipreqs tool for additional dependency detection

## Gitignore Integration

The action automatically respects your project's `.gitignore` file to avoid scanning irrelevant files:

### Supported Patterns

- **Directory patterns**: `build/`, `dist/`, `__pycache__/`
- **File patterns**: `*.pyc`, `*.log`, `temp_*`
- **Wildcard patterns**: `test_*`, `*_backup`
- **Nested patterns**: `docs/build/`, `src/*/temp`

### Example .gitignore

```gitignore
# Python
__pycache__/
*.py[cod]
*.so
.Python
build/
develop-eggs/
dist/

# Virtual environments
venv/
ENV/
env/

# IDE
.vscode/
.idea/

# Testing
.pytest_cache/
.coverage
htmlcov/

# Custom
temp_files/
test_data/
```

### Disabling Gitignore

You can disable gitignore respect if needed:

```yaml
- name: Check All Files
  uses: trivedi-vatsal/PyImportSync@v1
  with:
    respect-gitignore: false
```

## Default Ignored Directories

The action automatically ignores these common directories (in addition to gitignore patterns):

- `myenv`, `__pycache__`, `.git`, `.venv`, `venv`, `env`
- `node_modules`, `.pytest_cache`, `build`, `dist`, `static`

You can add additional directories using the `ignore-dirs` input.

## Known Import Mappings

The action includes mappings for common packages where the import name differs from the package name:

- `bs4` → `beautifulsoup4`
- `PIL` → `Pillow`
- `cv2` → `opencv-python`
- `sklearn` → `scikit-learn`
- And more...

## Command Line Usage

You can also use this tool locally:

```bash
# Basic usage
python src/check_dependencies.py

# Verbose output with detailed information
python src/check_dependencies.py --verbose

# Specify custom requirements file
python src/check_dependencies.py --requirements-file requirements-dev.txt

# Use configuration file
python src/check_dependencies.py --config-file examples/pyimportsync-config.json

# Disable caching for fresh analysis
python src/check_dependencies.py --no-cache

# Disable pipreqs integration
python src/check_dependencies.py --no-pipreqs

# Specify project root directory
python src/check_dependencies.py --project-root /path/to/project
```

## Troubleshooting

### Common Issues

#### Action fails with "Requirements file not found"

- Ensure your `requirements.txt` file exists in the specified location
- Check the `requirements-file` input path

#### False positives for internal modules

- Use the `ignore-dirs` input to exclude directories containing internal modules
- Add patterns to your `.gitignore` file
- The action automatically detects many common internal module patterns

#### pipreqs not working

- Set `use-pipreqs: false` if pipreqs is causing issues
- This disables additional dependency detection but the core functionality remains

#### Gitignore patterns not working

- Ensure your `.gitignore` file is in the project root
- Check that patterns follow standard gitignore syntax
- Use `respect-gitignore: false` to bypass gitignore temporarily for debugging

### Debug Mode

Enable debug output by setting the `ACTIONS_STEP_DEBUG` secret to `true` in your repository.

The action will show:

- Number of gitignore patterns loaded
- Whether gitignore is being respected
- Files being scanned vs skipped

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
