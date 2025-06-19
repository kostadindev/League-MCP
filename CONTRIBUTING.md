# Contributing to League MCP

We love your input! We want to make contributing to League MCP as easy and transparent as possible, whether it's:

- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features
- Becoming a maintainer

## Development Process

We use GitHub to host code, to track issues and feature requests, as well as accept pull requests.

## Pull Requests

Pull requests are the best way to propose changes to the codebase. We actively welcome your pull requests:

1. Fork the repo and create your branch from `main`.
2. If you've added code that should be tested, add tests.
3. If you've changed APIs, update the documentation.
4. Ensure the test suite passes.
5. Make sure your code lints.
6. Issue that pull request!

## Any contributions you make will be under the MIT Software License

In short, when you submit code changes, your submissions are understood to be under the same [MIT License](LICENSE) that covers the project. Feel free to contact the maintainers if that's a concern.

## Report bugs using GitHub's [issue tracker](../../issues)

We use GitHub issues to track public bugs. Report a bug by [opening a new issue](../../issues/new); it's that easy!

**Great Bug Reports** tend to have:

- A quick summary and/or background
- Steps to reproduce
  - Be specific!
  - Give sample code if you can
- What you expected would happen
- What actually happens
- Notes (possibly including why you think this might be happening, or stuff you tried that didn't work)

## Feature Requests

We welcome feature requests! Please:

1. Check if the feature already exists
2. Open an issue with the "enhancement" label
3. Describe the feature and its use case
4. Be open to discussion and feedback

## Development Setup

1. Fork and clone the repository
2. Install dependencies:
   ```bash
   # For MCP Server
   cd mcp-server
   uv sync  # or pip install -r requirements.txt
   
   # For MCP Client  
   cd ../mcp-client
   uv sync  # or pip install -r requirements.txt
   ```
3. Set up environment variables as described in README.md
4. Make your changes
5. Test your changes thoroughly

## Coding Standards

- Follow PEP 8 for Python code style
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and small
- Add type hints where appropriate

## Testing

- Write tests for new features
- Ensure all tests pass before submitting PR
- Include both unit tests and integration tests where appropriate

## Documentation

- Update README.md if you change installation, usage, or add features
- Add docstrings to new functions and classes
- Update API documentation for any API changes

## License

By contributing, you agree that your contributions will be licensed under its MIT License.

## Questions?

Feel free to open an issue for any questions about contributing! 