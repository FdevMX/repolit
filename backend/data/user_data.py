# Operaciones CRUD para usuarios usando PostgreSQL directo
import logging
from ..db.connection import execute_query
from ..utils.password_utils import hash_password
import uuid
from datetime import datetime, timezone

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("user_data")

def get_users():
    """Obtiene todos los usuarios."""
    try:
        query = "SELECT * FROM users"
        return execute_query(query)
    except Exception as e:
        logger.error(f"Error al obtener usuarios: {e}")
        return []

def get_user_by_id(user_id):
    """Obtiene un usuario por su ID."""
    try:
        query = "SELECT * FROM users WHERE id = %s"
        return execute_query(query, (user_id,), fetchone=True)
    except Exception as e:
        logger.error(f"Error al obtener usuario por ID {user_id}: {e}")
        return None

def get_user_by_email(email):
    """Obtiene un usuario por su correo electrónico."""
    try:
        query = "SELECT * FROM users WHERE email = %s"
        return execute_query(query, (email,), fetchone=True)
    except Exception as e:
        logger.error(f"Error al obtener usuario por email {email}: {e}")
        return None

def create_user(email, name, apellidos, password_hash, role="admin"):
    """Crea un nuevo usuario."""
    try:
        user_id = str(uuid.uuid4())
        created_at = datetime.now(timezone.utc).isoformat()
        
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
        
        logger.info(f"Usuario creado exitosamente: {email}")
        return user
        
    except Exception as e:
        logger.error(f"Error al crear usuario {email}: {e}")
        return None

def update_user(user_id, data):
    """Actualiza un usuario existente."""
    try:
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
        
        updated_user = execute_query(query, tuple(values), fetchone=True, commit=True)
        logger.info(f"Usuario actualizado exitosamente: {user_id}")
        return updated_user
        
    except Exception as e:
        logger.error(f"Error al actualizar usuario {user_id}: {e}")
        return None

def delete_user(user_id):
    """Elimina un usuario."""
    try:
        query = "DELETE FROM users WHERE id = %s RETURNING id"
        result = execute_query(query, (user_id,), fetchone=True, commit=True)
        success = result is not None
        
        if success:
            logger.info(f"Usuario eliminado exitosamente: {user_id}")
        else:
            logger.warning(f"No se encontró el usuario a eliminar: {user_id}")
        
        return success
        
    except Exception as e:
        logger.error(f"Error al eliminar usuario {user_id}: {e}")
        return False

def update_last_login(user_id):
    """Actualiza la última fecha de inicio de sesión de un usuario."""
    try:
        last_login = datetime.now(timezone.utc).isoformat()
        query = """
        UPDATE users
        SET last_login = %s
        WHERE id = %s
        RETURNING id, email, name, apellidos, role, created_at, last_login
        """
        result = execute_query(query, (last_login, user_id), fetchone=True, commit=True)
        logger.info(f"Actualizada fecha de último login: {user_id}")
        return result
        
    except Exception as e:
        logger.error(f"Error al actualizar fecha de último login {user_id}: {e}")
        return None