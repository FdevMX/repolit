# Operaciones CRUD para publicaciones usando PostgreSQL
import logging
import uuid
from datetime import datetime
from ..db.connection import execute_query
from .tag_data import get_or_create_tags, get_tag_by_id

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("publication_data")

def get_publications():
    """Obtiene todas las publicaciones ordenadas por fecha de creación descendente."""
    try:
        query = """
        SELECT p.*, u.name as author_name, c.name as category_name
        FROM publications p
        JOIN users u ON p.user_id = u.id
        JOIN categories c ON p.category_id = c.id
        ORDER BY p.created_at DESC
        """
        publications = execute_query(query)
        return publications
    except Exception as e:
        logger.error(f"Error al obtener publicaciones: {e}")
        return []

def get_public_publications(category_id=None, featured_only=False):
    """
    Obtiene todas las publicaciones públicas con sus etiquetas.
    
    Args:
        category_id: ID de la categoría para filtrar (opcional)
        featured_only: Si solo se muestran publicaciones destacadas
        
    Returns:
        list: Lista de publicaciones públicas con sus etiquetas
    """
    try:
        # Construir la consulta base
        query = """
        SELECT 
            p.*,
            u.name as author_name,
            c.name as category_name,
            COALESCE(
                json_agg(
                    json_build_object(
                        'id', t.id,
                        'name', t.name
                    )
                ) FILTER (WHERE t.id IS NOT NULL),
                '[]'
            ) as tags
        FROM publications p
        JOIN users u ON p.user_id = u.id
        JOIN categories c ON p.category_id = c.id
        LEFT JOIN publication_tags pt ON p.id = pt.publication_id
        LEFT JOIN tags t ON pt.tag_id = t.id
        WHERE p.is_public = TRUE
        """
        
        params = []
        
        # Añadir filtro por categoría si se especifica
        if category_id:
            query += " AND p.category_id = %s"
            params.append(category_id)
        
        # Añadir filtro para publicaciones destacadas
        if featured_only:
            query += " AND p.is_featured = TRUE"
        
        # Agrupar por los campos necesarios
        query += """
        GROUP BY p.id, u.name, c.name
        ORDER BY p.is_featured DESC, p.created_at DESC
        """
        
        # Ejecutar la consulta
        publications = execute_query(query, params if params else None)
        
        # Procesar las etiquetas JSON
        for pub in publications:
            if isinstance(pub['tags'], str):
                pub['tags'] = []
            
        return publications
        
    except Exception as e:
        logger.error(f"Error al obtener publicaciones públicas: {e}")
        return []

def get_publication_by_id(publication_id):
    """Obtiene una publicación por su ID, incluyendo sus etiquetas."""
    try:
        query = """
        SELECT p.*, u.name as author_name, c.name as category_name
        FROM publications p
        JOIN users u ON p.user_id = u.id
        JOIN categories c ON p.category_id = c.id
        WHERE p.id = %s
        """
        publication = execute_query(query, (publication_id,), fetchone=True)
        
        # Añadir tags a la publicación
        if publication:
            tags_query = """
            SELECT t.*
            FROM tags t
            JOIN publication_tags pt ON t.id = pt.tag_id
            WHERE pt.publication_id = %s
            ORDER BY t.name
            """
            publication['tags'] = execute_query(tags_query, (publication_id,))
            
        return publication
    except Exception as e:
        logger.error(f"Error al obtener publicación por ID {publication_id}: {e}")
        return None

def get_publications_by_user(user_id):
    """Obtiene todas las publicaciones de un usuario."""
    try:
        query = """
        SELECT p.*, u.name as author_name, c.name as category_name
        FROM publications p
        JOIN users u ON p.user_id = u.id
        JOIN categories c ON p.category_id = c.id
        WHERE p.user_id = %s
        ORDER BY p.created_at DESC
        """
        publications = execute_query(query, (user_id,))
        return publications
    except Exception as e:
        logger.error(f"Error al obtener publicaciones del usuario {user_id}: {e}")
        return []

def get_publications_by_category(category_id):
    """Obtiene todas las publicaciones de una categoría."""
    try:
        query = """
        SELECT p.*, u.name as author_name, c.name as category_name
        FROM publications p
        JOIN users u ON p.user_id = u.id
        JOIN categories c ON p.category_id = c.id
        WHERE p.category_id = %s
        ORDER BY p.created_at DESC
        """
        publications = execute_query(query, (category_id,))
        return publications
    except Exception as e:
        logger.error(f"Error al obtener publicaciones de categoría {category_id}: {e}")
        return []

def get_publication_tags(publication_id):
    """Obtiene las etiquetas asociadas a una publicación."""
    try:
        query = """
        SELECT t.*
        FROM tags t
        JOIN publication_tags pt ON t.id = pt.tag_id
        WHERE pt.publication_id = %s
        ORDER BY t.name
        """
        tags = execute_query(query, (publication_id,))
        return tags
    except Exception as e:
        logger.error(f"Error al obtener etiquetas de publicación {publication_id}: {e}")
        return []

def create_publication(title, description, category_id, user_id, is_featured=False, is_public=True, file_info=None, tag_names=None):
    """
    Crea una nueva publicación.
    
    Args:
        title: Título de la publicación
        description: Descripción de la publicación
        category_id: ID de la categoría
        user_id: ID del usuario que crea la publicación
        is_featured: Si la publicación debe destacarse
        is_public: Si la publicación es visible para todos
        file_info: Diccionario con información del archivo (opcional)
        tag_names: Lista de nombres de etiquetas (opcional)
        
    Returns:
        dict: La publicación creada
    """
    try:
        # Generar un UUID para la nueva publicación
        publication_id = str(uuid.uuid4())

        # Preparar los campos de archivo (si existen)
        file_url = file_info.get("url", file_info.get("file_url")) if file_info else None
        file_name = file_info.get("filename", file_info.get("file_name")) if file_info else None
        file_type = file_info.get("content_type", file_info.get("file_type")) if file_info else None
        file_size = file_info.get("file_size") if file_info else None
        is_external = file_info.get("is_external", False) if file_info else False
        media_type = file_info.get("media_type") if file_info else None

        # Insertar la publicación
        query = """
        INSERT INTO publications (
            id, title, description, category_id, user_id,
            file_url, file_name, file_type, file_size,
            is_featured, is_public, is_external, media_type,
            created_at, updated_at
        )
        VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            CURRENT_TIMESTAMP, CURRENT_TIMESTAMP
        )
        RETURNING id, title, description, category_id, user_id, 
                file_url, file_name, file_type, file_size,
                is_featured, is_public, is_external, media_type,
                created_at, updated_at
        """

        new_publication = execute_query(
            query, 
            (publication_id, title, description, category_id, user_id, 
            file_url, file_name, file_type, file_size,
            is_featured, is_public, is_external, media_type),
            fetchone=True,
            commit=True
        )

        # Asociar etiquetas si se proporcionan
        if tag_names and len(tag_names) > 0:
            tags = get_or_create_tags(tag_names)

            for tag in tags:
                tag_query = """
                INSERT INTO publication_tags (publication_id, tag_id)
                VALUES (%s, %s)
                """
                execute_query(tag_query, (publication_id, tag['id']), commit=True)

        logger.info(f"Nueva publicación creada: {title} (ID: {publication_id})")

        # Obtener la publicación completa con tags
        result = get_publication_by_id(publication_id)
        result['tags'] = get_publication_tags(publication_id)
        return result

    except Exception as e:
        logger.error(f"Error al crear publicación '{title}': {e}")
        return None

def update_publication(publication_id, data, new_file_info=None, tag_names=None):
    """
    Actualiza una publicación existente.
    
    Args:
        publication_id: ID de la publicación a actualizar
        data: Diccionario con los campos a actualizar
        new_file_info: Información del nuevo archivo (opcional)
        tag_names: Lista de nombres de etiquetas para actualizar (opcional)
        
    Returns:
        dict: La publicación actualizada o None si no se encuentra
    """
    try:
        # Verificar que la publicación existe
        existing = get_publication_by_id(publication_id)
        if not existing:
            logger.warning(f"Intento de actualizar publicación inexistente: {publication_id}")
            return None
        
        # Construir la consulta dinámica basada en los campos proporcionados
        update_fields = []
        params = []
        
        for key, value in data.items():
            if key in ['title', 'description', 'category_id', 'user_id', 'is_featured', 'is_public']:
                update_fields.append(f"{key} = %s")
                params.append(value)
        
        # Si hay un nuevo archivo, actualizar campos de archivo
        if new_file_info:
            # Campos estándar de archivo
            for field in ['file_url', 'file_name', 'file_type', 'file_size']:
                if field in new_file_info:
                    update_fields.append(f"{field} = %s")
                    params.append(new_file_info[field])
            
            # Agregar campos para URL externa
            if 'is_external' in new_file_info:
                update_fields.append("is_external = %s")
                params.append(new_file_info['is_external'])
            
            if 'media_type' in new_file_info:
                update_fields.append("media_type = %s")
                params.append(new_file_info['media_type'])
        
        # Si no hay campos para actualizar, salir
        if not update_fields:
            logger.warning(f"No se proporcionaron campos válidos para actualizar publicación: {publication_id}")
            return None
        
        # Añadir timestamp de actualización
        update_fields.append("updated_at = CURRENT_TIMESTAMP")
        
        # Construir y ejecutar la consulta
        query = f"""
        UPDATE publications
        SET {", ".join(update_fields)}
        WHERE id = %s
        RETURNING *
        """
        params.append(publication_id)
        
        updated_pub = execute_query(query, params, fetchone=True, commit=True)
        
        # Actualizar etiquetas si se proporcionan
        if tag_names is not None:
            # Eliminar asociaciones anteriores
            delete_tags_query = "DELETE FROM publication_tags WHERE publication_id = %s"
            execute_query(delete_tags_query, (publication_id,), commit=True)
            
            # Crear nuevas asociaciones
            if len(tag_names) > 0:
                tags = get_or_create_tags(tag_names)
                for tag in tags:
                    tag_query = """
                    INSERT INTO publication_tags (publication_id, tag_id)
                    VALUES (%s, %s)
                    """
                    execute_query(tag_query, (publication_id, tag['id']), commit=True)
        
        logger.info(f"Publicación actualizada: {publication_id}")
        
        # Obtener la publicación actualizada con etiquetas
        result = get_publication_by_id(publication_id)
        result['tags'] = get_publication_tags(publication_id)
        return result
        
    except Exception as e:
        logger.error(f"Error al actualizar publicación {publication_id}: {e}")
        return None

def delete_publication(publication_id):
    """
    Elimina una publicación y sus relaciones.
    
    Args:
        publication_id: ID de la publicación a eliminar
        
    Returns:
        bool: True si se elimina correctamente, False en caso contrario
    """
    try:
        # Verificar que la publicación existe
        publication = get_publication_by_id(publication_id)
        if not publication:
            logger.warning(f"Intento de eliminar publicación inexistente: {publication_id}")
            return False
        
        # Las relaciones se eliminarán automáticamente por las restricciones ON DELETE CASCADE
        
        # Eliminar la publicación
        query = "DELETE FROM publications WHERE id = %s RETURNING id"
        result = execute_query(query, (publication_id,), fetchone=True, commit=True)
        
        if result:
            logger.info(f"Publicación eliminada: {publication_id}")
            return True
        else:
            logger.warning(f"No se pudo eliminar publicación: {publication_id}")
            return False
            
    except Exception as e:
        logger.error(f"Error al eliminar publicación {publication_id}: {e}")
        return False

def get_publications_with_tags(limit=None, only_public=False, only_featured=False):
    """
    Obtiene todas las publicaciones con sus etiquetas.
    
    Args:
        limit: Número máximo de publicaciones a devolver (opcional)
        only_public: Si es True, solo devuelve publicaciones públicas
        only_featured: Si es True, solo devuelve publicaciones destacadas
        
    Returns:
        list: Lista de publicaciones con etiquetas añadidas
    """
    try:
        # Construir la consulta base
        query = """
        SELECT p.*, u.name as author_name, c.name as category_name
        FROM publications p
        JOIN users u ON p.user_id = u.id
        JOIN categories c ON p.category_id = c.id
        """
        
        # Añadir condiciones según parámetros
        conditions = []
        params = []
        
        if only_public:
            conditions.append("p.is_public = TRUE")
        
        if only_featured:
            conditions.append("p.is_featured = TRUE")
        
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        
        # Añadir ordenamiento
        query += " ORDER BY p.created_at DESC"
        
        # Añadir límite si corresponde
        if limit:
            query += " LIMIT %s"
            params.append(limit)
        
        # Ejecutar la consulta
        publications = execute_query(query, params if params else None)
        
        # Agregar etiquetas a cada publicación
        for pub in publications:
            pub['tags'] = get_publication_tags(pub['id'])
        
        return publications
        
    except Exception as e:
        logger.error(f"Error al obtener publicaciones con etiquetas: {e}")
        return []

def search_publications(query="", category_id=None, tag_ids=None, only_public=True):
    """
    Busca publicaciones según criterios.
    
    Args:
        query: Texto a buscar en título y descripción
        category_id: Filtrar por categoría (opcional)
        tag_ids: Filtrar por etiquetas (opcional)
        only_public: Si solo se muestran publicaciones públicas
        
    Returns:
        list: Publicaciones que cumplen los criterios
    """
    try:
        base_query = """
        SELECT DISTINCT p.*, u.name as author_name, c.name as category_name
        FROM publications p
        JOIN users u ON p.user_id = u.id
        JOIN categories c ON p.category_id = c.id
        """
        
        conditions = []
        params = []
        
        # Filtro por publicaciones públicas
        if only_public:
            conditions.append("p.is_public = TRUE")
        
        # Filtro por texto de búsqueda
        if query and query.strip():
            conditions.append("(p.title ILIKE %s OR p.description ILIKE %s)")
            search_term = f"%{query.strip()}%"
            params.extend([search_term, search_term])
        
        # Filtro por categoría
        if category_id:
            conditions.append("p.category_id = %s")
            params.append(category_id)
        
        # Filtro por etiquetas
        if tag_ids and len(tag_ids) > 0:
            base_query += " JOIN publication_tags pt ON p.id = pt.publication_id"
            conditions.append("pt.tag_id IN (" + ",".join(["%s"] * len(tag_ids)) + ")")
            params.extend(tag_ids)
        
        # Combinar consulta con condiciones
        if conditions:
            base_query += " WHERE " + " AND ".join(conditions)
        
        # Añadir orden
        base_query += " ORDER BY p.created_at DESC"
        
        # Ejecutar la consulta
        publications = execute_query(base_query, params)
        
        # Agregar etiquetas a cada publicación
        for pub in publications:
            pub['tags'] = get_publication_tags(pub['id'])
        
        return publications
        
    except Exception as e:
        logger.error(f"Error al buscar publicaciones: {e}")
        return []
