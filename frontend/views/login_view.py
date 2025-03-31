import streamlit as st
from frontend.components.form_components import text_input_custom, button_custom

def login_view():
    # Crear un diseño de 3 columnas y usar solo la columna central
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:  # Solo usar la columna central (más ancha)
        # st.markdown('<div class="auth-container">', unsafe_allow_html=True)
        st.markdown("## Inicio de sesión")
        st.write("")

        # Campos del formulario
        email = text_input_custom("Correo electrónico", key="login_email")
        password = text_input_custom("Contraseña", type="password", key="login_password")

        # Botón de Iniciar Sesión
        if button_custom("INICIAR SESIÓN"):
            # Aquí se podría llamar a la lógica de autenticación en la carpeta backend
            st.write("Lógica de autenticación pendiente...")

        st.write("")
        
        # Link para registro (ahora con botón)
        if button_custom("¿No tienes cuenta? Regístrate"):
            st.session_state.vista = "register"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)