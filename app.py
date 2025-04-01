import streamlit as st
st.set_page_config(layout="wide")
from frontend.views.login_view import login_view
from frontend.views.register_view import register_view
from frontend.views.view_public_apps import view_public_apps
from frontend.views.view_public_appsview import view_public_appsview
from frontend.views.view_private_general import view_private_general
from frontend.views.view_create_publication import view_create_publication
from frontend.views.view_manage_categories import view_manage_categories
from frontend.views.view_manage_tags import view_manage_tags
from frontend.views.view_private_pub_view import view_private_pub_view
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

    # Procesa cambios de vista pendientes
    # if "vista_target" in st.session_state:
    #     st.session_state.vista = st.session_state.vista_target
    #     del st.session_state.vista_target  # Limpia después de usarla

    # Manejar la lógica de cierre de sesión en la parte principal
    if st.session_state.vista == "logout":
        logout()  # Limpia la sesión de usuario
        st.session_state.vista = "login"
        st.rerun()

    # Actualizar manejo de parámetros URL
    pub_id = st.query_params.get("id")  # Nuevo método

    # Si hay un ID de publicación en los parámetros, actualizar vista según el contexto
    if pub_id:
        if is_authenticated():
            st.session_state.vista = "private_pub_view"
        else:
            st.session_state.vista = "public_appsview"
        st.session_state.pub_id = pub_id

    # Verificar autenticación solo para vistas privadas
    if (
        st.session_state.vista
        in [
            "private_general",
            "private_pub_view",
            "create_publication",
            "manage_categories",
            "manage_tags",
        ]
        and not is_authenticated()
    ):
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
    elif st.session_state.vista == "private_pub_view":
        view_private_pub_view()
    elif st.session_state.vista == "create_publication":
        view_create_publication()
    elif st.session_state.vista == "manage_categories":
        view_manage_categories()
    elif st.session_state.vista == "manage_tags":
        view_manage_tags()


if __name__ == "__main__":
    # Cargar estilos
    with open("frontend/assets/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    
    main()
