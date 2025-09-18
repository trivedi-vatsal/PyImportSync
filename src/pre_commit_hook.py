#!/usr/bin/env python3
"""
Pre-commit hook wrapper for dependency checking.
This script can be used directly as a pre-commit hook or called from other hooks.
"""

import sys
import subprocess
import os
from pathlib import Path


def run_dependency_check():
    """Run the dependency checker with appropriate arguments for pre-commit."""
    # Get the directory where this script is located
    script_dir = Path(__file__).parent.absolute()
    checker_script = script_dir / "check_dependencies.py"

    # Check if we're in a git repository
    try:
        subprocess.run(
            ["git", "rev-parse", "--git-dir"], capture_output=True, check=True
        )
    except subprocess.CalledProcessError:
        print("Error: Not in a git repository")
        return 1

    # Get the git root directory
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
            check=True,
        )
        git_root = result.stdout.strip()
    except subprocess.CalledProcessError:
        print("Error: Could not determine git root directory")
        return 1

    # Run the dependency checker
    try:
        cmd = [
            sys.executable,
            str(checker_script),
            "--project-root",
            git_root,
            "--quiet",  # Only show missing dependencies
            "--respect-gitignore",
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.stdout:
            print("Missing dependencies found:")
            print(result.stdout)

        if result.stderr:
            print("Error:", result.stderr, file=sys.stderr)

        return result.returncode

    except Exception as e:
        print(f"Error running dependency checker: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(run_dependency_check())
