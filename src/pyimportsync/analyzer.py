"""
Dependency analysis functionality for PyImportSync.

This module handles dependency analysis, package matching, and pipreqs integration
to identify missing or outdated dependencies.
"""

import re
import subprocess
from pathlib import Path
from typing import Set, Dict, List, Tuple

from .utils import get_known_import_mappings, normalize_package_name


class DependencyAnalyzer:
    """Analyzes dependencies and matches imports to packages."""
    
    def __init__(self, project_root: Path, requirements_file: str):
        """Initialize dependency analyzer."""
        self.project_root = project_root
        self.requirements_file = requirements_file
        self.known_mappings = get_known_import_mappings()
        self.package_metadata_mappings = self._get_package_metadata_mappings()
    
    def get_requirements_packages(self) -> Set[str]:
        """Parse requirements.txt and extract package names."""
        packages = set()
        requirements_path = self.project_root / self.requirements_file
        
        if not requirements_path.exists():
            return packages
        
        try:
            with open(requirements_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    
                    # Skip empty lines and comments
                    if not line or line.startswith('#'):
                        continue
                    
                    # Extract package name (handle version specifiers)
                    match = re.match(r'^([a-zA-Z0-9_.-]+)', line)
                    if match:
                        packages.add(match.group(1))
        
        except OSError as e:
            print(f"Error reading requirements file: {e}")
        
        return packages
    
    def run_pipreqs(self, use_pipreqs: bool = True) -> List[str]:
        """Run pipreqs to detect dependencies."""
        if not use_pipreqs:
            return []
        
        try:
            # Run pipreqs on the project directory
            result = subprocess.run([
                'pipreqs', str(self.project_root), '--print'
            ], capture_output=True, text=True, check=True)
            
            # Parse pipreqs output
            packages = []
            for line in result.stdout.strip().split('\\n'):
                if line and not line.startswith('#'):
                    packages.append(line)
            
            return packages
            
        except subprocess.CalledProcessError:
            print("Warning: pipreqs failed to run")
            return []
        except FileNotFoundError:
            print("Warning: pipreqs not found")
            return []
    
    def analyze_dependencies(self, imports: Set[str], use_pipreqs: bool = True) -> Dict[str, List[str]]:
        """Analyze dependencies and return missing/matched packages."""
        requirements_packages = self.get_requirements_packages()
        pipreqs_packages = self.run_pipreqs(use_pipreqs)
        
        # Enhanced package matching
        matched_packages = []
        missing_packages = []
        
        for import_name in imports:
            package_name = self._enhanced_package_matching(import_name)
            
            if package_name:
                # Check if package is in requirements
                normalized_requirements = {normalize_package_name(pkg) for pkg in requirements_packages}
                
                if normalize_package_name(package_name) in normalized_requirements:
                    matched_packages.append(f"{import_name} → {package_name}")
                else:
                    missing_packages.append(package_name)
        
        return {
            'missing': missing_packages,
            'matched': matched_packages,
            'pipreqs': pipreqs_packages,
            'requirements_count': len(requirements_packages),
            'imports_count': len(imports),
            'metadata_mappings_count': len(self.package_metadata_mappings)
        }
    
    def _enhanced_package_matching(self, import_name: str) -> str:
        """Enhanced package name matching using multiple strategies."""
        # Strategy 1: Check known mappings first
        if import_name in self.known_mappings:
            return self.known_mappings[import_name]
        
        # Strategy 2: Check package metadata mappings
        if import_name in self.package_metadata_mappings:
            return self.package_metadata_mappings[import_name]
        
        # Strategy 3: Direct name match (most common case)
        return import_name
    
    def _get_package_metadata_mappings(self) -> Dict[str, str]:
        """Get package metadata mappings from installed packages."""
        mappings = {}
        
        try:
            # Try to get installed packages and their top-level modules
            import pkg_resources
            
            for dist in pkg_resources.working_set:
                package_name = dist.project_name
                
                # Try to get top-level modules from metadata
                try:
                    if dist.has_metadata('top_level.txt'):
                        top_levels = dist.get_metadata('top_level.txt').strip().split('\\n')
                        for top_level in top_levels:
                            if top_level:
                                mappings[top_level] = package_name
                except Exception:
                    pass
                
                # Fallback: use package name as potential import name
                normalized_name = package_name.replace('-', '_').replace('.', '_')
                mappings[normalized_name] = package_name
        
        except ImportError:
            # pkg_resources not available
            pass
        except Exception as e:
            print(f"Warning: Could not load package metadata: {e}")
        
        return mappings