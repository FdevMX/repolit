import streamlit as st
st.set_page_config(layout="wide")
from frontend.views.login_view import login_view
from frontend.views.register_view import register_view
from frontend.views.view_public_apps import view_public_apps
from frontend.views.view_public_appsview import view_public_appsview
from frontend.views.view_private_general import view_private_general
from frontend.views.view_create_publication import view_create_publication
from frontend.views.view_manage_categories import view_manage_categories
from backend.auth.auth_service import logout, is_authenticated

def main():
    # Primero verificar autenticación para mantener sesiones
    if 'authenticated' in st.session_state and st.session_state.authenticated:
        # Si ya hay una sesión activa pero estamos en una vista pública o de login
        if 'vista' not in st.session_state or st.session_state.vista in ["public_apps", "login", "register"]:
            # Redirigir a la vista privada
            st.session_state.vista = "private_general"
    elif is_authenticated():
        # La función is_authenticated verifica si hay una sesión válida
        # Si no está en session_state pero la función dice que sí, restauramos
        st.session_state.vista = "private_general"
    
    # Inicializar el estado solo si no existe en absoluto
    if 'vista' not in st.session_state:
        st.session_state.vista = "public_apps"

    # Manejar la lógica de cierre de sesión en la parte principal
    if st.session_state.vista == "logout":
        logout()  # Limpia la sesión de usuario
        st.session_state.vista = "login"
        st.rerun()

    # Mostrar vista según el estado actual
    if st.session_state.vista == "public_apps":
        view_public_apps()
    elif st.session_state.vista == "public_appsview":
        view_public_appsview()
    elif st.session_state.vista == "login":
        login_view()
    elif st.session_state.vista == "register":
        register_view()
    elif st.session_state.vista == "private_general":
        view_private_general()
    elif st.session_state.vista == "create_publication":
        view_create_publication()
    elif st.session_state.vista == "manage_categories":
        view_manage_categories()

if __name__ == "__main__":
    # Cargar estilos
    with open("frontend/assets/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    
    main()