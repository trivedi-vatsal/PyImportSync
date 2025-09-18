"""
PyImportSync - Python Import Synchronization Tool

A modular dependency checker for Python projects that compares actual imports
in the codebase with requirements.txt and identifies missing or outdated dependencies.
"""

__version__ = "1.0.0"
__author__ = "trivedi-vatsal"

from .checker import DependencyChecker

__all__ = ["DependencyChecker"]