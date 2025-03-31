# Servicio de autenticación
import streamlit as st
from ..utils.password_utils import hash_password, verify_password
from ..data.user_data import get_user_by_email, create_user

def login(email, password):
    """
    Intenta iniciar sesión con las credenciales proporcionadas.
    
    Args:
        email: Correo electrónico del usuario
        password: Contraseña del usuario
        
    Returns:
        bool: True si el inicio de sesión es exitoso, False en caso contrario
    """
    user = get_user_by_email(email)
    
    if not user:
        return False
    
    if verify_password(user['password_hash'], password):
        # Guardar información del usuario en la sesión
        st.session_state.user = {
            'id': user['id'],
            'email': user['email'],
            'name': user['name'],
            'apellidos': user['apellidos'],
            'role': user['role']
        }
        st.session_state.authenticated = True
        return True
    
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
        dict: Información del usuario creado o None si ya existe
    """
    # Verificar si el usuario ya existe
    existing_user = get_user_by_email(email)
    if existing_user:
        return None
    
    # Crear hash de la contraseña
    password_hash = hash_password(password)
    
    # Crear el usuario
    return create_user(email, name, apellidos, password_hash)

def logout():
    """Cierra la sesión del usuario actual."""
    if 'user' in st.session_state:
        del st.session_state.user
    if 'authenticated' in st.session_state:
        del st.session_state.authenticated

def is_authenticated():
    """Verifica si el usuario está autenticado."""
    return st.session_state.get('authenticated', False)

def get_current_user():
    """Obtiene la información del usuario actual."""
    return st.session_state.get('user', None)

def is_admin():
    """Verifica si el usuario actual tiene rol de administrador."""
    user = get_current_user()
    return user and user.get('role') == 'admin'