<div align="center">

<img src="assets/logo.svg" alt="Prozes Logo" width="200"/>

# Prozes

**Professional Python Project Generator**

A powerful CLI tool for scaffolding production-ready Python applications.
Stop wasting time on boilerplate. Start building features from day one.

[![Tests](https://github.com/jaopdc11/prozes/actions/workflows/test.yml/badge.svg)](https://github.com/jaopdc11/prozes/actions/workflows/test.yml)
[![Lint](https://github.com/jaopdc11/prozes/actions/workflows/lint.yml/badge.svg)](https://github.com/jaopdc11/prozes/actions/workflows/lint.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![PyPI version](https://badge.fury.io/py/prozes.svg)](https://badge.fury.io/py/prozes)

[Installation](#installation) • [Quick Start](#quick-start) • [Documentation](#documentation) • [Examples](#examples) • [Contributing](#contributing)

</div>

---

## Overview

**Prozes** is a command-line project generator that creates production-ready Python applications with enterprise-grade architectures. Whether you're building a web application, REST API, CLI tool, or following Clean Architecture principles, Prozes provides the scaffolding you need to start coding immediately.

**Type**: CLI Tool / Project Generator (not a framework or library)
**Usage**: Run `prozes` commands to generate project structures - no imports needed

### Why Prozes?

- **Battle-Tested Architectures**: MVC, REST API, CLI, and Clean Architecture patterns
- **Framework Agnostic**: Works with Flask, FastAPI, and more
- **Production-Ready**: Includes logging, environment variables, real tests, and CI/CD
- **Zero Configuration**: Sensible defaults that work out of the box
- **Best Practices Included**: Testing setup, linting, Git integration, and virtual environments
- **Bilingual Support**: Full internationalization (English and Portuguese)
- **Beautiful CLI**: Rich terminal output with progress indicators and helpful messages

---

## Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Key Features](#key-features)
- [Architecture Types](#architecture-types)
- [Authentication](#-authentication)
- [Custom Templates](#-custom-templates)
- [Usage](#usage)
- [Examples](#examples)
- [Configuration](#configuration)
- [Development](#development)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)

---

## Installation

### Via pip (Recommended)

```bash
pip install prozes
```

### From Source

```bash
git clone https://github.com/jaopdc11/prozes.git
cd prozes
pip install -e .
```

### Verify Installation

```bash
prozes --version  # Should show 1.0.0
prozes --help
```

---

## Quick Start

Get up and running in 30 seconds:

```bash
# Create a FastAPI REST API with JWT authentication
prozes api my_api --type fastapi --auth jwt --venv --git --install-deps

cd my_api
cp .env.example .env  # Configure your JWT_SECRET_KEY
source venv/bin/activate  # or venv\Scripts\activate on Windows
uvicorn main:app --reload
```

That's it! Your API is running at `http://localhost:8000` with:
- ✅ Auto-generated docs at `/docs`
- ✅ JWT authentication ready
- ✅ User registration and login endpoints
- ✅ Protected routes

### Other Quick Examples

```bash
# MVC web application with Flask and Session auth
prozes mvc blog --type web-flask --auth session --venv --git

# API with Basic authentication
prozes api internal --type fastapi --auth basic --venv --git

# Clean Architecture with OAuth2
prozes clean backend --type fastapi --auth oauth2 --venv --git
```

---

## Key Features

<table>
<tr>
<td width="50%">

**🏗️ Multiple Architectures**
- MVC (Model-View-Controller)
- REST API
- CLI Applications
- Clean Architecture

**⚡ Framework Support**
- Flask
- FastAPI
- Click (for CLI)

**🔧 Development Tools**
- Automatic virtual environment creation
- Git initialization
- Dependency installation
- Testing scaffolding

**🔐 Authentication**
- JWT (Token-based)
- Session (Cookie-based)
- Basic (HTTP Basic Auth)
- OAuth2 (Third-party)

</td>
<td width="50%">

**🌍 Internationalization**
- English (default)
- Portuguese (pt)
- Easily extensible

**📦 Production Ready**
- Environment variables (`.env.example`)
- Logging configuration
- Real test cases (not placeholders)
- Separate dev dependencies
- CI/CD with GitHub Actions
- Configuration management

**🎨 Developer Experience**
- Beautiful CLI with Rich library
- Progress indicators
- Colored output
- Verbose mode for debugging

</td>
</tr>
</table>

---

## Architecture Types

### 🌐 MVC (Model-View-Controller)

Perfect for web applications with server-side rendering.

```bash
prozes mvc my_webapp --type web-flask --venv --git
```

**Includes:**
- Separate concerns: Models, Views, Controllers
- Template engine setup
- Static files organization
- Configuration management

**Use cases:** Traditional web apps, admin panels, dashboards

---

### 🔌 REST API

Lean and focused API without frontend bloat.

```bash
prozes api my_api --type fastapi --venv --git
```

**Includes:**
- RESTful route structure
- Data models and schemas
- Request/response handling
- Auto-generated API documentation (FastAPI)

**Use cases:** Backend services, mobile app APIs, microservices

---

### 💻 CLI Application

Command-line tools using Click framework.

```bash
prozes cli my_tool --venv --git
```

**Includes:**
- Command structure
- Argument parsing
- Configuration handling
- Distribution setup (setup.py)

**Use cases:** DevOps tools, automation scripts, data processing

---

### 🏛️ Clean Architecture

Enterprise-grade architecture with clear separation of concerns.

```bash
prozes clean my_project --type fastapi --venv --git
```

**Includes:**
- Entities (Domain layer)
- Use Cases (Business logic)
- Adapters (Interfaces)
- Frameworks (External dependencies)

**Use cases:** Large applications, microservices, long-term projects

---

## Usage

### Command Syntax

```bash
prozes <architecture> <project_name> [options]
```

### Common Options

All commands support these options:

| Option | Description | Default |
|--------|-------------|---------|
| `--venv` | Create virtual environment | `false` |
| `--git` | Initialize Git repository | `false` |
| `--python-version` | Python version for venv | System default |
| `--install-deps` | Install dependencies | `false` |
| `--auth` | Authentication type (`none`, `jwt`, `session`, `basic`, `oauth2`) | `none` |
| `-v, --verbose` | Verbose output | `false` |
| `-L, --lang` | Language (`en`, `pt`, `es`, `it`, `fr`) | Config or `en` |

### Architecture-Specific Options

#### MVC & API Commands

```bash
-t, --type   Framework type (web-flask, web-fastapi, flask, fastapi)
```

#### Configuration Command

```bash
prozes config --lang pt           # Set default language
prozes config --show              # Show current configuration
```

### Generated Project Structure

#### MVC Project
```
my_webapp/
├── .github/
│   └── workflows/       # CI/CD pipelines
├── app/
│   ├── controllers/     # Request handlers
│   ├── models/          # Data models
│   ├── views/           # View logic
│   ├── templates/       # HTML templates
│   └── static/          # CSS, JS, images
├── config/
│   ├── __init__.py      # Configuration
│   └── logging.py       # Logging setup
├── tests/               # Test suite with real tests
├── main.py              # Entry point
├── requirements.txt     # Production dependencies
├── requirements-dev.txt # Development dependencies
├── pyproject.toml       # Pytest configuration
├── .env.example         # Environment variables template
└── .gitignore          # Git ignore rules
```

#### API Project
```
my_api/
├── .github/workflows/   # CI/CD pipelines
├── app/
│   ├── auth/            # Authentication (if --auth specified)
│   │   ├── models.py    # User model
│   │   ├── routes.py    # Auth endpoints
│   │   ├── utils.py     # Password hashing, tokens
│   │   ├── storage.py   # User storage
│   │   └── config.py    # Auth configuration
│   ├── models/          # Data models
│   └── routes/          # API endpoints
├── config/
│   ├── __init__.py      # Configuration
│   └── logging.py       # Logging setup
├── tests/
│   ├── auth/            # Auth tests (if --auth specified)
│   └── test_api.py      # API tests
├── main.py              # Entry point
├── requirements.txt     # Production dependencies (with auth deps)
├── requirements-dev.txt # Development dependencies
├── pyproject.toml       # Pytest configuration
└── .env.example         # Environment variables (with auth vars)
```

#### CLI Project
```
my_tool/
├── .github/workflows/   # CI/CD pipelines
├── my_tool/
│   ├── commands/        # CLI commands
│   └── main.py          # Entry point
├── tests/               # Test suite with Click runner tests
├── setup.py             # Distribution setup
├── pyproject.toml       # Project metadata + pytest config
├── requirements.txt     # Production dependencies
├── requirements-dev.txt # Development dependencies
└── .env.example         # Environment variables template
```

#### Clean Architecture Project
```
my_project/
├── .github/workflows/   # CI/CD pipelines
├── src/
│   ├── entities/        # Domain entities
│   ├── use_cases/       # Business logic
│   ├── adapters/        # Interfaces & repositories
│   └── frameworks/      # External dependencies
├── config/
│   ├── __init__.py      # Configuration
│   └── logging.py       # Logging setup
├── tests/
│   ├── unit/            # Unit tests for use cases
│   └── integration/     # Integration tests
├── main.py              # Entry point
├── requirements.txt     # Production dependencies
├── requirements-dev.txt # Development dependencies
├── pyproject.toml       # Pytest configuration
└── .env.example         # Environment variables template
```

---

## 🔐 Authentication

Prozes includes **production-ready authentication** support for all project types. Choose from 4 authentication strategies:

### JWT (JSON Web Tokens)

Token-based authentication with access and refresh tokens.

```bash
prozes api my_api --type fastapi --auth jwt --venv --install-deps
```

**Features:**
- Access tokens (30min expiration)
- Refresh tokens (7 days expiration)
- Stateless authentication
- Ideal for APIs and SPAs

**Endpoints:**
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login and get tokens
- `POST /auth/refresh` - Refresh access token
- `GET /auth/me` - Get current user (protected)
- `POST /auth/logout` - Logout

### Session Authentication

Cookie-based authentication with server-side sessions.

```bash
prozes mvc my_app --type web-flask --auth session --venv
```

**Features:**
- HTTPOnly cookies
- Server-side session storage
- 7 days expiration
- Ideal for traditional web apps

**Endpoints:**
- `POST /auth/register` - Register and create session
- `POST /auth/login` - Login and create session
- `GET /auth/me` - Get current user (protected)
- `POST /auth/logout` - Logout and destroy session

### Basic Authentication

Simple HTTP Basic Auth with username and password.

```bash
prozes api internal_api --type fastapi --auth basic --venv
```

**Features:**
- Username/password authentication
- WWW-Authenticate headers
- Simple and lightweight
- Ideal for internal APIs

**Endpoints:**
- `POST /auth/register` - Register new user
- `GET /auth/me` - Get current user (requires Basic Auth)

### OAuth2

Third-party authentication (Google, GitHub, etc).

```bash
prozes api oauth_app --type fastapi --auth oauth2 --venv
```

**Features:**
- OAuth2 flow integration
- Automatic user creation
- Support for multiple providers
- Ideal for social login

**Endpoints:**
- `GET /auth/login` - Redirect to OAuth provider
- `GET /auth/callback` - OAuth callback handler
- `GET /auth/me` - Get current user (protected)
- `POST /auth/logout` - Logout

### What You Get

All authentication types include:

✅ **User Model** - Ready-to-use User dataclass
✅ **Password Hashing** - Bcrypt with automatic salting
✅ **Storage** - In-memory storage (replace with DB for production)
✅ **Protected Routes** - Middleware/dependencies ready
✅ **Tests** - Comprehensive test suite
✅ **Environment Variables** - Pre-configured in `.env.example`
✅ **Auto Dependencies** - All packages auto-added to `requirements.txt`

### Quick Example

```bash
# 1. Create API with JWT auth
prozes api secure_api --type fastapi --auth jwt --venv --install-deps

# 2. Configure
cd secure_api
cp .env.example .env
# Edit .env and set JWT_SECRET_KEY

# 3. Run
uvicorn main:app --reload

# 4. Test
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","email":"admin@example.com","password":"secret123"}'

# 5. Access protected route
curl http://localhost:8000/auth/me \
  -H "Authorization: Bearer <your-token>"
```

### Security Features

- ✅ Bcrypt password hashing
- ✅ Automatic salt generation
- ✅ Token expiration (JWT)
- ✅ Session expiration
- ✅ HTTPOnly cookies (Session)
- ✅ User active status check
- ✅ Duplicate prevention

### Production Notes

⚠️ **Important:** Generated projects use in-memory storage for quick development. For production:

1. Replace `app/auth/storage.py` with database implementation
2. Use PostgreSQL, MongoDB, or your preferred database
3. Set strong secrets in `.env` (32+ characters)
4. Enable HTTPS
5. Consider rate limiting for auth endpoints

📚 **Documentation:**
- [Quick Start Guide](QUICK_START_AUTH.md)
- [Testing Guide](AUTH_TESTING_GUIDE.md)
- [Implementation Details](AUTH_IMPLEMENTATION.md)

---

## 📦 Custom Templates

Save any project as a reusable template and generate new projects from it.

### Save a Project as Template

```bash
# Save current project as template
prozes template save ./my_project my_template

# With description and author
prozes template save ./my_project my_template \
  --description "FastAPI microservice template" \
  --author "Your Name"
```

### Use a Custom Template

```bash
# Create project from template
prozes template use my_template new_project

# With variables
prozes template use my_template new_project \
  --var author="John Doe" \
  --var version="1.0.0"

# Interactive mode (prompts for variables)
prozes template use my_template new_project --interactive

# With common options
prozes template use my_template new_project --venv --git --install-deps
```

### Manage Templates

```bash
# List all templates
prozes template list

# Show template details
prozes template show my_template

# Show with file tree
prozes template show my_template --show-files

# Delete template
prozes template delete my_template
```

### Template Variables

Templates automatically detect and substitute variables:

- `{{project_name}}` - Replaced with new project name
- `{{date}}` - Current date (YYYY-MM-DD)
- `{{year}}` - Current year
- `{{author}}` - Author name (if provided)
- `{{custom_var}}` - Any custom variable you define

**Example:**
```python
# In template: app.py
APP_NAME = "{{project_name}}"
VERSION = "{{version}}"
AUTHOR = "{{author}}"
CREATED_ON = "{{date}}"

# After generation:
APP_NAME = "my_new_app"
VERSION = "1.0.0"
AUTHOR = "John Doe"
CREATED_ON = "2025-02-03"
```

### Template Storage

Templates are stored in `~/.prozes/templates/` with:
- `template.json` - Metadata (name, description, author, variables)
- Full project structure preserved
- Binary files supported (images, fonts, etc.)

---

## Examples

### 1. Blog Application (MVC + Flask)

Build a full-featured blog with Flask:

```bash
# Generate the project
prozes mvc blog --type web-flask --venv --git --install-deps -v

# Start development
cd blog
source venv/bin/activate  # Windows: venv\Scripts\activate
python main.py

# Visit http://localhost:5000
```

**What you get:**
- MVC structure with controllers, models, and views
- Template system ready
- Static files organized
- Development server configured
- Real tests for routes and application
- Logging configured
- CI/CD pipeline ready

---

### 2. User Management API with Authentication (FastAPI)

Create a modern API with auth and auto-generated documentation:

```bash
# Generate the project with JWT authentication
prozes api user_service --type fastapi --auth jwt --venv --git --install-deps

# Configure
cd user_service
cp .env.example .env
# Edit .env and set JWT_SECRET_KEY

# Start the server
source venv/bin/activate
uvicorn main:app --reload

# Interactive docs at http://localhost:8000/docs
```

**What you get:**
- RESTful endpoints structure
- **Complete JWT authentication system**
- **User registration and login**
- **Protected routes with token validation**
- Pydantic models for validation
- Automatic OpenAPI documentation (FastAPI)
- Real API tests with test client (including auth tests)
- Health check endpoint
- Logging configured
- CI/CD pipeline ready

---

### 3. DevOps CLI Tool

Build a distributable command-line tool:

```bash
# Generate the project
prozes cli devops-tools --venv --git --install-deps

# Install in development mode
cd devops-tools
pip install -e .

# Use your CLI
devops-tools --help
devops-tools deploy --env production
```

**What you get:**
- Click framework integrated
- Command structure ready
- Configuration management
- Package ready for PyPI
- Tests with Click runner
- CI/CD pipeline ready

---

### 4. Microservice (Clean Architecture + FastAPI)

Enterprise-grade microservice with Clean Architecture:

```bash
# Generate the project
prozes clean payment-service --type fastapi --venv --git --install-deps

# Run tests
cd payment-service
pytest tests/ -v

# Start the service
uvicorn main:app --reload
```

**What you get:**
- Separated layers (entities, use cases, adapters, frameworks)
- Dependency injection examples
- Testability built-in (unit + integration tests)
- Dependency inversion principle applied
- Repository pattern implemented
- Ready for complex business logic

---

## Configuration

### Global Configuration

Set your preferences globally:

```bash
# Set default language to Portuguese
prozes config --lang pt

# View current configuration
prozes config --show
```

### Per-Project Configuration

Each generated project includes:
- `config/` directory for environment-specific settings
- `.env.example` for environment variables (where applicable)
- `requirements.txt` with pinned dependencies

---

## Documentation

- **PyPI Package**: [pypi.org/project/prozes](https://pypi.org/project/prozes/)
- **GitHub Repository**: [github.com/jaopdc11/prozes](https://github.com/jaopdc11/prozes)
- **Issue Tracker**: [GitHub Issues](https://github.com/jaopdc11/prozes/issues)
- **Changelog**: [CHANGELOG.md](CHANGELOG.md)

For detailed command information:
```bash
prozes --help
prozes mvc --help    # Help for specific commands
prozes api --help
prozes cli --help
prozes clean --help
```

---

## Roadmap

We have ambitious plans for Prozes. Check out our [ROADMAP.md](ROADMAP.md) to see what's coming:

- ✅ ~~Authentication scaffolding~~ **DONE** (JWT, Session, Basic, OAuth2)
- ✅ ~~Custom template system~~ **DONE** (save, use, list, delete templates)
- 🐳 Docker integration
- 🗄️ Database templates (PostgreSQL, MongoDB, etc.)
- 🌐 More frameworks (Django, Tornado, Sanic)
- 🏗️ More architectures (Hexagonal, CQRS, Event-Driven)

[View Full Roadmap →](ROADMAP.md)

---

## Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/jaopdc11/prozes.git
cd prozes

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install in development mode with all dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

### Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=prozes --cov-report=html

# Run specific test file
pytest tests/test_core.py -v
```

### Code Quality

```bash
# Format code
black prozes tests

# Lint code
ruff check prozes tests

# Type checking
mypy prozes

# Run all checks (what CI runs)
pre-commit run --all-files
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

---

## Contributing

We welcome contributions! Here's how you can help:

- 🐛 **Report bugs** via [GitHub Issues](https://github.com/jaopdc11/prozes/issues)
- 💡 **Suggest features** through [GitHub Discussions](https://github.com/jaopdc11/prozes/discussions)
- 📝 **Improve documentation**
- 🔧 **Submit pull requests**

Please read our [Contributing Guide](CONTRIBUTING.md) before submitting PRs.

### Contributors

Thanks to all our contributors!

<!-- ALL-CONTRIBUTORS-LIST:START -->
<!-- This section will be automatically generated -->
<!-- ALL-CONTRIBUTORS-LIST:END -->

---

## Community

- **GitHub Discussions**: [Ask questions and share ideas](https://github.com/jaopdc11/prozes/discussions)
- **Issues**: [Report bugs](https://github.com/jaopdc11/prozes/issues)
- **Discord**: [Coming Soon]
- **Twitter**: [Coming Soon]

---

## License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

Built with:
- [Click](https://click.palletsprojects.com/) - Command line interface
- [Rich](https://rich.readthedocs.io/) - Beautiful terminal output
- [Flask](https://flask.palletsprojects.com/) & [FastAPI](https://fastapi.tiangolo.com/) - Web frameworks

Inspired by:
- [Cookiecutter](https://github.com/cookiecutter/cookiecutter)
- [Vue CLI](https://cli.vuejs.org/)
- [Create React App](https://create-react-app.dev/)

---

<div align="center">

**[⬆ Back to Top](#prozes)**

Made with ❤️ by [jaopdc11](https://github.com/jaopdc11) & [mednick-sys](https://github.com/mednick-sys)

If you find this project useful, please consider giving it a ⭐️

</div>

