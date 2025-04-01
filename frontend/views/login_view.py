import streamlit as st
from frontend.components.form_components import text_input_custom, button_custom
from backend.auth.auth_service import login
import re
from email_validator import validate_email, EmailNotValidError

def login_view():
    # Crear un diseño de 3 columnas y usar solo la columna central
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:  # Solo usar la columna central (más ancha)
        # st.markdown('<div class="auth-container">', unsafe_allow_html=True)
        st.title("Iniciar Sesión")
        st.write("")

        # Campos del formulario
        email = text_input_custom("Correo electrónico", key="login_email")
        password = text_input_custom("Contraseña", type="password", key="login_password")

        # Botón de Iniciar Sesión
        if button_custom("INICIAR SESIÓN"):
            # Validación básica
            if not email or not password:
                st.error("Todos los campos son obligatorios")
            else:
                # Importar y llamar a la función de registro
                if login(email, password):
                    st.success("Inicio de sesión exitoso!")
                    st.session_state.vista = "private_general"
                    st.rerun()
                else:
                    st.error("Correo o contraseña incorrectos")

        st.write("")

        col1, col2 = st.columns([1, 1])
        
        with col1:
            # Link para registro (ahora con botón)
            if button_custom("¿No tienes cuenta? Regístrate"):
                st.session_state.vista = "register"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            # Link para volver a la página principal
            if button_custom("Volver a la página principal"):
                st.session_state.vista = "public_apps"
                st.rerun()
