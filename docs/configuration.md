# Configuration Guide

PyImportSync supports flexible configuration to customize its behavior for different projects and development workflows.

## Configuration Methods

### 1. Command Line Arguments

The primary way to configure PyImportSync:

\\\ash
# Basic usage
python src/check_dependencies.py

# With verbose output
python src/check_dependencies.py --verbose

# Custom configuration file
python src/check_dependencies.py --config-file examples/pyimportsync-config.json

# Disable caching
python src/check_dependencies.py --no-cache
\\\

### 2. Configuration File

Create a JSON configuration file and specify it with \--config-file\:

\\\json
{
  "ignore_dirs": ["__pycache__", ".venv", "tests", "docs"],
  "requirements_file": "requirements.txt",
  "enable_cache": true,
  "use_pathspec": true
}
\\\

## Configuration Options

### ignore_dirs
Directories to ignore when scanning for Python files.

### requirements_file  
Path to the requirements file to check against.

### enable_cache
Enable file content caching for improved performance.

### use_pathspec
Use .gitignore patterns to determine which files to scan.

## Best Practices

1. Include your configuration file in version control
2. Customize ignore_dirs for your project structure  
3. Enable caching for large projects
4. Test your configuration with --verbose mode first
