"""Module for managing custom templates."""

import json
import re
import shutil
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

from prozes.modules.console import console, print_error, print_success, print_info
from prozes.modules.i18n import t


# =============================================================================
# CONSTANTS
# =============================================================================

TEMPLATE_VERSION = "1.0"
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB
WARN_FILE_SIZE = 10 * 1024 * 1024  # 10MB
VARIABLE_PATTERN = re.compile(r'\{\{([a-zA-Z_][a-zA-Z0-9_]*)\}\}')

DEFAULT_TEXT_EXTENSIONS = {
    '.py', '.txt', '.md', '.json', '.toml', '.yaml', '.yml',
    '.ini', '.cfg', '.conf', '.rst', '.html', '.css', '.js',
    '.sh', '.bat', '.ps1', '.xml', '.env', '.gitignore'
}

DEFAULT_EXCLUDE_DIRS = {
    '__pycache__', '.git', 'venv', '.venv', 'env', '.env',
    'node_modules', '.pytest_cache', '.mypy_cache', '.tox',
    '*.egg-info', 'dist', 'build', '.idea', '.vscode'
}


# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class TemplateVariable:
    """Represents a template variable with type and validation."""

    name: str
    type: str = "string"
    description: str = ""
    required: bool = False
    default: Optional[Any] = None

    def validate_value(self, value: Any) -> Tuple[bool, Optional[str]]:
        """Validate a value against this variable's constraints.

        Returns:
            (is_valid, error_message)
        """
        if value is None:
            if self.required:
                return False, f"Variable '{self.name}' is required"
            return True, None

        # Type validation
        if self.type == "string":
            if not isinstance(value, str):
                return False, f"Variable '{self.name}' must be a string"
        elif self.type == "integer":
            if not isinstance(value, int):
                return False, f"Variable '{self.name}' must be an integer"
        elif self.type == "boolean":
            if not isinstance(value, bool):
                return False, f"Variable '{self.name}' must be a boolean"

        return True, None

    def prompt_user(self) -> Any:
        """Prompt user for variable value."""
        from rich.prompt import Prompt, Confirm

        if self.type == "boolean":
            return Confirm.ask(
                self.description or f"Enter value for {self.name}",
                default=bool(self.default) if self.default is not None else False
            )

        default_str = str(self.default) if self.default is not None else None
        value = Prompt.ask(
            self.description or f"Enter value for {self.name}",
            default=default_str
        )

        if self.type == "integer":
            try:
                return int(value)
            except ValueError:
                print_error(f"Invalid integer value: {value}")
                return self.prompt_user()

        return value

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            "type": self.type,
            "description": self.description,
            "required": self.required,
            "default": self.default
        }


@dataclass
class TemplateMetadata:
    """Represents template.json metadata."""

    version: str = TEMPLATE_VERSION
    name: str = ""
    description: str = ""
    author: str = ""
    created_at: str = ""
    prozes_version: str = "1.0.0"
    variables: Dict[str, TemplateVariable] = field(default_factory=dict)
    dependencies: Dict[str, str] = field(default_factory=dict)
    variable_substitution: Dict[str, Any] = field(default_factory=dict)
    file_patterns: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Initialize default values."""
        if not self.created_at:
            self.created_at = datetime.now().isoformat()

        if not self.variable_substitution:
            self.variable_substitution = {
                "enabled": True,
                "patterns": ["{{variable_name}}"],
                "files": ["**/*.py", "**/*.txt", "**/*.md", "**/*.toml", "**/*.json"],
                "exclude": ["**/*.pyc", "**/__pycache__/*", "**/venv/*"]
            }

        if not self.file_patterns:
            self.file_patterns = {
                "text_extensions": list(DEFAULT_TEXT_EXTENSIONS),
                "exclude_dirs": list(DEFAULT_EXCLUDE_DIRS)
            }

    @classmethod
    def from_json(cls, json_path: Path) -> 'TemplateMetadata':
        """Load metadata from template.json file."""
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Convert variables dict to TemplateVariable objects
        variables = {}
        for var_name, var_data in data.get('variables', {}).items():
            variables[var_name] = TemplateVariable(
                name=var_name,
                type=var_data.get('type', 'string'),
                description=var_data.get('description', ''),
                required=var_data.get('required', False),
                default=var_data.get('default')
            )

        return cls(
            version=data.get('version', TEMPLATE_VERSION),
            name=data.get('name', ''),
            description=data.get('description', ''),
            author=data.get('author', ''),
            created_at=data.get('created_at', ''),
            prozes_version=data.get('prozes_version', '1.0.0'),
            variables=variables,
            dependencies=data.get('dependencies', {}),
            variable_substitution=data.get('variable_substitution', {}),
            file_patterns=data.get('file_patterns', {})
        )

    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization."""
        variables_dict = {
            name: var.to_dict()
            for name, var in self.variables.items()
        }

        return {
            "version": self.version,
            "name": self.name,
            "description": self.description,
            "author": self.author,
            "created_at": self.created_at,
            "prozes_version": self.prozes_version,
            "variables": variables_dict,
            "dependencies": self.dependencies,
            "variable_substitution": self.variable_substitution,
            "file_patterns": self.file_patterns
        }

    def save(self, path: Path) -> None:
        """Save metadata to file."""
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)

    def validate(self) -> List[str]:
        """Validate metadata structure.

        Returns:
            List of error messages (empty if valid)
        """
        errors = []

        if not self.name:
            errors.append("Template name is required")

        if not self.version:
            errors.append("Template version is required")

        # Validate variables
        for var_name, var in self.variables.items():
            if var_name != var.name:
                errors.append(f"Variable key '{var_name}' doesn't match name '{var.name}'")

        return errors


@dataclass
class Template:
    """Represents a complete template."""

    name: str
    path: Path
    metadata: TemplateMetadata

    @classmethod
    def load(cls, name: str) -> 'Template':
        """Load template by name.

        Args:
            name: Template name

        Returns:
            Template instance

        Raises:
            FileNotFoundError: If template doesn't exist
            ValueError: If template is invalid
        """
        template_path = get_templates_directory() / name

        if not template_path.exists():
            raise FileNotFoundError(f"Template '{name}' not found")

        metadata_path = template_path / 'template.json'
        if not metadata_path.exists():
            raise ValueError(f"Template '{name}' is missing template.json")

        structure_path = template_path / 'structure'
        if not structure_path.exists():
            raise ValueError(f"Template '{name}' is missing structure directory")

        metadata = TemplateMetadata.from_json(metadata_path)

        # Validate metadata
        errors = metadata.validate()
        if errors:
            raise ValueError(f"Invalid template metadata: {', '.join(errors)}")

        return cls(
            name=name,
            path=template_path,
            metadata=metadata
        )

    def get_structure_path(self) -> Path:
        """Get path to structure directory."""
        return self.path / 'structure'

    def get_file_tree(self) -> List[Path]:
        """Get list of all files in template structure.

        Returns:
            List of relative paths to files
        """
        structure_path = self.get_structure_path()
        files = []

        for item in structure_path.rglob('*'):
            if item.is_file():
                files.append(item.relative_to(structure_path))

        return sorted(files)


# =============================================================================
# DISCOVERY FUNCTIONS
# =============================================================================

def get_templates_directory() -> Path:
    """Get path to templates directory.

    Creates directory if it doesn't exist.
    """
    templates_dir = Path.home() / '.prozes' / 'templates'
    templates_dir.mkdir(parents=True, exist_ok=True)
    return templates_dir


def list_custom_templates() -> List[Template]:
    """List all custom templates.

    Returns:
        List of Template objects
    """
    templates_dir = get_templates_directory()
    templates = []

    for item in templates_dir.iterdir():
        if item.is_dir():
            try:
                template = Template.load(item.name)
                templates.append(template)
            except (FileNotFoundError, ValueError) as e:
                # Skip invalid templates
                console.print(f"[yellow]Warning: Skipping invalid template '{item.name}': {e}[/yellow]")

    return sorted(templates, key=lambda t: t.name)


def template_exists(name: str) -> bool:
    """Check if template exists.

    Args:
        name: Template name

    Returns:
        True if template exists
    """
    template_path = get_templates_directory() / name
    return template_path.exists()


def get_template(name: str) -> Optional[Template]:
    """Get template by name.

    Args:
        name: Template name

    Returns:
        Template or None if not found
    """
    try:
        return Template.load(name)
    except (FileNotFoundError, ValueError):
        return None


# =============================================================================
# SCANNING FUNCTIONS
# =============================================================================

def detect_file_type(file_path: Path) -> str:
    """Detect if file is text, binary, or should be skipped.

    Args:
        file_path: Path to file

    Returns:
        'text', 'binary', or 'skip'
    """
    # Check extension first
    if file_path.suffix.lower() in DEFAULT_TEXT_EXTENSIONS:
        return 'text'

    # Known binary extensions
    binary_extensions = {
        '.pyc', '.pyo', '.so', '.dll', '.dylib', '.exe',
        '.png', '.jpg', '.jpeg', '.gif', '.ico', '.pdf',
        '.zip', '.tar', '.gz', '.bz2', '.whl', '.egg'
    }

    if file_path.suffix.lower() in binary_extensions:
        return 'binary'

    # Try to detect by reading first few bytes
    try:
        with open(file_path, 'rb') as f:
            chunk = f.read(8192)

        # Check for null bytes (indication of binary)
        if b'\x00' in chunk:
            return 'binary'

        # Try to decode as text
        try:
            chunk.decode('utf-8')
            return 'text'
        except UnicodeDecodeError:
            return 'binary'

    except Exception:
        return 'skip'


def detect_variables_in_file(content: str) -> Set[str]:
    """Detect template variables in file content.

    Args:
        content: File content as string

    Returns:
        Set of variable names found
    """
    matches = VARIABLE_PATTERN.findall(content)
    return set(matches)


def extract_dependencies(source_path: Path) -> Dict[str, str]:
    """Extract dependency files from source project.

    Args:
        source_path: Path to source project

    Returns:
        Dict mapping dependency file names to relative paths
    """
    dependencies = {}

    # Common dependency files
    dep_files = ['requirements.txt', 'requirements-dev.txt', 'Pipfile', 'poetry.lock', 'pyproject.toml']

    for dep_file in dep_files:
        dep_path = source_path / dep_file
        if dep_path.exists():
            dependencies[dep_file] = f"structure/{dep_file}"

    return dependencies


def scan_project_structure(
    source_path: Path,
    exclude_patterns: Optional[List[str]] = None
) -> Dict:
    """Scan project structure and collect information.

    Args:
        source_path: Path to source project
        exclude_patterns: Additional patterns to exclude

    Returns:
        Dict with structure information
    """
    if exclude_patterns is None:
        exclude_patterns = []

    exclude_dirs = DEFAULT_EXCLUDE_DIRS.copy()
    exclude_dirs.update(exclude_patterns)

    files = []
    text_files = []
    binary_files = []
    detected_variables = set()

    for item in source_path.rglob('*'):
        # Skip excluded directories
        if any(excluded in item.parts for excluded in exclude_dirs):
            continue

        if item.is_file():
            relative_path = item.relative_to(source_path)
            files.append(relative_path)

            # Detect file type
            file_type = detect_file_type(item)

            if file_type == 'text':
                text_files.append(relative_path)

                # Try to detect variables
                try:
                    content = item.read_text(encoding='utf-8')
                    variables = detect_variables_in_file(content)
                    detected_variables.update(variables)
                except Exception:
                    pass

            elif file_type == 'binary':
                binary_files.append(relative_path)

    return {
        'files': files,
        'text_files': text_files,
        'binary_files': binary_files,
        'detected_variables': detected_variables,
        'total_files': len(files)
    }


# =============================================================================
# TEMPLATE CREATION
# =============================================================================

def validate_template_name(name: str) -> Tuple[bool, Optional[str]]:
    """Validate template name.

    Args:
        name: Template name

    Returns:
        (is_valid, error_message)
    """
    if not name:
        return False, "Template name cannot be empty"

    # Same rules as project name
    if not re.match(r"^[a-zA-Z_]", name):
        return False, "Template name must start with a letter or underscore"

    if not re.match(r"^[a-zA-Z_][a-zA-Z0-9_-]*$", name):
        return False, "Template name can only contain letters, numbers, underscores, and hyphens"

    return True, None


def create_template_from_directory(
    source_path: Path,
    template_name: str,
    description: str = "",
    author: str = "",
    exclude_patterns: Optional[List[str]] = None,
    detect_variables: bool = True,
    verbose: bool = False
) -> Template:
    """Create template from existing directory.

    Args:
        source_path: Path to source project
        template_name: Name for the template
        description: Template description
        author: Template author
        exclude_patterns: Additional patterns to exclude
        detect_variables: Whether to auto-detect variables
        verbose: Verbose output

    Returns:
        Created Template instance

    Raises:
        FileNotFoundError: If source doesn't exist
        ValueError: If validation fails
    """
    # Validate source path
    if not source_path.exists():
        raise FileNotFoundError(f"Source directory not found: {source_path}")

    if not source_path.is_dir():
        raise ValueError(f"Source path is not a directory: {source_path}")

    # Validate template name
    is_valid, error = validate_template_name(template_name)
    if not is_valid:
        raise ValueError(error)

    # Create template directory
    template_path = get_templates_directory() / template_name
    template_path.mkdir(parents=True, exist_ok=True)
    structure_path = template_path / 'structure'
    structure_path.mkdir(exist_ok=True)

    if verbose:
        print_info(t('scanning_project'))

    # Scan source structure
    scan_result = scan_project_structure(source_path, exclude_patterns)

    if verbose:
        console.print(f"Found {scan_result['total_files']} files")
        console.print(f"Text files: {len(scan_result['text_files'])}")
        console.print(f"Binary files: {len(scan_result['binary_files'])}")

    # Create metadata
    variables = {}

    # Add built-in variables
    variables['project_name'] = TemplateVariable(
        name='project_name',
        type='string',
        description='Nome do projeto',
        required=True
    )

    variables['author'] = TemplateVariable(
        name='author',
        type='string',
        description='Nome do autor',
        required=False,
        default='Anonymous'
    )

    # Add detected variables
    if detect_variables:
        if verbose and scan_result['detected_variables']:
            print_info(t('detecting_variables'))
            console.print(f"Detected variables: {', '.join(scan_result['detected_variables'])}")

        for var_name in scan_result['detected_variables']:
            if var_name not in variables:
                variables[var_name] = TemplateVariable(
                    name=var_name,
                    type='string',
                    description=f'Variable {var_name}',
                    required=False
                )

    # Extract dependencies
    dependencies = extract_dependencies(source_path)

    # Create metadata
    metadata = TemplateMetadata(
        name=template_name,
        description=description,
        author=author,
        variables=variables,
        dependencies=dependencies
    )

    # Copy files
    if verbose:
        print_info(t('copying_files'))

    for file_path in scan_result['files']:
        source_file = source_path / file_path
        dest_file = structure_path / file_path

        # Create parent directories
        dest_file.parent.mkdir(parents=True, exist_ok=True)

        # Copy file
        try:
            if file_path in scan_result['text_files']:
                # Copy text file with encoding
                content = source_file.read_text(encoding='utf-8')
                dest_file.write_text(content, encoding='utf-8')
            else:
                # Copy binary file
                shutil.copy2(source_file, dest_file)

            if verbose:
                console.print(f"  Copied: {file_path}")

        except Exception as e:
            console.print(f"[yellow]Warning: Failed to copy {file_path}: {e}[/yellow]")

    # Save metadata
    metadata.save(template_path / 'template.json')

    if verbose:
        print_success(t('template_saved'))

    return Template.load(template_name)


# =============================================================================
# TEMPLATE APPLICATION
# =============================================================================

def substitute_variables(content: str, variables: Dict[str, Any]) -> str:
    """Substitute variables in content.

    Args:
        content: Content with {{variable}} patterns
        variables: Dict of variable values

    Returns:
        Content with variables substituted
    """
    def replace_var(match):
        var_name = match.group(1)
        return str(variables.get(var_name, match.group(0)))

    return VARIABLE_PATTERN.sub(replace_var, content)


def substitute_in_filename(filename: str, variables: Dict[str, Any]) -> str:
    """Substitute variables in filename.

    Args:
        filename: Filename with {{variable}} patterns
        variables: Dict of variable values

    Returns:
        Filename with variables substituted
    """
    return substitute_variables(filename, variables)


def apply_template(
    template: Template,
    project_name: str,
    variables: Dict[str, Any],
    destination: Optional[Path] = None,
    verbose: bool = False
) -> Path:
    """Apply template to create new project.

    Args:
        template: Template to apply
        project_name: Name for new project
        variables: Variable values
        destination: Destination directory (default: current dir)
        verbose: Verbose output

    Returns:
        Path to created project

    Raises:
        ValueError: If validation fails
    """
    # Set destination
    if destination is None:
        destination = Path.cwd()

    project_path = destination / project_name

    # Validate project doesn't exist
    if project_path.exists():
        raise ValueError(f"Project directory already exists: {project_path}")

    # Add built-in variables
    all_variables = {
        'project_name': project_name,
        'date': datetime.now().strftime('%Y-%m-%d'),
        'year': datetime.now().strftime('%Y'),
    }

    # Add defaults for template variables
    for var_name, var in template.metadata.variables.items():
        if var_name not in variables and var.default is not None:
            all_variables[var_name] = var.default

    # Merge provided variables (overrides defaults)
    all_variables.update(variables)

    # Validate required variables
    for var_name, var in template.metadata.variables.items():
        if var.required and var_name not in all_variables:
            raise ValueError(f"Required variable '{var_name}' is missing")

        # Validate variable value
        value = all_variables.get(var_name, var.default)
        is_valid, error = var.validate_value(value)
        if not is_valid:
            raise ValueError(error)

    # Create project directory
    project_path.mkdir(parents=True, exist_ok=True)

    if verbose:
        print_info(t('copying_files'))

    # Copy and process files
    structure_path = template.get_structure_path()

    for source_file in structure_path.rglob('*'):
        if source_file.is_file():
            relative_path = source_file.relative_to(structure_path)

            # Substitute variables in filename
            new_path_str = str(relative_path)
            for var_name, var_value in all_variables.items():
                new_path_str = new_path_str.replace(f'{{{{{var_name}}}}}', str(var_value))

            dest_file = project_path / new_path_str
            dest_file.parent.mkdir(parents=True, exist_ok=True)

            # Detect file type
            file_type = detect_file_type(source_file)

            if file_type == 'text':
                # Read, substitute, and write
                try:
                    content = source_file.read_text(encoding='utf-8')

                    if verbose:
                        print_info(t('substituting_variables'))

                    # Substitute variables
                    content = substitute_variables(content, all_variables)

                    dest_file.write_text(content, encoding='utf-8')

                except Exception as e:
                    console.print(f"[yellow]Warning: Failed to process {relative_path}: {e}[/yellow]")
                    # Fallback to binary copy
                    shutil.copy2(source_file, dest_file)
            else:
                # Binary copy
                shutil.copy2(source_file, dest_file)

            if verbose:
                console.print(f"  Created: {new_path_str}")

    return project_path


# =============================================================================
# TEMPLATE MANAGEMENT
# =============================================================================

def delete_template(name: str, force: bool = False) -> bool:
    """Delete custom template.

    Args:
        name: Template name
        force: Skip confirmation prompt

    Returns:
        True if deleted successfully

    Raises:
        FileNotFoundError: If template doesn't exist
    """
    template_path = get_templates_directory() / name

    if not template_path.exists():
        raise FileNotFoundError(f"Template '{name}' not found")

    if not force:
        from rich.prompt import Confirm
        confirmed = Confirm.ask(f"Delete template '{name}'?", default=False)
        if not confirmed:
            return False

    # Delete template directory
    shutil.rmtree(template_path)

    print_success(t('template_deleted'))
    return True
