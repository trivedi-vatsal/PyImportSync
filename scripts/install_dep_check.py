#!/usr/bin/env python3
"""
Easy installer for adding PyImportSync to your project's pre-commit hooks.
Usage: python -c "import urllib.request; exec(urllib.request.urlopen('https://raw.githubusercontent.com/trivedi-vatsal/PyImportSync/main/install_dep_check.py').read())"
"""

import os
import sys
import subprocess
from pathlib import Path


def install_precommit():
    """Install pre-commit if not already installed."""
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "show", "pre-commit"],
            capture_output=True,
            check=True,
        )
        print("✓ pre-commit is already installed")
        return True
    except subprocess.CalledProcessError:
        print("Installing pre-commit...")
        try:
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "pre-commit"], check=True
            )
            print("✓ pre-commit installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"✗ Failed to install pre-commit: {e}")
            return False


def create_or_update_precommit_config(
    repo_url="https://github.com/trivedi-vatsal/PyImportSync",
):
    """Create or update .pre-commit-config.yaml file."""
    config_file = Path(".pre-commit-config.yaml")

    # Template for the dependency checker configuration
    dep_check_config = f"""
  - repo: {repo_url}
    rev: main  # Consider using a specific version tag
    hooks:
      - id: check-python-dependencies
        name: Check Python Dependencies
        args: ['--quiet']"""

    if config_file.exists():
        print("Found existing .pre-commit-config.yaml")
        try:
            with open(config_file, "r") as f:
                content = f.read()

            # Check if our hook is already present
            if repo_url in content and "check-python-dependencies" in content:
                print("✓ Dependency checker is already configured")
                return True

            # Add our hook to existing config (simple append)
            if "repos:" in content:
                # Find the repos: line and add our config after it
                lines = content.split("\n")
                repos_line_idx = -1
                for i, line in enumerate(lines):
                    if line.strip().startswith("repos:"):
                        repos_line_idx = i
                        break

                if repos_line_idx >= 0:
                    # Insert our config after the repos: line
                    lines.insert(repos_line_idx + 1, dep_check_config)
                    content = "\n".join(lines)
                else:
                    # Just append to the end
                    content += dep_check_config
            else:
                # No repos section found, create one
                content = f"repos:{dep_check_config}\n" + content

        except Exception as e:
            print(f"Warning: Could not read existing config: {e}")
            content = f"repos:{dep_check_config}\n"
    else:
        print("Creating new .pre-commit-config.yaml")
        content = f"repos:{dep_check_config}\n"

    try:
        with open(config_file, "w") as f:
            f.write(content)
        print("✓ Updated .pre-commit-config.yaml")
        return True
    except Exception as e:
        print(f"✗ Failed to write config file: {e}")
        return False


def install_hooks():
    """Install the pre-commit hooks."""
    try:
        subprocess.run(["pre-commit", "install"], check=True, capture_output=True)
        print("✓ Pre-commit hooks installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to install hooks: {e}")
        return False


def main():
    """Main installation function."""
    print("🔧 Installing PyImportSync for pre-commit...")
    print()

    # Check if we're in a git repository
    if not Path(".git").exists():
        print("✗ This directory is not a git repository")
        print("  Please run this script from the root of your git repository")
        return 1

    # Install pre-commit
    if not install_precommit():
        return 1

    # Create/update pre-commit config
    if not create_or_update_precommit_config():
        return 1

    # Install hooks
    if not install_hooks():
        return 1

    print()
    print("🎉 Installation complete!")
    print()
    print("The dependency checker will now run before each commit.")
    print()
    print("Commands you can use:")
    print("  • Run all hooks manually: pre-commit run --all-files")
    print("  • Run only dependency check: pre-commit run check-python-dependencies")
    print("  • Skip hooks for one commit: git commit --no-verify")
    print("  • Update hook versions: pre-commit autoupdate")

    return 0


if __name__ == "__main__":
    sys.exit(main())
