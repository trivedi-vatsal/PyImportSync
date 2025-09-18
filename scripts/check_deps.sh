#!/bin/bash
# Automated dependency checker script

echo "🔍 Checking project dependencies..."

# Run the dependency checker
python src/check_dependencies.py

# Check exit code
if [ $? -eq 0 ]; then
    echo "✅ All dependencies are satisfied!"
else
    echo "❌ Missing dependencies found. Please review and update requirements.txt"
fi
