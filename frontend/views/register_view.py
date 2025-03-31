import streamlit as st
from frontend.components.form_components import text_input_custom, button_custom

def register_view():
    # Crear un diseño de 3 columnas y usar solo la columna central
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:  # Solo usar la columna central (más ancha)
        # st.markdown('<div class="auth-container">', unsafe_allow_html=True)
        st.markdown("## Regístrate como usuario")
        st.write("")

        # Campos del formulario
        nombre = text_input_custom("Nombre", key="nombre")
        apellidos = text_input_custom("Apellidos", key="apellidos")
        correo = text_input_custom("Correo electrónico", key="correo")
        contrasena = text_input_custom("Contraseña", type="password", key="contrasena")

        # Botón de Registro
        if button_custom("REGISTRARSE"):
            # Aquí se podría llamar a la lógica de registro en la carpeta backend
            st.write("Lógica de registro pendiente...")

        st.write("")
        
        # Link para iniciar sesión (ahora con botón)
        if button_custom("¿Ya tienes cuenta? Inicia Sesión"):
            st.session_state.vista = "login"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)