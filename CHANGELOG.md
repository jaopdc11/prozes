# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Docker integration
- Database templates (PostgreSQL, MongoDB)
- Additional framework support (Django, Tornado, Sanic)

## [1.1.1] - 2025-02-03

### Changed
- Main help text (`prozes --help`) now displays all common options
- Improved discoverability of --venv, --git, --auth, --install-deps, --python-version, --verbose flags
- Applied to all 5 languages (en, pt, es, it, fr)

## [1.1.0] - 2025-02-03

### Added

#### Authentication System
- **JWT Authentication**: Token-based authentication with access/refresh tokens
  - Automatic token generation and validation
  - Password hashing with bcrypt
  - In-memory user storage for quick development
  - Ready-to-use login, register, and protected routes
- **OAuth2 Authentication**: Third-party authentication support
  - Pre-configured OAuth flow with authlib
  - Google, GitHub provider examples
  - State management and token handling
- **Session Authentication**: Traditional session-based auth
  - Cookie-based sessions with Flask-Session
  - HTTPOnly and Secure flags for production
  - Session storage configuration
- **Basic Authentication**: HTTP Basic Auth implementation
  - Simple username/password authentication
  - Flask-HTTPAuth and FastAPI HTTPBasic support
- Authentication available via `--auth` flag for all architectures (MVC, API, Clean)
- Complete test suites for all auth types

#### Internationalization
- **3 New Languages**: Spanish (es), Italian (it), French (fr)
- **Language Configuration**: `prozes config --lang <code>` command
- All CLI messages and prompts translated
- Language persistence in user config (~/.prozes/config)

#### Update Checker
- **Automatic Update Detection**: Checks PyPI for new versions before project creation
- **Smart Caching**: Daily cache to avoid excessive checks (respects user bandwidth)
- **Multilingual Prompts**: Update notifications in all 5 supported languages
- **Auto-Update Option**: One-click update via pip from within prozes
- **Configurable**: Can skip check or force check with verbose mode

#### Custom Template System
- **Save Projects as Templates**: `prozes template save <path> <name>` to create reusable templates
- **Use Custom Templates**: `prozes template use <name> <project>` to generate from templates
- **Template Management**: List, show details, and delete custom templates
- **Variable Detection**: Automatic detection and substitution of template variables
- **Metadata Support**: Description, author, version tracking for templates
- **Template Validation**: Name validation and conflict detection
- Complete test suite with integration tests

#### Testing
- 30 new tests for update checker (20 unit + 10 integration)
- 7 new tests for authentication generation
- All tests passing (197 total)

### Changed
- Updated dependency management to support auth libraries
- Enhanced `.env.example` templates with auth configuration
- Improved error handling and validation
- Main help text now displays all common options (--venv, --git, --auth, etc.)
- README updated to show all 5 supported languages

### Fixed
- Version number consistency across all modules
- UTF-8 encoding in requirements.txt generation
- Bcrypt compatibility (pinned to <5.0.0)
- Email validation in FastAPI with pydantic[email]
- Simplified setup.py to avoid build issues (all config in pyproject.toml)

## [1.0.0] - 2025-02-03

### Added

#### Core Features
- MVC architecture generator with Flask and FastAPI support
- REST API generator with Flask and FastAPI support
- CLI application generator with Click framework
- Clean Architecture generator with dependency injection examples
- Virtual environment creation (`--venv`)
- Git repository initialization (`--git`)
- Automatic dependency installation (`--install-deps`)
- Internationalization support (English and Portuguese)
- Rich terminal output with progress indicators

#### Generated Project Features
- **Environment Variables**: `.env.example` template in all projects
- **Development Dependencies**: Separate `requirements-dev.txt` with pytest, black, ruff
- **Real Tests**: Actual test cases instead of placeholders
  - Flask: Tests for routes and application
  - FastAPI: Tests with TestClient
  - CLI: Tests with Click runner
  - Clean Architecture: Tests for use cases and entities
- **Logging Configuration**: Pre-configured logging setup in `config/logging.py`
- **Pytest Configuration**: `pyproject.toml` with pytest settings
- **CI/CD**: GitHub Actions workflow for automated testing
- **Enhanced READMEs**: Setup instructions, usage examples, and test commands

#### Developer Experience
- Comprehensive test suite (125 tests)
- Pre-commit hooks configuration
- CI/CD with GitHub Actions (test, lint, release)
- Type checking with mypy
- Code formatting with Black
- Linting with Ruff

### Documentation
- Complete README with examples and usage guides
- CHANGELOG following Keep a Changelog format
- SECURITY policy for vulnerability reporting
- Contributing guidelines
- Development setup instructions
- Architecture documentation
- Issue and PR templates
- Roadmap for future features

[Unreleased]: https://github.com/jaopdc11/prozes/compare/v1.1.1...HEAD
[1.1.1]: https://github.com/jaopdc11/prozes/compare/v1.1.0...v1.1.1
[1.1.0]: https://github.com/jaopdc11/prozes/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/jaopdc11/prozes/releases/tag/v1.0.0
