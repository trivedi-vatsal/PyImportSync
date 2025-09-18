#!/usr/bin/env python3
"""
Main entry point for PyImportSync when used as a module.
"""
import argparse
import sys
from pathlib import Path

from .checker import DependencyChecker
from .utils import load_config


def run():
    """Entry point function for python -m pyimportsync."""
    parser = argparse.ArgumentParser(
        description="PyImportSync - Python Import Synchronization Tool"
    )
    parser.add_argument("--project-root", default=None, help="Project root directory")
    parser.add_argument(
        "--requirements-file", default="requirements.txt", help="Requirements file path"
    )
    parser.add_argument("--config-file", default=None, help="Configuration file path")
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose output"
    )
    parser.add_argument(
        "--quiet", "-q", action="store_true", help="Enable quiet mode (minimal output)"
    )
    parser.add_argument("--no-cache", action="store_true", help="Disable caching")
    parser.add_argument("--no-pipreqs", action="store_true", help="Disable pipreqs")
    parser.add_argument(
        "--respect-gitignore",
        action="store_true",
        default=True,
        help="Respect .gitignore patterns",
    )
    parser.add_argument(
        "--no-gitignore", action="store_true", help="Ignore .gitignore patterns"
    )
    parser.add_argument(
        "--ignore-dirs",
        default="",
        help="Comma-separated list of directories to ignore",
    )
    parser.add_argument(
        "--output", default="", help="Output file to save missing dependencies"
    )
    args = parser.parse_args()

    # Prepare config overrides
    config_overrides = {}

    # Handle ignore directories - merge with defaults
    if args.ignore_dirs:
        additional_ignore_dirs = [
            d.strip() for d in args.ignore_dirs.split(",") if d.strip()
        ]
        # Load default config to get existing ignore dirs
        default_config = load_config(None, None)
        merged_ignore_dirs = list(
            set(default_config["ignore_dirs"] + additional_ignore_dirs)
        )
        config_overrides["ignore_dirs"] = merged_ignore_dirs

    # Handle gitignore settings
    if args.no_gitignore:
        config_overrides["use_pathspec"] = False

    # Handle verbose vs quiet
    verbose = args.verbose and not args.quiet

    checker = DependencyChecker(
        project_root=args.project_root,
        requirements_file=args.requirements_file,
        config_file=args.config_file,
        config=config_overrides,
        verbose=verbose,
        enable_cache=not args.no_cache,
    )

    # Run the check
    result = checker.check(use_pipreqs=not args.no_pipreqs)

    # Handle output file if specified
    if args.output and result != 0:
        try:
            # Get the analysis results for output
            analysis_results = checker.analyze_dependencies(
                use_pipreqs=not args.no_pipreqs
            )
            missing_deps = analysis_results.get("missing", [])

            with open(args.output, "w") as f:
                for dep in missing_deps:
                    f.write(f"{dep}\n")

            if verbose:
                print(f"Missing dependencies written to {args.output}")
        except Exception as e:
            if verbose:
                print(f"Warning: Could not write to output file {args.output}: {e}")

    # Handle quiet mode output for missing dependencies
    if args.quiet and result != 0:
        try:
            analysis_results = checker.analyze_dependencies(
                use_pipreqs=not args.no_pipreqs
            )
            missing_deps = analysis_results.get("missing", [])
            for dep in missing_deps:
                print(dep)
        except Exception:
            pass  # Suppress errors in quiet mode

    return result


if __name__ == "__main__":
    sys.exit(run())