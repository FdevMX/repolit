import streamlit as st
from frontend.components.card_component import card_component
from backend.data.category_data import get_categories
from backend.auth.auth_service import is_authenticated

def view_public_apps():
    # Sidebar para vista pública
    with st.sidebar:
        st.title("Categorías")

        # Obtener todas las categorías de la base de datos
        categories = get_categories()
        category_names = [cat["name"] for cat in categories]

        # Añadir otras opciones de navegación
        all_options = category_names + ["Archivos disponibles", "Vista de archivo"]

        # Añadir opciones de autenticación solo si no está autenticado
        if not is_authenticated():
            all_options += ["Iniciar sesión", "Registrarse"]
        else:
            all_options += ["Ir a mi panel"]

        opcion = st.radio("Filtrar por:", all_options)

        # Lógica de navegación
        if opcion == "Vista de archivo":
            st.session_state.vista = "public_appsview"
            st.rerun()
        elif opcion == "Iniciar sesión":
            st.session_state.vista = "login"
            st.rerun()
        elif opcion == "Registrarse":
            st.session_state.vista = "register"
            st.rerun()
        elif opcion == "Ir a mi panel":
            st.session_state.vista = "private_general"
            st.rerun()

    # Contenido principal
    st.title("Repositorio Digital")

    # Resto del contenido...
    st.markdown("## Archivos disponibles")
    st.write("")

    # Archivos disponibles
    files = [
        {
            "title": "Mejores lenguajes de programación",
            "tags": ["Tecnología", "ChatGPT"],
            "date": "12 de diciembre de 2024",
        },
        {
            "title": "Como crear una app responsiva",
            "tags": ["HTML", "Apps web", "Javascript"],
            "date": "29 de noviembre de 2024",
        },
        {
            "title": "Aprende Golang en 30 días sin más",
            "tags": ["IA", "VSCode"],
            "date": "07 de mayo de 2024",
        },
        {
            "title": "Conceptos básicos de redes",
            "tags": ["Redes", "Cisco"],
            "date": "15 de enero de 2025",
        },
        {
            "title": "Guía de ciberseguridad",
            "tags": ["Seguridad", "Internet"],
            "date": "20 de diciembre de 2024",
        },
        {
            "title": "Sistemas operativos populares",
            "tags": ["Windows", "Linux", "iOS"],
            "date": "30 de noviembre de 2024",
        },
    ]

    # Crear un diseño de grid con 3 columnas por fila
    cols = st.columns(4)
    for index, file in enumerate(files):
        with cols[index % 4]:  # Asignar cada archivo a una columna
            card_component(file["title"], file["tags"], file["date"])
