import streamlit as st
from frontend.components.form_components import text_input_custom, button_custom
from frontend.views.register_view import register_view

def login_view():
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
