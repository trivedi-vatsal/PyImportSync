"""
Main dependency checker class for PyImportSync.

This module provides the main DependencyChecker class that coordinates
all other modules to perform comprehensive dependency analysis.
"""

from pathlib import Path
from typing import Dict, List, Optional, Set

from .cache import FileCache
from .gitignore import GitignoreHandler
from .scanner import ImportScanner
from .analyzer import DependencyAnalyzer
from .reporter import DependencyReporter
from .utils import load_config


class DependencyChecker:
    """Main dependency checker that coordinates all analysis components."""

    def __init__(
        self,
        project_root: Optional[str] = None,
        requirements_file: str = "requirements.txt",
        config_file: Optional[str] = None,
        config: Optional[Dict] = None,
        verbose: bool = False,
        enable_cache: bool = True,
    ):
        """Initialize the dependency checker."""
        # Setup paths
        self.project_root = Path(project_root) if project_root else Path.cwd()
        self.verbose = verbose

        # Load configuration
        self.config = load_config(config_file, config)

        # Override config with explicit parameters
        if requirements_file != "requirements.txt":
            self.config["requirements_file"] = requirements_file
        if not enable_cache:
            self.config["enable_cache"] = False

        # Initialize components
        self.cache = FileCache(
            cache_file=self.config["cache_file"], enabled=self.config["enable_cache"]
        )

        self.gitignore_handler = GitignoreHandler(
            project_root=self.project_root, use_pathspec=self.config["use_pathspec"]
        )

        self.scanner = ImportScanner(
            project_root=self.project_root,
            ignore_dirs=set(self.config["ignore_dirs"]),
            cache=self.cache,
            gitignore_handler=self.gitignore_handler,
        )

        self.analyzer = DependencyAnalyzer(
            project_root=self.project_root,
            requirements_file=self.config["requirements_file"],
        )

        self.reporter = DependencyReporter(verbose=self.verbose)

    def analyze_dependencies(self, use_pipreqs: bool = True) -> Dict[str, List[str]]:
        """Perform complete dependency analysis."""
        if self.verbose:
            print("🔍 Analyzing dependencies...")

        # Print verbose configuration info
        self.reporter.print_verbose_info(
            project_root=self.project_root,
            requirements_file=self.config["requirements_file"],
            has_pathspec=self.gitignore_handler.has_pathspec_support(),
            has_rich=self.reporter.has_rich_support(),
            cache_enabled=self.config["enable_cache"],
            ignore_dirs=set(self.config["ignore_dirs"]),
            pattern_count=self.gitignore_handler.get_pattern_count(),
        )

        # Find imports in code
        imports = self.scanner.find_imports_in_code()

        # Analyze dependencies
        results = self.analyzer.analyze_dependencies(imports, use_pipreqs)

        # Save cache if enabled
        self.cache.save_cache()

        return results

    def generate_report(self, analysis_results: Dict[str, List[str]]) -> int:
        """Generate and display the dependency analysis report."""
        return self.reporter.generate_report(analysis_results)

    def check(self, use_pipreqs: bool = True) -> int:
        """Perform complete dependency check and return exit code."""
        results = self.analyze_dependencies(use_pipreqs)
        return self.generate_report(results)
