# Operaciones CRUD para usuarios
from ..utils.data_utils import load_json, save_json, generate_uuid, get_current_timestamp

def get_users():
    """Obtiene todos los usuarios."""
    return load_json("users")

def get_user_by_id(user_id):
    """Obtiene un usuario por su ID."""
    users = get_users()
    for user in users:
        if user['id'] == user_id:
            return user
    return None

def get_user_by_email(email):
    """Obtiene un usuario por su correo electrónico."""
    users = get_users()
    for user in users:
        if user['email'].lower() == email.lower():
            return user
    return None

def create_user(email, name, apellidos, password_hash, role="user"):
    """Crea un nuevo usuario."""
    users = get_users()
    
    new_user = {
        "id": generate_uuid(),
        "email": email,
        "name": name,
        "apellidos": apellidos,
        "password_hash": password_hash,
        "role": role,
        "created_at": get_current_timestamp(),
        "last_login": None
    }
    
    users.append(new_user)
    save_json("users", users)
    
    # Devolver copia del usuario sin password_hash
    user_copy = new_user.copy()
    user_copy.pop("password_hash", None)
    return user_copy

def update_user(user_id, data):
    """Actualiza un usuario existente."""
    users = get_users()
    
    for i, user in enumerate(users):
        if user['id'] == user_id:
            # Actualizar solo los campos proporcionados
            for key, value in data.items():
                if key != 'id' and key != 'created_at':  # No permitir cambiar id o created_at
                    user[key] = value
            
            save_json("users", users)
            
            # Devolver copia del usuario sin password_hash
            user_copy = user.copy()
            user_copy.pop("password_hash", None)
            return user_copy
    
    return None

def delete_user(user_id):
    """Elimina un usuario."""
    users = get_users()
    
    for i, user in enumerate(users):
        if user['id'] == user_id:
            del users[i]
            save_json("users", users)
            return True
    
    return False

def update_last_login(user_id):
    """Actualiza la última fecha de inicio de sesión de un usuario."""
    return update_user(user_id, {"last_login": get_current_timestamp()})