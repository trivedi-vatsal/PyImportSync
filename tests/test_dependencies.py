#!/usr/bin/env python3
"""
Basic tests for the dependency checker.
"""

import unittest
import tempfile
import os
from pathlib import Path
import sys

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from pyimportsync import DependencyChecker


class TestDependencyChecker(unittest.TestCase):
    """Test cases for the DependencyChecker class."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.project_path = Path(self.temp_dir)

    def test_init(self):
        """Test DependencyChecker initialization."""
        checker = DependencyChecker(self.temp_dir)
        self.assertEqual(checker.project_root, self.project_path)
        self.assertTrue(isinstance(checker.config["ignore_dirs"], list))

    def test_gitignore_loading(self):
        """Test .gitignore pattern loading."""
        # Create a simple .gitignore file
        gitignore_path = self.project_path / ".gitignore"
        gitignore_content = """
# Python
__pycache__/
*.pyc

# Virtual environments
venv/
env/
"""
        gitignore_path.write_text(gitignore_content)

        checker = DependencyChecker(self.temp_dir)
        patterns = checker.gitignore_handler.patterns

        self.assertIn("__pycache__/", patterns)
        self.assertIn("*.pyc", patterns)
        self.assertIn("venv/", patterns)

    def test_python_file_detection(self):
        """Test Python file detection through imports scanning."""
        # Create some test files
        (self.project_path / "main.py").write_text("import os\nimport requests\n")
        (self.project_path / "utils.py").write_text("import json\nimport flask\n")
        (self.project_path / "README.md").write_text("# Test project\n")

        checker = DependencyChecker(self.temp_dir)
        imports = checker.scanner.find_imports_in_code()

        # Should find external imports (not stdlib)
        self.assertIn("requests", imports)
        self.assertIn("flask", imports)
        # Should not find stdlib imports
        self.assertNotIn("os", imports)
        self.assertNotIn("json", imports)

    def tearDown(self):
        """Clean up test fixtures."""
        import shutil

        shutil.rmtree(self.temp_dir)


if __name__ == "__main__":
    unittest.main()
