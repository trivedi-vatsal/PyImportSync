# Script to install pre-commit hooks for dependency checking

Write-Host "Installing pre-commit hooks for dependency checking..." -ForegroundColor Cyan

# Install pre-commit if not already installed
try {
    pre-commit --version | Out-Null
    Write-Host "pre-commit is already installed" -ForegroundColor Green
} catch {
    Write-Host "Installing pre-commit..." -ForegroundColor Yellow
    pip install pre-commit
}

# Install the pre-commit hooks
pre-commit install

Write-Host "Pre-commit hooks installed successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "The following hooks will now run before each commit:"
Write-Host "  - Code formatting (black, isort)"
Write-Host "  - Code quality checks"
Write-Host "  - Dependency validation"
Write-Host ""
Write-Host "To run hooks manually: pre-commit run --all-files"
Write-Host "To skip hooks temporarily: git commit --no-verify"
