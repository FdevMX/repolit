# Operaciones CRUD para tags usando PostgreSQL
import logging
from ..db.connection import execute_query
import uuid
from datetime import datetime

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("tag_data")

def get_tags():
    """Obtiene todos los tags ordenados por nombre."""
    try:
        query = "SELECT id, name, created_at, updated_at FROM tags ORDER BY name"
        tags = execute_query(query)
        logger.debug(f"Recuperados {len(tags)} tags")
        return tags
    except Exception as e:
        logger.error(f"Error al obtener tags: {e}")
        return []

def get_tag_by_id(tag_id):
    """Obtiene un tag por su ID."""
    try:
        query = "SELECT id, name, created_at, updated_at FROM tags WHERE id = %s"
        tag = execute_query(query, (tag_id,), fetchone=True)
        return tag
    except Exception as e:
        logger.error(f"Error al obtener tag por ID {tag_id}: {e}")
        return None

def get_tag_by_name(name):
    """Obtiene un tag por su nombre (case insensitive)."""
    try:
        query = "SELECT id, name, created_at, updated_at FROM tags WHERE lower(name) = lower(%s)"
        tag = execute_query(query, (name,), fetchone=True)
        return tag
    except Exception as e:
        logger.error(f"Error al obtener tag por nombre '{name}': {e}")
        return None

def create_tag(name):
    """Crea un nuevo tag."""
    # Verificar si ya existe un tag con el mismo nombre
    if get_tag_by_name(name):
        logger.warning(f"Intento de crear tag con nombre duplicado: {name}")
        return None
    
    try:
        # Generar un UUID para el nuevo tag
        tag_id = str(uuid.uuid4())
        
        query = """
        INSERT INTO tags (id, name, created_at, updated_at)
        VALUES (%s, %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
        RETURNING id, name, created_at, updated_at
        """
        
        new_tag = execute_query(query, (tag_id, name), fetchone=True, commit=True)
        logger.info(f"Tag creado: {name} (ID: {tag_id})")
        return new_tag
    
    except Exception as e:
        logger.error(f"Error al crear tag '{name}': {e}")
        return None

def update_tag(tag_id, name):
    """Actualiza un tag existente."""
    # Verificar si ya existe otro tag con el mismo nombre
    existing = get_tag_by_name(name)
    if existing and existing['id'] != tag_id:
        logger.warning(f"Intento de actualizar tag a nombre duplicado: {name}")
        return None
    
    try:
        query = """
        UPDATE tags
        SET name = %s, updated_at = CURRENT_TIMESTAMP
        WHERE id = %s
        RETURNING id, name, created_at, updated_at
        """
        
        updated_tag = execute_query(query, (name, tag_id), fetchone=True, commit=True)
        
        if updated_tag:
            logger.info(f"Tag actualizado: {tag_id} -> {name}")
            return updated_tag
        else:
            logger.warning(f"No se encontró tag con ID: {tag_id}")
            return None
            
    except Exception as e:
        logger.error(f"Error al actualizar tag {tag_id}: {e}")
        return None

def delete_tag(tag_id):
    """Elimina un tag si no está en uso."""
    try:
        # Verificar si hay publicaciones usando este tag
        check_query = """
        SELECT COUNT(*) as count 
        FROM publication_tags 
        WHERE tag_id = %s
        """
        result = execute_query(check_query, (tag_id,), fetchone=True)
        
        if result and result['count'] > 0:
            logger.warning(f"No se puede eliminar tag {tag_id}: tiene {result['count']} publicaciones asociadas")
            return False
        
        # Eliminar el tag si no está en uso
        delete_query = "DELETE FROM tags WHERE id = %s RETURNING id"
        result = execute_query(delete_query, (tag_id,), fetchone=True, commit=True)
        
        if result:
            logger.info(f"Tag eliminado: {tag_id}")
            return True
        else:
            logger.warning(f"No se encontró tag con ID: {tag_id}")
            return False
            
    except Exception as e:
        logger.error(f"Error al eliminar tag {tag_id}: {e}")
        return False

def get_or_create_tags(tag_names):
    """
    Obtiene o crea múltiples tags a partir de una lista de nombres.
    Útil para asignar tags a una publicación sin tener que crearlos previamente.
    
    Args:
        tag_names: Lista de nombres de tags
        
    Returns:
        list: Lista de objetos tag (con sus IDs)
    """
    if not tag_names:
        return []
    
    # Eliminar duplicados y strings vacíos
    unique_tags = list(set(filter(None, [name.strip() for name in tag_names])))
    
    result_tags = []
    
    for tag_name in unique_tags:
        try:
            # Intentar obtener el tag existente
            existing_tag = get_tag_by_name(tag_name)
            
            if existing_tag:
                # Si existe, añadirlo a la lista de resultados
                result_tags.append(existing_tag)
            else:
                # Si no existe, crear nuevo tag y añadirlo
                new_tag = create_tag(tag_name)
                if new_tag:
                    result_tags.append(new_tag)
                    logger.info(f"Tag creado automáticamente: {tag_name}")
                else:
                    logger.warning(f"No se pudo crear el tag: {tag_name}")
        
        except Exception as e:
            logger.error(f"Error al procesar tag '{tag_name}': {e}")
    
    return result_tags