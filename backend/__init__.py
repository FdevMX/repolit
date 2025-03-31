# Importaciones principales para facilitar el acceso a las funciones del backend

# Auth
from .auth.auth_service import (
    login, register, logout, is_authenticated, get_current_user, is_admin
)

# Data Services
from .data.user_data import (
    get_users, get_user_by_id, get_user_by_email, create_user, update_user, delete_user
)
from .data.category_data import (
    get_categories, get_category_by_id, get_category_by_name, 
    create_category, update_category, delete_category
)
from .data.tag_data import (
    get_tags, get_tag_by_id, get_tag_by_name, create_tag, delete_tag, get_or_create_tags
)
from .data.publication_data import (
    get_publications, get_publication_by_id, get_publications_by_user,
    get_publications_by_category, create_publication, update_publication,
    delete_publication, get_publication_tags, get_publications_with_tags,
    search_publications
)

# File Handling
from .storage.file_handler import (
    save_uploaded_file, delete_file, get_file_path
)

# Archivo inicializador del paquete storage
from .storage.setup_directories import create_files_directory

# Crear directorio de archivos al importar el módulo
create_files_directory()