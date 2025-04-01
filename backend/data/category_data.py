# Operaciones CRUD para categorías usando PostgreSQL
import logging
from ..db.connection import execute_query
import uuid
from datetime import datetime

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("category_data")

def get_categories():
    """Obtiene todas las categorías ordenadas por nombre."""
    try:
        query = "SELECT id, name, created_at, updated_at FROM categories ORDER BY name"
        categories = execute_query(query)
        logger.debug(f"Recuperadas {len(categories)} categorías")
        return categories
    except Exception as e:
        logger.error(f"Error al obtener categorías: {e}")
        return []

def get_category_by_id(category_id):
    """Obtiene una categoría por su ID."""
    try:
        query = "SELECT id, name, created_at, updated_at FROM categories WHERE id = %s"
        category = execute_query(query, (category_id,), fetchone=True)
        return category
    except Exception as e:
        logger.error(f"Error al obtener categoría por ID {category_id}: {e}")
        return None

def get_category_by_name(name):
    """Obtiene una categoría por su nombre (case insensitive)."""
    try:
        query = "SELECT id, name, created_at, updated_at FROM categories WHERE lower(name) = lower(%s)"
        category = execute_query(query, (name,), fetchone=True)
        return category
    except Exception as e:
        logger.error(f"Error al obtener categoría por nombre '{name}': {e}")
        return None

def create_category(name):
    """Crea una nueva categoría."""
    # Verificar si ya existe una categoría con el mismo nombre
    if get_category_by_name(name):
        logger.warning(f"Intento de crear categoría con nombre duplicado: {name}")
        return None
    
    try:
        # Generar un UUID para la nueva categoría
        category_id = str(uuid.uuid4())
        
        query = """
        INSERT INTO categories (id, name, created_at, updated_at)
        VALUES (%s, %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
        RETURNING id, name, created_at, updated_at
        """
        
        new_category = execute_query(query, (category_id, name), fetchone=True, commit=True)
        logger.info(f"Categoría creada: {name} (ID: {category_id})")
        return new_category
    
    except Exception as e:
        logger.error(f"Error al crear categoría '{name}': {e}")
        return None

def update_category(category_id, name):
    """Actualiza una categoría existente."""
    # Verificar si ya existe otra categoría con el mismo nombre
    existing = get_category_by_name(name)
    if existing and existing['id'] != category_id:
        logger.warning(f"Intento de actualizar categoría a nombre duplicado: {name}")
        return None
    
    try:
        query = """
        UPDATE categories
        SET name = %s, updated_at = CURRENT_TIMESTAMP
        WHERE id = %s
        RETURNING id, name, created_at, updated_at
        """
        
        updated_category = execute_query(query, (name, category_id), fetchone=True, commit=True)
        
        if updated_category:
            logger.info(f"Categoría actualizada: {category_id} -> {name}")
            return updated_category
        else:
            logger.warning(f"No se encontró categoría con ID: {category_id}")
            return None
            
    except Exception as e:
        logger.error(f"Error al actualizar categoría {category_id}: {e}")
        return None

def delete_category(category_id):
    """Elimina una categoría si no está en uso."""
    try:
        # Verificar si hay publicaciones usando esta categoría
        check_query = "SELECT COUNT(*) as count FROM publications WHERE category_id = %s"
        result = execute_query(check_query, (category_id,), fetchone=True)
        
        if result and result['count'] > 0:
            logger.warning(f"No se puede eliminar categoría {category_id}: tiene {result['count']} publicaciones asociadas")
            return False
        
        # Eliminar la categoría si no está en uso
        delete_query = "DELETE FROM categories WHERE id = %s RETURNING id"
        result = execute_query(delete_query, (category_id,), fetchone=True, commit=True)
        
        if result:
            logger.info(f"Categoría eliminada: {category_id}")
            return True
        else:
            logger.warning(f"No se encontró categoría con ID: {category_id}")
            return False
            
    except Exception as e:
        logger.error(f"Error al eliminar categoría {category_id}: {e}")
        return False