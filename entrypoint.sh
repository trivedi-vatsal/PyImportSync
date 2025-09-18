#!/bin/bash

set -e

# GitHub Action inputs
PROJECT_PATH=${1:-"."}
REQUIREMENTS_FILE=${2:-"requirements.txt"}
IGNORE_DIRS=${3:-""}
FAIL_ON_MISSING=${4:-"true"}
OUTPUT_FILE=${5:-""}
USE_PIPREQS=${6:-"true"}
RESPECT_GITIGNORE=${7:-"true"}

echo "🔍 PyImportSync GitHub Action"
echo "============================================="
echo "Project path: $PROJECT_PATH"
echo "Requirements file: $REQUIREMENTS_FILE"
echo "Ignore directories: $IGNORE_DIRS"
echo "Fail on missing: $FAIL_ON_MISSING"
echo "Output file: $OUTPUT_FILE"
echo "Use pipreqs: $USE_PIPREQS"
echo "Respect gitignore: $RESPECT_GITIGNORE"
echo ""

# Change to the GitHub workspace
cd "$GITHUB_WORKSPACE"

# Validate project path exists
if [ ! -d "$PROJECT_PATH" ]; then
    echo "❌ Error: Project path '$PROJECT_PATH' does not exist"
    echo "status=error" >> $GITHUB_OUTPUT
    exit 1
fi

# Change to project directory
cd "$PROJECT_PATH"

# Check if requirements file exists
if [ ! -f "$REQUIREMENTS_FILE" ]; then
    echo "⚠️  Warning: Requirements file '$REQUIREMENTS_FILE' not found"
    echo "Creating empty requirements.txt for analysis..."
    touch "$REQUIREMENTS_FILE"
fi

# Prepare command arguments
ARGS=(
    "--project-root" "."
    "--requirements-file" "$REQUIREMENTS_FILE"
)

# Add gitignore handling
if [ "$RESPECT_GITIGNORE" = "false" ]; then
    ARGS+=("--no-gitignore")
else
    ARGS+=("--respect-gitignore")
fi

# Add ignore directories if specified
if [ -n "$IGNORE_DIRS" ]; then
    # Convert comma-separated to space-separated and add to ignore list
    ARGS+=("--ignore-dirs" "$IGNORE_DIRS")
fi

# Add output file if specified
if [ -n "$OUTPUT_FILE" ]; then
    ARGS+=("--output" "$OUTPUT_FILE")
fi

# Add pipreqs flag
if [ "$USE_PIPREQS" = "false" ]; then
    ARGS+=("--no-pipreqs")
fi

# Run the dependency checker
echo "🔍 Running dependency analysis..."
echo ""

# Create a temporary file to capture output
TEMP_OUTPUT=$(mktemp)
TEMP_MISSING=$(mktemp)

# Run the checker and capture output
if python /action/src/check_dependencies.py "${ARGS[@]}" > "$TEMP_OUTPUT" 2>&1; then
    CHECK_EXIT_CODE=0
else
    CHECK_EXIT_CODE=$?
fi

# Display the output
cat "$TEMP_OUTPUT"

# Extract missing dependencies if any
MISSING_DEPS=""
MISSING_COUNT=0

if [ $CHECK_EXIT_CODE -ne 0 ]; then
    # Run again with quiet mode to get just the missing packages
    if python /action/src/check_dependencies.py "${ARGS[@]}" --quiet > "$TEMP_MISSING" 2>/dev/null; then
        MISSING_DEPS=$(cat "$TEMP_MISSING")
        MISSING_COUNT=$(cat "$TEMP_MISSING" | wc -l)
        if [ -z "$MISSING_DEPS" ]; then
            MISSING_COUNT=0
        fi
    fi
fi

# Set GitHub Action outputs
echo "missing-dependencies<<EOF" >> $GITHUB_OUTPUT
echo "$MISSING_DEPS" >> $GITHUB_OUTPUT
echo "EOF" >> $GITHUB_OUTPUT

echo "missing-count=$MISSING_COUNT" >> $GITHUB_OUTPUT

# Set status output
if [ $CHECK_EXIT_CODE -eq 0 ]; then
    echo "status=success" >> $GITHUB_OUTPUT
    echo ""
    echo "✅ All dependencies are satisfied!"
else
    echo "status=missing-deps" >> $GITHUB_OUTPUT
    echo ""
    echo "❌ Missing dependencies detected!"
fi

# Clean up temp files
rm -f "$TEMP_OUTPUT" "$TEMP_MISSING"

# Handle exit behavior based on fail-on-missing setting
if [ "$FAIL_ON_MISSING" = "true" ] && [ $CHECK_EXIT_CODE -ne 0 ]; then
    echo ""
    echo "💡 Tip: Set 'fail-on-missing: false' in your workflow to make this step non-blocking"
    exit $CHECK_EXIT_CODE
else
    echo ""
    echo "📝 Action completed (non-blocking mode)"
    exit 0
fi