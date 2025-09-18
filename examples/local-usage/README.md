# Local usage examples

This directory contains examples of how to use the dependency checker locally.

## Sample Project

The `sample-project/` directory contains a minimal Python project that demonstrates:

- A `requirements.txt` file with declared dependencies
- A Python script that imports both standard library and third-party packages
- Example of how the dependency checker would work on a real project

## Running the checker locally

From the sample project directory:

```bash
# Basic check
python ../../../src/check_dependencies.py

# Check with custom arguments
python ../../../src/check_dependencies.py --quiet --output missing.txt

# Check specific requirements file
python ../../../src/check_dependencies.py --requirements-file requirements-dev.txt
```

## Expected output

When run on the sample project, the dependency checker should find all dependencies satisfied (assuming the commented numpy import is not uncommented).

If you uncomment the numpy import in `main.py`, the checker should detect it as a missing dependency
