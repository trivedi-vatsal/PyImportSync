"""
Gitignore pattern handling for PyImportSync.

This module handles .gitignore pattern parsing and file filtering using pathspec
when available, with fallback to basic pattern matching.
"""

import fnmatch
from pathlib import Path
from typing import List, Optional

# Optional pathspec support
try:
    import pathspec
    HAS_PATHSPEC = True
except ImportError:
    HAS_PATHSPEC = False


class GitignoreHandler:
    """Handles gitignore pattern matching and file filtering."""
    
    def __init__(self, project_root: Path, use_pathspec: bool = True):
        """Initialize gitignore handler."""
        self.project_root = project_root
        self.use_pathspec = use_pathspec and HAS_PATHSPEC
        self.patterns = self._load_gitignore_patterns()
        self.pathspec_matcher = self._create_pathspec_matcher()
    
    def _load_gitignore_patterns(self) -> List[str]:
        """Load patterns from .gitignore file."""
        gitignore_file = self.project_root / '.gitignore'
        patterns = []
        
        if gitignore_file.exists():
            try:
                with open(gitignore_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        # Skip empty lines and comments
                        if line and not line.startswith('#'):
                            patterns.append(line)
            except OSError as e:
                print(f"Warning: Could not read .gitignore: {e}")
        
        return patterns
    
    def _create_pathspec_matcher(self):
        """Create pathspec matcher if available."""
        if not self.use_pathspec:
            return None
        
        try:
            return pathspec.PathSpec.from_lines('gitwildmatch', self.patterns)
        except Exception as e:
            print(f"Warning: Could not create pathspec matcher: {e}")
            return None
    
    def is_ignored(self, path: Path) -> bool:
        """Check if a path should be ignored based on gitignore patterns."""
        if self.use_pathspec and self.pathspec_matcher:
            return self._is_ignored_by_pathspec(path)
        else:
            return self._is_ignored_by_fnmatch(path)
    
    def _is_ignored_by_pathspec(self, path: Path) -> bool:
        """Check if path is ignored using pathspec (more accurate)."""
        if not self.pathspec_matcher:
            return False
        
        try:
            # Convert to relative path from project root
            if path.is_absolute():
                rel_path = path.relative_to(self.project_root)
            else:
                rel_path = path
            
            # Use forward slashes for pathspec (works on all platforms)
            path_str = str(rel_path).replace('\\', '/')
            
            return self.pathspec_matcher.match_file(path_str)
        except (ValueError, OSError):
            return False
    
    def _is_ignored_by_fnmatch(self, path: Path) -> bool:
        """Check if path is ignored using basic fnmatch patterns."""
        try:
            # Convert to relative path from project root
            if path.is_absolute():
                rel_path = path.relative_to(self.project_root)
            else:
                rel_path = path
            
            path_str = str(rel_path)
            
            for pattern in self.patterns:
                # Simple pattern matching - not as sophisticated as git
                if fnmatch.fnmatch(path_str, pattern):
                    return True
                # Check if any parent directory matches
                for parent in rel_path.parents:
                    if fnmatch.fnmatch(str(parent), pattern):
                        return True
        except (ValueError, OSError):
            pass
        
        return False
    
    def get_pattern_count(self) -> int:
        """Get number of loaded gitignore patterns."""
        return len(self.patterns)
    
    def has_pathspec_support(self) -> bool:
        """Check if pathspec is available and being used."""
        return self.use_pathspec and HAS_PATHSPEC