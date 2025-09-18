"""
Caching functionality for PyImportSync.

This module handles file content caching to improve performance when analyzing
large codebases by avoiding re-parsing unchanged files.
"""

import json
import hashlib
import time
from pathlib import Path
from typing import Dict, Set, Optional


class FileCache:
    """Manages file content caching for import analysis."""
    
    def __init__(self, cache_file: str = '.pyimportsync_cache.json', enabled: bool = True):
        """Initialize cache with specified cache file."""
        self.cache_file = Path(cache_file)
        self.enabled = enabled
        self.cache_data: Dict[str, Dict] = {}
        self._load_cache()
    
    def _load_cache(self) -> Dict[str, Dict]:
        """Load cache from file if it exists."""
        if not self.enabled:
            return {}
            
        if self.cache_file.exists():
            try:
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    self.cache_data = json.load(f)
                return self.cache_data
            except (json.JSONDecodeError, OSError):
                # If cache is corrupted, start fresh
                self.cache_data = {}
        else:
            self.cache_data = {}
        
        return self.cache_data
    
    def save_cache(self):
        """Save current cache to file."""
        if not self.enabled:
            return
            
        try:
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(self.cache_data, f, indent=2)
        except OSError as e:
            print(f"Warning: Could not save cache: {e}")
    
    def get_file_hash(self, filepath: Path) -> str:
        """Get MD5 hash of file content."""
        try:
            with open(filepath, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except OSError:
            return ""
    
    def is_file_cached(self, filepath: Path) -> bool:
        """Check if file is cached and up-to-date."""
        if not self.enabled:
            return False
            
        file_key = str(filepath)
        if file_key not in self.cache_data:
            return False
        
        cached_entry = self.cache_data[file_key]
        current_hash = self.get_file_hash(filepath)
        
        return (
            current_hash and 
            cached_entry.get('hash') == current_hash and
            'imports' in cached_entry
        )
    
    def get_cached_imports(self, filepath: Path) -> Set[str]:
        """Get cached imports for a file."""
        if not self.enabled:
            return set()
            
        file_key = str(filepath)
        if file_key in self.cache_data:
            imports = self.cache_data[file_key].get('imports', [])
            return set(imports)
        return set()
    
    def cache_file_imports(self, filepath: Path, imports: Set[str]):
        """Cache imports for a file with current hash and timestamp."""
        if not self.enabled:
            return
            
        file_key = str(filepath)
        self.cache_data[file_key] = {
            'hash': self.get_file_hash(filepath),
            'imports': list(imports),
            'timestamp': time.time()
        }
    
    def clear_cache(self):
        """Clear all cache data."""
        self.cache_data = {}
        if self.cache_file.exists():
            try:
                self.cache_file.unlink()
            except OSError:
                pass
    
    def get_cache_stats(self) -> Dict[str, int]:
        """Get cache statistics."""
        return {
            'total_files': len(self.cache_data),
            'cache_size_bytes': self.cache_file.stat().st_size if self.cache_file.exists() else 0
        }