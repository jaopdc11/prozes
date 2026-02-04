"""Funções de output colorido pro terminal."""

import sys
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich import box

from prozes.modules.i18n import t

# Global console
console = Console()


def _supports_emoji():
    """Verifica se o terminal aguenta emojis."""
    try:
        "\U0001f680".encode(sys.stdout.encoding or 'utf-8')
        return True
    except (UnicodeEncodeError, LookupError):
        return False


EMOJI_SUPPORT = _supports_emoji()

# Icons with fallback
ICONS = {
    'rocket': '\U0001f680' if EMOJI_SUPPORT else '[>]',
    'folder': '\U0001f4c1' if EMOJI_SUPPORT else '[D]',
    'file': '\U0001f4c4' if EMOJI_SUPPORT else '[F]',
    'check': '\u2705' if EMOJI_SUPPORT else '[OK]',
    'error': '\u274c' if EMOJI_SUPPORT else '[X]',
    'warning': '\u26a0\ufe0f' if EMOJI_SUPPORT else '[!]',
    'info': '\u2139\ufe0f' if EMOJI_SUPPORT else '[i]',
    'python': '\U0001f40d' if EMOJI_SUPPORT else '[Py]',
    'package': '\U0001f4e6' if EMOJI_SUPPORT else '[P]',
    'git': '\U0001f500' if EMOJI_SUPPORT else '[Git]',
    'star': '\u2728' if EMOJI_SUPPORT else '[*]',
    'tree': '\U0001f333' if EMOJI_SUPPORT else '[T]',
    'gear': '\u2699\ufe0f' if EMOJI_SUPPORT else '[*]',
    'link': '\U0001f517' if EMOJI_SUPPORT else '[>]',
}


def print_header(title: str, subtitle: str = None):
    """Imprime o cabeçalho bonito."""
    text = Text()
    text.append(f"{ICONS['rocket']} ", style="bold yellow")
    text.append(title, style="bold cyan")

    if subtitle:
        panel = Panel(
            text,
            subtitle=f"[dim]{subtitle}[/dim]",
            box=box.ROUNDED,
            border_style="cyan",
            padding=(0, 2),
        )
    else:
        panel = Panel(
            text,
            box=box.ROUNDED,
            border_style="cyan",
            padding=(0, 2),
        )
    console.print(panel)


def print_success(message: str):
    """Mostra mensagem de sucesso."""
    console.print(f"{ICONS['check']} [bold green]{message}[/bold green]")


def print_error(message: str):
    """Mostra erro."""
    console.print(f"{ICONS['error']} [bold red]{message}[/bold red]")


def print_warning(message: str):
    """Mostra aviso."""
    console.print(f"{ICONS['warning']} [yellow]{message}[/yellow]")


def print_info(message: str):
    """Mostra info."""
    console.print(f"{ICONS['info']} [dim]{message}[/dim]")


def print_step(message: str):
    """Mostra um passo do processo."""
    console.print(f"  [cyan]{ICONS['gear']}[/cyan] {message}")


def print_summary(project_path: str, project_type: str, options: dict = None):
    """Mostra resumo do que foi criado."""
    console.print()

    table = Table(
        show_header=False,
        box=box.ROUNDED,
        border_style="green",
        padding=(0, 2),
    )
    table.add_column("Key", style="bold cyan")
    table.add_column("Value", style="white")

    table.add_row(t('project'), str(project_path))
    table.add_row(t('type'), project_type)

    if options:
        if options.get('venv'):
            table.add_row(t('venv'), f"{ICONS['check']} {t('created')}")
        if options.get('git'):
            table.add_row(t('git'), f"{ICONS['check']} {t('initialized')}")
        if options.get('deps'):
            table.add_row(t('deps'), f"{ICONS['check']} {t('installed')}")

    panel = Panel(
        table,
        title=f"{ICONS['star']} [bold green]{t('project_created')}[/bold green]",
        border_style="green",
    )
    console.print(panel)


def print_next_steps(steps: list):
    """Mostra próximos passos."""
    console.print()
    console.print(f"{ICONS['link']} [bold]{t('next_steps')}:[/bold]")
    for i, step in enumerate(steps, 1):
        console.print(f"   [dim]{i}.[/dim] [cyan]{step}[/cyan]")


def print_command(cmd: str):
    """Mostra um comando pra executar."""
    console.print(f"   [dim]$[/dim] [bold yellow]{cmd}[/bold yellow]")


def print_creating(item_type: str, name: str):
    """Mostra o item sendo criado."""
    if item_type == 'dir':
        console.print(f"    {ICONS['folder']} [blue]{name}/[/blue]")
    else:
        if name.endswith('.py'):
            console.print(f"    {ICONS['file']} [green]{name}[/green]")
        elif name.endswith(('.html', '.css', '.js')):
            console.print(f"    {ICONS['file']} [yellow]{name}[/yellow]")
        else:
            console.print(f"    {ICONS['file']} {name}")


def print_template_info(template):
    """Display template information in a Rich table.

    Args:
        template: Template object with metadata
    """
    from rich.tree import Tree

    console.print()

    table = Table(
        show_header=False,
        box=box.ROUNDED,
        border_style="cyan",
        padding=(0, 2),
    )
    table.add_column("Key", style="bold cyan")
    table.add_column("Value", style="white")

    table.add_row(t('template_name'), template.name)

    if template.metadata.description:
        table.add_row(t('template_description'), template.metadata.description)

    if template.metadata.author:
        table.add_row(t('template_author'), template.metadata.author)

    if template.metadata.created_at:
        created = template.metadata.created_at.split('T')[0]  # Just the date
        table.add_row(t('template_created'), created)

    table.add_row(t('template_location'), str(template.path))

    # Variables
    if template.metadata.variables:
        var_count = len(template.metadata.variables)
        table.add_row(t('template_variables'), str(var_count))

    # File count
    files = template.get_file_tree()
    table.add_row(t('template_files'), str(len(files)))

    panel = Panel(
        table,
        title=f"{ICONS['star']} [bold cyan]{t('template_details')}[/bold cyan]",
        border_style="cyan",
    )
    console.print(panel)


def print_template_tree(template):
    """Display template file structure as a tree.

    Args:
        template: Template object
    """
    from rich.tree import Tree

    console.print()
    tree = Tree(
        f"{ICONS['tree']} [bold cyan]{template.name}/[/bold cyan]",
        guide_style="dim"
    )

    files = template.get_file_tree()

    # Build tree structure
    dirs = {}

    for file_path in files:
        parts = file_path.parts

        # Create directory nodes
        current_tree = tree
        for i, part in enumerate(parts[:-1]):
            path_key = '/'.join(parts[:i+1])

            if path_key not in dirs:
                dirs[path_key] = current_tree.add(f"{ICONS['folder']} [blue]{part}/[/blue]")

            current_tree = dirs[path_key]

        # Add file
        filename = parts[-1]
        if filename.endswith('.py'):
            current_tree.add(f"{ICONS['file']} [green]{filename}[/green]")
        elif filename.endswith(('.html', '.css', '.js')):
            current_tree.add(f"{ICONS['file']} [yellow]{filename}[/yellow]")
        else:
            current_tree.add(f"{ICONS['file']} {filename}")

    console.print(tree)


def print_template_list(templates: list, builtin_templates: list = None, verbose: bool = False):
    """Display list of templates.

    Args:
        templates: List of Template objects (custom templates)
        builtin_templates: List of built-in template info dicts
        verbose: Show detailed information
    """
    console.print()

    # Built-in templates
    if builtin_templates:
        console.print(f"[bold cyan]{t('builtin_templates')}:[/bold cyan]")

        if verbose:
            table = Table(
                show_header=True,
                box=box.ROUNDED,
                border_style="cyan",
            )
            table.add_column("Name", style="cyan")
            table.add_column("Description", style="white")

            for tpl in builtin_templates:
                table.add_row(tpl['name'], tpl.get('description', ''))

            console.print(table)
        else:
            for tpl in builtin_templates:
                console.print(f"  {ICONS['star']} [cyan]{tpl['name']}[/cyan] - {tpl.get('description', '')}")

        console.print()

    # Custom templates
    console.print(f"[bold cyan]{t('custom_templates')} ({len(templates)}):[/bold cyan]")

    if not templates:
        console.print(f"  [dim]{t('no_custom_templates')}[/dim]")
        return

    if verbose:
        for template in templates:
            print_template_info(template)
            console.print()
    else:
        for template in templates:
            desc = template.metadata.description or "[dim]No description[/dim]"
            author = f" by {template.metadata.author}" if template.metadata.author else ""
            created = template.metadata.created_at.split('T')[0] if template.metadata.created_at else ""

            console.print(f"  {ICONS['package']} [bold cyan]{template.name}[/bold cyan]")
            console.print(f"    {desc}")
            if author or created:
                console.print(f"    [dim]{author}{' - ' if author and created else ''}{created}[/dim]")


def print_variable_prompt(variable):
    """Print variable information when prompting.

    Args:
        variable: TemplateVariable object
    """
    required_text = "[red]*[/red]" if variable.required else ""
    type_text = f"[dim]({variable.type})[/dim]"

    console.print(f"{required_text} [cyan]{variable.name}[/cyan] {type_text}")
    if variable.description:
        console.print(f"  [dim]{variable.description}[/dim]")
