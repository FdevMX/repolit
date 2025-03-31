# Operaciones CRUD para categorías
from ..utils.data_utils import load_json, save_json, generate_uuid, get_current_timestamp

def get_categories():
    """Obtiene todas las categorías."""
    return load_json("categories")

def get_category_by_id(category_id):
    """Obtiene una categoría por su ID."""
    categories = get_categories()
    for category in categories:
        if category['id'] == category_id:
            return category
    return None

def get_category_by_name(name):
    """Obtiene una categoría por su nombre."""
    categories = get_categories()
    for category in categories:
        if category['name'].lower() == name.lower():
            return category
    return None

def create_category(name):
    """Crea una nueva categoría."""
    # Verificar si ya existe
    existing = get_category_by_name(name)
    if existing:
        return None
    
    categories = get_categories()
    
    new_category = {
        "id": generate_uuid(),
        "name": name,
        "created_at": get_current_timestamp(),
        "updated_at": get_current_timestamp()
    }
    
    categories.append(new_category)
    save_json("categories", categories)
    
    return new_category

def update_category(category_id, name):
    """Actualiza una categoría existente."""
    # Verificar si el nuevo nombre ya existe para otra categoría
    existing = get_category_by_name(name)
    if existing and existing['id'] != category_id:
        return None
    
    categories = get_categories()
    
    for i, category in enumerate(categories):
        if category['id'] == category_id:
            category['name'] = name
            category['updated_at'] = get_current_timestamp()
            
            save_json("categories", categories)
            return category
    
    return None

def delete_category(category_id):
    """Elimina una categoría."""
    # Nota: En una implementación completa, deberíamos verificar si hay publicaciones
    # que usan esta categoría antes de eliminarla
    categories = get_categories()
    
    for i, category in enumerate(categories):
        if category['id'] == category_id:
            del categories[i]
            save_json("categories", categories)
            return True
    
    return False