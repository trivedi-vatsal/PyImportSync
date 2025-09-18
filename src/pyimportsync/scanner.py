"""
Import scanning functionality for PyImportSync.

This module handles scanning Python files for import statements using AST parsing
with regex fallback for malformed files.
"""

import ast
import re
from pathlib import Path
from typing import Set

from .cache import FileCache
from .gitignore import GitignoreHandler
from .utils import get_dynamic_stdlib_modules, is_local_module


class ImportScanner:
    """Scans Python files for import statements."""

    def __init__(
        self,
        project_root: Path,
        ignore_dirs: Set[str],
        cache: FileCache,
        gitignore_handler: GitignoreHandler,
    ):
        """Initialize import scanner."""
        self.project_root = project_root
        self.ignore_dirs = ignore_dirs
        self.cache = cache
        self.gitignore_handler = gitignore_handler
        self.stdlib_modules = get_dynamic_stdlib_modules()

    def find_imports_in_code(self) -> Set[str]:
        """Find all unique imports in the codebase."""
        all_imports = set()

        # Walk through all Python files
        for py_file in self.project_root.rglob("*.py"):
            # Skip if file is in ignored directory
            if self._should_skip_file(py_file):
                continue

            # Skip if file is ignored by gitignore
            if self.gitignore_handler.is_ignored(py_file):
                continue

            # Get imports from file (using cache if available)
            if self.cache.is_file_cached(py_file):
                if self.cache.enabled:
                    print(f"Using cached imports for {py_file}")
                file_imports = self.cache.get_cached_imports(py_file)
            else:
                file_imports = self._extract_imports_from_file(py_file)
                self.cache.cache_file_imports(py_file, file_imports)

            all_imports.update(file_imports)

        # Filter out standard library modules and local modules
        return self._filter_external_imports(all_imports)

    def _should_skip_file(self, filepath: Path) -> bool:
        """Check if file should be skipped based on ignore patterns."""
        # Check if any parent directory is in ignore list
        for part in filepath.parts:
            if part in self.ignore_dirs:
                return True
        return False

    def _extract_imports_from_file(self, filepath: Path) -> Set[str]:
        """Extract import statements from a Python file using AST."""
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

            # Try AST parsing first
            try:
                tree = ast.parse(content)
                return self._extract_imports_from_ast(tree)
            except SyntaxError:
                # Fall back to regex parsing for malformed files
                return self._extract_imports_regex(filepath)

        except (OSError, UnicodeDecodeError) as e:
            print(f"Warning: Could not read {filepath}: {e}")
            return set()

    def _extract_imports_from_ast(self, tree: ast.AST) -> Set[str]:
        """Extract imports from AST tree."""
        imports = set()

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.add(alias.name.split(".")[0])
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.add(node.module.split(".")[0])

        return imports

    def _extract_imports_regex(self, filepath: Path) -> Set[str]:
        """Extract imports using regex patterns as fallback."""
        imports = set()

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

            # Match various import patterns
            patterns = [
                r"^import\s+(\w+)",
                r"^from\s+(\w+)",
                r"^\s*import\s+(\w+)",
                r"^\s*from\s+(\w+)",
            ]

            for pattern in patterns:
                matches = re.findall(pattern, content, re.MULTILINE)
                imports.update(matches)

        except (OSError, UnicodeDecodeError):
            pass

        return imports

    def _filter_external_imports(self, all_imports: Set[str]) -> Set[str]:
        """Filter out standard library and local modules."""
        external_imports = set()

        for imp in all_imports:
            # Skip standard library modules
            if imp in self.stdlib_modules:
                continue

            # Skip local modules
            if is_local_module(imp, self.project_root):
                continue

            # Skip common built-ins that might not be in stdlib list
            if imp in {"__future__", "__main__", "__builtin__", "builtins"}:
                continue

            external_imports.add(imp)

        return external_imports
