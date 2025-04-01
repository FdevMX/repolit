import streamlit as st
from backend.auth.auth_service import is_admin

def show_sidebar(user, current_view):
    with st.sidebar:
        st.title(f"Bienvenido, {user['name']}")

        # Estilo CSS para la navegación
        st.markdown("""
            <style>
            .nav-link {
                padding: 0.5rem 1rem;
                color: #333;
                text-decoration: none;
                border-radius: 0.5rem;
                margin: 0.2rem 0;
                display: block;
            }
            .nav-link:hover {
                background-color: rgba(49, 51, 63, 0.1);
            }
            .nav-link.active {
                background-color: rgba(49, 51, 63, 0.2);
                font-weight: bold;
            }
            .nav-section {
                margin: 1rem 0;
                padding-bottom: 0.5rem;
                border-bottom: 1px solid rgba(49, 51, 63, 0.1);
            }
            </style>
        """, unsafe_allow_html=True)

        # Sección principal de navegación
        st.markdown("<div class='nav-section'>", unsafe_allow_html=True)
        st.markdown("#### Principal")
        if st.sidebar.button(
            "📚 Todas las publicaciones",
            use_container_width=True,
            type="secondary",
            help="Ver todas las publicaciones",
        ):
            st.session_state.vista = "private_general"
            st.rerun()

        if st.sidebar.button(
            "📝 Crear nueva publicación",
            use_container_width=True,
            help="Crear una nueva publicación",
        ):
            st.session_state.vista = "create_publication"
            st.rerun()

        # Sección de administración (solo para admins)
        if is_admin():
            st.markdown("<div class='nav-section'>", unsafe_allow_html=True)
            st.markdown("#### Administración")

            if st.sidebar.button(
                "🏷️ Gestionar categorías",
                use_container_width=True,
                help="Administrar categorías del sistema",
            ):
                st.session_state.vista = "manage_categories"
                st.rerun()

            if st.sidebar.button(
                "🔖 Gestionar etiquetas",
                use_container_width=True,
                help="Administrar etiquetas del sistema",
            ):
                st.session_state.vista = "manage_tags"
                st.rerun()

        # Sección de navegación secundaria
        # st.markdown("<div class='nav-section'>", unsafe_allow_html=True)
        # st.markdown("#### Publico")
        # if st.sidebar.button(
        #     "🌐 Ir a la página pública",
        #     use_container_width=True,
        #     type="secondary",
        #     help="Ver el sitio público",
        # ):
        #     st.session_state.vista = "public_apps"
        #     st.rerun()

        # Sección de cierre de sesión
        st.markdown(
            "<div class='nav-section' style='margin-top: auto;'>",
            unsafe_allow_html=True,
        )
        st.markdown("#### Cuenta")
        if st.sidebar.button(
            "🚪 Cerrar sesión",
            use_container_width=True,
            type="secondary",
            help="Salir de la aplicación",
        ):
            st.session_state.vista = "logout"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)