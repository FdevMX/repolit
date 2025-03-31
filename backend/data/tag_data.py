# Operaciones CRUD para etiquetas
from ..utils.data_utils import load_json, save_json, generate_uuid, get_current_timestamp

def get_tags():
    """Obtiene todas las etiquetas."""
    return load_json("tags")

def get_tag_by_id(tag_id):
    """Obtiene una etiqueta por su ID."""
    tags = get_tags()
    for tag in tags:
        if tag['id'] == tag_id:
            return tag
    return None

def get_tag_by_name(name):
    """Obtiene una etiqueta por su nombre."""
    tags = get_tags()
    for tag in tags:
        if tag['name'].lower() == name.lower():
            return tag
    return None

def create_tag(name):
    """Crea una nueva etiqueta si no existe."""
    # Verificar si ya existe
    existing = get_tag_by_name(name)
    if existing:
        return existing
    
    tags = get_tags()
    
    new_tag = {
        "id": generate_uuid(),
        "name": name,
        "created_at": get_current_timestamp()
    }
    
    tags.append(new_tag)
    save_json("tags", tags)
    
    return new_tag

def delete_tag(tag_id):
    """Elimina una etiqueta."""
    # Nota: En una implementación completa, deberíamos verificar si hay publicaciones
    # que usan esta etiqueta antes de eliminarla
    tags = get_tags()
    
    for i, tag in enumerate(tags):
        if tag['id'] == tag_id:
            del tags[i]
            save_json("tags", tags)
            return True
    
    return False

def get_or_create_tags(tag_names):
    """Obtiene o crea múltiples etiquetas a partir de sus nombres."""
    result = []
    
    for name in tag_names:
        tag = get_tag_by_name(name)
        if not tag:
            tag = create_tag(name)
        result.append(tag)
    
    return result