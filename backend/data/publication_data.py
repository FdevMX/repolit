# Operaciones CRUD para publicaciones
from ..utils.data_utils import load_json, save_json, generate_uuid, get_current_timestamp
from .tag_data import get_or_create_tags
from ..storage.file_handler import delete_file

def get_publications():
    """Obtiene todas las publicaciones."""
    return load_json("publications")

def get_publication_by_id(publication_id):
    """Obtiene una publicación por su ID."""
    publications = get_publications()
    for pub in publications:
        if pub['id'] == publication_id:
            return pub
    return None

def get_publications_by_user(user_id):
    """Obtiene todas las publicaciones de un usuario."""
    publications = get_publications()
    return [pub for pub in publications if pub['user_id'] == user_id]

def get_publications_by_category(category_id):
    """Obtiene todas las publicaciones de una categoría."""
    publications = get_publications()
    return [pub for pub in publications if pub['category_id'] == category_id]

def get_publication_tags(publication_id):
    """Obtiene las etiquetas asociadas a una publicación."""
    publication_tags = load_json("publication_tags")
    tag_ids = [pt['tag_id'] for pt in publication_tags if pt['publication_id'] == publication_id]
    
    tags = load_json("tags")
    return [tag for tag in tags if tag['id'] in tag_ids]

def create_publication(title, description, category_id, user_id, file_info=None, tag_names=None):
    """
    Crea una nueva publicación.
    
    Args:
        title: Título de la publicación
        description: Descripción de la publicación
        category_id: ID de la categoría
        user_id: ID del usuario que crea la publicación
        file_info: Diccionario con información del archivo (opcional)
        tag_names: Lista de nombres de etiquetas (opcional)
        
    Returns:
        dict: La publicación creada
    """
    publications = get_publications()
    
    new_publication = {
        "id": generate_uuid(),
        "title": title,
        "description": description,
        "category_id": category_id,
        "user_id": user_id,
        "created_at": get_current_timestamp(),
        "updated_at": get_current_timestamp()
    }
    
    # Agregar información del archivo si está disponible
    if file_info:
        new_publication["file_url"] = file_info.get("file_url")
        new_publication["file_name"] = file_info.get("file_name")
        new_publication["file_type"] = file_info.get("file_type")
        new_publication["file_size"] = file_info.get("file_size")
    
    publications.append(new_publication)
    save_json("publications", publications)
    
    # Asociar etiquetas si se proporcionan
    if tag_names and len(tag_names) > 0:
        tags = get_or_create_tags(tag_names)
        publication_tags = load_json("publication_tags")
        
        for tag in tags:
            publication_tags.append({
                "publication_id": new_publication["id"],
                "tag_id": tag["id"]
            })
        
        save_json("publication_tags", publication_tags)
    
    return new_publication

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
    publications = get_publications()
    
    for i, pub in enumerate(publications):
        if pub['id'] == publication_id:
            # Actualizar campos básicos
            for key, value in data.items():
                if key not in ['id', 'created_at', 'file_url', 'file_name', 'file_type', 'file_size']:
                    pub[key] = value
            
            # Actualizar timestamp
            pub['updated_at'] = get_current_timestamp()
            
            # Actualizar información del archivo si se proporciona
            if new_file_info:
                # Eliminar archivo anterior si existe
                if 'file_url' in pub and pub['file_url']:
                    delete_file(pub['file_url'])
                
                pub["file_url"] = new_file_info.get("file_url")
                pub["file_name"] = new_file_info.get("file_name")
                pub["file_type"] = new_file_info.get("file_type")
                pub["file_size"] = new_file_info.get("file_size")
            
            save_json("publications", publications)
            
            # Actualizar etiquetas si se proporcionan
            if tag_names is not None:
                # Eliminar asociaciones anteriores
                publication_tags = load_json("publication_tags")
                publication_tags = [pt for pt in publication_tags if pt['publication_id'] != publication_id]
                
                # Crear nuevas asociaciones
                if len(tag_names) > 0:
                    tags = get_or_create_tags(tag_names)
                    for tag in tags:
                        publication_tags.append({
                            "publication_id": publication_id,
                            "tag_id": tag["id"]
                        })
                
                save_json("publication_tags", publication_tags)
            
            return pub
    
    return None

def delete_publication(publication_id):
    """
    Elimina una publicación y sus relaciones.
    
    Args:
        publication_id: ID de la publicación a eliminar
        
    Returns:
        bool: True si se elimina correctamente, False en caso contrario
    """
    publications = get_publications()
    
    for i, pub in enumerate(publications):
        if pub['id'] == publication_id:
            # Eliminar el archivo si existe
            if 'file_url' in pub and pub['file_url']:
                delete_file(pub['file_url'])
            
            # Eliminar la publicación
            del publications[i]
            save_json("publications", publications)
            
            # Eliminar relaciones con etiquetas
            publication_tags = load_json("publication_tags")
            publication_tags = [pt for pt in publication_tags if pt['publication_id'] != publication_id]
            save_json("publication_tags", publication_tags)
            
            return True
    
    return False

def get_publications_with_tags():
    """
    Obtiene todas las publicaciones con sus etiquetas.
    
    Returns:
        list: Lista de publicaciones con etiquetas añadidas
    """
    publications = get_publications()
    result = []
    
    for pub in publications:
        pub_copy = pub.copy()
        pub_copy['tags'] = get_publication_tags(pub['id'])
        result.append(pub_copy)
    
    return result

def search_publications(query, category_id=None, tag_ids=None):
    """
    Busca publicaciones según criterios.
    
    Args:
        query: Texto a buscar en título y descripción
        category_id: Filtrar por categoría (opcional)
        tag_ids: Filtrar por etiquetas (opcional)
        
    Returns:
        list: Publicaciones que cumplen los criterios
    """
    publications = get_publications_with_tags()
    results = []
    
    query = query.lower() if query else ""
    
    for pub in publications:
        # Filtrar por texto
        title_match = query == "" or query in pub['title'].lower()
        desc_match = 'description' in pub and pub['description'] and query in pub['description'].lower()
        
        # Filtrar por categoría
        cat_match = category_id is None or pub['category_id'] == category_id
        
        # Filtrar por etiquetas
        tag_match = True
        if tag_ids and len(tag_ids) > 0:
            pub_tag_ids = [tag['id'] for tag in pub['tags']]
            tag_match = any(tag_id in pub_tag_ids for tag_id in tag_ids)
        
        if (title_match or desc_match) and cat_match and tag_match:
            results.append(pub)
    
    return results