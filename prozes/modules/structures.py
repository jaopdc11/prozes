"""Module for generating architecture structures."""

from pathlib import Path
from prozes.modules.console import print_creating, print_success, console
from prozes.modules.i18n import t


# =============================================================================
# BUILT-IN TEMPLATES REGISTRY
# =============================================================================

BUILTIN_TEMPLATES = {
    'mvc-flask': {
        'name': 'mvc-flask',
        'display_name': 'MVC com Flask',
        'description': 'Arquitetura MVC com Flask',
        'function': lambda project_path, verbose: create_mvc_structure(project_path, 'web-flask', verbose),
    },
    'mvc-fastapi': {
        'name': 'mvc-fastapi',
        'display_name': 'MVC com FastAPI',
        'description': 'Arquitetura MVC com FastAPI',
        'function': lambda project_path, verbose: create_mvc_structure(project_path, 'web-fastapi', verbose),
    },
    'api-flask': {
        'name': 'api-flask',
        'display_name': 'API REST com Flask',
        'description': 'API REST com Flask',
        'function': lambda project_path, verbose: create_api_structure(project_path, 'api-flask', verbose),
    },
    'api-fastapi': {
        'name': 'api-fastapi',
        'display_name': 'API REST com FastAPI',
        'description': 'API REST com FastAPI',
        'function': lambda project_path, verbose: create_api_structure(project_path, 'api-fastapi', verbose),
    },
    'cli': {
        'name': 'cli',
        'display_name': 'CLI com Click',
        'description': 'Aplicação CLI com Click',
        'function': lambda project_path, verbose: create_cli_structure(project_path, verbose),
    },
    'clean-flask': {
        'name': 'clean-flask',
        'display_name': 'Clean Architecture com Flask',
        'description': 'Clean Architecture com Flask',
        'function': lambda project_path, verbose: create_clean_structure(project_path, 'clean-flask', verbose),
    },
    'clean-fastapi': {
        'name': 'clean-fastapi',
        'display_name': 'Clean Architecture com FastAPI',
        'description': 'Clean Architecture com FastAPI',
        'function': lambda project_path, verbose: create_clean_structure(project_path, 'clean-fastapi', verbose),
    },
}


def get_builtin_template_list():
    """Retorna lista de templates built-in para exibição.

    Returns:
        List of dicts with template info
    """
    return [
        {
            'name': tpl['name'],
            'display_name': tpl.get('display_name', tpl['name']),
            'description': tpl.get('description', '')
        }
        for tpl in BUILTIN_TEMPLATES.values()
    ]


# =============================================================================
# TEMPLATES COMUNS
# =============================================================================

GITIGNORE_CONTENT = '''# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# Virtual environment
venv/
.venv/
ENV/

# IDE
.idea/
.vscode/
*.swp
*.swo

# Environment variables
.env
.env.local

# Distribution / packaging
dist/
build/
*.egg-info/

# Testing
.pytest_cache/
.coverage
htmlcov/

# OS
.DS_Store
Thumbs.db
'''

CONFIG_INIT = '''"""Configuracoes da aplicacao."""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


class Config:
    """Configuracao base."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key')
    DEBUG = False


class DevelopmentConfig(Config):
    """Configuracao de desenvolvimento."""
    DEBUG = True


class ProductionConfig(Config):
    """Configuracao de producao."""
    pass
'''

TESTS_INIT = '''"""Testes da aplicacao."""
'''

TEST_PLACEHOLDER = '''"""Testes basicos da aplicacao."""

import pytest


def test_placeholder():
    """Teste placeholder."""
    assert True
'''

ENV_EXAMPLE = '''# Application
SECRET_KEY=your-secret-key-change-this-in-production
DEBUG=True

# Database (if needed)
# DATABASE_URL=sqlite:///app.db
# DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# API Keys (if needed)
# API_KEY=your-api-key-here
'''

REQUIREMENTS_DEV = '''-r requirements.txt

# Development tools
pytest>=8.0.0
pytest-cov>=4.1.0
black>=24.0.0
ruff>=0.2.0

# Optional: API testing
# httpx>=0.24.0
'''

PYTEST_CONFIG = '''[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_functions = ["test_*"]
addopts = "-v --tb=short"

[tool.coverage.run]
source = ["."]
omit = ["tests/*", "venv/*"]
'''

GITHUB_WORKFLOW_TEST = '''name: Tests

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install pytest pytest-cov

      - name: Run tests
        run: |
          pytest --cov --cov-report=term-missing
'''

LOGGING_CONFIG = '''"""Configuracao de logging."""

import logging
import sys

def setup_logging(level=logging.INFO):
    """Configura logging da aplicacao."""
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('app.log')
        ]
    )

    return logging.getLogger(__name__)
'''

TEST_FLASK_MVC = '''"""Testes da aplicacao Flask MVC."""

import pytest
from main import app


@pytest.fixture
def client():
    """Fixture do cliente de teste."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_app_exists(client):
    """Testa se a aplicacao existe."""
    assert app is not None


def test_index_route(client):
    """Testa a rota principal."""
    response = client.get('/')
    assert response.status_code == 200
'''

TEST_FASTAPI_MVC = '''"""Testes da aplicacao FastAPI MVC."""

import pytest
from fastapi.testclient import TestClient
from main import app


@pytest.fixture
def client():
    """Fixture do cliente de teste."""
    return TestClient(app)


def test_app_exists():
    """Testa se a aplicacao existe."""
    assert app is not None


def test_root_route(client):
    """Testa a rota principal."""
    response = client.get('/')
    assert response.status_code == 200
'''

TEST_FLASK_API = '''"""Testes da API Flask."""

import pytest
from main import app


@pytest.fixture
def client():
    """Fixture do cliente de teste."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_health_check(client):
    """Testa o health check."""
    response = client.get('/api/health')
    assert response.status_code == 200
    assert response.json['status'] == 'ok'


def test_list_items(client):
    """Testa a listagem de items."""
    response = client.get('/api/v1/items')
    assert response.status_code == 200
    assert 'items' in response.json
'''

TEST_FASTAPI_API = '''"""Testes da API FastAPI."""

import pytest
from fastapi.testclient import TestClient
from main import app


@pytest.fixture
def client():
    """Fixture do cliente de teste."""
    return TestClient(app)


def test_health_check(client):
    """Testa o health check."""
    response = client.get('/api/health')
    assert response.status_code == 200
    assert response.json()['status'] == 'ok'


def test_list_items(client):
    """Testa a listagem de items."""
    response = client.get('/api/v1/items')
    assert response.status_code == 200
    assert 'items' in response.json()
'''

TEST_CLI = '''"""Testes do CLI."""

import pytest
from click.testing import CliRunner
from {project_name}.main import cli


@pytest.fixture
def runner():
    """Fixture do CLI runner."""
    return CliRunner()


def test_cli_help(runner):
    """Testa o help do CLI."""
    result = runner.invoke(cli, ['--help'])
    assert result.exit_code == 0
    assert 'Usage' in result.output


def test_hello_command(runner):
    """Testa o comando hello."""
    result = runner.invoke(cli, ['hello'])
    assert result.exit_code == 0
'''


# =============================================================================
# TEMPLATES FLASK MVC
# =============================================================================

FLASK_MAIN_PY = '''"""Aplicacao Flask principal."""

from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return 'Hello, World!'


if __name__ == '__main__':
    app.run(debug=True)
'''

FLASK_APP_INIT = '''"""Inicializacao do pacote app."""

from flask import Flask


def create_app():
    """Factory function para criar a aplicacao Flask."""
    app = Flask(__name__)

    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    from app.controllers import main_bp
    app.register_blueprint(main_bp)

    return app
'''

FLASK_CONTROLLER = '''"""Controllers principais da aplicacao."""

from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """Pagina inicial."""
    return render_template('base.html')
'''

FLASK_BASE_TEMPLATE = '''<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title if title else 'Minha Aplicacao' }}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>
    <main>
        {% block content %}
        <h1>Bem-vindo!</h1>
        {% endblock %}
    </main>
    <script src="{{ url_for('static', filename='js/main.js') }}"></script>
</body>
</html>
'''

FLASK_CSS = '''/* Estilos principais */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    line-height: 1.6;
    padding: 2rem;
}

main {
    max-width: 1200px;
    margin: 0 auto;
}
'''

FLASK_JS = '''// JavaScript principal
console.log('Aplicacao carregada');
'''


# =============================================================================
# TEMPLATES FASTAPI MVC
# =============================================================================

FASTAPI_MAIN_PY = '''"""Aplicacao FastAPI principal."""

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.controllers import router

app = FastAPI(title="Minha API", version="1.0.0")

# Static files e templates
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# Registrar rotas
app.include_router(router)


@app.get("/")
async def root():
    return {"message": "Hello, World!"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
'''

FASTAPI_APP_INIT = '''"""Inicializacao do pacote app."""

from fastapi import FastAPI


def create_app() -> FastAPI:
    """Factory function para criar a aplicacao FastAPI."""
    app = FastAPI(
        title="Minha API",
        version="1.0.0",
    )

    from app.controllers import router
    app.include_router(router)

    return app
'''

FASTAPI_CONTROLLER = '''"""Controllers principais da aplicacao."""

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/hello")
async def hello():
    """Endpoint de exemplo."""
    return {"message": "Hello from controller!"}


@router.get("/page", response_class=HTMLResponse)
async def page(request: Request):
    """Pagina de exemplo."""
    return templates.TemplateResponse("base.html", {"request": request})
'''

FASTAPI_BASE_TEMPLATE = '''<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title if title else 'Minha Aplicacao' }}</title>
    <link rel="stylesheet" href="/static/css/style.css">
</head>
<body>
    <main>
        <h1>Bem-vindo!</h1>
    </main>
    <script src="/static/js/main.js"></script>
</body>
</html>
'''


# =============================================================================
# TEMPLATES API REST (sem frontend)
# =============================================================================

FLASK_API_MAIN = '''"""API REST Flask."""

from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/api/health')
def health():
    return jsonify({"status": "ok"})


@app.route('/api/v1/items', methods=['GET'])
def list_items():
    return jsonify({"items": []})


@app.route('/api/v1/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    return jsonify({"id": item_id, "name": "Item exemplo"})


if __name__ == '__main__':
    app.run(debug=True)
'''

FLASK_API_ROUTES = '''"""Rotas da API."""

from flask import Blueprint, jsonify, request

api_bp = Blueprint('api', __name__, url_prefix='/api/v1')


@api_bp.route('/items', methods=['GET'])
def list_items():
    """Lista todos os items."""
    return jsonify({"items": []})


@api_bp.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    """Retorna um item pelo ID."""
    return jsonify({"id": item_id, "name": "Item exemplo"})


@api_bp.route('/items', methods=['POST'])
def create_item():
    """Cria um novo item."""
    data = request.get_json()
    return jsonify({"id": 1, **data}), 201
'''

FASTAPI_API_MAIN = '''"""API REST FastAPI."""

import uvicorn
from fastapi import FastAPI

from app.routes import router

app = FastAPI(
    title="Minha API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.include_router(router, prefix="/api/v1")


@app.get("/api/health")
async def health():
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
'''

FASTAPI_API_ROUTES = '''"""Rotas da API."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

router = APIRouter()


class ItemCreate(BaseModel):
    name: str
    description: Optional[str] = None


class ItemResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None


@router.get("/items")
async def list_items():
    """Lista todos os items."""
    return {"items": []}


@router.get("/items/{item_id}")
async def get_item(item_id: int):
    """Retorna um item pelo ID."""
    return {"id": item_id, "name": "Item exemplo"}


@router.post("/items", response_model=ItemResponse, status_code=201)
async def create_item(item: ItemCreate):
    """Cria um novo item."""
    return {"id": 1, **item.model_dump()}
'''

API_MODELS_INIT = '''"""Models da API."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Item:
    id: int
    name: str
    description: Optional[str] = None
'''


# =============================================================================
# TEMPLATES CLI
# =============================================================================

CLI_MAIN_PY = '''"""CLI principal."""

import click
from {project_name}.commands import hello, greet


@click.group()
@click.version_option(version='0.1.0')
def cli():
    """Descricao do seu CLI."""
    pass


cli.add_command(hello)
cli.add_command(greet)


def main():
    cli()


if __name__ == '__main__':
    main()
'''

CLI_COMMANDS_INIT = '''"""Comandos do CLI."""

from .hello import hello
from .greet import greet

__all__ = ['hello', 'greet']
'''

CLI_HELLO_CMD = '''"""Comando hello."""

import click


@click.command()
def hello():
    """Exibe uma mensagem de boas-vindas."""
    click.echo("Hello, World!")
'''

CLI_GREET_CMD = '''"""Comando greet."""

import click


@click.command()
@click.argument('name')
@click.option('-c', '--caps', is_flag=True, help='Saida em maiusculas')
def greet(name, caps):
    """Cumprimenta o usuario pelo nome.

    NAME: Nome do usuario
    """
    message = f"Ola, {name}!"
    if caps:
        message = message.upper()
    click.echo(message)
'''

CLI_SETUP_PY = '''"""Setup do pacote."""

from setuptools import setup, find_packages

setup(
    name='{project_name}',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'click>=8.0.0',
    ],
    entry_points={{
        'console_scripts': [
            '{project_name}={project_name}.main:main',
        ],
    }},
)
'''

CLI_PYPROJECT = '''[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "{project_name}"
version = "0.1.0"
description = "Descricao do seu CLI"
requires-python = ">=3.8"
dependencies = [
    "click>=8.0.0",
]

[project.scripts]
{project_name} = "{project_name}.main:main"
'''


# =============================================================================
# TEMPLATES CLEAN ARCHITECTURE
# =============================================================================

CLEAN_MAIN_PY = '''"""Ponto de entrada da aplicacao."""

from src.frameworks.web.app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
'''

CLEAN_ENTITY = '''"""Entidades do dominio."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class User:
    """Entidade User."""
    id: Optional[int] = None
    name: str = ""
    email: str = ""

    def is_valid(self) -> bool:
        """Valida a entidade."""
        return bool(self.name and self.email)
'''

CLEAN_USE_CASE = '''"""Casos de uso da aplicacao."""

from abc import ABC, abstractmethod
from typing import Optional
from src.entities.user import User


class UserRepositoryInterface(ABC):
    """Interface do repositorio de usuarios."""

    @abstractmethod
    def get_by_id(self, user_id: int) -> Optional[User]:
        pass

    @abstractmethod
    def save(self, user: User) -> User:
        pass


class CreateUserUseCase:
    """Caso de uso: criar usuario."""

    def __init__(self, repository: UserRepositoryInterface):
        self.repository = repository

    def execute(self, name: str, email: str) -> User:
        """Executa o caso de uso."""
        user = User(name=name, email=email)

        if not user.is_valid():
            raise ValueError("Dados do usuario invalidos")

        return self.repository.save(user)


class GetUserUseCase:
    """Caso de uso: buscar usuario."""

    def __init__(self, repository: UserRepositoryInterface):
        self.repository = repository

    def execute(self, user_id: int) -> Optional[User]:
        """Executa o caso de uso."""
        return self.repository.get_by_id(user_id)
'''

CLEAN_ADAPTER_REPO = '''"""Implementacao do repositorio."""

from typing import Optional, Dict
from src.entities.user import User
from src.use_cases.user import UserRepositoryInterface


class InMemoryUserRepository(UserRepositoryInterface):
    """Repositorio em memoria (para desenvolvimento/testes)."""

    def __init__(self):
        self._users: Dict[int, User] = {}
        self._next_id = 1

    def get_by_id(self, user_id: int) -> Optional[User]:
        return self._users.get(user_id)

    def save(self, user: User) -> User:
        if user.id is None:
            user.id = self._next_id
            self._next_id += 1
        self._users[user.id] = user
        return user
'''

CLEAN_ADAPTER_PRESENTER = '''"""Presenters para formatacao de saida."""

from dataclasses import dataclass
from typing import Optional
from src.entities.user import User


@dataclass
class UserViewModel:
    """View model do usuario."""
    id: int
    name: str
    email: str


class UserPresenter:
    """Presenter de usuario."""

    @staticmethod
    def to_view_model(user: Optional[User]) -> Optional[UserViewModel]:
        if user is None:
            return None
        return UserViewModel(
            id=user.id,
            name=user.name,
            email=user.email,
        )

    @staticmethod
    def to_dict(user: Optional[User]) -> Optional[dict]:
        if user is None:
            return None
        return {
            "id": user.id,
            "name": user.name,
            "email": user.email,
        }
'''

CLEAN_FRAMEWORK_WEB_FLASK = '''"""Framework web (Flask)."""

from flask import Flask, jsonify, request
from src.use_cases.user import CreateUserUseCase, GetUserUseCase
from src.adapters.repositories.user_repository import InMemoryUserRepository
from src.adapters.presenters.user_presenter import UserPresenter


def create_app() -> Flask:
    """Cria a aplicacao Flask."""
    app = Flask(__name__)

    # Dependency injection
    user_repo = InMemoryUserRepository()
    create_user = CreateUserUseCase(user_repo)
    get_user = GetUserUseCase(user_repo)
    presenter = UserPresenter()

    @app.route('/api/health')
    def health():
        return jsonify({"status": "ok"})

    @app.route('/api/users', methods=['POST'])
    def create_user_endpoint():
        data = request.get_json()
        user = create_user.execute(data['name'], data['email'])
        return jsonify(presenter.to_dict(user)), 201

    @app.route('/api/users/<int:user_id>')
    def get_user_endpoint(user_id):
        user = get_user.execute(user_id)
        if user is None:
            return jsonify({"error": "User not found"}), 404
        return jsonify(presenter.to_dict(user))

    return app
'''

CLEAN_FRAMEWORK_WEB_FASTAPI = '''"""Framework web (FastAPI)."""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.use_cases.user import CreateUserUseCase, GetUserUseCase
from src.adapters.repositories.user_repository import InMemoryUserRepository
from src.adapters.presenters.user_presenter import UserPresenter


class UserCreateRequest(BaseModel):
    name: str
    email: str


# Dependency injection
user_repo = InMemoryUserRepository()
create_user_uc = CreateUserUseCase(user_repo)
get_user_uc = GetUserUseCase(user_repo)
presenter = UserPresenter()


def create_app() -> FastAPI:
    """Cria a aplicacao FastAPI."""
    app = FastAPI(title="Clean Architecture API", version="1.0.0")

    @app.get("/api/health")
    async def health():
        return {"status": "ok"}

    @app.post("/api/users", status_code=201)
    async def create_user_endpoint(data: UserCreateRequest):
        user = create_user_uc.execute(data.name, data.email)
        return presenter.to_dict(user)

    @app.get("/api/users/{user_id}")
    async def get_user_endpoint(user_id: int):
        user = get_user_uc.execute(user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return presenter.to_dict(user)

    return app
'''

CLEAN_MAIN_FASTAPI = '''"""Ponto de entrada da aplicacao."""

import uvicorn
from src.frameworks.web.app import create_app

app = create_app()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
'''

CLEAN_TEST_USE_CASE = '''"""Testes dos casos de uso."""

import pytest
from src.entities.user import User
from src.use_cases.user import CreateUserUseCase, GetUserUseCase
from src.adapters.repositories.user_repository import InMemoryUserRepository


@pytest.fixture
def repository():
    return InMemoryUserRepository()


def test_create_user(repository):
    use_case = CreateUserUseCase(repository)
    user = use_case.execute("John", "john@example.com")

    assert user.id is not None
    assert user.name == "John"
    assert user.email == "john@example.com"


def test_get_user(repository):
    # Arrange
    create_use_case = CreateUserUseCase(repository)
    created_user = create_use_case.execute("John", "john@example.com")

    # Act
    get_use_case = GetUserUseCase(repository)
    found_user = get_use_case.execute(created_user.id)

    # Assert
    assert found_user is not None
    assert found_user.name == "John"


def test_create_user_invalid():
    repository = InMemoryUserRepository()
    use_case = CreateUserUseCase(repository)

    with pytest.raises(ValueError):
        use_case.execute("", "")
'''


# =============================================================================
# AUTHENTICATION TEMPLATES - BASE COMMON
# =============================================================================

AUTH_USER_MODEL_BASE = '''"""User model for authentication."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
import uuid


@dataclass
class User:
    """User model."""
    username: str
    email: str
    password_hash: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=datetime.utcnow)
    is_active: bool = True
    full_name: Optional[str] = None

    def to_dict(self):
        """Convert user to dictionary (without password hash)."""
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "full_name": self.full_name,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
'''

AUTH_PASSWORD_UTILS = '''"""Password hashing utilities."""

from passlib.context import CryptContext

# Configure password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a password using bcrypt.

    Args:
        password: Plain text password

    Returns:
        Hashed password
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash.

    Args:
        plain_password: Plain text password to verify
        hashed_password: Hashed password to check against

    Returns:
        True if password matches, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)
'''

AUTH_STORAGE_BASE = '''"""In-memory storage for authentication.

WARNING: This is for development/demo purposes only.
For production, replace with a real database (PostgreSQL, MongoDB, etc).
"""

from typing import Dict, Optional
from .models import User


class UserStorage:
    """In-memory user storage."""

    def __init__(self):
        self._users: Dict[str, User] = {}
        self._users_by_username: Dict[str, str] = {}  # username -> user_id
        self._users_by_email: Dict[str, str] = {}  # email -> user_id

    def create_user(self, user: User) -> User:
        """Create a new user."""
        if user.username in self._users_by_username:
            raise ValueError(f"Username '{user.username}' already exists")
        if user.email in self._users_by_email:
            raise ValueError(f"Email '{user.email}' already exists")

        self._users[user.id] = user
        self._users_by_username[user.username] = user.id
        self._users_by_email[user.email] = user.id
        return user

    def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Get user by ID."""
        return self._users.get(user_id)

    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username."""
        user_id = self._users_by_username.get(username)
        return self._users.get(user_id) if user_id else None

    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        user_id = self._users_by_email.get(email)
        return self._users.get(user_id) if user_id else None

    def update_user(self, user: User) -> User:
        """Update an existing user."""
        if user.id not in self._users:
            raise ValueError(f"User with id '{user.id}' not found")
        self._users[user.id] = user
        return user

    def delete_user(self, user_id: str) -> bool:
        """Delete a user."""
        user = self._users.get(user_id)
        if not user:
            return False

        del self._users[user_id]
        del self._users_by_username[user.username]
        del self._users_by_email[user.email]
        return True


# Global storage instance
user_storage = UserStorage()
'''


# =============================================================================
# JWT AUTHENTICATION TEMPLATES - FLASK
# =============================================================================

JWT_FLASK_CONFIG = '''"""JWT authentication configuration."""

import os
from datetime import timedelta

# JWT settings
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'dev-secret-key-change-in-production')
JWT_ALGORITHM = os.getenv('JWT_ALGORITHM', 'HS256')
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRE_MINUTES', '30'))
JWT_REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv('JWT_REFRESH_TOKEN_EXPIRE_DAYS', '7'))

# Token expiration
ACCESS_TOKEN_EXPIRE = timedelta(minutes=JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
REFRESH_TOKEN_EXPIRE = timedelta(days=JWT_REFRESH_TOKEN_EXPIRE_DAYS)
'''

JWT_FLASK_UTILS = '''"""JWT token utilities."""

from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import jwt
from .config import JWT_SECRET_KEY, JWT_ALGORITHM, ACCESS_TOKEN_EXPIRE, REFRESH_TOKEN_EXPIRE


def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token.

    Args:
        data: Data to encode in the token
        expires_delta: Custom expiration time (optional)

    Returns:
        Encoded JWT token
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + ACCESS_TOKEN_EXPIRE

    to_encode.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: Dict[str, Any]) -> str:
    """Create a JWT refresh token.

    Args:
        data: Data to encode in the token

    Returns:
        Encoded JWT refresh token
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + REFRESH_TOKEN_EXPIRE
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt


def decode_token(token: str) -> Dict[str, Any]:
    """Decode and verify a JWT token.

    Args:
        token: JWT token to decode

    Returns:
        Decoded token data

    Raises:
        jwt.ExpiredSignatureError: If token has expired
        jwt.JWTError: If token is invalid
    """
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise jwt.ExpiredSignatureError("Token has expired")
    except jwt.JWTError as e:
        raise jwt.JWTError(f"Invalid token: {str(e)}")
'''

JWT_FLASK_MIDDLEWARE = '''"""JWT authentication middleware."""

from functools import wraps
from flask import request, jsonify, g
import jwt as pyjwt
from .utils import decode_token
from .storage import user_storage


def jwt_required(f):
    """Decorator to require JWT authentication.

    Usage:
        @app.route('/protected')
        @jwt_required
        def protected_route():
            current_user = g.current_user
            return jsonify({"message": f"Hello {current_user.username}"})
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None

        # Get token from Authorization header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]  # Bearer <token>
            except IndexError:
                return jsonify({"error": "Invalid authorization header format"}), 401

        if not token:
            return jsonify({"error": "Authorization token is missing"}), 401

        try:
            # Decode token
            payload = decode_token(token)

            # Verify token type
            if payload.get('type') != 'access':
                return jsonify({"error": "Invalid token type"}), 401

            # Get user from storage
            user_id = payload.get('sub')
            user = user_storage.get_user_by_id(user_id)

            if not user:
                return jsonify({"error": "User not found"}), 401

            if not user.is_active:
                return jsonify({"error": "User account is disabled"}), 401

            # Store user in Flask's g object
            g.current_user = user

        except pyjwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired"}), 401
        except pyjwt.JWTError:
            return jsonify({"error": "Invalid token"}), 401
        except Exception as e:
            return jsonify({"error": f"Authentication failed: {str(e)}"}), 401

        return f(*args, **kwargs)

    return decorated_function


def get_current_user():
    """Get the current authenticated user from Flask's g object.

    Returns:
        Current user or None
    """
    return getattr(g, 'current_user', None)
'''

JWT_FLASK_ROUTES = '''"""JWT authentication routes."""

from flask import Blueprint, request, jsonify
from .models import User
from .utils import create_access_token, create_refresh_token, decode_token
from passlib.context import CryptContext
from .storage import user_storage
from .middleware import jwt_required, get_current_user
import jwt as pyjwt

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user.

    Request body:
        {
            "username": "string",
            "email": "string",
            "password": "string",
            "full_name": "string" (optional)
        }
    """
    data = request.get_json()

    # Validate input
    if not data:
        return jsonify({"error": "No data provided"}), 400

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    full_name = data.get('full_name')

    if not username or not email or not password:
        return jsonify({"error": "Username, email, and password are required"}), 400

    # Validate password strength
    if len(password) < 6:
        return jsonify({"error": "Password must be at least 6 characters"}), 400

    try:
        # Create user
        password_hash = hash_password(password)
        user = User(
            username=username,
            email=email,
            password_hash=password_hash,
            full_name=full_name
        )
        user = user_storage.create_user(user)

        # Create tokens
        access_token = create_access_token(data={"sub": user.id})
        refresh_token = create_refresh_token(data={"sub": user.id})

        return jsonify({
            "message": "User created successfully",
            "user": user.to_dict(),
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }), 201

    except ValueError as e:
        return jsonify({"error": str(e)}), 409


@auth_bp.route('/login', methods=['POST'])
def login():
    """Login user and return JWT tokens.

    Request body:
        {
            "username": "string",
            "password": "string"
        }
    """
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    # Get user
    user = user_storage.get_user_by_username(username)
    if not user:
        return jsonify({"error": "Invalid username or password"}), 401

    # Verify password
    if not verify_password(password, user.password_hash):
        return jsonify({"error": "Invalid username or password"}), 401

    if not user.is_active:
        return jsonify({"error": "User account is disabled"}), 401

    # Create tokens
    access_token = create_access_token(data={"sub": user.id})
    refresh_token = create_refresh_token(data={"sub": user.id})

    return jsonify({
        "message": "Login successful",
        "user": user.to_dict(),
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }), 200


@auth_bp.route('/refresh', methods=['POST'])
def refresh():
    """Refresh access token using refresh token.

    Request body:
        {
            "refresh_token": "string"
        }
    """
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    refresh_token = data.get('refresh_token')

    if not refresh_token:
        return jsonify({"error": "Refresh token is required"}), 400

    try:
        # Decode refresh token
        payload = decode_token(refresh_token)

        # Verify token type
        if payload.get('type') != 'refresh':
            return jsonify({"error": "Invalid token type"}), 401

        # Get user
        user_id = payload.get('sub')
        user = user_storage.get_user_by_id(user_id)

        if not user:
            return jsonify({"error": "User not found"}), 401

        if not user.is_active:
            return jsonify({"error": "User account is disabled"}), 401

        # Create new access token
        access_token = create_access_token(data={"sub": user.id})

        return jsonify({
            "access_token": access_token,
            "token_type": "bearer"
        }), 200

    except pyjwt.ExpiredSignatureError:
        return jsonify({"error": "Refresh token has expired"}), 401
    except pyjwt.JWTError:
        return jsonify({"error": "Invalid refresh token"}), 401


@auth_bp.route('/me', methods=['GET'])
@jwt_required
def get_current_user_info():
    """Get current user information (protected route)."""
    user = get_current_user()
    return jsonify(user.to_dict()), 200


@auth_bp.route('/logout', methods=['POST'])
@jwt_required
def logout():
    """Logout user (client should delete tokens).

    Note: With JWT, logout is primarily handled client-side by deleting tokens.
    This endpoint is provided for consistency and can be extended with token blacklisting.
    """
    return jsonify({"message": "Logout successful. Please delete your tokens."}), 200
'''

JWT_FLASK_INIT = '''"""JWT authentication module for Flask."""

from .routes import auth_bp
from .middleware import jwt_required, get_current_user
from .models import User
from .storage import user_storage

__all__ = ['auth_bp', 'jwt_required', 'get_current_user', 'User', 'user_storage']
'''


# =============================================================================
# JWT AUTHENTICATION TEMPLATES - FASTAPI
# =============================================================================

JWT_FASTAPI_CONFIG = JWT_FLASK_CONFIG  # Same config for both

JWT_FASTAPI_UTILS = JWT_FLASK_UTILS  # Same utils for both

JWT_FASTAPI_DEPENDENCIES = '''"""JWT authentication dependencies for FastAPI."""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt as pyjwt
from typing import Optional
from .utils import decode_token
from .storage import user_storage
from .models import User

security = HTTPBearer()


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
    """Dependency to get current authenticated user.

    Usage:
        @app.get("/protected")
        async def protected_route(current_user: User = Depends(get_current_user)):
            return {"message": f"Hello {current_user.username}"}
    """
    token = credentials.credentials

    try:
        # Decode token
        payload = decode_token(token)

        # Verify token type
        if payload.get('type') != 'access':
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type"
            )

        # Get user from storage
        user_id = payload.get('sub')
        user = user_storage.get_user_by_id(user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User account is disabled"
            )

        return user

    except pyjwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except pyjwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Authentication failed: {str(e)}"
        )


async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """Dependency to get current active user."""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return current_user
'''

JWT_FASTAPI_ROUTES = '''"""JWT authentication routes for FastAPI."""

from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
import jwt as pyjwt
from passlib.context import CryptContext
from .models import User
from .utils import create_access_token, create_refresh_token, decode_token
from .storage import user_storage
from .dependencies import get_current_user

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

router = APIRouter(prefix="/auth", tags=["authentication"])


# Request/Response models
class UserRegister(BaseModel):
    """User registration request."""
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)
    full_name: Optional[str] = None


class UserLogin(BaseModel):
    """User login request."""
    username: str
    password: str


class TokenRefresh(BaseModel):
    """Token refresh request."""
    refresh_token: str


class TokenResponse(BaseModel):
    """Token response."""
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = "bearer"


class UserResponse(BaseModel):
    """User response."""
    id: str
    username: str
    email: str
    full_name: Optional[str] = None
    is_active: bool


class AuthResponse(BaseModel):
    """Authentication response with tokens and user."""
    message: str
    user: UserResponse
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserRegister):
    """Register a new user."""
    try:
        # Create user
        password_hash = hash_password(user_data.password)
        user = User(
            username=user_data.username,
            email=user_data.email,
            password_hash=password_hash,
            full_name=user_data.full_name
        )
        user = user_storage.create_user(user)

        # Create tokens
        access_token = create_access_token(data={"sub": user.id})
        refresh_token = create_refresh_token(data={"sub": user.id})

        return AuthResponse(
            message="User created successfully",
            user=UserResponse(**user.to_dict()),
            access_token=access_token,
            refresh_token=refresh_token
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )


@router.post("/login", response_model=AuthResponse)
async def login(credentials: UserLogin):
    """Login user and return JWT tokens."""
    # Get user
    user = user_storage.get_user_by_username(credentials.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    # Verify password
    if not verify_password(credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User account is disabled"
        )

    # Create tokens
    access_token = create_access_token(data={"sub": user.id})
    refresh_token = create_refresh_token(data={"sub": user.id})

    return AuthResponse(
        message="Login successful",
        user=UserResponse(**user.to_dict()),
        access_token=access_token,
        refresh_token=refresh_token
    )


@router.post("/refresh", response_model=TokenResponse)
async def refresh(token_data: TokenRefresh):
    """Refresh access token using refresh token."""
    try:
        # Decode refresh token
        payload = decode_token(token_data.refresh_token)

        # Verify token type
        if payload.get('type') != 'refresh':
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type"
            )

        # Get user
        user_id = payload.get('sub')
        user = user_storage.get_user_by_id(user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User account is disabled"
            )

        # Create new access token
        access_token = create_access_token(data={"sub": user.id})

        return TokenResponse(access_token=access_token)

    except pyjwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token has expired"
        )
    except pyjwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    """Get current user information (protected route)."""
    return UserResponse(**current_user.to_dict())


@router.post("/logout")
async def logout(current_user: User = Depends(get_current_user)):
    """Logout user (client should delete tokens)."""
    return {"message": "Logout successful. Please delete your tokens."}
'''

JWT_FASTAPI_INIT = '''"""JWT authentication module for FastAPI."""

from .routes import router
from .dependencies import get_current_user, get_current_active_user
from .models import User
from .storage import user_storage

__all__ = ['router', 'get_current_user', 'get_current_active_user', 'User', 'user_storage']
'''


# =============================================================================
# JWT AUTHENTICATION TESTS
# =============================================================================

JWT_TESTS = '''"""Tests for JWT authentication."""

import pytest
from passlib.context import CryptContext
from app.auth.models import User
from app.auth.utils import create_access_token, decode_token
from app.auth.storage import UserStorage

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def test_password_hashing():
    """Test password hashing and verification."""
    password = "mysecretpassword"
    hashed = hash_password(password)

    assert hashed != password
    assert verify_password(password, hashed) is True
    assert verify_password("wrongpassword", hashed) is False


def test_user_creation():
    """Test user model creation."""
    user = User(
        username="testuser",
        email="test@example.com",
        password_hash=hash_password("password123")
    )

    assert user.username == "testuser"
    assert user.email == "test@example.com"
    assert user.is_active is True
    assert user.id is not None


def test_user_storage():
    """Test user storage operations."""
    storage = UserStorage()

    # Create user
    user = User(
        username="john",
        email="john@example.com",
        password_hash=hash_password("password")
    )
    created_user = storage.create_user(user)

    assert created_user.id is not None

    # Get by ID
    found = storage.get_user_by_id(created_user.id)
    assert found is not None
    assert found.username == "john"

    # Get by username
    found = storage.get_user_by_username("john")
    assert found is not None
    assert found.email == "john@example.com"

    # Get by email
    found = storage.get_user_by_email("john@example.com")
    assert found is not None
    assert found.username == "john"


def test_duplicate_username():
    """Test that duplicate usernames are rejected."""
    storage = UserStorage()

    user1 = User(username="john", email="john1@example.com", password_hash=hash_password("pass"))
    storage.create_user(user1)

    user2 = User(username="john", email="john2@example.com", password_hash=hash_password("pass"))

    with pytest.raises(ValueError, match="Username .* already exists"):
        storage.create_user(user2)


def test_duplicate_email():
    """Test that duplicate emails are rejected."""
    storage = UserStorage()

    user1 = User(username="john", email="test@example.com", password_hash=hash_password("pass"))
    storage.create_user(user1)

    user2 = User(username="jane", email="test@example.com", password_hash=hash_password("pass"))

    with pytest.raises(ValueError, match="Email .* already exists"):
        storage.create_user(user2)


def test_jwt_token_creation():
    """Test JWT token creation and decoding."""
    user_id = "test-user-123"
    token = create_access_token(data={"sub": user_id})

    assert token is not None
    assert isinstance(token, str)

    # Decode token
    payload = decode_token(token)
    assert payload["sub"] == user_id
    assert payload["type"] == "access"
'''


# =============================================================================
# SESSION AUTHENTICATION TEMPLATES - FLASK
# =============================================================================

SESSION_FLASK_CONFIG = '''"""Session authentication configuration."""

import os
from datetime import timedelta

# Session settings
SESSION_SECRET_KEY = os.getenv('SESSION_SECRET_KEY', 'dev-secret-key-change-in-production')
SESSION_COOKIE_NAME = os.getenv('SESSION_COOKIE_NAME', 'session')
SESSION_COOKIE_HTTPONLY = os.getenv('SESSION_COOKIE_HTTPONLY', 'True').lower() == 'true'
SESSION_COOKIE_SECURE = os.getenv('SESSION_COOKIE_SECURE', 'False').lower() == 'true'
SESSION_PERMANENT = os.getenv('SESSION_PERMANENT', 'True').lower() == 'true'
SESSION_LIFETIME_DAYS = int(os.getenv('SESSION_LIFETIME_DAYS', '7'))

# Session expiration
PERMANENT_SESSION_LIFETIME = timedelta(days=SESSION_LIFETIME_DAYS)
'''

SESSION_FLASK_UTILS = '''"""Session utilities for Flask."""

from flask import session
from typing import Optional
from passlib.context import CryptContext

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)


def create_session(user_id: str, username: str) -> None:
    """Create a session for a user.

    Args:
        user_id: User ID
        username: Username
    """
    session['user_id'] = user_id
    session['username'] = username
    session.permanent = True


def get_session_user_id() -> Optional[str]:
    """Get the current user ID from session.

    Returns:
        User ID or None if not logged in
    """
    return session.get('user_id')


def destroy_session() -> None:
    """Destroy the current session."""
    session.clear()
'''

SESSION_FLASK_MIDDLEWARE = '''"""Session authentication middleware for Flask."""

from functools import wraps
from flask import session, jsonify, g, redirect, url_for
from .storage import user_storage


def login_required(f):
    """Decorator to require session authentication.

    Usage:
        @app.route('/protected')
        @login_required
        def protected_route():
            current_user = g.current_user
            return jsonify({"message": f"Hello {current_user.username}"})
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = session.get('user_id')

        if not user_id:
            return jsonify({"error": "Not authenticated"}), 401

        # Get user from storage
        user = user_storage.get_user_by_id(user_id)

        if not user:
            session.clear()
            return jsonify({"error": "User not found"}), 401

        if not user.is_active:
            return jsonify({"error": "User account is disabled"}), 401

        # Store user in Flask's g object
        g.current_user = user

        return f(*args, **kwargs)

    return decorated_function


def get_current_user():
    """Get the current authenticated user from Flask's g object.

    Returns:
        Current user or None
    """
    return getattr(g, 'current_user', None)
'''

SESSION_FLASK_ROUTES = '''"""Session authentication routes for Flask."""

from flask import Blueprint, request, jsonify, session
from .models import User
from .utils import hash_password, verify_password, create_session, destroy_session
from .storage import user_storage
from .middleware import login_required, get_current_user

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user."""
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    full_name = data.get('full_name')

    if not username or not email or not password:
        return jsonify({"error": "Username, email, and password are required"}), 400

    if len(password) < 6:
        return jsonify({"error": "Password must be at least 6 characters"}), 400

    try:
        # Create user
        password_hash = hash_password(password)
        user = User(
            username=username,
            email=email,
            password_hash=password_hash,
            full_name=full_name
        )
        user = user_storage.create_user(user)

        # Create session
        create_session(user.id, user.username)

        return jsonify({
            "message": "User created successfully",
            "user": user.to_dict()
        }), 201

    except ValueError as e:
        return jsonify({"error": str(e)}), 409


@auth_bp.route('/login', methods=['POST'])
def login():
    """Login user and create session."""
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    # Get user
    user = user_storage.get_user_by_username(username)
    if not user:
        return jsonify({"error": "Invalid username or password"}), 401

    # Verify password
    if not verify_password(password, user.password_hash):
        return jsonify({"error": "Invalid username or password"}), 401

    if not user.is_active:
        return jsonify({"error": "User account is disabled"}), 401

    # Create session
    create_session(user.id, user.username)

    return jsonify({
        "message": "Login successful",
        "user": user.to_dict()
    }), 200


@auth_bp.route('/me', methods=['GET'])
@login_required
def get_current_user_info():
    """Get current user information (protected route)."""
    user = get_current_user()
    return jsonify(user.to_dict()), 200


@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    """Logout user and destroy session."""
    destroy_session()
    return jsonify({"message": "Logout successful"}), 200
'''

SESSION_FLASK_INIT = '''"""Session authentication module for Flask."""

from .routes import auth_bp
from .middleware import login_required, get_current_user
from .models import User
from .storage import user_storage

__all__ = ['auth_bp', 'login_required', 'get_current_user', 'User', 'user_storage']
'''


# =============================================================================
# SESSION AUTHENTICATION TEMPLATES - FASTAPI
# =============================================================================

SESSION_FASTAPI_CONFIG = SESSION_FLASK_CONFIG  # Same config

SESSION_FASTAPI_UTILS = '''"""Session utilities for FastAPI."""

from starlette.requests import Request
from typing import Optional
from passlib.context import CryptContext
import secrets

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)


def create_session_token() -> str:
    """Create a secure session token."""
    return secrets.token_urlsafe(32)


def get_session_user_id(request: Request) -> Optional[str]:
    """Get the current user ID from session.

    Args:
        request: FastAPI request

    Returns:
        User ID or None if not logged in
    """
    return request.session.get('user_id')
'''

SESSION_FASTAPI_DEPENDENCIES = '''"""Session authentication dependencies for FastAPI."""

from fastapi import Depends, HTTPException, status, Request
from typing import Optional
from .storage import user_storage
from .models import User


async def get_current_user(request: Request) -> User:
    """Dependency to get current authenticated user from session.

    Usage:
        @app.get("/protected")
        async def protected_route(current_user: User = Depends(get_current_user)):
            return {"message": f"Hello {current_user.username}"}
    """
    user_id = request.session.get('user_id')

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )

    # Get user from storage
    user = user_storage.get_user_by_id(user_id)

    if not user:
        request.session.clear()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User account is disabled"
        )

    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """Dependency to get current active user."""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return current_user
'''

SESSION_FASTAPI_ROUTES = '''"""Session authentication routes for FastAPI."""

from fastapi import APIRouter, HTTPException, status, Depends, Request
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from .models import User
from .utils import hash_password, verify_password
from .storage import user_storage
from .dependencies import get_current_user

router = APIRouter(prefix="/auth", tags=["authentication"])


# Request/Response models
class UserRegister(BaseModel):
    """User registration request."""
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)
    full_name: Optional[str] = None


class UserLogin(BaseModel):
    """User login request."""
    username: str
    password: str


class UserResponse(BaseModel):
    """User response."""
    id: str
    username: str
    email: str
    full_name: Optional[str] = None
    is_active: bool


class AuthResponse(BaseModel):
    """Authentication response."""
    message: str
    user: UserResponse


@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserRegister, request: Request):
    """Register a new user."""
    try:
        # Create user
        password_hash = hash_password(user_data.password)
        user = User(
            username=user_data.username,
            email=user_data.email,
            password_hash=password_hash,
            full_name=user_data.full_name
        )
        user = user_storage.create_user(user)

        # Create session
        request.session['user_id'] = user.id
        request.session['username'] = user.username

        return AuthResponse(
            message="User created successfully",
            user=UserResponse(**user.to_dict())
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )


@router.post("/login", response_model=AuthResponse)
async def login(credentials: UserLogin, request: Request):
    """Login user and create session."""
    # Get user
    user = user_storage.get_user_by_username(credentials.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    # Verify password
    if not verify_password(credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User account is disabled"
        )

    # Create session
    request.session['user_id'] = user.id
    request.session['username'] = user.username

    return AuthResponse(
        message="Login successful",
        user=UserResponse(**user.to_dict())
    )


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    """Get current user information (protected route)."""
    return UserResponse(**current_user.to_dict())


@router.post("/logout")
async def logout(request: Request, current_user: User = Depends(get_current_user)):
    """Logout user and destroy session."""
    request.session.clear()
    return {"message": "Logout successful"}
'''

SESSION_FASTAPI_INIT = '''"""Session authentication module for FastAPI."""

from .routes import router
from .dependencies import get_current_user, get_current_active_user
from .models import User
from .storage import user_storage

__all__ = ['router', 'get_current_user', 'get_current_active_user', 'User', 'user_storage']
'''


# =============================================================================
# SESSION AUTHENTICATION TESTS
# =============================================================================

SESSION_TESTS = '''"""Tests for Session authentication."""

import pytest
from passlib.context import CryptContext
from app.auth.models import User
from app.auth.storage import UserStorage

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def test_password_hashing():
    """Test password hashing and verification."""
    password = "mysecretpassword"
    hashed = hash_password(password)

    assert hashed != password
    assert verify_password(password, hashed) is True
    assert verify_password("wrongpassword", hashed) is False


def test_user_creation():
    """Test user model creation."""
    user = User(
        username="testuser",
        email="test@example.com",
        password_hash=hash_password("password123")
    )

    assert user.username == "testuser"
    assert user.email == "test@example.com"
    assert user.is_active is True
    assert user.id is not None


def test_user_storage():
    """Test user storage operations."""
    storage = UserStorage()

    user = User(
        username="john",
        email="john@example.com",
        password_hash=hash_password("password")
    )
    created_user = storage.create_user(user)

    assert created_user.id is not None

    found = storage.get_user_by_username("john")
    assert found is not None
    assert found.email == "john@example.com"
'''


# =============================================================================
# BASIC AUTHENTICATION TEMPLATES - FLASK
# =============================================================================

BASIC_FLASK_CONFIG = '''"""Basic authentication configuration."""

import os

# Basic Auth settings
BASIC_AUTH_REALM = os.getenv('BASIC_AUTH_REALM', 'Protected Area')
BASIC_AUTH_FORCE = os.getenv('BASIC_AUTH_FORCE', 'True').lower() == 'true'
'''

BASIC_FLASK_UTILS = '''"""Basic authentication utilities."""

from passlib.context import CryptContext

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)
'''

BASIC_FLASK_MIDDLEWARE = '''"""Basic authentication middleware for Flask."""

from functools import wraps
from flask import request, jsonify, g
import base64
from .storage import user_storage
from .utils import verify_password
from .config import BASIC_AUTH_REALM


def verify_basic_auth(username: str, password: str) -> bool:
    """Verify basic auth credentials.

    Args:
        username: Username
        password: Password

    Returns:
        True if credentials are valid
    """
    user = user_storage.get_user_by_username(username)
    if not user:
        return False

    if not user.is_active:
        return False

    return verify_password(password, user.password_hash)


def basic_auth_required(f):
    """Decorator to require HTTP Basic authentication.

    Usage:
        @app.route('/protected')
        @basic_auth_required
        def protected_route():
            current_user = g.current_user
            return jsonify({"message": f"Hello {current_user.username}"})
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth = request.authorization

        if not auth:
            return jsonify({"error": "Authentication required"}), 401, {
                'WWW-Authenticate': f'Basic realm="{BASIC_AUTH_REALM}"'
            }

        if not verify_basic_auth(auth.username, auth.password):
            return jsonify({"error": "Invalid credentials"}), 401, {
                'WWW-Authenticate': f'Basic realm="{BASIC_AUTH_REALM}"'
            }

        # Get and store user
        user = user_storage.get_user_by_username(auth.username)
        g.current_user = user

        return f(*args, **kwargs)

    return decorated_function


def get_current_user():
    """Get the current authenticated user from Flask's g object.

    Returns:
        Current user or None
    """
    return getattr(g, 'current_user', None)
'''

BASIC_FLASK_ROUTES = '''"""Basic authentication routes for Flask."""

from flask import Blueprint, request, jsonify
from .models import User
from .utils import hash_password
from .storage import user_storage
from .middleware import basic_auth_required, get_current_user

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user."""
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    full_name = data.get('full_name')

    if not username or not email or not password:
        return jsonify({"error": "Username, email, and password are required"}), 400

    if len(password) < 6:
        return jsonify({"error": "Password must be at least 6 characters"}), 400

    try:
        # Create user
        password_hash = hash_password(password)
        user = User(
            username=username,
            email=email,
            password_hash=password_hash,
            full_name=full_name
        )
        user = user_storage.create_user(user)

        return jsonify({
            "message": "User created successfully",
            "user": user.to_dict()
        }), 201

    except ValueError as e:
        return jsonify({"error": str(e)}), 409


@auth_bp.route('/me', methods=['GET'])
@basic_auth_required
def get_current_user_info():
    """Get current user information (protected route)."""
    user = get_current_user()
    return jsonify(user.to_dict()), 200
'''

BASIC_FLASK_INIT = '''"""Basic authentication module for Flask."""

from .routes import auth_bp
from .middleware import basic_auth_required, get_current_user
from .models import User
from .storage import user_storage

__all__ = ['auth_bp', 'basic_auth_required', 'get_current_user', 'User', 'user_storage']
'''


# =============================================================================
# BASIC AUTHENTICATION TEMPLATES - FASTAPI
# =============================================================================

BASIC_FASTAPI_CONFIG = BASIC_FLASK_CONFIG  # Same config

BASIC_FASTAPI_UTILS = BASIC_FLASK_UTILS  # Same utils

BASIC_FASTAPI_DEPENDENCIES = '''"""Basic authentication dependencies for FastAPI."""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from passlib.context import CryptContext
from .storage import user_storage
from .models import User

security = HTTPBasic()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def get_current_user(credentials: HTTPBasicCredentials = Depends(security)) -> User:
    """Dependency to get current authenticated user using HTTP Basic Auth.

    Usage:
        @app.get("/protected")
        async def protected_route(current_user: User = Depends(get_current_user)):
            return {"message": f"Hello {current_user.username}"}
    """
    user = user_storage.get_user_by_username(credentials.username)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )

    if not pwd_context.verify(credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User account is disabled",
            headers={"WWW-Authenticate": "Basic"},
        )

    return user
'''

BASIC_FASTAPI_ROUTES = '''"""Basic authentication routes for FastAPI."""

from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from passlib.context import CryptContext
from .models import User
from .storage import user_storage
from .dependencies import get_current_user

router = APIRouter(prefix="/auth", tags=["authentication"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserRegister(BaseModel):
    """User registration request."""
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)
    full_name: Optional[str] = None


class UserResponse(BaseModel):
    """User response."""
    id: str
    username: str
    email: str
    full_name: Optional[str] = None
    is_active: bool


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserRegister):
    """Register a new user."""
    try:
        # Create user
        password_hash = pwd_context.hash(user_data.password)
        user = User(
            username=user_data.username,
            email=user_data.email,
            password_hash=password_hash,
            full_name=user_data.full_name
        )
        user = user_storage.create_user(user)

        return UserResponse(**user.to_dict())

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    """Get current user information (protected route)."""
    return UserResponse(**current_user.to_dict())
'''

BASIC_FASTAPI_INIT = '''"""Basic authentication module for FastAPI."""

from .routes import router
from .dependencies import get_current_user
from .models import User
from .storage import user_storage

__all__ = ['router', 'get_current_user', 'User', 'user_storage']
'''

BASIC_TESTS = '''"""Tests for Basic authentication."""

import pytest
from passlib.context import CryptContext
from app.auth.models import User
from app.auth.storage import UserStorage

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def test_user_creation():
    """Test user model creation."""
    user = User(
        username="testuser",
        email="test@example.com",
        password_hash=pwd_context.hash("password123")
    )

    assert user.username == "testuser"
    assert user.email == "test@example.com"
    assert user.is_active is True
'''


# =============================================================================
# OAUTH2 AUTHENTICATION TEMPLATES - FLASK
# =============================================================================

OAUTH2_FLASK_CONFIG = '''"""OAuth2 authentication configuration."""

import os

# OAuth2 settings
OAUTH2_CLIENT_ID = os.getenv('OAUTH2_CLIENT_ID', '')
OAUTH2_CLIENT_SECRET = os.getenv('OAUTH2_CLIENT_SECRET', '')
OAUTH2_REDIRECT_URI = os.getenv('OAUTH2_REDIRECT_URI', 'http://localhost:5000/auth/callback')
OAUTH2_AUTHORIZATION_URL = os.getenv('OAUTH2_AUTHORIZATION_URL', 'https://provider.com/oauth/authorize')
OAUTH2_TOKEN_URL = os.getenv('OAUTH2_TOKEN_URL', 'https://provider.com/oauth/token')
OAUTH2_USER_INFO_URL = os.getenv('OAUTH2_USER_INFO_URL', 'https://provider.com/oauth/userinfo')
'''

OAUTH2_FLASK_UTILS = '''"""OAuth2 utilities for Flask."""

from authlib.integrations.flask_client import OAuth
from flask import Flask
from .config import (
    OAUTH2_CLIENT_ID, OAUTH2_CLIENT_SECRET, OAUTH2_AUTHORIZATION_URL,
    OAUTH2_TOKEN_URL, OAUTH2_USER_INFO_URL
)

oauth = OAuth()


def init_oauth(app: Flask):
    """Initialize OAuth client.

    Args:
        app: Flask application instance
    """
    oauth.init_app(app)

    oauth.register(
        name='oauth_provider',
        client_id=OAUTH2_CLIENT_ID,
        client_secret=OAUTH2_CLIENT_SECRET,
        authorize_url=OAUTH2_AUTHORIZATION_URL,
        access_token_url=OAUTH2_TOKEN_URL,
        userinfo_endpoint=OAUTH2_USER_INFO_URL,
        client_kwargs={'scope': 'openid profile email'}
    )

    return oauth
'''

OAUTH2_FLASK_MIDDLEWARE = '''"""OAuth2 authentication middleware for Flask."""

from functools import wraps
from flask import session, jsonify, g, redirect, url_for
from .storage import user_storage


def oauth_required(f):
    """Decorator to require OAuth2 authentication.

    Usage:
        @app.route('/protected')
        @oauth_required
        def protected_route():
            current_user = g.current_user
            return jsonify({"message": f"Hello {current_user.username}"})
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = session.get('user_id')

        if not user_id:
            return jsonify({"error": "Not authenticated"}), 401

        user = user_storage.get_user_by_id(user_id)

        if not user:
            session.clear()
            return jsonify({"error": "User not found"}), 401

        if not user.is_active:
            return jsonify({"error": "User account is disabled"}), 401

        g.current_user = user

        return f(*args, **kwargs)

    return decorated_function


def get_current_user():
    """Get the current authenticated user from Flask's g object."""
    return getattr(g, 'current_user', None)
'''

OAUTH2_FLASK_ROUTES = '''"""OAuth2 authentication routes for Flask."""

from flask import Blueprint, session, jsonify, redirect, url_for, request
from .models import User
from .storage import user_storage
from .middleware import oauth_required, get_current_user
from .utils import oauth
from passlib.context import CryptContext
import secrets

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@auth_bp.route('/login')
def login():
    """Redirect to OAuth2 provider for login."""
    redirect_uri = url_for('auth.callback', _external=True)
    return oauth.oauth_provider.authorize_redirect(redirect_uri)


@auth_bp.route('/callback')
def callback():
    """OAuth2 callback handler."""
    try:
        token = oauth.oauth_provider.authorize_access_token()
        userinfo = oauth.oauth_provider.parse_id_token(token)

        # Get or create user
        email = userinfo.get('email')
        username = userinfo.get('preferred_username') or userinfo.get('sub')
        full_name = userinfo.get('name')

        user = user_storage.get_user_by_email(email)

        if not user:
            # Create new user from OAuth data
            user = User(
                username=username,
                email=email,
                password_hash=pwd_context.hash(secrets.token_urlsafe(32)),  # Random password
                full_name=full_name
            )
            user = user_storage.create_user(user)

        # Create session
        session['user_id'] = user.id
        session['username'] = user.username

        return jsonify({
            "message": "Login successful",
            "user": user.to_dict()
        }), 200

    except Exception as e:
        return jsonify({"error": f"OAuth authentication failed: {str(e)}"}), 401


@auth_bp.route('/me', methods=['GET'])
@oauth_required
def get_current_user_info():
    """Get current user information (protected route)."""
    user = get_current_user()
    return jsonify(user.to_dict()), 200


@auth_bp.route('/logout', methods=['POST'])
@oauth_required
def logout():
    """Logout user and destroy session."""
    session.clear()
    return jsonify({"message": "Logout successful"}), 200
'''

OAUTH2_FLASK_INIT = '''"""OAuth2 authentication module for Flask."""

from .routes import auth_bp
from .middleware import oauth_required, get_current_user
from .models import User
from .storage import user_storage
from .utils import init_oauth

__all__ = ['auth_bp', 'oauth_required', 'get_current_user', 'User', 'user_storage', 'init_oauth']
'''


# =============================================================================
# OAUTH2 AUTHENTICATION TEMPLATES - FASTAPI
# =============================================================================

OAUTH2_FASTAPI_CONFIG = OAUTH2_FLASK_CONFIG  # Same config

OAUTH2_FASTAPI_UTILS = '''"""OAuth2 utilities for FastAPI."""

from authlib.integrations.starlette_client import OAuth
from starlette.config import Config
from .config import (
    OAUTH2_CLIENT_ID, OAUTH2_CLIENT_SECRET, OAUTH2_AUTHORIZATION_URL,
    OAUTH2_TOKEN_URL, OAUTH2_USER_INFO_URL
)

config = Config()
oauth = OAuth(config)

oauth.register(
    name='oauth_provider',
    client_id=OAUTH2_CLIENT_ID,
    client_secret=OAUTH2_CLIENT_SECRET,
    authorize_url=OAUTH2_AUTHORIZATION_URL,
    access_token_url=OAUTH2_TOKEN_URL,
    userinfo_endpoint=OAUTH2_USER_INFO_URL,
    client_kwargs={'scope': 'openid profile email'}
)
'''

OAUTH2_FASTAPI_DEPENDENCIES = '''"""OAuth2 authentication dependencies for FastAPI."""

from fastapi import Depends, HTTPException, status, Request
from .storage import user_storage
from .models import User


async def get_current_user(request: Request) -> User:
    """Dependency to get current authenticated user from session.

    Usage:
        @app.get("/protected")
        async def protected_route(current_user: User = Depends(get_current_user)):
            return {"message": f"Hello {current_user.username}"}
    """
    user_id = request.session.get('user_id')

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )

    user = user_storage.get_user_by_id(user_id)

    if not user:
        request.session.clear()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User account is disabled"
        )

    return user
'''

OAUTH2_FASTAPI_ROUTES = '''"""OAuth2 authentication routes for FastAPI."""

from fastapi import APIRouter, HTTPException, status, Depends, Request
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from typing import Optional
from passlib.context import CryptContext
import secrets
from .models import User
from .storage import user_storage
from .dependencies import get_current_user
from .utils import oauth

router = APIRouter(prefix="/auth", tags=["authentication"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserResponse(BaseModel):
    """User response."""
    id: str
    username: str
    email: str
    full_name: Optional[str] = None
    is_active: bool


@router.get("/login")
async def login(request: Request):
    """Redirect to OAuth2 provider for login."""
    redirect_uri = request.url_for('callback')
    return await oauth.oauth_provider.authorize_redirect(request, redirect_uri)


@router.get("/callback")
async def callback(request: Request):
    """OAuth2 callback handler."""
    try:
        token = await oauth.oauth_provider.authorize_access_token(request)
        userinfo = token.get('userinfo')

        if not userinfo:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Failed to get user info from OAuth provider"
            )

        # Get or create user
        email = userinfo.get('email')
        username = userinfo.get('preferred_username') or userinfo.get('sub')
        full_name = userinfo.get('name')

        user = user_storage.get_user_by_email(email)

        if not user:
            # Create new user from OAuth data
            user = User(
                username=username,
                email=email,
                password_hash=pwd_context.hash(secrets.token_urlsafe(32)),  # Random password
                full_name=full_name
            )
            user = user_storage.create_user(user)

        # Create session
        request.session['user_id'] = user.id
        request.session['username'] = user.username

        return {
            "message": "Login successful",
            "user": user.to_dict()
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"OAuth authentication failed: {str(e)}"
        )


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    """Get current user information (protected route)."""
    return UserResponse(**current_user.to_dict())


@router.post("/logout")
async def logout(request: Request, current_user: User = Depends(get_current_user)):
    """Logout user and destroy session."""
    request.session.clear()
    return {"message": "Logout successful"}
'''

OAUTH2_FASTAPI_INIT = '''"""OAuth2 authentication module for FastAPI."""

from .routes import router
from .dependencies import get_current_user
from .models import User
from .storage import user_storage

__all__ = ['router', 'get_current_user', 'User', 'user_storage']
'''

OAUTH2_TESTS = '''"""Tests for OAuth2 authentication."""

import pytest
from app.auth.models import User
from app.auth.storage import UserStorage


def test_user_storage():
    """Test user storage operations."""
    storage = UserStorage()

    user = User(
        username="oauth_user",
        email="oauth@example.com",
        password_hash="random_hash"
    )
    created_user = storage.create_user(user)

    assert created_user.id is not None
    found = storage.get_user_by_email("oauth@example.com")
    assert found is not None
'''


# =============================================================================
# FUNCOES DE CRIACAO
# =============================================================================

def _create_dirs_and_files(project_path, directories, files, verbose=False):
    """Helper para criar diretorios e arquivos."""
    project_path = Path(project_path)

    for dir_name in directories:
        dir_path = project_path / dir_name
        dir_path.mkdir(parents=True, exist_ok=True)
        if verbose:
            print_creating('dir', dir_name)

    for file_name, content in files.items():
        file_path = project_path / file_name
        file_path.write_text(content, encoding='utf-8')
        if verbose:
            print_creating('file', file_name)


# =============================================================================
# AUTH HELPER FUNCTIONS
# =============================================================================

def get_jwt_auth_files(project_type):
    """Get JWT authentication files based on framework.

    Args:
        project_type: Project type (web-flask, api-flask, web-fastapi, api-fastapi, etc)

    Returns:
        Dict of auth files with their content
    """
    is_flask = 'flask' in project_type.lower()

    files = {
        'app/auth/__init__.py': JWT_FLASK_INIT if is_flask else JWT_FASTAPI_INIT,
        'app/auth/models.py': AUTH_USER_MODEL_BASE,
        'app/auth/storage.py': AUTH_STORAGE_BASE,
        'app/auth/utils.py': JWT_FLASK_UTILS if is_flask else JWT_FASTAPI_UTILS,
        'app/auth/config.py': JWT_FLASK_CONFIG,
        'tests/auth/__init__.py': '',
        'tests/auth/test_auth.py': JWT_TESTS,
    }

    if is_flask:
        files['app/auth/routes.py'] = JWT_FLASK_ROUTES
        files['app/auth/middleware.py'] = JWT_FLASK_MIDDLEWARE
    else:
        files['app/auth/routes.py'] = JWT_FASTAPI_ROUTES
        files['app/auth/dependencies.py'] = JWT_FASTAPI_DEPENDENCIES

    return files


def get_session_auth_files(project_type):
    """Get Session authentication files based on framework.

    Args:
        project_type: Project type (web-flask, api-flask, web-fastapi, api-fastapi, etc)

    Returns:
        Dict of auth files with their content
    """
    is_flask = 'flask' in project_type.lower()

    files = {
        'app/auth/__init__.py': SESSION_FLASK_INIT if is_flask else SESSION_FASTAPI_INIT,
        'app/auth/models.py': AUTH_USER_MODEL_BASE,
        'app/auth/storage.py': AUTH_STORAGE_BASE,
        'app/auth/utils.py': SESSION_FLASK_UTILS if is_flask else SESSION_FASTAPI_UTILS,
        'app/auth/config.py': SESSION_FLASK_CONFIG,
        'tests/auth/__init__.py': '',
        'tests/auth/test_auth.py': SESSION_TESTS,
    }

    if is_flask:
        files['app/auth/routes.py'] = SESSION_FLASK_ROUTES
        files['app/auth/middleware.py'] = SESSION_FLASK_MIDDLEWARE
    else:
        files['app/auth/routes.py'] = SESSION_FASTAPI_ROUTES
        files['app/auth/dependencies.py'] = SESSION_FASTAPI_DEPENDENCIES

    return files


def get_basic_auth_files(project_type):
    """Get Basic authentication files based on framework.

    Args:
        project_type: Project type (web-flask, api-flask, web-fastapi, api-fastapi, etc)

    Returns:
        Dict of auth files with their content
    """
    is_flask = 'flask' in project_type.lower()

    files = {
        'app/auth/__init__.py': BASIC_FLASK_INIT if is_flask else BASIC_FASTAPI_INIT,
        'app/auth/models.py': AUTH_USER_MODEL_BASE,
        'app/auth/storage.py': AUTH_STORAGE_BASE,
        'app/auth/utils.py': BASIC_FLASK_UTILS if is_flask else BASIC_FASTAPI_UTILS,
        'app/auth/config.py': BASIC_FLASK_CONFIG,
        'tests/auth/__init__.py': '',
        'tests/auth/test_auth.py': BASIC_TESTS,
    }

    if is_flask:
        files['app/auth/routes.py'] = BASIC_FLASK_ROUTES
        files['app/auth/middleware.py'] = BASIC_FLASK_MIDDLEWARE
    else:
        files['app/auth/routes.py'] = BASIC_FASTAPI_ROUTES
        files['app/auth/dependencies.py'] = BASIC_FASTAPI_DEPENDENCIES

    return files


def get_oauth2_auth_files(project_type):
    """Get OAuth2 authentication files based on framework.

    Args:
        project_type: Project type (web-flask, api-flask, web-fastapi, api-fastapi, etc)

    Returns:
        Dict of auth files with their content
    """
    is_flask = 'flask' in project_type.lower()

    files = {
        'app/auth/__init__.py': OAUTH2_FLASK_INIT if is_flask else OAUTH2_FASTAPI_INIT,
        'app/auth/models.py': AUTH_USER_MODEL_BASE,
        'app/auth/storage.py': AUTH_STORAGE_BASE,
        'app/auth/utils.py': OAUTH2_FLASK_UTILS if is_flask else OAUTH2_FASTAPI_UTILS,
        'app/auth/config.py': OAUTH2_FLASK_CONFIG,
        'tests/auth/__init__.py': '',
        'tests/auth/test_auth.py': OAUTH2_TESTS,
    }

    if is_flask:
        files['app/auth/routes.py'] = OAUTH2_FLASK_ROUTES
        files['app/auth/middleware.py'] = OAUTH2_FLASK_MIDDLEWARE
    else:
        files['app/auth/routes.py'] = OAUTH2_FASTAPI_ROUTES
        files['app/auth/dependencies.py'] = OAUTH2_FASTAPI_DEPENDENCIES

    return files


def get_auth_files(auth_type, project_type):
    """Get authentication files based on auth type and framework.

    Args:
        auth_type: Auth type (jwt, oauth2, session, basic, none)
        project_type: Project type (web-flask, api-fastapi, etc)

    Returns:
        Dict of auth files or empty dict if auth_type is 'none'
    """
    if auth_type == 'none':
        return {}

    if auth_type == 'jwt':
        return get_jwt_auth_files(project_type)
    elif auth_type == 'oauth2':
        return get_oauth2_auth_files(project_type)
    elif auth_type == 'session':
        return get_session_auth_files(project_type)
    elif auth_type == 'basic':
        return get_basic_auth_files(project_type)

    return {}


def get_auth_directories(auth_type):
    """Get authentication directories.

    Args:
        auth_type: Auth type (jwt, oauth2, session, basic, none)

    Returns:
        List of auth directories or empty list if auth_type is 'none'
    """
    if auth_type == 'none':
        return []

    return ['app/auth', 'tests/auth']


def create_mvc_structure(project_path, project_type, auth_type='none', verbose=False):
    """Cria a estrutura de pastas MVC para um projeto."""
    project_path = Path(project_path)

    directories = [
        'app',
        'app/models',
        'app/views',
        'app/controllers',
        'app/static',
        'app/static/css',
        'app/static/js',
        'app/static/img',
        'app/templates',
        'config',
        'tests',
    ]

    # Add auth directories if needed
    directories.extend(get_auth_directories(auth_type))

    if project_type == 'web-flask':
        directories.extend(['.github', '.github/workflows'])
        files = {
            'app/__init__.py': FLASK_APP_INIT,
            'app/models/__init__.py': '"""Models da aplicacao."""\n',
            'app/views/__init__.py': '"""Views da aplicacao."""\n',
            'app/controllers/__init__.py': FLASK_CONTROLLER,
            'app/static/css/style.css': FLASK_CSS,
            'app/static/js/main.js': FLASK_JS,
            'app/templates/base.html': FLASK_BASE_TEMPLATE,
            'config/__init__.py': CONFIG_INIT,
            'config/logging.py': LOGGING_CONFIG,
            'tests/__init__.py': TESTS_INIT,
            'tests/test_app.py': TEST_FLASK_MVC,
            'main.py': FLASK_MAIN_PY,
            '.gitignore': GITIGNORE_CONTENT,
            '.env.example': ENV_EXAMPLE,
            'requirements-dev.txt': REQUIREMENTS_DEV,
            'pyproject.toml': PYTEST_CONFIG,
            '.github/workflows/test.yml': GITHUB_WORKFLOW_TEST,
            'README.md': f'# {project_path.name}\n\nProjeto Flask MVC criado com Prozees.\n\n## Setup\n\n```bash\npip install -r requirements.txt\ncp .env.example .env\n```\n\n## Rodar\n\n```bash\npython main.py\n```\n\n## Testes\n\n```bash\npytest\n```\n',
        }
    elif project_type == 'web-fastapi':
        directories.extend(['.github', '.github/workflows'])
        files = {
            'app/__init__.py': FASTAPI_APP_INIT,
            'app/models/__init__.py': '"""Models da aplicacao."""\n',
            'app/views/__init__.py': '"""Views da aplicacao."""\n',
            'app/controllers/__init__.py': FASTAPI_CONTROLLER,
            'app/static/css/style.css': FLASK_CSS,
            'app/static/js/main.js': FLASK_JS,
            'app/templates/base.html': FASTAPI_BASE_TEMPLATE,
            'config/__init__.py': CONFIG_INIT,
            'config/logging.py': LOGGING_CONFIG,
            'tests/__init__.py': TESTS_INIT,
            'tests/test_app.py': TEST_FASTAPI_MVC,
            'main.py': FASTAPI_MAIN_PY,
            '.gitignore': GITIGNORE_CONTENT,
            '.env.example': ENV_EXAMPLE,
            'requirements-dev.txt': REQUIREMENTS_DEV,
            'pyproject.toml': PYTEST_CONFIG,
            '.github/workflows/test.yml': GITHUB_WORKFLOW_TEST,
            'README.md': f'# {project_path.name}\n\nProjeto FastAPI MVC criado com Prozees.\n\n## Setup\n\n```bash\npip install -r requirements.txt\ncp .env.example .env\n```\n\n## Rodar\n\n```bash\nuvicorn main:app --reload\n```\n\n## Testes\n\n```bash\npytest\n```\n\n## Docs\n\nAcesse http://localhost:8000/docs para ver a documentação interativa.\n',
        }
    else:
        files = {}

    # Add auth files if needed
    auth_files = get_auth_files(auth_type, project_type)
    files.update(auth_files)

    _create_dirs_and_files(project_path, directories, files, verbose)

    if verbose:
        print_success(t('structure_mvc_created'))

    return True


def create_api_structure(project_path, project_type, auth_type='none', verbose=False):
    """Create REST API structure."""
    project_path = Path(project_path)

    directories = [
        'app',
        'app/models',
        'app/routes',
        'config',
        'tests',
    ]

    # Add auth directories if needed
    directories.extend(get_auth_directories(auth_type))

    if project_type == 'api-flask':
        directories.extend(['.github', '.github/workflows'])
        files = {
            'app/__init__.py': '"""Pacote da aplicacao."""\n',
            'app/models/__init__.py': API_MODELS_INIT,
            'app/routes/__init__.py': FLASK_API_ROUTES,
            'config/__init__.py': CONFIG_INIT,
            'config/logging.py': LOGGING_CONFIG,
            'tests/__init__.py': TESTS_INIT,
            'tests/test_api.py': TEST_FLASK_API,
            'main.py': FLASK_API_MAIN,
            '.gitignore': GITIGNORE_CONTENT,
            '.env.example': ENV_EXAMPLE,
            'requirements-dev.txt': REQUIREMENTS_DEV,
            'pyproject.toml': PYTEST_CONFIG,
            '.github/workflows/test.yml': GITHUB_WORKFLOW_TEST,
            'README.md': f'# {project_path.name}\n\nAPI REST Flask criada com Prozees.\n\n## Setup\n\n```bash\npip install -r requirements.txt\ncp .env.example .env\n```\n\n## Rodar\n\n```bash\npython main.py\n```\n\n## Testes\n\n```bash\npytest\n```\n',
        }
    elif project_type == 'api-fastapi':
        directories.extend(['.github', '.github/workflows'])
        files = {
            'app/__init__.py': '"""Pacote da aplicacao."""\n',
            'app/models/__init__.py': API_MODELS_INIT,
            'app/routes/__init__.py': FASTAPI_API_ROUTES,
            'config/__init__.py': CONFIG_INIT,
            'config/logging.py': LOGGING_CONFIG,
            'tests/__init__.py': TESTS_INIT,
            'tests/test_api.py': TEST_FASTAPI_API,
            'main.py': FASTAPI_API_MAIN,
            '.gitignore': GITIGNORE_CONTENT,
            '.env.example': ENV_EXAMPLE,
            'requirements-dev.txt': REQUIREMENTS_DEV,
            'pyproject.toml': PYTEST_CONFIG,
            '.github/workflows/test.yml': GITHUB_WORKFLOW_TEST,
            'README.md': f'# {project_path.name}\n\nAPI REST FastAPI criada com Prozees.\n\n## Setup\n\n```bash\npip install -r requirements.txt\ncp .env.example .env\n```\n\n## Rodar\n\n```bash\nuvicorn main:app --reload\n```\n\n## Testes\n\n```bash\npytest\n```\n\n## Docs\n\nAcesse http://localhost:8000/docs\n',
        }
    else:
        files = {}

    # Add auth files if needed
    auth_files = get_auth_files(auth_type, project_type)
    files.update(auth_files)

    _create_dirs_and_files(project_path, directories, files, verbose)

    if verbose:
        print_success(t('structure_api_created'))

    return True


def create_cli_structure(project_path, verbose=False):
    """Create CLI project structure."""
    project_path = Path(project_path)
    project_name = project_path.name

    directories = [
        project_name,
        f'{project_name}/commands',
        'tests',
    ]

    directories.extend(['.github', '.github/workflows'])

    files = {
        f'{project_name}/__init__.py': '"""Pacote principal."""\n',
        f'{project_name}/main.py': CLI_MAIN_PY.replace('{project_name}', project_name),
        f'{project_name}/commands/__init__.py': CLI_COMMANDS_INIT,
        f'{project_name}/commands/hello.py': CLI_HELLO_CMD,
        f'{project_name}/commands/greet.py': CLI_GREET_CMD,
        'tests/__init__.py': TESTS_INIT,
        'tests/test_cli.py': TEST_CLI.replace('{project_name}', project_name),
        'setup.py': CLI_SETUP_PY.replace('{project_name}', project_name),
        'pyproject.toml': CLI_PYPROJECT.replace('{project_name}', project_name) + '\n\n' + PYTEST_CONFIG,
        '.gitignore': GITIGNORE_CONTENT,
        '.env.example': ENV_EXAMPLE,
        'requirements-dev.txt': REQUIREMENTS_DEV,
        '.github/workflows/test.yml': GITHUB_WORKFLOW_TEST,
        'README.md': f'# {project_name}\n\nCLI criado com Prozees.\n\n## Setup\n\n```bash\npip install -e .\ncp .env.example .env\n```\n\n## Uso\n\n```bash\n{project_name} --help\n{project_name} hello\n{project_name} greet Mundo\n```\n\n## Testes\n\n```bash\npytest\n```\n',
    }

    _create_dirs_and_files(project_path, directories, files, verbose)

    if verbose:
        print_success(t('structure_cli_created'))

    return True


def create_clean_structure(project_path, project_type, auth_type='none', verbose=False):
    """Create Clean Architecture structure."""
    project_path = Path(project_path)

    directories = [
        'src',
        'src/entities',
        'src/use_cases',
        'src/adapters',
        'src/adapters/repositories',
        'src/adapters/presenters',
        'src/frameworks',
        'src/frameworks/web',
        'config',
        'tests',
        'tests/unit',
        'tests/integration',
        '.github',
        '.github/workflows',
    ]

    # Add auth directories if needed (in Clean Architecture, auth goes in src/adapters/auth)
    if auth_type != 'none':
        directories.extend(['src/adapters/auth', 'tests/auth'])

    # Escolhe o template correto baseado no tipo
    if project_type == 'clean-fastapi':
        web_app_template = CLEAN_FRAMEWORK_WEB_FASTAPI
        main_template = CLEAN_MAIN_FASTAPI
    else:
        web_app_template = CLEAN_FRAMEWORK_WEB_FLASK
        main_template = CLEAN_MAIN_PY

    files = {
        'src/__init__.py': '"""Codigo fonte."""\n',
        'src/entities/__init__.py': '"""Entidades do dominio."""\n',
        'src/entities/user.py': CLEAN_ENTITY,
        'src/use_cases/__init__.py': '"""Casos de uso."""\n',
        'src/use_cases/user.py': CLEAN_USE_CASE,
        'src/adapters/__init__.py': '"""Adapters."""\n',
        'src/adapters/repositories/__init__.py': '"""Repositorios."""\n',
        'src/adapters/repositories/user_repository.py': CLEAN_ADAPTER_REPO,
        'src/adapters/presenters/__init__.py': '"""Presenters."""\n',
        'src/adapters/presenters/user_presenter.py': CLEAN_ADAPTER_PRESENTER,
        'src/frameworks/__init__.py': '"""Frameworks externos."""\n',
        'src/frameworks/web/__init__.py': '"""Framework web."""\n',
        'src/frameworks/web/app.py': web_app_template,
        'config/__init__.py': CONFIG_INIT,
        'config/logging.py': LOGGING_CONFIG,
        'tests/__init__.py': TESTS_INIT,
        'tests/unit/__init__.py': '"""Testes unitarios."""\n',
        'tests/unit/test_use_cases.py': CLEAN_TEST_USE_CASE,
        'tests/integration/__init__.py': '"""Testes de integracao."""\n',
        'main.py': main_template,
        '.gitignore': GITIGNORE_CONTENT,
        '.env.example': ENV_EXAMPLE,
        'requirements-dev.txt': REQUIREMENTS_DEV,
        'pyproject.toml': PYTEST_CONFIG,
        '.github/workflows/test.yml': GITHUB_WORKFLOW_TEST,
        'README.md': f'# {project_path.name}\n\nProjeto com Clean Architecture criado com Prozees.\n\n## Estrutura\n\n```\nsrc/\n  entities/      # Entidades do dominio\n  use_cases/     # Casos de uso (regras de negocio)\n  adapters/      # Adaptadores (repositories, presenters)\n  frameworks/    # Frameworks externos (web, db)\n```\n\n## Setup\n\n```bash\npip install -r requirements.txt\ncp .env.example .env\n```\n\n## Rodar\n\n```bash\npython main.py\n```\n\n## Testes\n\n```bash\npytest\n```\n',
    }

    # Add auth files if needed (adapt paths for Clean Architecture)
    if auth_type != 'none':
        auth_files_raw = get_auth_files(auth_type, project_type)
        # Remap app/auth/* to src/adapters/auth/*
        auth_files = {}
        for path, content in auth_files_raw.items():
            if path.startswith('app/auth/'):
                new_path = path.replace('app/auth/', 'src/adapters/auth/')
                auth_files[new_path] = content
            else:
                auth_files[path] = content
        files.update(auth_files)

    _create_dirs_and_files(project_path, directories, files, verbose)

    if verbose:
        print_success(t('structure_clean_created'))

    return True
