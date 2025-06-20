# Development Guide

## Package Development

This guide covers developing and maintaining the `league-mcp` Python package.

## Setup Development Environment

1. Clone the repository:
   ```bash
   git clone https://github.com/kostadindevLeague-of-Legends-MCP.git
   cd League-of-Legends-MCP/mcp-server
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install in development mode:
   ```bash
   pip install -e .
   ```

4. Install development dependencies:
   ```bash
   pip install -e .[dev]
   ```

## Building the Package

1. Install build tools:
   ```bash
   pip install build
   ```

2. Build the package:
   ```bash
   python -m build
   ```

This creates both a wheel (`.whl`) and source distribution (`.tar.gz`) in the `dist/` directory.

## Testing the Package

1. Install the built package in a fresh environment:
   ```bash
   pip install dist/league_mcp-0.1.0-py3-none-any.whl
   ```

2. Test the console script:
   ```bash
   league-mcp --help
   ```

3. Run the server:
   ```bash
   league-mcp --transport stdio
   ```

## Publishing

### Test PyPI (Recommended first)

1. Install twine:
   ```bash
   pip install twine
   ```

2. Upload to Test PyPI:
   ```bash
   twine upload --repository testpypi dist/*
   ```

3. Test installation from Test PyPI:
   ```bash
   pip install --index-url https://test.pypi.org/simple/ league-mcp
   ```

### Production PyPI

1. Upload to PyPI:
   ```bash
   twine upload dist/*
   ```

## Package Structure

```
mcp-server/
├── __init__.py              # Package initialization
├── main.py                  # Main entry point
├── setup.py                 # Compatibility setup script
├── pyproject.toml           # Modern Python package configuration
├── MANIFEST.in              # Package file inclusion rules
├── LICENSE                  # License file
├── README.md                # Package documentation
├── requirements.txt         # Dependencies (legacy)
├── primitives/              # MCP primitives
├── services/                # Business logic
└── utils/                   # Helper functions
```

## Console Script

The package provides a console script `league-mcp` that points to `main:main`. This allows users to run:

```bash
league-mcp [--transport {stdio,sse}]
```

Instead of:

```bash
python main.py [--transport {stdio,sse}]
```

## Version Management

Update the version in:
- `pyproject.toml` (main version)
- `__init__.py` (package version)

## Dependencies

- Runtime dependencies are specified in `pyproject.toml` under `dependencies`
- Development dependencies are in `optional-dependencies.dev`
- Keep `requirements.txt` for legacy compatibility 