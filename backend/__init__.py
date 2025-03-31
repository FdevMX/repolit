# Importaciones principales para facilitar el acceso a las funciones del backend
import os

# Determinar si usar la base de datos o almacenamiento local
USE_DATABASE = os.getenv("USE_DATABASE", "False").lower() == "true"

# Auth
from .auth.auth_service import (
    login,
    register,
    logout,
    is_authenticated,
    get_current_user,
    is_admin,
)

# Importar servicios según la configuración
if USE_DATABASE:
    # Servicios basados en base de datos
    try:
        from .data.user_data import (
            get_users,
            get_user_by_id,
            get_user_by_email,
            create_user,
            update_user,
            delete_user,
        )

        # Aquí irían las importaciones del resto de módulos con base de datos

        print("Usando PostgreSQL como fuente de datos")
    except Exception as e:
        print(f"Error al importar módulos de base de datos: {e}")
        print("Fallback: usando almacenamiento local JSON")
        from .data.user_data import (
            get_users,
            get_user_by_id,
            get_user_by_email,
            create_user,
            update_user,
            delete_user,
        )
else:
    # Servicios basados en almacenamiento local
    from .data.user_data import (
        get_users,
        get_user_by_id,
        get_user_by_email,
        create_user,
        update_user,
        delete_user,
    )

    print("Usando almacenamiento local JSON")

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
