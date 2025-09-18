"""
Utility functions for PyImportSync.

This module contains core utility functions including standard library detection,
configuration loading, and common helper functions.
"""

import sys
import json
import re
from pathlib import Path
from typing import Set, Dict, Optional, List


def get_dynamic_stdlib_modules() -> Set[str]:
    """Get standard library modules dynamically for current Python version."""
    if sys.version_info >= (3, 10):
        # Use built-in sys.stdlib_module_names for Python 3.10+
        return set(sys.stdlib_module_names)
    else:
        # Fallback for older Python versions
        return {
            "__future__",
            "_thread",
            "abc",
            "aifc",
            "argparse",
            "array",
            "ast",
            "asynchat",
            "asyncio",
            "asyncore",
            "atexit",
            "audioop",
            "base64",
            "bdb",
            "binascii",
            "binhex",
            "bisect",
            "builtins",
            "bz2",
            "calendar",
            "cgi",
            "cgitb",
            "chunk",
            "cmath",
            "cmd",
            "code",
            "codecs",
            "codeop",
            "collections",
            "colorsys",
            "compileall",
            "concurrent",
            "configparser",
            "contextlib",
            "copy",
            "copyreg",
            "cProfile",
            "csv",
            "ctypes",
            "curses",
            "datetime",
            "dbm",
            "decimal",
            "difflib",
            "dis",
            "distutils",
            "doctest",
            "email",
            "encodings",
            "ensurepip",
            "enum",
            "errno",
            "faulthandler",
            "fcntl",
            "filecmp",
            "fileinput",
            "fnmatch",
            "formatter",
            "fractions",
            "ftplib",
            "functools",
            "gc",
            "getopt",
            "getpass",
            "gettext",
            "glob",
            "grp",
            "gzip",
            "hashlib",
            "heapq",
            "hmac",
            "html",
            "http",
            "imaplib",
            "imghdr",
            "imp",
            "importlib",
            "inspect",
            "io",
            "ipaddress",
            "itertools",
            "json",
            "keyword",
            "lib2to3",
            "linecache",
            "locale",
            "logging",
            "lzma",
            "mailbox",
            "mailcap",
            "marshal",
            "math",
            "mimetypes",
            "mmap",
            "modulefinder",
            "multiprocessing",
            "netrc",
            "nntplib",
            "numbers",
            "operator",
            "optparse",
            "os",
            "pathlib",
            "pdb",
            "pickle",
            "pickletools",
            "pipes",
            "pkgutil",
            "platform",
            "plistlib",
            "poplib",
            "posix",
            "pprint",
            "profile",
            "pstats",
            "pty",
            "pwd",
            "py_compile",
            "pyclbr",
            "pydoc",
            "queue",
            "quopri",
            "random",
            "re",
            "readline",
            "reprlib",
            "resource",
            "rlcompleter",
            "runpy",
            "sched",
            "secrets",
            "select",
            "selectors",
            "shelve",
            "shlex",
            "shutil",
            "signal",
            "site",
            "smtpd",
            "smtplib",
            "sndhdr",
            "socket",
            "socketserver",
            "sqlite3",
            "ssl",
            "stat",
            "statistics",
            "string",
            "stringprep",
            "struct",
            "subprocess",
            "sunau",
            "symbol",
            "symtable",
            "sys",
            "sysconfig",
            "tabnanny",
            "tarfile",
            "telnetlib",
            "tempfile",
            "termios",
            "textwrap",
            "threading",
            "time",
            "timeit",
            "tkinter",
            "token",
            "tokenize",
            "trace",
            "traceback",
            "tracemalloc",
            "tty",
            "turtle",
            "turtledemo",
            "types",
            "typing",
            "unicodedata",
            "unittest",
            "urllib",
            "uu",
            "uuid",
            "venv",
            "warnings",
            "wave",
            "weakref",
            "webbrowser",
            "winreg",
            "winsound",
            "wsgiref",
            "xdrlib",
            "xml",
            "xmlrpc",
            "zipapp",
            "zipfile",
            "zipimport",
            "zlib",
        }


def load_config(config_file: Optional[str], config: Optional[Dict]) -> Dict:
    """Load configuration from file or dictionary with defaults."""
    default_config = {
        "ignore_dirs": [
            ".git",
            ".pytest_cache",
            ".venv",
            "__pycache__",
            "build",
            "dist",
            "docs",
            "env",
            "examples",
            "node_modules",
            "static",
            "tests",
            "venv",
        ],
        "requirements_file": "requirements.txt",
        "enable_cache": True,
        "cache_file": ".pyimportsync_cache.json",
        "use_pathspec": True,
        # New configuration option for skipping specific import names
        "skip_imports": [
            # Common internal module names that should be skipped
            # Users can add their own app names here
        ],
    }

    # If explicit config provided, merge with defaults
    if config:
        default_config.update(config)
        return default_config

    # Try to load from config file
    if config_file and Path(config_file).exists():
        try:
            with open(config_file, "r", encoding="utf-8") as f:
                file_config = json.load(f)
            default_config.update(file_config)
        except (json.JSONDecodeError, OSError) as e:
            print(f"Warning: Could not load config file {config_file}: {e}")

    return default_config


def get_known_import_mappings() -> Dict[str, str]:
    """Get known mappings from import names to package names."""
    return {
        "cv2": "opencv-python",
        "PIL": "Pillow",
        "yaml": "PyYAML",
        "dateutil": "python-dateutil",
        "sklearn": "scikit-learn",
        "skimage": "scikit-image",
        "bs4": "beautifulsoup4",
        "requests_oauthlib": "requests-oauthlib",
        "jwt": "PyJWT",
        "serial": "pyserial",
        "magic": "python-magic",
        "MySQLdb": "mysqlclient",
        "psycopg2": "psycopg2-binary",
        "OpenSSL": "pyOpenSSL",
        "Crypto": "pycrypto",
        "nacl": "PyNaCl",
        "lxml": "lxml",
        "dotenv": "python-dotenv",
        "google": "google-cloud",
        "azure": "azure",
        "boto3": "boto3",
        "tensorflow": "tensorflow",
        "torch": "torch",
        "transformers": "transformers",
        "datasets": "datasets",
        "accelerate": "accelerate",
        # Django-specific mappings
        "rest_framework": "djangorestframework",
        "django_extensions": "django-extensions",
        "django_debug_toolbar": "django-debug-toolbar",
        "django_cors_headers": "django-cors-headers",
        "django_filter": "django-filter",
    }


def normalize_package_name(name: str) -> str:
    """
    Normalize package name for comparison following PEP 508 standards.
    
    This function handles various edge cases:
    - Converts to lowercase
    - Replaces underscores, dots, and spaces with hyphens
    - Collapses multiple consecutive separators into single hyphens
    - Removes leading/trailing separators
    - Handles empty/whitespace-only strings
    
    Args:
        name: Package name to normalize
        
    Returns:
        Normalized package name in lowercase with standardized separators
    """
    if not name or not isinstance(name, str):
        return ""
    
    # Remove extra whitespace and convert to lowercase
    name = name.strip().lower()
    
    if not name:
        return ""
    
    # Step 1: Replace various separators with hyphens
    # Handle underscores, dots, spaces
    normalized = name.replace('_', '-').replace('.', '-').replace(' ', '-')
    
    # Step 2: Collapse multiple consecutive hyphens into single hyphens
    while '--' in normalized:
        normalized = normalized.replace('--', '-')
    
    # Step 3: Remove leading/trailing hyphens
    normalized = normalized.strip('-')
    
    return normalized


def is_local_module(import_name: str, project_root: Path) -> bool:
    """Check if an import is a local module within the project."""
    # Check for relative imports
    if import_name.startswith("."):
        return True

    # Check if there's a corresponding file/directory in the project
    potential_paths = [
        # Standard Python module patterns
        project_root / f"{import_name}.py",
        project_root / import_name / "__init__.py",
        
        # Source directory patterns (common in many projects)
        project_root / "src" / f"{import_name}.py",
        project_root / "src" / import_name / "__init__.py",
        
        # Common app directory patterns
        project_root / "apps" / import_name / "__init__.py",
    ]

    # Direct path check - if the module exists as a directory/file, it's local
    return any(path.exists() for path in potential_paths)


def should_skip_import(import_name: str, skip_imports: List[str]) -> bool:
    """Check if an import should be skipped based on configuration."""
    return import_name in skip_imports


def create_config_template() -> int:
    """Create a pyimportsync-config.json template file."""
    config_template = {
        "_comment": "PyImportSync configuration file",
        "_documentation": "https://github.com/trivedi-vatsal/PyImportSync/blob/main/docs/configuration.md",
        
        "ignore_dirs": [
            "__pycache__",
            ".git", 
            ".venv",
            "venv",
            "env",
            "tests",
            "docs",
            "examples", 
            "build",
            "dist",
            "node_modules",
            ".pytest_cache"
        ],
        
        "requirements_file": "requirements.txt",
        "enable_cache": True,
        "use_pathspec": True,
        
        "_skip_imports_explanation": "List import names that should be ignored (internal modules, app names, etc.)",
        "_skip_imports_examples": {
            "django_projects": ["users", "blog", "accounts", "core", "api", "models", "views", "utils", "forms"],
            "flask_projects": ["blueprints", "models", "views", "utils", "forms", "auth"],
            "general_projects": ["config", "utils", "helpers", "constants", "exceptions"]
        },
        
        "skip_imports": [
            
        ]
    }
    
    config_file = Path("pyimportsync-config.json")
    
    if config_file.exists():
        print(f"⚠️  Configuration file '{config_file}' already exists.")
        response = input("Do you want to overwrite it? (y/N): ").strip().lower()
        if response not in ['y', 'yes']:
            print("Configuration file creation cancelled.")
            return 0
    
    try:
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config_template, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Configuration template created: {config_file}")
        print("📝 Edit the file to customize settings for your project.")
        print("🔧 Use --config-file pyimportsync-config.json to use this configuration.")
        return 0
        
    except Exception as e:
        print(f"❌ Error creating configuration file: {e}")
        return 1
