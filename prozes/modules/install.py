"""Modulo para geracao de arquivos de dependencias."""

from pathlib import Path


REQUIREMENTS_TEMPLATES = {
    # MVC
    'web-flask': """flask>=3.0.0
python-dotenv>=1.0.0
pytest>=8.0.0
""",
    'web-fastapi': """fastapi>=0.109.0
uvicorn[standard]>=0.27.0
jinja2>=3.1.0
python-multipart>=0.0.6
pydantic[email]>=2.0.0
python-dotenv>=1.0.0
pytest>=8.0.0
""",
    # API REST
    'api-flask': """flask>=3.0.0
python-dotenv>=1.0.0
pytest>=8.0.0
""",
    'api-fastapi': """fastapi>=0.109.0
uvicorn[standard]>=0.27.0
pydantic[email]>=2.0.0
python-dotenv>=1.0.0
pytest>=8.0.0
""",
    # CLI
    'cli': """click>=8.0.0
pytest>=8.0.0
""",
    # Clean Architecture
    'clean-flask': """flask>=3.0.0
python-dotenv>=1.0.0
pytest>=8.0.0
""",
    'clean-fastapi': """fastapi>=0.109.0
uvicorn[standard]>=0.27.0
pydantic[email]>=2.0.0
python-dotenv>=1.0.0
pytest>=8.0.0
""",
}

DEFAULT_REQUIREMENTS = """python-dotenv>=1.0.0
pytest>=8.0.0
"""

# Authentication dependencies
AUTH_DEPENDENCIES = {
    'jwt': ['PyJWT>=2.8.0', 'passlib>=1.7.4', 'bcrypt>=4.0.0,<5.0.0', 'python-jose[cryptography]>=3.3.0'],
    'oauth2': ['authlib>=1.3.0', 'passlib>=1.7.4', 'bcrypt>=4.0.0,<5.0.0', 'requests>=2.31.0', 'itsdangerous>=2.1.0'],
    'session': ['passlib>=1.7.4', 'bcrypt>=4.0.0,<5.0.0', 'itsdangerous>=2.1.0'],
    'basic': ['passlib>=1.7.4', 'bcrypt>=4.0.0,<5.0.0'],
}


ENV_TEMPLATES = {
    # MVC
    'web-flask': """# Flask Configuration
FLASK_APP=main.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here-change-in-production
DEBUG=True

# Database
DATABASE_URL=sqlite:///app.db

# Server
HOST=0.0.0.0
PORT=5000
""",
    'web-fastapi': """# FastAPI Configuration
APP_NAME=MyApp
DEBUG=True
SECRET_KEY=your-secret-key-here-change-in-production

# Database
DATABASE_URL=sqlite:///./app.db

# Server
HOST=0.0.0.0
PORT=8000

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:8000
""",
    # API REST
    'api-flask': """# Flask API Configuration
FLASK_APP=main.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here-change-in-production
DEBUG=True

# Database
DATABASE_URL=sqlite:///api.db

# API Configuration
API_VERSION=v1
RATE_LIMIT=100

# CORS
CORS_ORIGINS=*
""",
    'api-fastapi': """# FastAPI API Configuration
APP_NAME=MyAPI
DEBUG=True
SECRET_KEY=your-secret-key-here-change-in-production

# Database
DATABASE_URL=sqlite:///./api.db

# API Configuration
API_VERSION=v1
API_PREFIX=/api/v1

# CORS
CORS_ORIGINS=*

# Server
HOST=0.0.0.0
PORT=8000
""",
    # CLI
    'cli': """# CLI Configuration
LOG_LEVEL=INFO
CONFIG_PATH=~/.config/myapp
DEBUG=False

# Output
VERBOSE=False
COLOR_OUTPUT=True
""",
    # Clean Architecture
    'clean-flask': """# Flask Configuration
FLASK_APP=main.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here-change-in-production
DEBUG=True

# Database
DATABASE_URL=sqlite:///clean.db

# Server
HOST=0.0.0.0
PORT=5000
""",
    'clean-fastapi': """# FastAPI Configuration
APP_NAME=MyCleanApp
DEBUG=True
SECRET_KEY=your-secret-key-here-change-in-production

# Database
DATABASE_URL=sqlite:///./clean.db

# Server
HOST=0.0.0.0
PORT=8000

# CORS
CORS_ORIGINS=*
""",
}

DEFAULT_ENV = """# Application Configuration
DEBUG=True
LOG_LEVEL=INFO

# Add your environment variables here
"""

# Authentication environment templates
AUTH_ENV_TEMPLATES = {
    'jwt': """
# JWT Authentication
JWT_SECRET_KEY=your-super-secret-jwt-key-change-in-production-min-32-chars
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7
""",
    'oauth2': """
# OAuth2 Authentication
OAUTH2_CLIENT_ID=your-oauth2-client-id
OAUTH2_CLIENT_SECRET=your-oauth2-client-secret
OAUTH2_REDIRECT_URI=http://localhost:8000/auth/callback
OAUTH2_AUTHORIZATION_URL=https://provider.com/oauth/authorize
OAUTH2_TOKEN_URL=https://provider.com/oauth/token
OAUTH2_USER_INFO_URL=https://provider.com/oauth/userinfo
""",
    'session': """
# Session Authentication
SESSION_SECRET_KEY=your-super-secret-session-key-change-in-production
SESSION_COOKIE_NAME=session
SESSION_COOKIE_HTTPONLY=True
SESSION_COOKIE_SECURE=False
SESSION_PERMANENT=True
SESSION_LIFETIME_DAYS=7
""",
    'basic': """
# Basic Authentication
BASIC_AUTH_REALM=Protected Area
BASIC_AUTH_FORCE=True
""",
}


def create_default_requirements(project_path, project_type, auth_type='none'):
    """Cria um requirements.txt padrao baseado no tipo de projeto.

    Args:
        project_path: Path do projeto
        project_type: Tipo do projeto (web-flask, api-fastapi, etc)
        auth_type: Tipo de autenticacao (none, jwt, oauth2, session, basic)
    """
    content = REQUIREMENTS_TEMPLATES.get(project_type, DEFAULT_REQUIREMENTS)

    # Add auth dependencies if auth is enabled
    if auth_type != 'none' and auth_type in AUTH_DEPENDENCIES:
        auth_deps = AUTH_DEPENDENCIES[auth_type]
        content = content.rstrip() + '\n\n# Authentication dependencies\n'
        for dep in auth_deps:
            content += f'{dep}\n'

    requirements_file = Path(project_path) / 'requirements.txt'
    requirements_file.write_text(content, encoding='utf-8')


def create_env_example(project_path, project_type, auth_type='none'):
    """Cria um arquivo .env.example baseado no tipo de projeto.

    Args:
        project_path: Path do projeto
        project_type: Tipo do projeto (web-flask, api-fastapi, etc)
        auth_type: Tipo de autenticacao (none, jwt, oauth2, session, basic)
    """
    content = ENV_TEMPLATES.get(project_type, DEFAULT_ENV)

    # Add auth environment variables if auth is enabled
    if auth_type != 'none' and auth_type in AUTH_ENV_TEMPLATES:
        content = content.rstrip() + '\n' + AUTH_ENV_TEMPLATES[auth_type]

    env_file = Path(project_path) / '.env.example'
    env_file.write_text(content, encoding='utf-8')
