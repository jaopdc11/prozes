"""Prozes CLI - Python project generator."""

import sys
from pathlib import Path
import click
from prozes.modules.dirs import create_project_folder, command_git
from prozes.modules.venv import criar_venv, instalar_dependencias
from prozes.modules.install import create_default_requirements, create_env_example
from prozes.modules.structures import (
    create_mvc_structure,
    create_api_structure,
    create_cli_structure,
    create_clean_structure,
)
from prozes.modules.console import (
    console,
    print_header,
    print_success,
    print_error,
    print_info,
    print_step,
    print_summary,
    print_next_steps,
    print_template_info,
    print_template_tree,
    print_template_list,
    ICONS,
)
from prozes.modules.i18n import t, set_language
from prozes.modules.validation import run_all_validations, validate_project_name
from prozes.modules.templates import (
    create_template_from_directory,
    list_custom_templates,
    get_template,
    apply_template,
    delete_template,
    template_exists,
    validate_template_name,
)
from prozes.modules.update_checker import check_and_prompt_update


class LanguageOption(click.Option):
    """Option que troca o idioma antes de executar o comando."""

    def __init__(self, *args, help_key=None, **kwargs):
        self.help_key = help_key
        super().__init__(*args, **kwargs)

    def handle_parse_result(self, ctx, opts, args):
        # Only override if user explicitly passed --lang
        if 'lang' in opts and opts['lang'] is not None:
            set_language(opts['lang'])
        return super().handle_parse_result(ctx, opts, args)

    def get_help_record(self, ctx):
        if self.help_key:
            self.help = t(self.help_key)
        return super().get_help_record(ctx)


class TranslatedGroup(click.Group):
    """Grupo do Click com textos de ajuda traduzidos."""

    def __init__(self, *args, help_key=None, **kwargs):
        self.help_key = help_key
        super().__init__(*args, **kwargs)

    def get_short_help_str(self, limit=150):
        if self.help_key:
            return t(self.help_key)[:limit]
        return super().get_short_help_str(limit)

    def format_help(self, ctx, formatter):
        if self.help_key:
            self.help = t(self.help_key)
        super().format_help(ctx, formatter)


class TranslatedCommand(click.Command):
    """Comando do Click com help traduzido."""

    def __init__(self, *args, help_key=None, help_long_key=None, **kwargs):
        self.help_key = help_key
        self.help_long_key = help_long_key
        super().__init__(*args, **kwargs)

    def get_short_help_str(self, limit=150):
        if self.help_key:
            return t(self.help_key)[:limit]
        return super().get_short_help_str(limit)

    def format_help(self, ctx, formatter):
        if self.help_key:
            help_text = t(self.help_key)
            if self.help_long_key:
                help_text += "\n\n" + t(self.help_long_key)
            self.help = help_text
        super().format_help(ctx, formatter)


class TranslatedOption(click.Option):
    """Opção do Click com help traduzido."""

    def __init__(self, *args, help_key=None, **kwargs):
        self.help_key = help_key
        super().__init__(*args, **kwargs)

    def get_help_record(self, ctx):
        if self.help_key:
            self.help = t(self.help_key)
        return super().get_help_record(ctx)


@click.group(cls=TranslatedGroup, help_key='help_main')
@click.option(
    '--lang', '-L',
    type=click.Choice(['en', 'pt', 'es', 'it', 'fr'], case_sensitive=False),
    default=None,
    cls=LanguageOption,
    is_eager=True,
    help_key='help_lang',
)
@click.version_option(version='1.1.1', prog_name='prozes')
@click.pass_context
def cli(ctx, lang):
    """Prozes - gerador de projetos Python com arquiteturas prontas."""
    from prozes.modules.i18n import get_language
    ctx.ensure_object(dict)
    ctx.obj['lang'] = lang if lang else get_language()


# =============================================================================
# Common options decorator
# =============================================================================

def common_options(f):
    """Decorator que adiciona as opções comuns em todos os comandos."""
    f = click.option('-v', '--verbose', is_flag=True,
                     cls=TranslatedOption, help_key='help_verbose')(f)
    f = click.option('--git', is_flag=True,
                     cls=TranslatedOption, help_key='help_git')(f)
    f = click.option('--venv', is_flag=True,
                     cls=TranslatedOption, help_key='help_venv')(f)
    f = click.option('--python-version', type=str, default=None,
                     cls=TranslatedOption, help_key='help_python_version')(f)
    f = click.option('--install-deps', is_flag=True,
                     cls=TranslatedOption, help_key='help_install_deps')(f)
    f = click.option('--auth', type=click.Choice(['none', 'jwt', 'oauth2', 'session', 'basic'], case_sensitive=False),
                     default='none', cls=TranslatedOption, help_key='help_auth')(f)
    return f


def validate_and_exit_on_error(project_name, git, venv, python_version, install_deps):
    """Valida as entradas e sai com erro se algo estiver errado."""
    errors = run_all_validations(
        project_name=project_name,
        git=git,
        venv=venv,
        python_version=python_version,
        install_deps=install_deps,
    )

    if errors:
        console.print()
        console.print(f"[bold red]{t('validation_errors_header')}:[/bold red]")
        for error in errors:
            print_error(error)
        console.print()
        sys.exit(1)


def finalize_project(project_path, project_name, project_type, verbose, git, venv, python_version, install_deps, auth='none'):
    """Finaliza a criação do projeto (venv, git, deps)."""
    options = {'venv': False, 'git': False, 'deps': False}

    # Create requirements.txt
    create_default_requirements(project_path, project_type, auth)
    if verbose:
        print_info(t('requirements_created'))

    # Create .env.example
    create_env_example(project_path, project_type, auth)
    if verbose:
        print_info('.env.example criado')

    # Print auth configuration message
    if auth != 'none':
        print_success(f"{t('auth_configured')}: {auth.upper()}")
        if verbose:
            print_info(t('auth_warning_database'))

    # Virtual environment setup
    if venv:
        console.print()
        print_step(f"{ICONS['python']} {t('creating_venv')}")
        venv_success = criar_venv(project_path, python_version, verbose=False)
        if venv_success:
            options['venv'] = True
            print_success(t('venv_created'))

            if install_deps:
                print_step(f"{ICONS['package']} {t('installing_deps')}")
                deps_success = instalar_dependencias(project_path, 'requirements.txt', verbose=False)
                if deps_success:
                    options['deps'] = True
                    print_success(t('deps_installed'))

    # Git initialization
    if git:
        console.print()
        print_step(f"{ICONS['git']} {t('initializing_git')}")
        git_success = command_git(project_path, verbose=verbose)
        if git_success:
            options['git'] = True
            print_success(t('git_initialized'))

    # Final summary
    print_summary(project_path, project_type, options)

    return options


# =============================================================================
# MVC Command
# =============================================================================

@cli.command(cls=TranslatedCommand, help_key='help_mvc', help_long_key='help_mvc_long')
@click.argument('project_name')
@click.option(
    '-t', '--type', 'project_type',
    type=click.Choice(['web-flask', 'web-fastapi'], case_sensitive=False),
    default='web-flask',
    cls=TranslatedOption, help_key='help_mvc_type'
)
@common_options
@click.pass_context
def mvc(ctx, project_name, project_type, verbose, git, venv, python_version, install_deps, auth):
    """Create a project with MVC architecture."""
    validate_and_exit_on_error(project_name, git, venv, python_version, install_deps)

    # Check for updates before creating project
    check_and_prompt_update(lang=ctx.obj.get('lang', 'en'))

    try:
        print_header(f"{t('creating_project_mvc')}: {project_name}", project_type)
        console.print()

        project_path = create_project_folder(project_name, verbose=False)
        print_step(t('creating_folder_structure'))
        create_mvc_structure(project_path, project_type, auth, verbose)

        options = finalize_project(project_path, project_name, project_type, verbose, git, venv, python_version, install_deps, auth)

        # Next steps
        steps = [f"cd {project_name}"]
        if options.get('venv'):
            steps.append(f"{project_name}\\venv\\Scripts\\activate  [dim]{t('activate_venv_win')}[/dim]")
        if project_type == 'web-fastapi':
            steps.append("uvicorn main:app --reload")
        else:
            steps.append("python main.py")

        print_next_steps(steps)

    except Exception as e:
        print_error(f"{t('error_creating_project')}: {e}")
        if verbose:
            console.print_exception()
        sys.exit(1)


# =============================================================================
# API Command
# =============================================================================

@cli.command(cls=TranslatedCommand, help_key='help_api', help_long_key='help_api_long')
@click.argument('project_name')
@click.option(
    '-t', '--type', 'project_type',
    type=click.Choice(['flask', 'fastapi'], case_sensitive=False),
    default='fastapi',
    cls=TranslatedOption, help_key='help_api_type'
)
@common_options
@click.pass_context
def api(ctx, project_name, project_type, verbose, git, venv, python_version, install_deps, auth):
    """Create a pure REST API (no frontend)."""
    validate_and_exit_on_error(project_name, git, venv, python_version, install_deps)

    # Check for updates before creating project
    check_and_prompt_update(lang=ctx.obj.get('lang', 'en'))

    try:
        full_type = f"api-{project_type}"
        print_header(f"{t('creating_project_api')}: {project_name}", full_type)
        console.print()

        project_path = create_project_folder(project_name, verbose=False)
        print_step(t('creating_folder_structure'))
        create_api_structure(project_path, full_type, auth, verbose)

        options = finalize_project(project_path, project_name, full_type, verbose, git, venv, python_version, install_deps, auth)

        # Next steps
        steps = [f"cd {project_name}"]
        if options.get('venv'):
            steps.append(f"{project_name}\\venv\\Scripts\\activate  [dim]{t('activate_venv_win')}[/dim]")
        if project_type == 'fastapi':
            steps.append("uvicorn main:app --reload")
            steps.append(f"{t('open_docs')} http://localhost:8000/docs")
        else:
            steps.append("python main.py")

        print_next_steps(steps)

    except Exception as e:
        print_error(f"{t('error_creating_project')}: {e}")
        if verbose:
            console.print_exception()
        sys.exit(1)


# =============================================================================
# CLI Command
# =============================================================================

@cli.command('cli', cls=TranslatedCommand, help_key='help_cli', help_long_key='help_cli_long')
@click.argument('project_name')
@common_options
def cli_cmd(project_name, verbose, git, venv, python_version, install_deps, auth):
    """Create a CLI project with Click."""
    validate_and_exit_on_error(project_name, git, venv, python_version, install_deps)

    try:
        print_header(f"{t('creating_project_cli')}: {project_name}", "click")
        console.print()

        project_path = create_project_folder(project_name, verbose=False)
        print_step(t('creating_folder_structure'))
        create_cli_structure(project_path, verbose)

        options = finalize_project(project_path, project_name, 'cli', verbose, git, venv, python_version, install_deps, auth)

        # Next steps
        steps = [
            f"cd {project_name}",
            "pip install -e .",
            f"{project_name} --help",
        ]

        print_next_steps(steps)

    except Exception as e:
        print_error(f"{t('error_creating_project')}: {e}")
        if verbose:
            console.print_exception()
        sys.exit(1)


# =============================================================================
# Clean Architecture Command
# =============================================================================

@cli.command(cls=TranslatedCommand, help_key='help_clean', help_long_key='help_clean_long')
@click.argument('project_name')
@click.option(
    '-t', '--type', 'project_type',
    type=click.Choice(['flask', 'fastapi'], case_sensitive=False),
    default='flask',
    cls=TranslatedOption, help_key='help_clean_type'
)
@common_options
@click.pass_context
def clean(ctx, project_name, project_type, verbose, git, venv, python_version, install_deps, auth):
    """Create a project with Clean Architecture."""
    validate_and_exit_on_error(project_name, git, venv, python_version, install_deps)

    # Check for updates before creating project
    check_and_prompt_update(lang=ctx.obj.get('lang', 'en'))

    try:
        full_type = f"clean-{project_type}"
        print_header(f"{t('creating_project_clean')}: {project_name}", full_type)
        console.print()

        project_path = create_project_folder(project_name, verbose=False)
        print_step(t('creating_folder_structure'))
        create_clean_structure(project_path, full_type, auth, verbose)

        options = finalize_project(project_path, project_name, full_type, verbose, git, venv, python_version, install_deps, auth)

        # Next steps
        steps = [f"cd {project_name}"]
        if options.get('venv'):
            steps.append(f"{project_name}\\venv\\Scripts\\activate  [dim]{t('activate_venv_win')}[/dim]")
        steps.append("python main.py")

        print_next_steps(steps)

    except Exception as e:
        print_error(f"{t('error_creating_project')}: {e}")
        if verbose:
            console.print_exception()
        sys.exit(1)


# =============================================================================
# Template Commands
# =============================================================================

@cli.group(cls=TranslatedGroup, help_key='help_template')
def template():
    """Gerenciar templates customizados."""
    pass


@template.command('save', cls=TranslatedCommand, help_key='help_template_save')
@click.argument('source_path', type=click.Path(exists=True, file_okay=False, dir_okay=True))
@click.argument('template_name')
@click.option('-d', '--description', default='', help='Template description')
@click.option('-a', '--author', default='', help='Template author')
@click.option('-e', '--exclude-pattern', multiple=True, help='Additional patterns to exclude')
@click.option('--detect-variables/--no-detect-variables', default=True, help='Auto-detect variables')
@click.option('-v', '--verbose', is_flag=True, cls=TranslatedOption, help_key='help_verbose')
def template_save(source_path, template_name, description, author, exclude_pattern, detect_variables, verbose):
    """Save existing project as template."""
    try:
        source = Path(source_path)

        # Validate template name
        is_valid, error = validate_template_name(template_name)
        if not is_valid:
            print_error(t('error_template_name_invalid') + f": {error}")
            sys.exit(1)

        # Check if template already exists
        if template_exists(template_name):
            from rich.prompt import Confirm
            confirmed = Confirm.ask(
                t('template_exists', name=template_name) + " " + t('confirm_overwrite'),
                default=False
            )
            if not confirmed:
                console.print("[yellow]Operation cancelled[/yellow]")
                sys.exit(0)

        # Create template
        print_header(f"Saving template: {template_name}")

        created_template = create_template_from_directory(
            source_path=source,
            template_name=template_name,
            description=description,
            author=author,
            exclude_patterns=list(exclude_pattern) if exclude_pattern else None,
            detect_variables=detect_variables,
            verbose=verbose
        )

        console.print()
        print_success(t('template_saved'))
        console.print(f"  Template: [cyan]{created_template.name}[/cyan]")
        console.print(f"  Location: [dim]{created_template.path}[/dim]")

        if created_template.metadata.variables:
            var_count = len(created_template.metadata.variables)
            console.print(f"  Variables: [yellow]{var_count}[/yellow]")

    except Exception as e:
        print_error(f"Error saving template: {e}")
        if verbose:
            console.print_exception()
        sys.exit(1)


@template.command('list', cls=TranslatedCommand, help_key='help_template_list')
@click.option('--custom-only', is_flag=True, help='Show only custom templates')
@click.option('-v', '--verbose', is_flag=True, cls=TranslatedOption, help_key='help_verbose')
def template_list(custom_only, verbose):
    """List all available templates."""
    try:
        # Get custom templates
        custom_templates = list_custom_templates()

        # Get built-in templates info
        builtin_templates = None
        if not custom_only:
            from prozes.modules.structures import get_builtin_template_list
            builtin_templates = get_builtin_template_list()

        print_template_list(custom_templates, builtin_templates, verbose)

    except Exception as e:
        print_error(f"Error listing templates: {e}")
        if verbose:
            console.print_exception()
        sys.exit(1)


@template.command('use', cls=TranslatedCommand, help_key='help_template_use')
@click.argument('template_name')
@click.argument('project_name')
@click.option('--var', '-V', multiple=True, help='Set template variable (KEY=VALUE)')
@click.option('-i', '--interactive', is_flag=True, help='Prompt for all variables')
@common_options
def template_use(template_name, project_name, var, interactive, verbose, git, venv, python_version, install_deps, auth):
    """Create project from custom template."""
    try:
        # Validate project name
        is_valid, error = validate_project_name(project_name)
        if not is_valid:
            print_error(error)
            sys.exit(1)

        # Check if project already exists
        project_path = Path.cwd() / project_name
        if project_path.exists():
            print_error(f"Project '{project_name}' already exists in current directory")
            sys.exit(1)

        # Load template
        tpl = get_template(template_name)
        if tpl is None:
            print_error(t('template_not_found', name=template_name))
            sys.exit(1)

        print_header(f"Creating project from template: {template_name}")

        # Parse variables from --var options
        variables = {}
        for var_str in var:
            if '=' not in var_str:
                print_error(f"Invalid variable format: {var_str} (expected KEY=VALUE)")
                sys.exit(1)

            key, value = var_str.split('=', 1)
            variables[key.strip()] = value.strip()

        # Interactive mode: prompt for missing variables
        if interactive or not variables:
            from prozes.modules.console import print_variable_prompt

            console.print("\n[bold cyan]Template Variables:[/bold cyan]")

            for var_name, var_obj in tpl.metadata.variables.items():
                # Skip if already provided via --var
                if var_name in variables:
                    continue

                # Skip built-in variables that will be auto-filled
                if var_name in ['project_name', 'date', 'year']:
                    continue

                print_variable_prompt(var_obj)
                value = var_obj.prompt_user()
                variables[var_name] = value

            console.print()

        # Apply template
        if verbose:
            print_info("Applying template...")

        created_path = apply_template(
            template=tpl,
            project_name=project_name,
            variables=variables,
            verbose=verbose
        )

        # Finalize project (venv, git, deps)
        project_type = f"template:{template_name}"
        options = finalize_project(
            created_path,
            project_name,
            project_type,
            verbose,
            git,
            venv,
            python_version,
            install_deps,
            auth
        )

        # Next steps
        steps = [f"cd {project_name}"]
        if options.get('venv'):
            steps.append(f"{project_name}\\venv\\Scripts\\activate  [dim]{t('activate_venv_win')}[/dim]")

        print_next_steps(steps)

    except Exception as e:
        print_error(f"Error using template: {e}")
        if verbose:
            console.print_exception()
        sys.exit(1)


@template.command('show', cls=TranslatedCommand, help_key='help_template_show')
@click.argument('template_name')
@click.option('--show-files', is_flag=True, help='Show file tree')
def template_show(template_name, show_files):
    """Show template details."""
    try:
        tpl = get_template(template_name)
        if tpl is None:
            print_error(t('template_not_found', name=template_name))
            sys.exit(1)

        print_template_info(tpl)

        # Show variables
        if tpl.metadata.variables:
            console.print("\n[bold cyan]Variables:[/bold cyan]")
            for var_name, var_obj in tpl.metadata.variables.items():
                required = "[red]*[/red]" if var_obj.required else " "
                default = f" [dim](default: {var_obj.default})[/dim]" if var_obj.default else ""
                console.print(f"  {required} [cyan]{var_name}[/cyan] ({var_obj.type}){default}")
                if var_obj.description:
                    console.print(f"      [dim]{var_obj.description}[/dim]")

        # Show file tree
        if show_files:
            print_template_tree(tpl)

    except Exception as e:
        print_error(f"Error showing template: {e}")
        console.print_exception()
        sys.exit(1)


@template.command('delete', cls=TranslatedCommand, help_key='help_template_delete')
@click.argument('template_name')
@click.option('-f', '--force', is_flag=True, help='Skip confirmation')
def template_delete(template_name, force):
    """Delete custom template."""
    try:
        # Check if template exists
        tpl = get_template(template_name)
        if tpl is None:
            print_error(t('template_not_found', name=template_name))
            sys.exit(1)

        # Delete template
        success = delete_template(template_name, force=force)

        if success:
            console.print(f"[green]Template '{template_name}' deleted successfully[/green]")

    except Exception as e:
        print_error(f"Error deleting template: {e}")
        sys.exit(1)


# =============================================================================
# Config Command
# =============================================================================

@cli.command(cls=TranslatedCommand, help_key='help_config')
@click.option(
    '--lang', '-l',
    type=click.Choice(['en', 'pt', 'es', 'it', 'fr'], case_sensitive=False),
    cls=TranslatedOption, help_key='help_config_lang'
)
@click.option('--show', '-s', is_flag=True,
              cls=TranslatedOption, help_key='help_config_show')
def config(lang, show):
    """Configure Prozes settings."""
    from pathlib import Path
    import os

    config_dir = Path.home() / '.prozes'
    config_file = config_dir / 'config'

    if show:
        from prozes.modules.i18n import get_language

        console.print(f"\n[bold cyan]Prozes Configuration[/bold cyan]")
        console.print(f"  Config file: [dim]{config_file}[/dim]")

        if config_file.exists():
            content = config_file.read_text().strip()
            console.print(f"  Contents:")
            for line in content.split('\n'):
                console.print(f"    [green]{line}[/green]")
        else:
            console.print(f"  [dim]No config file found (using defaults)[/dim]")

        console.print(f"\n  Environment:")
        env_lang = os.environ.get('PROZEES_LANG', '[dim]not set[/dim]')
        console.print(f"    PROZEES_LANG: {env_lang}")

        console.print(f"\n  [bold]Active language:[/bold] [green]{get_language()}[/green]")
        return

    if lang:
        # Create config directory if it doesn't exist
        config_dir.mkdir(parents=True, exist_ok=True)

        # Write config
        config_file.write_text(f"lang={lang}\n")

        print_success(f"Language set to '{lang}'")
        console.print(f"  Config saved to: [dim]{config_file}[/dim]")
    else:
        # No options provided, show help
        ctx = click.get_current_context()
        click.echo(ctx.get_help())


def main():
    """Ponto de entrada do CLI."""
    cli()


if __name__ == '__main__':
    main()
