# Advanced Usage

This document covers advanced usage patterns, technical details, and troubleshooting for PyImportSync.

## How It Works

1. **Code Analysis**: Scans all Python files in the specified project path
1. **Git-aware Filtering**: Respects `.gitignore` patterns to skip ignored files and directories
1. **Import Extraction**: Uses AST parsing to extract all import statements
1. **Smart Filtering**: Removes standard library modules and internal project modules
1. **Comparison**: Compares found imports with packages listed in requirements.txt
1. **Reporting**: Generates a detailed report of missing dependencies
1. **Optional pipreqs**: Uses pipreqs tool for additional dependency detection

## Gitignore Integration

PyImportSync automatically respects your project's `.gitignore` file to avoid scanning irrelevant files.

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
  uses: trivedi-vatsal/PyImportSync@v1.0.0
  with:
    respect-gitignore: false
```

## Default Ignored Directories

PyImportSync automatically ignores these common directories (in addition to gitignore patterns):

- `myenv`, `__pycache__`, `.git`, `.venv`, `venv`, `env`
- `node_modules`, `.pytest_cache`, `build`, `dist`, `static`

You can add additional directories using the `ignore-dirs` input.

## Known Import Mappings

PyImportSync includes mappings for common packages where the import name differs from the package name:

- `bs4` → `beautifulsoup4`
- `PIL` → `Pillow`
- `cv2` → `opencv-python`
- `sklearn` → `scikit-learn`
- And more...

## Command Line Options

Full list of command line options:

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

## Performance Tips

1. **Use caching**: Enable file content caching for faster subsequent runs
1. **Optimize gitignore**: Well-structured `.gitignore` patterns improve scan speed
1. **Targeted scanning**: Use `ignore-dirs` to skip large irrelevant directories
1. **Configuration files**: Use config files for complex setups instead of command line args
