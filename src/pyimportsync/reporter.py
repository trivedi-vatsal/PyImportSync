"""
Reporting functionality for PyImportSync.

This module handles report generation with optional rich formatting for
better visual output and comprehensive dependency analysis results.
"""

from pathlib import Path
from typing import Dict, List, Set

# Optional rich formatting support
try:
    from rich.console import Console
    from rich.table import Table
    from rich import print as rich_print

    HAS_RICH = True
except ImportError:
    HAS_RICH = False


class DependencyReporter:
    """Generates dependency analysis reports."""

    def __init__(self, verbose: bool = False):
        """Initialize reporter with verbosity setting."""
        self.verbose = verbose
        self.console = Console() if HAS_RICH else None

    def print_verbose_info(
        self,
        project_root: Path,
        requirements_file: str,
        has_pathspec: bool,
        has_rich: bool,
        cache_enabled: bool,
        ignore_dirs: Set[str],
        pattern_count: int,
    ):
        """Print verbose configuration information."""
        if not self.verbose:
            return

        print(f"📂 Project root: {project_root}")
        print(f"📄 Requirements file: {requirements_file}")
        print(f"🔧 Pathspec available: {has_pathspec}")
        print(f"🎨 Rich formatting available: {has_rich}")
        print(f"💾 Cache enabled: {cache_enabled}")
        print(f"🚫 Ignore directories: {', '.join(sorted(ignore_dirs))}")
        print(f"📋 Respecting .gitignore patterns ({pattern_count} patterns loaded)")

    def generate_report(self, analysis_results: Dict[str, List[str]]) -> int:
        """Generate and print dependency analysis report."""
        missing = analysis_results.get("missing", [])
        matched = analysis_results.get("matched", [])
        pipreqs = analysis_results.get("pipreqs", [])
        requirements_count = analysis_results.get("requirements_count", 0)
        imports_count = analysis_results.get("imports_count", 0)
        metadata_count = analysis_results.get("metadata_mappings_count", 0)

        if self.verbose:
            print(
                f"Found {len(set(missing + [m.split(' → ')[0] for m in matched]))} unique imports in code"
            )
            print(f"Found {requirements_count} packages in requirements.txt")
            if pipreqs:
                print(f"pipreqs found {len(pipreqs)} packages")
            if metadata_count:
                print(f"Found {metadata_count} package metadata mappings")

        if HAS_RICH and self.console:
            return self._generate_rich_report(
                missing, matched, pipreqs, imports_count, requirements_count
            )
        else:
            return self._generate_plain_report(
                missing, matched, pipreqs, imports_count, requirements_count
            )

    def _generate_rich_report(
        self,
        missing: List[str],
        matched: List[str],
        pipreqs: List[str],
        imports_count: int,
        requirements_count: int,
    ) -> int:
        """Generate rich formatted report."""
        self.console.print("\n" + "=" * 60)
        self.console.print(
            "🔍 [bold blue]PyImportSync DEPENDENCY ANALYSIS REPORT[/bold blue]"
        )
        self.console.print("=" * 60)

        if missing:
            self.console.print(
                "\n❌ [bold red]MISSING FROM REQUIREMENTS.TXT:[/bold red]"
            )
            self.console.print("-" * 40)
            for package in missing:
                self.console.print(f"  • [red]{package}[/red]")
        else:
            self.console.print(
                "\n✅ [bold green]All dependencies are satisfied![/bold green]"
            )

        if matched:
            self.console.print("\n📋 [bold green]MATCHED PACKAGES:[/bold green]")
            self.console.print("-" * 40)
            for match in matched:
                self.console.print(f"  • [green]{match}[/green]")

        if pipreqs:
            self.console.print(
                f"\n📦 [bold yellow]PIPREQS DETECTED ({len(pipreqs)} packages):[/bold yellow]"
            )
            self.console.print("-" * 40)
            for package in pipreqs:
                self.console.print(f"  • [yellow]{package}[/yellow]")

        # Summary
        self.console.print("\n📊 [bold cyan]SUMMARY:[/bold cyan]")
        self.console.print("-" * 40)
        self.console.print(f"  • Code imports: [cyan]{imports_count}[/cyan]")
        self.console.print(
            f"  • Requirements packages: [cyan]{requirements_count}[/cyan]"
        )
        self.console.print(f"  • Missing packages: [cyan]{len(missing)}[/cyan]")

        if not missing:
            self.console.print(
                "\n🎉 [bold green]All dependencies are satisfied![/bold green]"
            )

        return 1 if missing else 0

    def _generate_plain_report(
        self,
        missing: List[str],
        matched: List[str],
        pipreqs: List[str],
        imports_count: int,
        requirements_count: int,
    ) -> int:
        """Generate plain text report."""
        print("\n" + "=" * 60)
        print("🔍 PyImportSync DEPENDENCY ANALYSIS REPORT")
        print("=" * 60)

        if missing:
            print("\n❌ MISSING FROM REQUIREMENTS.TXT:")
            print("-" * 40)
            for package in missing:
                print(f"  • {package}")
        else:
            print("\n✅ All dependencies are satisfied!")

        if matched:
            print("\n📋 MATCHED PACKAGES:")
            print("-" * 40)
            for match in matched:
                print(f"  • {match}")

        if pipreqs:
            print(f"\n📦 PIPREQS DETECTED ({len(pipreqs)} packages):")
            print("-" * 40)
            for package in pipreqs:
                print(f"  • {package}")

        # Summary
        print("\n📊 SUMMARY:")
        print("-" * 40)
        print(f"  • Code imports: {imports_count}")
        print(f"  • Requirements packages: {requirements_count}")
        print(f"  • Missing packages: {len(missing)}")

        if not missing:
            print("\n🎉 All dependencies are satisfied!")

        return 1 if missing else 0

    def has_rich_support(self) -> bool:
        """Check if rich formatting is available."""
        return HAS_RICH
