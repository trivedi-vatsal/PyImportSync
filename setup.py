#!/usr/bin/env python3
"""
Setup configuration for PyImportSync package.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file for long description
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

# Read version from __init__.py
def get_version():
    version_file = this_directory / "src" / "pyimportsync" / "__init__.py"
    with open(version_file) as f:
        for line in f:
            if line.startswith("__version__"):
                return line.split("=")[1].strip().strip('"').strip("'")
    return "1.0.0"

setup(
    name="pyimportsync",
    version=get_version(),
    author="trivedi-vatsal",
    author_email="",
    description="Python Import & Requirements Synchronizer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/trivedi-vatsal/PyImportSync",
    project_urls={
        "Bug Tracker": "https://github.com/trivedi-vatsal/PyImportSync/issues",
        "Documentation": "https://github.com/trivedi-vatsal/PyImportSync/blob/main/README.md",
        "Source Code": "https://github.com/trivedi-vatsal/PyImportSync",
    },
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Quality Assurance",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "gitpython",
        "pathspec",
        "pipreqs",
        "colorama",
    ],
    extras_require={
        "dev": [
            "pytest",
            "pytest-cov",
            "black",
            "flake8",
            "mypy",
        ],
    },
    entry_points={
        "console_scripts": [
            "pyimportsync=pyimportsync.main:run",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)