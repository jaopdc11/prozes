"""Modulos auxiliares do Prozees."""

from prozes.modules.venv import criar_venv, instalar_dependencias
from prozes.modules.dirs import create_project_folder, command_git
from prozes.modules.install import create_default_requirements
from prozes.modules.structures import (
    create_mvc_structure,
    create_api_structure,
    create_cli_structure,
    create_clean_structure,
)

__all__ = [
    'criar_venv',
    'instalar_dependencias',
    'create_project_folder',
    'command_git',
    'create_default_requirements',
    'create_mvc_structure',
    'create_api_structure',
    'create_cli_structure',
    'create_clean_structure',
]
