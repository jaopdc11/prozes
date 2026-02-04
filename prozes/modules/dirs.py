"""Módulo para criação de diretórios e configuração Git."""

import subprocess
from pathlib import Path
import click
import re


def create_project_folder(project_name, verbose=False):
    """Cria a pasta do projeto no diretório atual do usuário."""
    current_dir = Path.cwd()
    project_path = current_dir / project_name

    project_path.mkdir(parents=True, exist_ok=True)

    if verbose:
        click.echo(f"[*] Pasta criada em: {project_path}")

    return project_path


def create_gitignore(project_path, verbose=False):
    """Cria arquivo .gitignore para projetos Python.

    Args:
        project_path: Path do projeto
        verbose: Modo verboso
    """
    gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
env/
ENV/
.venv

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~

# Environment variables
.env
.env.local

# Database
*.db
*.sqlite
*.sqlite3

# Logs
*.log

# Testing
.pytest_cache/
.coverage
htmlcov/
.tox/

# OS
.DS_Store
Thumbs.db
"""

    gitignore_path = project_path / '.gitignore'
    gitignore_path.write_text(gitignore_content.strip())

    if verbose:
        click.echo("[OK] .gitignore criado")


def validate_git_remote_url(url):
    """Valida se a URL do remote Git é válida.

    Args:
        url: URL do repositório Git

    Returns:
        bool: True se válida, False caso contrário
    """
    if not url:
        return True  # URL vazia é válida (usuário pode pular)

    # Padrões válidos:
    # - https://github.com/user/repo.git
    # - git@github.com:user/repo.git
    # - https://gitlab.com/user/repo.git
    # - https://bitbucket.org/user/repo.git

    patterns = [
        r'^https?://[a-zA-Z0-9.-]+/[\w.-]+/[\w.-]+(\.git)?$',  # HTTPS
        r'^git@[a-zA-Z0-9.-]+:[\w.-]+/[\w.-]+(\.git)?$',        # SSH
    ]

    for pattern in patterns:
        if re.match(pattern, url):
            return True

    return False


def check_git_config(verbose=False):
    """Verifica se Git user.name e user.email estão configurados.

    Args:
        verbose: Modo verboso

    Returns:
        tuple: (has_name, has_email)
    """
    try:
        # Verificar user.name
        name_result = subprocess.run(
            ['git', 'config', '--global', 'user.name'],
            capture_output=True,
            text=True
        )
        has_name = bool(name_result.stdout.strip())

        # Verificar user.email
        email_result = subprocess.run(
            ['git', 'config', '--global', 'user.email'],
            capture_output=True,
            text=True
        )
        has_email = bool(email_result.stdout.strip())

        if verbose:
            if has_name:
                click.echo(f"[OK] Git user.name: {name_result.stdout.strip()}")
            else:
                click.echo("[AVISO] Git user.name nao configurado")

            if has_email:
                click.echo(f"[OK] Git user.email: {email_result.stdout.strip()}")
            else:
                click.echo("[AVISO] Git user.email nao configurado")

        return has_name, has_email

    except Exception:
        return False, False


def command_git(project_path, verbose=False):
    """Inicializa um repositório Git na pasta do projeto e pede URL do remote.

    Args:
        project_path: Path do projeto
        verbose: Modo verboso

    Returns:
        bool: True se sucesso, False caso contrário
    """
    try:
        if verbose:
            click.echo("\n[*] Iniciando configuracao do Git...")
            click.echo(f"[*] Diretorio do projeto: {project_path}")

        # 0. Verificar configuração do Git
        has_name, has_email = check_git_config(verbose=verbose)

        if not has_name or not has_email:
            click.echo("\n[!] Configuracao do Git incompleta!")
            if not has_name:
                click.echo("    Execute: git config --global user.name \"Seu Nome\"")
            if not has_email:
                click.echo("    Execute: git config --global user.email \"seu@email.com\"")
            click.echo()

        # 1. git init
        git_init_result = subprocess.run(
            ['git', 'init'],
            cwd=str(project_path),
            capture_output=True,
            text=True
        )

        git_dir = project_path / '.git'
        success = git_dir.exists()

        if verbose:
            if success:
                click.echo("[OK] Repositorio Git criado com sucesso")
            else:
                click.echo("[ERRO] Falha: Pasta .git nao foi criada")
                return False

        if not success:
            return False

        # 2. Criar .gitignore
        create_gitignore(project_path, verbose=verbose)

        # 3. Configurar branch main
        branch_result = subprocess.run(
            ['git', 'branch', '--show-current'],
            cwd=str(project_path),
            capture_output=True,
            text=True
        )
        current_branch = branch_result.stdout.strip()

        if current_branch != 'main':
            subprocess.run(
                ['git', 'branch', '-M', 'main'],
                cwd=str(project_path),
                capture_output=True,
                text=True
            )
        if verbose:
            click.echo("[*] Branch 'main' configurado")

        # 4. Pedir URL do remote ao usuário
        while True:
            git_remote = click.prompt(
                '\nGit remote URL (deixe em branco para pular)',
                default='',
                show_default=False
            ).strip()

            if not git_remote:
                break

            # Validar URL
            if not validate_git_remote_url(git_remote):
                click.echo("[ERRO] URL invalida. Formato esperado:")
                click.echo("  - https://github.com/user/repo.git")
                click.echo("  - git@github.com:user/repo.git")
                continue

            # Adicionar remote
            remote_result = subprocess.run(
                ['git', 'remote', 'add', 'origin', git_remote],
                cwd=str(project_path),
                capture_output=True,
                text=True
            )

            if remote_result.returncode == 0:
                if verbose:
                    click.echo(f"[OK] Remote 'origin' configurado: {git_remote}")
                break
            else:
                click.echo(f"[ERRO] Falha ao adicionar remote: {remote_result.stderr.strip()}")
                continue

        # 5. Commit inicial
        if click.confirm('\nFazer commit inicial?', default=True):
            # git add .
            add_result = subprocess.run(
                ['git', 'add', '.'],
                cwd=str(project_path),
                capture_output=True,
                text=True
            )

            if add_result.returncode == 0:
                if verbose:
                    click.echo("[*] Arquivos adicionados ao stage")

                # git commit
                commit_msg = "Initial commit"
                commit_result = subprocess.run(
                    ['git', 'commit', '-m', commit_msg],
                    cwd=str(project_path),
                    capture_output=True,
                    text=True
                )

                if commit_result.returncode == 0:
                    if verbose:
                        click.echo("[OK] Commit inicial criado")
                else:
                    click.echo(f"[AVISO] Falha ao criar commit: {commit_result.stderr.strip()}")
            else:
                click.echo(f"[AVISO] Falha ao adicionar arquivos: {add_result.stderr.strip()}")

        return True

    except FileNotFoundError:
        if verbose:
            click.echo("[ERRO] Git nao encontrado. Certifique-se de que o Git esta instalado.")
        return False
    except Exception as e:
        if verbose:
            click.echo(f"[ERRO] Erro inesperado: {e}")
        return False
