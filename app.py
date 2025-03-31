import streamlit as st
st.set_page_config(layout="wide")
from frontend.views.login_view import login_view
from frontend.views.register_view import register_view
from frontend.views.view_public_apps import view_public_apps
from frontend.views.view_public_appsview import view_public_appsview
from frontend.views.view_private_general import view_private_general
from frontend.views.view_create_publication import view_create_publication
from frontend.views.view_manage_categories import view_manage_categories


def main():
    # Inicializar el estado si no existe
    if 'vista' not in st.session_state:
        st.session_state.vista = "public_apps"

    # Sidebar con radio que refleja el estado actual
    st.sidebar.title("Categorias")
    opcion = st.sidebar.radio(
        "Ir a:",
        (
            "Seguridad en computo",
            "Desarrollo de apps móviles",
            "Inteligencia artificial",
            "Análisis de vulnerabilidades",
            "Redes y conmutadores",
            "Sistemas operativos",
            "Archivos disponibles",
            "Vista de archivo",
            "Iniciar sesión",
            "Registrarse",
            "Todas las publicaciones",
            "Crear nueva publicación",
            "Gestionar categorías",
            "Ir a la página pública",
            "Cerrar sesión",
        ),
        index=[
            "public_apps",
            "public_apps",
            "public_apps",
            "public_apps",
            "public_apps",
            "public_apps",
            "public_apps",
            "public_appsview",
            "login",
            "register",
            "private_general",
            "create_publication",
            "manage_categories",
            "public_apps",
            "login",
        ].index(st.session_state.vista),
    )

    # Actualizar el estado cuando cambia el radio
    if opcion == "Seguridad en computo":
        st.session_state.vista = "public_apps"
    elif opcion == "Desarrollo de apps móviles":
        st.session_state.vista = "public_apps"
    elif opcion == "Inteligencia artificial":
        st.session_state.vista = "public_apps"
    elif opcion == "Análisis de vulnerabilidades":
        st.session_state.vista = "public_apps"
    elif opcion == "Redes y conmutadores":
        st.session_state.vista = "public_apps"
    elif opcion == "Sistemas operativos":
        st.session_state.vista = "public_apps"
    elif opcion == "Archivos disponibles":
        st.session_state.vista = "public_apps"
    elif opcion == "Vista de archivo":
        st.session_state.vista = "public_appsview"
    elif opcion == "Iniciar sesión":
        st.session_state.vista = "login"
    elif opcion == "Registrarse":
        st.session_state.vista = "register"
    elif opcion == "Todas las publicaciones":
        st.session_state.vista = "private_general"
    elif opcion == "Crear nueva publicación":
        st.session_state.vista = "create_publication"
    elif opcion == "Gestionar categorías":
        st.session_state.vista = "manage_categories"
    elif opcion == "Ir a la página pública":
        st.session_state.vista = "public_apps"
    elif opcion == "Cerrar sesión":
        st.session_state.vista = "login"

    # Mostrar vista según el estado
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
