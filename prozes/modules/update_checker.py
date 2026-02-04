"""Update checker module for Prozes."""

import json
import sys
import time
from pathlib import Path
from typing import Optional, Tuple
import urllib.request
import urllib.error
from packaging import version


def get_current_version() -> str:
    """Get the current installed version of Prozes.

    Returns:
        Current version string
    """
    return "1.1.1"  # This will be updated automatically by packaging


def get_latest_version() -> Optional[str]:
    """Get the latest version from PyPI.

    Returns:
        Latest version string or None if failed to fetch
    """
    try:
        url = "https://pypi.org/pypi/prozes/json"
        req = urllib.request.Request(
            url,
            headers={'User-Agent': 'prozes-update-checker'}
        )

        with urllib.request.urlopen(req, timeout=2) as response:
            data = json.loads(response.read().decode())
            return data['info']['version']
    except (urllib.error.URLError, urllib.error.HTTPError, KeyError, json.JSONDecodeError):
        return None
    except Exception:
        return None


def is_update_available() -> Tuple[bool, Optional[str]]:
    """Check if an update is available.

    Returns:
        Tuple of (is_available, latest_version)
    """
    current = get_current_version()
    latest = get_latest_version()

    if latest is None:
        return False, None

    try:
        return version.parse(latest) > version.parse(current), latest
    except Exception:
        return False, None


def get_cache_file() -> Path:
    """Get the cache file path.

    Returns:
        Path to cache file
    """
    cache_dir = Path.home() / '.prozes'
    cache_dir.mkdir(exist_ok=True)
    return cache_dir / 'update_check_cache'


def should_check_update() -> bool:
    """Check if we should check for updates (once per day).

    Returns:
        True if should check, False otherwise
    """
    cache_file = get_cache_file()

    if not cache_file.exists():
        return True

    try:
        last_check = float(cache_file.read_text().strip())
        # Check once per day (86400 seconds)
        return (time.time() - last_check) > 86400
    except (ValueError, FileNotFoundError):
        return True


def update_cache():
    """Update the cache file with current timestamp."""
    cache_file = get_cache_file()
    cache_file.write_text(str(time.time()))


def check_for_updates(verbose: bool = False) -> Tuple[bool, Optional[str]]:
    """Check for updates with caching.

    Args:
        verbose: If True, always check regardless of cache

    Returns:
        Tuple of (is_available, latest_version)
    """
    # Skip check if recently checked (unless verbose mode)
    if not verbose and not should_check_update():
        return False, None

    # Check for updates
    is_available, latest_version = is_update_available()

    # Update cache
    if is_available or latest_version is not None:
        update_cache()

    return is_available, latest_version


def prompt_update(latest_version: str, lang: str = 'en') -> bool:
    """Prompt user to update.

    Args:
        latest_version: The latest version available
        lang: Language code

    Returns:
        True if user wants to update, False otherwise
    """
    from rich.prompt import Confirm
    from prozes.modules.console import console

    messages = {
        'en': {
            'available': f'🎉 New version available: {latest_version}',
            'current': f'Current version: {get_current_version()}',
            'prompt': 'Would you like to update now?',
            'updating': 'Updating Prozes...',
            'success': '✅ Update successful! Please run your command again.',
            'error': '❌ Update failed. You can manually update with: pip install --upgrade prozes',
            'skipped': 'Update skipped. You can update later with: pip install --upgrade prozes',
        },
        'pt': {
            'available': f'🎉 Nova versão disponível: {latest_version}',
            'current': f'Versão atual: {get_current_version()}',
            'prompt': 'Gostaria de atualizar agora?',
            'updating': 'Atualizando Prozes...',
            'success': '✅ Atualização bem-sucedida! Por favor, execute seu comando novamente.',
            'error': '❌ Falha na atualização. Você pode atualizar manualmente com: pip install --upgrade prozes',
            'skipped': 'Atualização ignorada. Você pode atualizar depois com: pip install --upgrade prozes',
        },
        'es': {
            'available': f'🎉 Nueva versión disponible: {latest_version}',
            'current': f'Versión actual: {get_current_version()}',
            'prompt': '¿Le gustaría actualizar ahora?',
            'updating': 'Actualizando Prozes...',
            'success': '✅ ¡Actualización exitosa! Por favor, ejecute su comando nuevamente.',
            'error': '❌ Error en la actualización. Puede actualizar manualmente con: pip install --upgrade prozes',
            'skipped': 'Actualización omitida. Puede actualizar después con: pip install --upgrade prozes',
        },
        'it': {
            'available': f'🎉 Nuova versione disponibile: {latest_version}',
            'current': f'Versione attuale: {get_current_version()}',
            'prompt': 'Vuoi aggiornare ora?',
            'updating': 'Aggiornamento di Prozes...',
            'success': '✅ Aggiornamento riuscito! Esegui nuovamente il comando.',
            'error': '❌ Aggiornamento fallito. Puoi aggiornare manualmente con: pip install --upgrade prozes',
            'skipped': 'Aggiornamento saltato. Puoi aggiornare dopo con: pip install --upgrade prozes',
        },
        'fr': {
            'available': f'🎉 Nouvelle version disponible : {latest_version}',
            'current': f'Version actuelle : {get_current_version()}',
            'prompt': 'Voulez-vous mettre à jour maintenant ?',
            'updating': 'Mise à jour de Prozes...',
            'success': '✅ Mise à jour réussie ! Veuillez exécuter votre commande à nouveau.',
            'error': '❌ Échec de la mise à jour. Vous pouvez mettre à jour manuellement avec : pip install --upgrade prozes',
            'skipped': 'Mise à jour ignorée. Vous pouvez mettre à jour plus tard avec : pip install --upgrade prozes',
        },
    }

    msg = messages.get(lang, messages['en'])

    console.print()
    console.print(f"[bold yellow]{msg['available']}[/bold yellow]")
    console.print(f"[dim]{msg['current']}[/dim]")
    console.print()

    should_update = Confirm.ask(msg['prompt'], default=False)

    if should_update:
        console.print(f"[cyan]{msg['updating']}[/cyan]")

        import subprocess
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", "--upgrade", "prozes"],
                capture_output=True,
                text=True,
                timeout=60
            )

            if result.returncode == 0:
                console.print(f"[green]{msg['success']}[/green]")
                console.print()
                sys.exit(0)
            else:
                console.print(f"[red]{msg['error']}[/red]")
                return False
        except Exception:
            console.print(f"[red]{msg['error']}[/red]")
            return False
    else:
        console.print(f"[yellow]{msg['skipped']}[/yellow]")
        console.print()

    return should_update


def check_and_prompt_update(verbose: bool = False, lang: str = 'en'):
    """Check for updates and prompt user if available.

    Args:
        verbose: If True, always check regardless of cache
        lang: Language code
    """
    is_available, latest_version = check_for_updates(verbose)

    if is_available and latest_version:
        prompt_update(latest_version, lang)
