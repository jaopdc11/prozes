"""Internationalization module for Prozes."""

import os
from pathlib import Path

# Default language
_current_lang = 'en'

# Translations
TRANSLATIONS = {
    'en': {
        # Headers
        'creating_project_mvc': 'Creating MVC project',
        'creating_project_api': 'Creating REST API',
        'creating_project_cli': 'Creating CLI project',
        'creating_project_clean': 'Creating Clean Architecture project',

        # Steps
        'creating_folder_structure': 'Creating folder structure...',
        'creating_venv': 'Creating virtual environment...',
        'installing_deps': 'Installing dependencies...',
        'initializing_git': 'Initializing Git repository...',

        # Success messages
        'venv_created': 'Virtual environment created',
        'deps_installed': 'Dependencies installed',
        'git_initialized': 'Git repository initialized',
        'structure_mvc_created': 'MVC structure created',
        'structure_api_created': 'REST API structure created',
        'structure_cli_created': 'CLI structure created',
        'structure_clean_created': 'Clean Architecture structure created',
        'requirements_created': 'requirements.txt created',
        'project_created': 'Project created successfully!',

        # Error messages
        'error_creating_project': 'Error creating project',
        'venv_already_exists': 'Virtual environment already exists',
        'venv_not_found': 'Virtual environment not found',
        'python_not_found': 'Python version {version} not found',
        'requirements_not_found': 'Requirements file not found',
        'git_not_found': 'Git not found. Make sure Git is installed.',

        # Validation messages
        'validation_name_empty': 'Project name cannot be empty',
        'validation_name_start': 'Project name must start with a letter or underscore',
        'validation_name_chars': 'Project name can only contain letters, numbers, and underscores',
        'validation_name_keyword': "'{name}' is a Python reserved keyword",
        'validation_project_exists': "Project '{name}' already exists in the current directory",
        'validation_python_version_format': "Invalid Python version format: '{version}'. Use format like 3.8 or 3.11",
        'validation_git_not_available': 'Git is not installed or not available in PATH',
        'validation_install_deps_requires_venv': '--install-deps requires --venv to be specified',
        'validation_errors_header': 'Validation errors',

        # Summary table
        'project': 'Project',
        'type': 'Type',
        'venv': 'Venv',
        'git': 'Git',
        'deps': 'Deps',
        'created': 'Created',
        'initialized': 'Initialized',
        'installed': 'Installed',

        # Next steps
        'next_steps': 'Next steps',
        'activate_venv_win': '(Windows)',
        'activate_venv_unix': '(Linux/Mac)',
        'open_docs': 'Open',

        # CLI Help texts
        'help_main': 'Prozes - Python project generator with predefined architectures.\n\nAll commands support: --venv, --git, --auth, --install-deps, --python-version, -v/--verbose',
        'help_lang': 'Language (en=English, pt=Portuguese). Uses global config if not specified.',
        'help_verbose': 'Verbose mode',
        'help_git': 'Initialize Git repository',
        'help_venv': 'Create virtual environment',
        'help_python_version': 'Python version for venv (e.g., 3.11)',
        'help_install_deps': 'Install dependencies automatically',
        'help_auth': 'Authentication type (default: none)',

        # Auth types
        'auth_jwt': 'JWT token-based authentication',
        'auth_oauth2': 'OAuth2 third-party authentication',
        'auth_session': 'Session-based authentication',
        'auth_basic': 'HTTP Basic authentication',

        # Auth messages
        'auth_configured': 'Authentication configured',
        'auth_warning_database': 'Note: Using in-memory storage. For production, replace with a real database.',

        'help_mvc': 'Create a project with MVC architecture.',
        'help_mvc_long': 'Structure with Models, Views, Controllers, templates and static files.',
        'help_mvc_type': 'Project type (default: web-flask)',

        'help_api': 'Create a pure REST API (no frontend).',
        'help_api_long': 'Lean structure focused on REST endpoints.',
        'help_api_type': 'API framework (default: fastapi)',

        'help_cli': 'Create a CLI project with Click.',
        'help_cli_long': 'Structure for command-line applications.',

        'help_clean': 'Create a project with Clean Architecture.',
        'help_clean_long': '''Structure:
  src/entities/     - Domain entities
  src/use_cases/    - Use cases (business rules)
  src/adapters/     - Repositories, Presenters
  src/frameworks/   - External frameworks (web, db)''',
        'help_clean_type': 'Web framework (default: flask)',

        'help_config': 'Configure Prozes settings.',
        'help_config_lang': 'Set default language (en=English, pt=Portuguese)',
        'help_config_show': 'Show current configuration',

        # Template commands
        'help_template': 'Manage custom templates',
        'help_template_save': 'Save existing project as template',
        'help_template_list': 'List all available templates',
        'help_template_use': 'Create project from custom template',
        'help_template_show': 'Show template details',
        'help_template_delete': 'Delete custom template',

        # Template messages
        'template_saved': 'Template saved successfully',
        'template_not_found': "Template '{name}' not found",
        'scanning_project': 'Scanning project structure...',
        'detecting_variables': 'Detecting variables...',
        'copying_files': 'Copying files...',
        'substituting_variables': 'Substituting variables...',
        'template_exists': "Template '{name}' already exists",
        'confirm_overwrite': 'Overwrite existing template?',
        'template_deleted': 'Template deleted successfully',
        'custom_templates': 'Custom Templates',
        'builtin_templates': 'Built-in Templates',
        'no_custom_templates': 'No custom templates found',
        'template_details': 'Template Details',
        'template_name': 'Name',
        'template_description': 'Description',
        'template_author': 'Author',
        'template_created': 'Created',
        'template_location': 'Location',
        'template_variables': 'Variables',
        'template_files': 'Files',

        # Template errors
        'error_invalid_template': 'Invalid template structure',
        'error_source_not_found': 'Source directory not found',
        'error_template_validation': 'Template validation failed',
        'error_template_exists': "Template '{name}' already exists",
        'error_template_name_invalid': 'Invalid template name',
    },
    'pt': {
        # Headers
        'creating_project_mvc': 'Criando projeto MVC',
        'creating_project_api': 'Criando API REST',
        'creating_project_cli': 'Criando projeto CLI',
        'creating_project_clean': 'Criando projeto Clean Architecture',

        # Steps
        'creating_folder_structure': 'Criando estrutura de pastas...',
        'creating_venv': 'Criando ambiente virtual...',
        'installing_deps': 'Instalando dependencias...',
        'initializing_git': 'Inicializando repositorio Git...',

        # Success messages
        'venv_created': 'Ambiente virtual criado',
        'deps_installed': 'Dependencias instaladas',
        'git_initialized': 'Repositorio Git inicializado',
        'structure_mvc_created': 'Estrutura MVC criada',
        'structure_api_created': 'Estrutura API REST criada',
        'structure_cli_created': 'Estrutura CLI criada',
        'structure_clean_created': 'Estrutura Clean Architecture criada',
        'requirements_created': 'requirements.txt criado',
        'project_created': 'Projeto criado com sucesso!',

        # Error messages
        'error_creating_project': 'Erro ao criar projeto',
        'venv_already_exists': 'Ambiente virtual ja existe',
        'venv_not_found': 'Ambiente virtual nao encontrado',
        'python_not_found': 'Python versao {version} nao encontrado',
        'requirements_not_found': 'Arquivo de requirements nao encontrado',
        'git_not_found': 'Git nao encontrado. Certifique-se de que o Git esta instalado.',

        # Validation messages
        'validation_name_empty': 'Nome do projeto nao pode ser vazio',
        'validation_name_start': 'Nome do projeto deve comecar com uma letra ou underscore',
        'validation_name_chars': 'Nome do projeto pode conter apenas letras, numeros e underscores',
        'validation_name_keyword': "'{name}' e uma palavra reservada do Python",
        'validation_project_exists': "Projeto '{name}' ja existe no diretorio atual",
        'validation_python_version_format': "Formato de versao Python invalido: '{version}'. Use formato como 3.8 ou 3.11",
        'validation_git_not_available': 'Git nao esta instalado ou nao esta disponivel no PATH',
        'validation_install_deps_requires_venv': '--install-deps requer que --venv seja especificado',
        'validation_errors_header': 'Erros de validacao',

        # Summary table
        'project': 'Projeto',
        'type': 'Tipo',
        'venv': 'Venv',
        'git': 'Git',
        'deps': 'Deps',
        'created': 'Criado',
        'initialized': 'Inicializado',
        'installed': 'Instalado',

        # Next steps
        'next_steps': 'Proximos passos',
        'activate_venv_win': '(Windows)',
        'activate_venv_unix': '(Linux/Mac)',
        'open_docs': 'Abrir',

        # CLI Help texts
        'help_main': 'Prozes - Gerador de projetos Python com arquiteturas predefinidas.\n\nTodos os comandos suportam: --venv, --git, --auth, --install-deps, --python-version, -v/--verbose',
        'help_lang': 'Idioma (en=Ingles, pt=Portugues). Usa config global se nao especificado.',
        'help_verbose': 'Modo detalhado',
        'help_git': 'Inicializar repositorio Git',
        'help_venv': 'Criar ambiente virtual',
        'help_python_version': 'Versao do Python para venv (ex: 3.11)',
        'help_install_deps': 'Instalar dependencias automaticamente',
        'help_auth': 'Tipo de autenticacao (padrao: none)',

        # Auth types
        'auth_jwt': 'Autenticacao baseada em tokens JWT',
        'auth_oauth2': 'Autenticacao OAuth2 com terceiros',
        'auth_session': 'Autenticacao baseada em sessao',
        'auth_basic': 'Autenticacao HTTP Basic',

        # Auth messages
        'auth_configured': 'Autenticacao configurada',
        'auth_warning_database': 'Nota: Usando armazenamento em memoria. Para producao, substitua por um banco de dados real.',

        'help_mvc': 'Criar projeto com arquitetura MVC.',
        'help_mvc_long': 'Estrutura com Models, Views, Controllers, templates e arquivos estaticos.',
        'help_mvc_type': 'Tipo do projeto (padrao: web-flask)',

        'help_api': 'Criar uma API REST pura (sem frontend).',
        'help_api_long': 'Estrutura enxuta focada em endpoints REST.',
        'help_api_type': 'Framework da API (padrao: fastapi)',

        'help_cli': 'Criar projeto CLI com Click.',
        'help_cli_long': 'Estrutura para aplicacoes de linha de comando.',

        'help_clean': 'Criar projeto com Clean Architecture.',
        'help_clean_long': '''Estrutura:
  src/entities/     - Entidades do dominio
  src/use_cases/    - Casos de uso (regras de negocio)
  src/adapters/     - Repositorios, Presenters
  src/frameworks/   - Frameworks externos (web, db)''',
        'help_clean_type': 'Framework web (padrao: flask)',

        'help_config': 'Configurar opcoes do Prozes.',
        'help_config_lang': 'Definir idioma padrao (en=Ingles, pt=Portugues)',
        'help_config_show': 'Mostrar configuracao atual',

        # Template commands
        'help_template': 'Gerenciar templates customizados',
        'help_template_save': 'Salvar projeto existente como template',
        'help_template_list': 'Listar todos os templates disponiveis',
        'help_template_use': 'Criar projeto a partir de template customizado',
        'help_template_show': 'Mostrar detalhes do template',
        'help_template_delete': 'Deletar template customizado',

        # Template messages
        'template_saved': 'Template salvo com sucesso',
        'template_not_found': "Template '{name}' nao encontrado",
        'scanning_project': 'Escaneando estrutura do projeto...',
        'detecting_variables': 'Detectando variaveis...',
        'copying_files': 'Copiando arquivos...',
        'substituting_variables': 'Substituindo variaveis...',
        'template_exists': "Template '{name}' ja existe",
        'confirm_overwrite': 'Sobrescrever template existente?',
        'template_deleted': 'Template deletado com sucesso',
        'custom_templates': 'Templates Customizados',
        'builtin_templates': 'Templates Built-in',
        'no_custom_templates': 'Nenhum template customizado encontrado',
        'template_details': 'Detalhes do Template',
        'template_name': 'Nome',
        'template_description': 'Descricao',
        'template_author': 'Autor',
        'template_created': 'Criado',
        'template_location': 'Localizacao',
        'template_variables': 'Variaveis',
        'template_files': 'Arquivos',

        # Template errors
        'error_invalid_template': 'Estrutura de template invalida',
        'error_source_not_found': 'Diretorio fonte nao encontrado',
        'error_template_validation': 'Validacao de template falhou',
        'error_template_exists': "Template '{name}' ja existe",
        'error_template_name_invalid': 'Nome de template invalido',
    },
    'es': {
        # Headers
        'creating_project_mvc': 'Creando proyecto MVC',
        'creating_project_api': 'Creando API REST',
        'creating_project_cli': 'Creando proyecto CLI',
        'creating_project_clean': 'Creando proyecto Clean Architecture',

        # Steps
        'creating_folder_structure': 'Creando estructura de carpetas...',
        'creating_venv': 'Creando entorno virtual...',
        'installing_deps': 'Instalando dependencias...',
        'initializing_git': 'Inicializando repositorio Git...',

        # Success messages
        'venv_created': 'Entorno virtual creado',
        'deps_installed': 'Dependencias instaladas',
        'git_initialized': 'Repositorio Git inicializado',
        'structure_mvc_created': 'Estructura MVC creada',
        'structure_api_created': 'Estructura API REST creada',
        'structure_cli_created': 'Estructura CLI creada',
        'structure_clean_created': 'Estructura Clean Architecture creada',
        'requirements_created': 'requirements.txt creado',
        'project_created': '¡Proyecto creado con éxito!',

        # Error messages
        'error_creating_project': 'Error al crear proyecto',
        'venv_already_exists': 'El entorno virtual ya existe',
        'venv_not_found': 'Entorno virtual no encontrado',
        'python_not_found': 'Python versión {version} no encontrado',
        'requirements_not_found': 'Archivo de requirements no encontrado',
        'git_not_found': 'Git no encontrado. Asegúrate de que Git esté instalado.',

        # Validation messages
        'validation_name_empty': 'El nombre del proyecto no puede estar vacío',
        'validation_name_start': 'El nombre del proyecto debe comenzar con una letra o guion bajo',
        'validation_name_chars': 'El nombre del proyecto solo puede contener letras, números y guiones bajos',
        'validation_name_keyword': "'{name}' es una palabra reservada de Python",
        'validation_project_exists': "El proyecto '{name}' ya existe en el directorio actual",
        'validation_python_version_format': "Formato de versión de Python inválido: '{version}'. Use formato como 3.8 o 3.11",
        'validation_git_not_available': 'Git no está instalado o no está disponible en PATH',
        'validation_install_deps_requires_venv': '--install-deps requiere que se especifique --venv',
        'validation_errors_header': 'Errores de validación',

        # Summary table
        'project': 'Proyecto',
        'type': 'Tipo',
        'venv': 'Venv',
        'git': 'Git',
        'deps': 'Deps',
        'created': 'Creado',
        'initialized': 'Inicializado',
        'installed': 'Instalado',

        # Next steps
        'next_steps': 'Próximos pasos',
        'activate_venv_win': '(Windows)',
        'activate_venv_unix': '(Linux/Mac)',
        'open_docs': 'Abrir',

        # CLI Help texts
        'help_main': 'Prozes - Generador de proyectos Python con arquitecturas predefinidas.\n\nTodos los comandos soportan: --venv, --git, --auth, --install-deps, --python-version, -v/--verbose',
        'help_lang': 'Idioma (en=Inglés, pt=Portugués, es=Español, it=Italiano, fr=Francés). Usa config global si no se especifica.',
        'help_verbose': 'Modo detallado',
        'help_git': 'Inicializar repositorio Git',
        'help_venv': 'Crear entorno virtual',
        'help_python_version': 'Versión de Python para venv (ej: 3.11)',
        'help_install_deps': 'Instalar dependencias automáticamente',
        'help_auth': 'Tipo de autenticación (predeterminado: none)',

        # Auth types
        'auth_jwt': 'Autenticación basada en tokens JWT',
        'auth_oauth2': 'Autenticación OAuth2 con terceros',
        'auth_session': 'Autenticación basada en sesión',
        'auth_basic': 'Autenticación HTTP Basic',

        # Auth messages
        'auth_configured': 'Autenticación configurada',
        'auth_warning_database': 'Nota: Usando almacenamiento en memoria. Para producción, reemplaza con una base de datos real.',

        'help_mvc': 'Crear proyecto con arquitectura MVC.',
        'help_mvc_long': 'Estructura con Models, Views, Controllers, templates y archivos estáticos.',
        'help_mvc_type': 'Tipo de proyecto (predeterminado: web-flask)',

        'help_api': 'Crear una API REST pura (sin frontend).',
        'help_api_long': 'Estructura limpia enfocada en endpoints REST.',
        'help_api_type': 'Framework de API (predeterminado: fastapi)',

        'help_cli': 'Crear proyecto CLI con Click.',
        'help_cli_long': 'Estructura para aplicaciones de línea de comandos.',

        'help_clean': 'Crear proyecto con Clean Architecture.',
        'help_clean_long': '''Estructura:
  src/entities/     - Entidades del dominio
  src/use_cases/    - Casos de uso (reglas de negocio)
  src/adapters/     - Repositorios, Presentadores
  src/frameworks/   - Frameworks externos (web, db)''',
        'help_clean_type': 'Framework web (predeterminado: flask)',

        'help_config': 'Configurar opciones de Prozes.',
        'help_config_lang': 'Definir idioma predeterminado (en=Inglés, pt=Portugués, es=Español, it=Italiano, fr=Francés)',
        'help_config_show': 'Mostrar configuración actual',

        # Template commands
        'help_template': 'Gestionar templates personalizados',
        'help_template_save': 'Guardar proyecto existente como template',
        'help_template_list': 'Listar todos los templates disponibles',
        'help_template_use': 'Crear proyecto a partir de template personalizado',
        'help_template_show': 'Mostrar detalles del template',
        'help_template_delete': 'Eliminar template personalizado',

        # Template messages
        'template_saved': 'Template guardado con éxito',
        'template_not_found': "Template '{name}' no encontrado",
        'scanning_project': 'Escaneando estructura del proyecto...',
        'detecting_variables': 'Detectando variables...',
        'copying_files': 'Copiando archivos...',
        'substituting_variables': 'Sustituyendo variables...',
        'template_exists': "El template '{name}' ya existe",
        'confirm_overwrite': '¿Sobrescribir template existente?',
        'template_deleted': 'Template eliminado con éxito',
        'custom_templates': 'Templates Personalizados',
        'builtin_templates': 'Templates Integrados',
        'no_custom_templates': 'No se encontraron templates personalizados',
        'template_details': 'Detalles del Template',
        'template_name': 'Nombre',
        'template_description': 'Descripción',
        'template_author': 'Autor',
        'template_created': 'Creado',
        'template_location': 'Ubicación',
        'template_variables': 'Variables',
        'template_files': 'Archivos',

        # Template errors
        'error_invalid_template': 'Estructura de template inválida',
        'error_source_not_found': 'Directorio fuente no encontrado',
        'error_template_validation': 'Validación de template falló',
        'error_template_exists': "El template '{name}' ya existe",
        'error_template_name_invalid': 'Nombre de template inválido',
    },
    'it': {
        # Headers
        'creating_project_mvc': 'Creazione progetto MVC',
        'creating_project_api': 'Creazione API REST',
        'creating_project_cli': 'Creazione progetto CLI',
        'creating_project_clean': 'Creazione progetto Clean Architecture',

        # Steps
        'creating_folder_structure': 'Creazione struttura cartelle...',
        'creating_venv': 'Creazione ambiente virtuale...',
        'installing_deps': 'Installazione dipendenze...',
        'initializing_git': 'Inizializzazione repository Git...',

        # Success messages
        'venv_created': 'Ambiente virtuale creato',
        'deps_installed': 'Dipendenze installate',
        'git_initialized': 'Repository Git inizializzato',
        'structure_mvc_created': 'Struttura MVC creata',
        'structure_api_created': 'Struttura API REST creata',
        'structure_cli_created': 'Struttura CLI creata',
        'structure_clean_created': 'Struttura Clean Architecture creata',
        'requirements_created': 'requirements.txt creato',
        'project_created': 'Progetto creato con successo!',

        # Error messages
        'error_creating_project': 'Errore durante la creazione del progetto',
        'venv_already_exists': "L'ambiente virtuale esiste già",
        'venv_not_found': 'Ambiente virtuale non trovato',
        'python_not_found': 'Python versione {version} non trovato',
        'requirements_not_found': 'File requirements non trovato',
        'git_not_found': 'Git non trovato. Assicurati che Git sia installato.',

        # Validation messages
        'validation_name_empty': 'Il nome del progetto non può essere vuoto',
        'validation_name_start': 'Il nome del progetto deve iniziare con una lettera o underscore',
        'validation_name_chars': 'Il nome del progetto può contenere solo lettere, numeri e underscore',
        'validation_name_keyword': "'{name}' è una parola riservata di Python",
        'validation_project_exists': "Il progetto '{name}' esiste già nella directory corrente",
        'validation_python_version_format': "Formato versione Python non valido: '{version}'. Usa formato come 3.8 o 3.11",
        'validation_git_not_available': 'Git non è installato o non è disponibile in PATH',
        'validation_install_deps_requires_venv': '--install-deps richiede che sia specificato --venv',
        'validation_errors_header': 'Errori di validazione',

        # Summary table
        'project': 'Progetto',
        'type': 'Tipo',
        'venv': 'Venv',
        'git': 'Git',
        'deps': 'Deps',
        'created': 'Creato',
        'initialized': 'Inizializzato',
        'installed': 'Installato',

        # Next steps
        'next_steps': 'Prossimi passi',
        'activate_venv_win': '(Windows)',
        'activate_venv_unix': '(Linux/Mac)',
        'open_docs': 'Apri',

        # CLI Help texts
        'help_main': 'Prozes - Generatore di progetti Python con architetture predefinite.\n\nTutti i comandi supportano: --venv, --git, --auth, --install-deps, --python-version, -v/--verbose',
        'help_lang': 'Lingua (en=Inglese, pt=Portoghese, es=Spagnolo, it=Italiano, fr=Francese). Usa config globale se non specificato.',
        'help_verbose': 'Modalità dettagliata',
        'help_git': 'Inizializza repository Git',
        'help_venv': 'Crea ambiente virtuale',
        'help_python_version': 'Versione Python per venv (es: 3.11)',
        'help_install_deps': 'Installa dipendenze automaticamente',
        'help_auth': 'Tipo di autenticazione (predefinito: none)',

        # Auth types
        'auth_jwt': 'Autenticazione basata su token JWT',
        'auth_oauth2': 'Autenticazione OAuth2 con terze parti',
        'auth_session': 'Autenticazione basata su sessione',
        'auth_basic': 'Autenticazione HTTP Basic',

        # Auth messages
        'auth_configured': 'Autenticazione configurata',
        'auth_warning_database': 'Nota: Utilizzo di storage in memoria. Per produzione, sostituisci con un database reale.',

        'help_mvc': 'Crea progetto con architettura MVC.',
        'help_mvc_long': 'Struttura con Models, Views, Controllers, template e file statici.',
        'help_mvc_type': 'Tipo di progetto (predefinito: web-flask)',

        'help_api': 'Crea una API REST pura (senza frontend).',
        'help_api_long': 'Struttura snella focalizzata su endpoint REST.',
        'help_api_type': 'Framework API (predefinito: fastapi)',

        'help_cli': 'Crea progetto CLI con Click.',
        'help_cli_long': 'Struttura per applicazioni da riga di comando.',

        'help_clean': 'Crea progetto con Clean Architecture.',
        'help_clean_long': '''Struttura:
  src/entities/     - Entità del dominio
  src/use_cases/    - Casi d\'uso (regole di business)
  src/adapters/     - Repository, Presenter
  src/frameworks/   - Framework esterni (web, db)''',
        'help_clean_type': 'Framework web (predefinito: flask)',

        'help_config': 'Configura opzioni di Prozes.',
        'help_config_lang': 'Imposta lingua predefinita (en=Inglese, pt=Portoghese, es=Spagnolo, it=Italiano, fr=Francese)',
        'help_config_show': 'Mostra configurazione corrente',

        # Template commands
        'help_template': 'Gestisci template personalizzati',
        'help_template_save': 'Salva progetto esistente come template',
        'help_template_list': 'Elenca tutti i template disponibili',
        'help_template_use': 'Crea progetto da template personalizzato',
        'help_template_show': 'Mostra dettagli template',
        'help_template_delete': 'Elimina template personalizzato',

        # Template messages
        'template_saved': 'Template salvato con successo',
        'template_not_found': "Template '{name}' non trovato",
        'scanning_project': 'Scansione struttura progetto...',
        'detecting_variables': 'Rilevamento variabili...',
        'copying_files': 'Copia file...',
        'substituting_variables': 'Sostituzione variabili...',
        'template_exists': "Il template '{name}' esiste già",
        'confirm_overwrite': 'Sovrascrivere template esistente?',
        'template_deleted': 'Template eliminato con successo',
        'custom_templates': 'Template Personalizzati',
        'builtin_templates': 'Template Integrati',
        'no_custom_templates': 'Nessun template personalizzato trovato',
        'template_details': 'Dettagli Template',
        'template_name': 'Nome',
        'template_description': 'Descrizione',
        'template_author': 'Autore',
        'template_created': 'Creato',
        'template_location': 'Posizione',
        'template_variables': 'Variabili',
        'template_files': 'File',

        # Template errors
        'error_invalid_template': 'Struttura template non valida',
        'error_source_not_found': 'Directory sorgente non trovata',
        'error_template_validation': 'Validazione template fallita',
        'error_template_exists': "Il template '{name}' esiste già",
        'error_template_name_invalid': 'Nome template non valido',
    },
    'fr': {
        # Headers
        'creating_project_mvc': 'Création du projet MVC',
        'creating_project_api': 'Création de l\'API REST',
        'creating_project_cli': 'Création du projet CLI',
        'creating_project_clean': 'Création du projet Clean Architecture',

        # Steps
        'creating_folder_structure': 'Création de la structure de dossiers...',
        'creating_venv': 'Création de l\'environnement virtuel...',
        'installing_deps': 'Installation des dépendances...',
        'initializing_git': 'Initialisation du dépôt Git...',

        # Success messages
        'venv_created': 'Environnement virtuel créé',
        'deps_installed': 'Dépendances installées',
        'git_initialized': 'Dépôt Git initialisé',
        'structure_mvc_created': 'Structure MVC créée',
        'structure_api_created': 'Structure API REST créée',
        'structure_cli_created': 'Structure CLI créée',
        'structure_clean_created': 'Structure Clean Architecture créée',
        'requirements_created': 'requirements.txt créé',
        'project_created': 'Projet créé avec succès !',

        # Error messages
        'error_creating_project': 'Erreur lors de la création du projet',
        'venv_already_exists': 'L\'environnement virtuel existe déjà',
        'venv_not_found': 'Environnement virtuel non trouvé',
        'python_not_found': 'Python version {version} non trouvé',
        'requirements_not_found': 'Fichier requirements non trouvé',
        'git_not_found': 'Git non trouvé. Assurez-vous que Git est installé.',

        # Validation messages
        'validation_name_empty': 'Le nom du projet ne peut pas être vide',
        'validation_name_start': 'Le nom du projet doit commencer par une lettre ou un underscore',
        'validation_name_chars': 'Le nom du projet ne peut contenir que des lettres, des chiffres et des underscores',
        'validation_name_keyword': "'{name}' est un mot-clé réservé de Python",
        'validation_project_exists': "Le projet '{name}' existe déjà dans le répertoire actuel",
        'validation_python_version_format': "Format de version Python invalide : '{version}'. Utilisez un format comme 3.8 ou 3.11",
        'validation_git_not_available': 'Git n\'est pas installé ou n\'est pas disponible dans PATH',
        'validation_install_deps_requires_venv': '--install-deps nécessite que --venv soit spécifié',
        'validation_errors_header': 'Erreurs de validation',

        # Summary table
        'project': 'Projet',
        'type': 'Type',
        'venv': 'Venv',
        'git': 'Git',
        'deps': 'Deps',
        'created': 'Créé',
        'initialized': 'Initialisé',
        'installed': 'Installé',

        # Next steps
        'next_steps': 'Prochaines étapes',
        'activate_venv_win': '(Windows)',
        'activate_venv_unix': '(Linux/Mac)',
        'open_docs': 'Ouvrir',

        # CLI Help texts
        'help_main': 'Prozes - Générateur de projets Python avec architectures prédéfinies.\n\nToutes les commandes supportent : --venv, --git, --auth, --install-deps, --python-version, -v/--verbose',
        'help_lang': 'Langue (en=Anglais, pt=Portugais, es=Espagnol, it=Italien, fr=Français). Utilise config globale si non spécifié.',
        'help_verbose': 'Mode détaillé',
        'help_git': 'Initialiser le dépôt Git',
        'help_venv': 'Créer un environnement virtuel',
        'help_python_version': 'Version Python pour venv (ex : 3.11)',
        'help_install_deps': 'Installer les dépendances automatiquement',
        'help_auth': 'Type d\'authentification (par défaut : none)',

        # Auth types
        'auth_jwt': 'Authentification basée sur tokens JWT',
        'auth_oauth2': 'Authentification OAuth2 avec tiers',
        'auth_session': 'Authentification basée sur session',
        'auth_basic': 'Authentification HTTP Basic',

        # Auth messages
        'auth_configured': 'Authentification configurée',
        'auth_warning_database': 'Note : Utilisation du stockage en mémoire. Pour la production, remplacez par une vraie base de données.',

        'help_mvc': 'Créer un projet avec architecture MVC.',
        'help_mvc_long': 'Structure avec Models, Views, Controllers, templates et fichiers statiques.',
        'help_mvc_type': 'Type de projet (par défaut : web-flask)',

        'help_api': 'Créer une API REST pure (sans frontend).',
        'help_api_long': 'Structure légère axée sur les endpoints REST.',
        'help_api_type': 'Framework API (par défaut : fastapi)',

        'help_cli': 'Créer un projet CLI avec Click.',
        'help_cli_long': 'Structure pour applications en ligne de commande.',

        'help_clean': 'Créer un projet avec Clean Architecture.',
        'help_clean_long': '''Structure :
  src/entities/     - Entités du domaine
  src/use_cases/    - Cas d\'usage (règles métier)
  src/adapters/     - Dépôts, Présentateurs
  src/frameworks/   - Frameworks externes (web, db)''',
        'help_clean_type': 'Framework web (par défaut : flask)',

        'help_config': 'Configurer les options de Prozes.',
        'help_config_lang': 'Définir la langue par défaut (en=Anglais, pt=Portugais, es=Espagnol, it=Italien, fr=Français)',
        'help_config_show': 'Afficher la configuration actuelle',

        # Template commands
        'help_template': 'Gérer les templates personnalisés',
        'help_template_save': 'Enregistrer un projet existant comme template',
        'help_template_list': 'Lister tous les templates disponibles',
        'help_template_use': 'Créer un projet à partir d\'un template personnalisé',
        'help_template_show': 'Afficher les détails du template',
        'help_template_delete': 'Supprimer un template personnalisé',

        # Template messages
        'template_saved': 'Template enregistré avec succès',
        'template_not_found': "Template '{name}' non trouvé",
        'scanning_project': 'Analyse de la structure du projet...',
        'detecting_variables': 'Détection des variables...',
        'copying_files': 'Copie des fichiers...',
        'substituting_variables': 'Substitution des variables...',
        'template_exists': "Le template '{name}' existe déjà",
        'confirm_overwrite': 'Écraser le template existant ?',
        'template_deleted': 'Template supprimé avec succès',
        'custom_templates': 'Templates Personnalisés',
        'builtin_templates': 'Templates Intégrés',
        'no_custom_templates': 'Aucun template personnalisé trouvé',
        'template_details': 'Détails du Template',
        'template_name': 'Nom',
        'template_description': 'Description',
        'template_author': 'Auteur',
        'template_created': 'Créé',
        'template_location': 'Emplacement',
        'template_variables': 'Variables',
        'template_files': 'Fichiers',

        # Template errors
        'error_invalid_template': 'Structure de template invalide',
        'error_source_not_found': 'Répertoire source non trouvé',
        'error_template_validation': 'Validation du template échouée',
        'error_template_exists': "Le template '{name}' existe déjà",
        'error_template_name_invalid': 'Nom de template invalide',
    },
}


def set_language(lang: str):
    """Set the current language."""
    global _current_lang
    if lang in TRANSLATIONS:
        _current_lang = lang
    else:
        _current_lang = 'en'


def get_language() -> str:
    """Get the current language."""
    return _current_lang


def t(key: str, **kwargs) -> str:
    """Get translated string by key.

    Args:
        key: Translation key
        **kwargs: Format arguments for the string

    Returns:
        Translated string, or the key if not found
    """
    lang_dict = TRANSLATIONS.get(_current_lang, TRANSLATIONS['en'])
    text = lang_dict.get(key, key)

    if kwargs:
        try:
            text = text.format(**kwargs)
        except KeyError:
            pass

    return text


def load_language_from_env():
    """Load language from PROZEES_LANG environment variable."""
    lang = os.environ.get('PROZEES_LANG', 'en').lower()
    set_language(lang)


def load_language_from_config():
    """Load language from config file if exists."""
    config_paths = [
        Path.home() / '.prozes' / 'config',
        Path.home() / '.config' / 'prozes' / 'config',
    ]

    for config_path in config_paths:
        if config_path.exists():
            try:
                content = config_path.read_text().strip()
                for line in content.split('\n'):
                    if line.startswith('lang=') or line.startswith('language='):
                        lang = line.split('=')[1].strip()
                        set_language(lang)
                        return
            except Exception:
                pass

    # Fallback to environment variable
    load_language_from_env()


# Initialize language on module load
load_language_from_config()
