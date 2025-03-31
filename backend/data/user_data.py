# Operaciones CRUD para usuarios usando PostgreSQL directo
from ..db.connection import execute_query
from ..utils.password_utils import hash_password
import uuid
from datetime import datetime

def get_users():
    """Obtiene todos los usuarios."""
    query = "SELECT * FROM users"
    return execute_query(query)

def get_user_by_id(user_id):
    """Obtiene un usuario por su ID."""
    query = "SELECT * FROM users WHERE id = %s"
    return execute_query(query, (user_id,), fetchone=True)

def get_user_by_email(email):
    """Obtiene un usuario por su correo electrónico."""
    query = "SELECT * FROM users WHERE email = %s"
    return execute_query(query, (email,), fetchone=True)

def create_user(email, name, apellidos, password_hash, role="user"):
    """Crea un nuevo usuario."""
    user_id = str(uuid.uuid4())
    created_at = datetime.utcnow().isoformat()
    
    query = """
    INSERT INTO users (id, email, name, apellidos, password_hash, role, created_at)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    RETURNING id, email, name, apellidos, role, created_at
    """
    
    user = execute_query(
        query, 
        (user_id, email, name, apellidos, password_hash, role, created_at),
        fetchone=True,
        commit=True
    )
    
    return user

def update_user(user_id, data):
    """Actualiza un usuario existente."""
    # Construir dinámicamente la consulta de actualización
    fields = []
    values = []
    
    for key, value in data.items():
        if key not in ['id', 'created_at']:  # Campos que no se deben actualizar
            fields.append(f"{key} = %s")
            values.append(value)
    
    if not fields:
        return None  # No hay campos para actualizar
        
    query = f"""
    UPDATE users 
    SET {', '.join(fields)}
    WHERE id = %s
    RETURNING id, email, name, apellidos, role, created_at, last_login
    """
    
    values.append(user_id)  # Añadir el ID para la condición WHERE
    
    return execute_query(query, tuple(values), fetchone=True, commit=True)

def delete_user(user_id):
    """Elimina un usuario."""
    query = "DELETE FROM users WHERE id = %s RETURNING id"
    result = execute_query(query, (user_id,), fetchone=True, commit=True)
    return result is not None

def update_last_login(user_id):
    """Actualiza la última fecha de inicio de sesión de un usuario."""
    last_login = datetime.utcnow().isoformat()
    query = """
    UPDATE users
    SET last_login = %s
    WHERE id = %s
    RETURNING id, email, name, apellidos, role, created_at, last_login
    """
    return execute_query(query, (last_login, user_id), fetchone=True, commit=True)