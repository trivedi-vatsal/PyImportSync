# Configuration Guide

PyImportSync supports flexible configuration to customize its behavior for different projects and development workflows.

## Configuration Methods

### 1. Command Line Arguments

The primary way to configure PyImportSync:

```bash
# Basic usage
python src/check_dependencies.py

# With verbose output
python src/check_dependencies.py --verbose

# Custom configuration file
python src/check_dependencies.py --config-file examples/pyimportsync-config.json

# Disable caching
python src/check_dependencies.py --no-cache
```

### 2. Configuration File

Create a JSON configuration file and specify it with `--config-file`:

```json
{
  "ignore_dirs": ["__pycache__", ".venv", "tests", "docs"],
  "requirements_file": "requirements.txt",
  "enable_cache": true,
  "use_pathspec": true
}
```

## Configuration Options

### ignore_dirs

**Type**: Array of strings  
**Default**: `["__pycache__", ".git", ".venv", "venv", "env"]`  
**Description**: Directories to ignore when scanning for Python files.

**Example**:

```json
{
  "ignore_dirs": ["tests", "docs", "examples", "build", "dist"]
}
```

### requirements_file

**Type**: String  
**Default**: `"requirements.txt"`  
**Description**: Path to the requirements file to check against.

**Example**:

```json
{
  "requirements_file": "requirements/production.txt"
}
```

### enable_cache

**Type**: Boolean  
**Default**: `true`  
**Description**: Enable file content caching for improved performance on subsequent runs.

**Example**:

```json
{
  "enable_cache": false
}
```

### cache_file

**Type**: String  
**Default**: `".pyimportsync_cache.json"`  
**Description**: Path to the cache file for storing file hashes.

**Example**:

```json
{
  "cache_file": ".cache/pyimportsync.json"
}
```

### use_pathspec

**Type**: Boolean  
**Default**: `true`  
**Description**: Use .gitignore patterns to determine which files to scan.

**Example**:

```json
{
  "use_pathspec": false
}
```

## Best Practices

1. Include your configuration file in version control
1. Customize ignore_dirs for your project structure
1. Enable caching for large projects
1. Test your configuration with --verbose mode first

## Configuration Examples

### Basic Project Configuration

```json
{
  "ignore_dirs": ["tests", "docs", "examples"],
  "requirements_file": "requirements.txt",
  "enable_cache": true,
  "use_pathspec": true
}
```

### Advanced Project Configuration

```json
{
  "ignore_dirs": ["tests", "docs", "examples", "build", "dist", "scripts"],
  "requirements_file": "requirements/production.txt",
  "enable_cache": true,
  "cache_file": ".cache/pyimportsync.json",
  "use_pathspec": true
}
```

### Development Configuration

```json
{
  "ignore_dirs": ["tests", "docs"],
  "requirements_file": "requirements-dev.txt",
  "enable_cache": false,
  "use_pathspec": false
}
```

### Large Project Configuration

```json
{
  "ignore_dirs": [
    "tests", "docs", "examples", "build", "dist", 
    "node_modules", "vendor", "third_party"
  ],
  "requirements_file": "requirements.txt",
  "enable_cache": true,
  "cache_file": ".pyimportsync_cache.json",
  "use_pathspec": true
}
```

## Command Line Override

Configuration file options can be overridden using command line arguments:

```bash
# Override requirements file
python src/check_dependencies.py --config-file config.json --requirements-file dev-requirements.txt

# Disable caching even if enabled in config
python src/check_dependencies.py --config-file config.json --no-cache

# Add additional ignore directories
python src/check_dependencies.py --config-file config.json --ignore-dirs "temp,backup"
```
