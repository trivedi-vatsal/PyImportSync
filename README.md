# PyImportSync - Python Import & Requirements Synchronizer

A versatile tool that automatically checks if all Python imports in your codebase are properly declared in `requirements.txt`. Works as both a GitHub Action and a pre-commit hook to help ensure your project dependencies are complete and up-to-date.

## Features

- 🔍 **Comprehensive Analysis**: Scans all Python files using AST parsing
- 📦 **Requirements Validation**: Compares imports against your `requirements.txt` file
- 🚀 **CI/CD Integration**: Works seamlessly with GitHub workflows
- 🪝 **Pre-commit Hook**: Easy local development integration
- 📊 **Detailed Reporting**: Clear output with optional rich formatting
- 🛠️ **Configurable**: Flexible options for different project structures
- ⚡ **Git-aware & Fast**: Respects `.gitignore` patterns with file caching

## Quick Start

### GitHub Action

```yaml
- name: Check Python Dependencies
  uses: trivedi-vatsal/PyImportSync@v1
  with:
    project-path: '.'
    fail-on-missing: true
```

### Pre-commit Hook

```yaml
repos:
  - repo: https://github.com/trivedi-vatsal/PyImportSync
    rev: v1.0.0
    hooks:
      - id: check-python-dependencies
```

## Documentation

- 📚 [Quick Start Guide](docs/quick-start.md) - Installation and basic setup
- ⚙️ [Configuration](docs/configuration.md) - Customize for your project
- 📖 [Usage Examples](docs/examples.md) - Real-world usage scenarios
- 🎯 [GitHub Action Setup](docs/github-action.md) - Complete action documentation
- 🪝 [Pre-commit Hooks](docs/pre-commit-hooks.md) - Local development integration
- 🔧 [Advanced Usage](docs/advanced-usage.md) - Technical details and troubleshooting
- 📋 [Project Structure](docs/project-structure.md) - Repository organization

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
