import streamlit as st
from backend.auth.auth_service import is_authenticated

def show_sidebar_public(categories, current_category=None):
    with st.sidebar:
        st.title("Cuenta")
        
        st.markdown("""
            <style>
            .nav-section {
                margin: 1rem 0;
                padding-bottom: 0.5rem;
                border-bottom: 1px solid rgba(49, 51, 63, 0.1);
            }
            .stRadio [role="radiogroup"] {
                padding: 0.5rem;
                border-radius: 0.5rem;
            }
            .stRadio label {
                padding: 0.5rem 1rem;
                border-radius: 0.5rem;
                transition: all 0.2s ease;
            }
            .stRadio label:hover {
                background-color: #FBD8FD;
                color: #3a3a3a;
            }
            </style>
        """, unsafe_allow_html=True)

        # # Sección de navegación principal
        # st.markdown("#### Navegación")
        # nav_options = ["📚 Todas las publicaciones"]
        
        # # Añadir categorías si existen
        # if categories:
        #     nav_options.extend([f"📂 {cat['name']}" for cat in categories])

        # Opciones de autenticación
        # st.markdown("#### Cuenta")
        if not is_authenticated():
            if st.button("🔑 Iniciar sesión", use_container_width=True, type="secondary"):
                st.session_state.vista = "login"
                st.rerun()
            if st.button("📝 Registrarse", use_container_width=True, type="secondary"):
                st.session_state.vista = "register"
                st.rerun()
        else:
            if st.button("🏠 Ir a mi panel", use_container_width=True, type="secondary"):
                st.session_state.vista = "private_general"
                st.rerun()