# Contributing to Prozees

Thank you for your interest in contributing to Prozees! This document provides guidelines and instructions for contributing.

## Development Setup

### Prerequisites

- Python 3.8 or higher
- Git
- pip

### Setting Up Your Development Environment

1. **Clone the repository:**

   ```bash
   git clone https://github.com/jaopdc11/prozes.git
   cd prozes
   ```

2. **Create a virtual environment:**

   ```bash
   python -m venv venv

   # On Windows
   venv\Scripts\activate

   # On Linux/Mac
   source venv/bin/activate
   ```

3. **Install in development mode with dev dependencies:**

   ```bash
   pip install -e ".[dev]"
   ```

4. **Install pre-commit hooks:**

   ```bash
   pre-commit install
   ```

## Running Tests

### Run all tests

```bash
pytest
```

### Run tests with coverage

```bash
pytest --cov=prozes --cov-report=html
```

The coverage report will be generated in `htmlcov/index.html`.

### Run specific test files

```bash
pytest tests/test_core.py
pytest tests/test_validation.py
pytest tests/test_modules/
```

### Run tests with verbose output

```bash
pytest -v
```

## Code Quality

### Formatting

We use Black for code formatting:

```bash
black prozes tests
```

### Linting

We use Ruff for linting:

```bash
ruff check prozes tests
ruff check --fix prozes tests  # Auto-fix issues
```

### Type Checking

We use mypy for type checking:

```bash
mypy prozes
```

### Run All Checks

Pre-commit will run all checks:

```bash
pre-commit run --all-files
```

## Project Structure

```
prozes/
├── prozes/                  # Main package
│   ├── __init__.py
│   ├── core.py              # CLI commands and entry point
│   └── modules/             # Internal modules
│       ├── console.py       # Rich console output
│       ├── dirs.py          # Directory operations
│       ├── i18n.py          # Internationalization
│       ├── install.py       # Requirements templates
│       ├── structures.py    # Project structure generators
│       ├── validation.py    # Input validation
│       └── venv.py          # Virtual environment handling
├── tests/                   # Test suite
│   ├── conftest.py          # Shared fixtures
│   ├── test_core.py         # CLI tests
│   ├── test_validation.py   # Validation tests
│   └── test_modules/        # Module-specific tests
├── .github/workflows/       # CI/CD pipelines
├── pyproject.toml           # Project configuration
└── README.md
```

## Contribution Workflow

1. **Create a new branch:**

   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** and ensure:
   - Tests pass: `pytest`
   - Code is formatted: `black prozes tests`
   - No lint errors: `ruff check prozes tests`
   - Types are correct: `mypy prozes`

3. **Commit your changes:**

   ```bash
   git add .
   git commit -m "Description of your changes"
   ```

   Pre-commit hooks will run automatically.

4. **Push and create a pull request:**

   ```bash
   git push origin feature/your-feature-name
   ```

   Then open a pull request on GitHub.

## Adding New Features

### Adding a New Architecture

1. Create templates in `prozes/modules/structures.py`
2. Add a `create_*_structure()` function
3. Add requirements template in `prozes/modules/install.py`
4. Create a new command in `prozes/core.py`
5. Add translations in `prozes/modules/i18n.py`
6. Write tests in `tests/`

### Adding New Translations

1. Add keys to both `en` and `pt` dictionaries in `prozes/modules/i18n.py`
2. Use the `t()` function to retrieve translations in code

## Reporting Issues

When reporting issues, please include:

- Python version (`python --version`)
- Operating system
- Prozees version (`prozes --version`)
- Steps to reproduce the issue
- Expected vs actual behavior

## Code Style Guidelines

- Follow PEP 8 (enforced by Black and Ruff)
- Write docstrings for all public functions
- Keep functions focused and small
- Use type hints where appropriate
- Write tests for new features

## License

By contributing to Prozees, you agree that your contributions will be licensed under the MIT License.
