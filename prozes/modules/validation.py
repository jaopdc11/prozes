"""Validações de input do usuário."""

import re
import shutil
from pathlib import Path
from typing import List, Optional, Tuple

from prozes.modules.i18n import t


class ValidationError(Exception):
    """Erro de validação."""
    pass


def validate_project_name(name: str) -> Tuple[bool, Optional[str]]:
    """
    Valida se o nome do projeto é válido pra Python.
    Precisa começar com letra/underscore e não pode ser palavra reservada.
    """
    if not name:
        return False, t("validation_name_empty")

    # Check if it starts with a letter or underscore
    if not re.match(r"^[a-zA-Z_]", name):
        return False, t("validation_name_start")

    # Check if it contains only valid characters
    if not re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*$", name):
        return False, t("validation_name_chars")

    # Python reserved keywords
    keywords = {
        "False",
        "None",
        "True",
        "and",
        "as",
        "assert",
        "async",
        "await",
        "break",
        "class",
        "continue",
        "def",
        "del",
        "elif",
        "else",
        "except",
        "finally",
        "for",
        "from",
        "global",
        "if",
        "import",
        "in",
        "is",
        "lambda",
        "nonlocal",
        "not",
        "or",
        "pass",
        "raise",
        "return",
        "try",
        "while",
        "with",
        "yield",
    }

    if name in keywords:
        return False, t("validation_name_keyword", name=name)

    return True, None


def validate_project_not_exists(name: str) -> Tuple[bool, Optional[str]]:
    """Verifica se já não existe uma pasta com esse nome."""
    project_path = Path.cwd() / name
    if project_path.exists():
        return False, t("validation_project_exists", name=name)
    return True, None


def validate_python_version(version: Optional[str]) -> Tuple[bool, Optional[str]]:
    """Valida formato da versão do Python (ex: 3, 3.8, 3.11)."""
    if version is None:
        return True, None

    # Valid format: single digit (3) or major.minor (3.8, 3.11)
    if not re.match(r"^\d+(\.\d+)?$", version):
        return False, t("validation_python_version_format", version=version)

    return True, None


def validate_git_available() -> Tuple[bool, Optional[str]]:
    """Checa se o Git está instalado."""
    if shutil.which("git") is None:
        return False, t("validation_git_not_available")
    return True, None


def validate_venv_for_install_deps(venv: bool, install_deps: bool) -> Tuple[bool, Optional[str]]:
    """Garante que --install-deps só é usado com --venv."""
    if install_deps and not venv:
        return False, t("validation_install_deps_requires_venv")
    return True, None


def run_all_validations(
    project_name: str,
    git: bool = False,
    venv: bool = False,
    python_version: Optional[str] = None,
    install_deps: bool = False,
) -> List[str]:
    """Roda todas as validações e retorna lista de erros (vazia se tudo OK)."""
    errors: List[str] = []

    # Validate project name
    valid, error = validate_project_name(project_name)
    if not valid and error:
        errors.append(error)

    # Validate project doesn't exist
    valid, error = validate_project_not_exists(project_name)
    if not valid and error:
        errors.append(error)

    # Validate Python version format
    valid, error = validate_python_version(python_version)
    if not valid and error:
        errors.append(error)

    # Validate Git is available if --git is used
    if git:
        valid, error = validate_git_available()
        if not valid and error:
            errors.append(error)

    # Validate --install-deps requires --venv
    valid, error = validate_venv_for_install_deps(venv, install_deps)
    if not valid and error:
        errors.append(error)

    return errors
