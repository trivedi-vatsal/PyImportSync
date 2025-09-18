"""
Utility functions for PyImportSync.

This module contains core utility functions including standard library detection,
configuration loading, and common helper functions.
"""

import sys
import json
from pathlib import Path
from typing import Set, Dict, Optional


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
    }


def normalize_package_name(name: str) -> str:
    """Normalize package name for comparison."""
    # Convert to lowercase and replace underscores/hyphens
    return name.lower().replace("_", "-").replace(".", "-")


def is_local_module(import_name: str, project_root: Path) -> bool:
    """Check if an import is a local module within the project."""
    # Check for relative imports
    if import_name.startswith("."):
        return True

    # Check if there's a corresponding file/directory in the project
    potential_paths = [
        project_root / f"{import_name}.py",
        project_root / import_name / "__init__.py",
        project_root / "src" / f"{import_name}.py",
        project_root / "src" / import_name / "__init__.py",
    ]

    return any(path.exists() for path in potential_paths)
