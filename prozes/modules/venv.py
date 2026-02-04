"""Módulo para criação e gerenciamento de ambientes virtuais."""

import os
import subprocess
import sys
import shutil
from pathlib import Path
import click


def encontrar_python(versao=None):
    """Encontra o executável do Python na versão especificada ou usa o atual."""
    if not versao:
        return sys.executable

    # Versões a tentar (compatível com Windows e Unix)
    versoes_testar = [
        f"python{versao}",
        f"python{versao.replace('.', '')}",
        f"python{versao.split('.')[0]}",
    ]

    # No Windows, adiciona variantes com .exe
    if os.name == 'nt':
        versoes_testar = [f"{v}.exe" for v in versoes_testar] + versoes_testar

    for py in versoes_testar:
        caminho = shutil.which(py)
        if caminho:
            return caminho

    return None


def criar_venv(caminho_projeto, versao_python=None, verbose=False):
    """Cria um ambiente virtual Python."""
    venv_path = caminho_projeto / 'venv'

    if verbose:
        click.echo(f"\n[*] Criando ambiente virtual em {venv_path}")

    if venv_path.exists():
        if verbose:
            click.echo("[*] Ambiente virtual ja existe")
        return True

    python_exec = encontrar_python(versao_python)
    if not python_exec:
        raise FileNotFoundError(
            f"Python versao {versao_python} nao encontrado.\n"
            f"Certifique-se de que o Python esta instalado e no PATH."
        )

    if verbose:
        click.echo(f"[*] Usando Python: {python_exec}")

    resultado = subprocess.run(
        [python_exec, "-m", "venv", str(venv_path)],
        capture_output=True,
        text=True
    )

    if resultado.returncode != 0:
        erro = resultado.stderr or "Erro desconhecido ao criar venv"
        raise RuntimeError(f"Falha ao criar venv: {erro}")

    if verbose:
        click.echo("[OK] Ambiente virtual criado com sucesso")
        pip_exec = _get_pip_path(venv_path)
        versao_pip = subprocess.run([str(pip_exec), "--version"], capture_output=True, text=True)
        click.echo(versao_pip.stdout)

    return True


def _get_pip_path(venv_path):
    """Retorna o caminho do pip baseado no sistema operacional."""
    if os.name == 'nt':
        return venv_path / 'Scripts' / 'pip.exe'
    return venv_path / 'bin' / 'pip'


def _get_python_path(venv_path):
    """Retorna o caminho do python do venv baseado no sistema operacional."""
    if os.name == 'nt':
        return venv_path / 'Scripts' / 'python.exe'
    return venv_path / 'bin' / 'python'


def instalar_dependencias(caminho_projeto, caminho_requirements=None, verbose=False):
    """Instala as dependências do projeto a partir do arquivo requirements.txt."""
    venv_path = caminho_projeto / 'venv'
    if not venv_path.exists():
        raise FileNotFoundError("Ambiente virtual nao encontrado.")

    if caminho_requirements:
        arquivo_req = Path(caminho_requirements)
        if not arquivo_req.is_absolute():
            arquivo_req = caminho_projeto / caminho_requirements
    else:
        arquivo_req = caminho_projeto / 'requirements.txt'

    if not arquivo_req.exists():
        raise FileNotFoundError(f"Arquivo de requirements nao encontrado: {arquivo_req}")

    if verbose:
        click.echo(f"\n[*] Instalando dependencias de {arquivo_req}")

    pip_exec = _get_pip_path(venv_path)

    resultado = subprocess.run(
        [str(pip_exec), "install", "-r", str(arquivo_req)],
        capture_output=True,
        text=True
    )

    if verbose:
        if resultado.returncode == 0:
            click.echo("[OK] Dependencias instaladas com sucesso")
            if resultado.stdout:
                click.echo(resultado.stdout)
        else:
            click.echo(f"[ERRO] Erro ao instalar dependencias: {resultado.stderr}")

    return resultado.returncode == 0


def configurar_ambiente_projeto(caminho_projeto, versao_python=None, caminho_requirements=None, verbose=False):
    """Função principal para configurar o ambiente do projeto."""
    venv_criado = criar_venv(caminho_projeto, versao_python, verbose)
    if not venv_criado:
        return False

    if caminho_requirements or (caminho_projeto / 'requirements.txt').exists():
        return instalar_dependencias(caminho_projeto, caminho_requirements, verbose)

    return True
