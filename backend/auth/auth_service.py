# Servicio de autenticación
import streamlit as st
import logging
import pickle
import os
import time
import hashlib
from ..utils.password_utils import hash_password, verify_password
from ..data.user_data import (
    get_user_by_email, 
    create_user,
    update_last_login
)

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("auth_service")


# Agregar esta función para manejar persistencia de sesión
def _save_session_cookie():
    """Guarda una cookie de sesión en el disco"""
    if "user" in st.session_state:
        cookie_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            "session_cookies",
        )
        if not os.path.exists(cookie_dir):
            os.makedirs(cookie_dir)

        # Crear un ID único para esta sesión basado en la información del usuario
        user_id = st.session_state.user["id"]
        session_id = hashlib.md5(f"{user_id}:{time.time()}".encode()).hexdigest()

        # Guardar la cookie en el disco
        cookie_path = os.path.join(cookie_dir, f"session_{user_id}.cookie")
        with open(cookie_path, "wb") as f:
            pickle.dump(
                {
                    "user": st.session_state.user,
                    "session_id": session_id,
                    "expiry": time.time() + 86400,  # 24 horas
                },
                f,
            )

        # También guardar en session_state para referencia rápida
        st.session_state.session_id = session_id

def _load_session_cookie():
    """Intenta cargar una cookie de sesión existente"""
    if "user" in st.session_state:
        # Ya hay una sesión activa
        return True

    cookie_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "session_cookies"
    )
    if not os.path.exists(cookie_dir):
        return False

    # Buscar todas las cookies
    for file in os.listdir(cookie_dir):
        if file.startswith("session_") and file.endswith(".cookie"):
            cookie_path = os.path.join(cookie_dir, file)
            try:
                with open(cookie_path, "rb") as f:
                    session_data = pickle.load(f)

                # Verificar si la cookie ha expirado
                if session_data["expiry"] > time.time():
                    # Cargar la sesión
                    st.session_state.user = session_data["user"]
                    st.session_state.authenticated = True
                    st.session_state.session_id = session_data["session_id"]
                    return True
                else:
                    # Cookie expirada, eliminarla
                    os.remove(cookie_path)
            except Exception as e:
                print(f"Error al cargar cookie: {e}")

    return False

def login(email, password):
    """
    Intenta iniciar sesión con las credenciales proporcionadas.

    Args:
        email: Correo electrónico del usuario
        password: Contraseña del usuario

    Returns:
        bool: True si el inicio de sesión es exitoso, False en caso contrario
    """
    if not email or not password:
        logger.warning("Intento de inicio de sesión con campos vacíos")
        return False

    try:
        user = get_user_by_email(email)

        if not user:
            logger.info(f"Intento de inicio de sesión con email no registrado: {email}")
            return False

        if verify_password(user["password_hash"], password):
            # Actualizar última fecha de inicio de sesión
            update_last_login(user["id"])

            # Guardar información del usuario en la sesión
            st.session_state.user = {
                "id": user["id"],
                "email": user["email"],
                "name": user["name"],
                "apellidos": user["apellidos"],
                "role": user["role"],
            }
            st.session_state.authenticated = True

            # Guardar cookie para persistencia
            _save_session_cookie()

            logger.info(f"Inicio de sesión exitoso: {email}")
            return True

        logger.warning(f"Contraseña incorrecta para el usuario: {email}")
        return False

    except Exception as e:
        logger.error(f"Error en el proceso de login: {e}")
        return False

def register(email, name, apellidos, password):
    """
    Registra un nuevo usuario en el sistema.
    
    Args:
        email: Correo electrónico del usuario
        name: Nombre del usuario
        apellidos: Apellidos del usuario
        password: Contraseña del usuario
        
    Returns:
        dict: Información del usuario creado o None si ya existe o hay error
    """
    # Validaciones básicas
    if not email or not name or not apellidos or not password:
        logger.warning("Intento de registro con campos vacíos")
        return None

    try:
        # Verificar si el usuario ya existe
        existing_user = get_user_by_email(email)
        if existing_user:
            logger.info(f"Intento de registro con email ya existente: {email}")
            return None

        # Crear hash de la contraseña
        password_hash = hash_password(password)

        # Crear el usuario
        new_user = create_user(email, name, apellidos, password_hash)
        logger.info(f"Usuario registrado exitosamente: {email}")
        return new_user

    except Exception as e:
        logger.error(f"Error en el proceso de registro: {e}")
        return None

def logout():
    """Cierra la sesión del usuario actual."""
    if "user" in st.session_state:
        email = st.session_state.user.get("email", "Unknown")
        user_id = st.session_state.user.get("id", "")

        # Eliminar cookie de sesión si existe
        cookie_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            "session_cookies",
        )
        cookie_path = os.path.join(cookie_dir, f"session_{user_id}.cookie")
        if os.path.exists(cookie_path):
            os.remove(cookie_path)

        del st.session_state.user
        logger.info(f"Cierre de sesión: {email}")

    if "authenticated" in st.session_state:
        del st.session_state.authenticated

    if "session_id" in st.session_state:
        del st.session_state.session_id

def is_authenticated():
    """Verifica si el usuario está autenticado."""
    # Si ya hay una bandera de autenticación en session_state, usarla
    if st.session_state.get("authenticated", False):
        return True

    # Intentar cargar una sesión guardada
    if _load_session_cookie():
        return True

    return False

def get_current_user():
    """Obtiene la información del usuario actual."""
    return st.session_state.get('user', None)

def is_admin():
    """Verifica si el usuario actual tiene rol de administrador."""
    user = get_current_user()
    return user and user.get('role') == 'admin'
