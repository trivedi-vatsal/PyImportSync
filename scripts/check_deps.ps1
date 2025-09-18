# Automated dependency checker script
Write-Host "🔍 Checking project dependencies..." -ForegroundColor Cyan

# Run the dependency checker
python src/check_dependencies.py

# Check exit code
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ All dependencies are satisfied!" -ForegroundColor Green
} else {
    Write-Host "❌ Missing dependencies found. Please review and update requirements.txt" -ForegroundColor Red
}
