import streamlit as st
from frontend.components.form_components import text_input_custom, button_custom
from backend.auth.auth_service import login
from backend.auth.auth_service import register
import time
import re
from email_validator import validate_email, EmailNotValidError

def is_valid_email(email):
    try:
        # Using the email_validator package for comprehensive validation
        validate_email(email)
        return True
    except ImportError:
        # Fallback to regex if email_validator isn't installed
        pattern = r"[a-zA-Z0-9_]+([.][a-zA-Z0-9_]+)*@[a-zA-Z0-9_]+([.][a-zA-Z0-9_]+)*[.][a-zA-Z]{2,5}"
        return re.match(pattern, email) is not None
    except EmailNotValidError:
        return False

def register_view():
    # Crear un diseño de 3 columnas y usar solo la columna central
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:  # Solo usar la columna central (más ancha)
        # st.markdown('<div class="auth-container">', unsafe_allow_html=True)
        st.title("Regístrate como usuario")
        st.write("")

        # Campos del formulario
        nombre = text_input_custom("Nombre", key="nombre")
        apellidos = text_input_custom("Apellidos", key="apellidos")
        correo = text_input_custom("Correo electrónico", key="correo")
        password = text_input_custom("Contraseña", type="password", key="contrasena")

        # Botón de Registro
        if button_custom("REGISTRARSE"):
            # Validación básica
            if not nombre or not apellidos or not correo or not password:
                st.error("Todos los campos son obligatorios")
            elif not is_valid_email(correo):
                st.error("Por favor, introduce un correo electrónico válido")
            else:
                # Importar y llamar a la función de registro
                if register(correo, nombre, apellidos, password):
                    st.success("¡Registro exitoso! Ahora puedes iniciar sesión")
                    # Redirigir a la página de login después de un registro exitoso
                    with st.spinner("Redirigiendo a la página de inicio de sesión en 5 segundos..."):
                        time.sleep(5)
                    st.session_state.vista = "login"
                    st.rerun()
                else:
                    st.error("No se pudo completar el registro. El correo podría estar ya registrado.")

        st.write("")

        col1, col2 = st.columns([1, 1])

        with col1:
            # Link para iniciar sesión (ahora con botón)
            if button_custom("¿Ya tienes cuenta? Inicia Sesión"):
                st.session_state.vista = "login"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            # Link para volver a la página principal
            if button_custom("Volver a la página principal"):
                st.session_state.vista = "public_apps"
                st.rerun()
