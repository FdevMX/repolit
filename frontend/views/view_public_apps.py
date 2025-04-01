import streamlit as st
from datetime import datetime
from frontend.components.sidebar_public_component import show_sidebar_public
from backend.data.category_data import get_categories
from backend.data.publication_data import get_public_publications
from backend.data.tag_data import get_tags

def format_date(date_str):
    if not date_str:
        return ""
    try:
        date_obj = datetime.fromisoformat(str(date_str).replace('Z', '+00:00'))
        return date_obj.strftime("%d de %B de %Y")
    except:
        return str(date_str)

def view_public_apps():
    st.title("Repositorio Digital")

    try:
        # Obtener categorías para el sidebar
        categories = get_categories()
        show_sidebar_public(categories)

        # Filtros de búsqueda
        with st.expander("Filtros de búsqueda", expanded=False):
            col1, col2 = st.columns(2)

            with col1:
                search_query = st.text_input(
                    "Buscar por título o descripción", key="search_query"
                )

                # Obtener categorías de la base de datos
                try:
                    category_names = ["Todas las categorías"] + [
                        cat["name"] for cat in categories
                    ]
                    selected_category = st.selectbox(
                        "Filtrar por categoría", category_names
                    )
                except Exception as e:
                    st.error(f"Error al cargar categorías: {e}")
                    selected_category = "Todas las categorías"

            with col2:
                # Obtener etiquetas de la base de datos
                try:
                    tags = get_tags()
                    selected_tags = st.multiselect(
                        "Filtrar por etiquetas",
                        [tag["name"] for tag in tags] if tags else [],
                    )
                except Exception as e:
                    st.error(f"Error al cargar etiquetas: {e}")
                    selected_tags = []

        # Obtener publicaciones según los filtros
        try:
            # Obtener publicaciones públicas
            publications = get_public_publications()

            # Aplicar filtros
            if search_query:
                publications = [
                    p
                    for p in publications
                    if search_query.lower() in p["title"].lower()
                    or search_query.lower() in p["description"].lower()
                ]

            if selected_category and selected_category != "Todas las categorías":
                publications = [
                    p for p in publications if p["category_name"] == selected_category
                ]

            if selected_tags:
                filtered_pubs = []
                for pub in publications:
                    pub_tag_names = [tag["name"] for tag in pub.get("tags", [])]
                    if any(tag in pub_tag_names for tag in selected_tags):
                        filtered_pubs.append(pub)
                publications = filtered_pubs

        except Exception as e:
            st.error(f"Error al cargar publicaciones: {e}")
            publications = []

        # Obtener publicaciones públicas
        # publications = get_public_publications()

        # Mostrar resultados
        if not publications:
            st.info("No hay publicaciones disponibles.")
        else:
            st.success(f"{len(publications)} publicaciones disponibles")

            # Crear grid de publicaciones
            cols = st.columns(3)
            for index, pub in enumerate(publications):
                with cols[index % 3]:
                    # Datos para mostrar
                    title = pub['title'][:50] + "..." if len(pub['title']) > 50 else pub['title']
                    description = pub['description'][:100] + "..." if len(pub['description']) > 100 else pub['description']

                    # Generar HTML para las etiquetas
                    tags = [tag['name'] for tag in pub.get('tags', [])]
                    tags_html = " ".join([
                        f'<span class="tag">{tag}</span>' for tag in tags[:3]
                    ])
                    if len(tags) > 3:
                        tags_html += f' <span class="tag">+{len(tags)-3}</span>'

                    # HTML de la tarjeta
                    card_html = f"""
                    <div class="pub-card">
                        <h4>{title}</h4>
                        <p class="card-category">{pub['category_name']}</p>
                        <p class="card-desc">{description}</p>
                        <div class="card-tags">{tags_html}</div>
                        <p class="card-date">Publicado: {format_date(pub['created_at'])}</p>
                    </div>
                    """
                    st.markdown(card_html, unsafe_allow_html=True)

                    # Botón para ver detalles
                    if st.button("Ver publicación", key=f"view_pub_{pub['id']}", use_container_width=True):
                        st.query_params["id"] = pub["id"]
                        st.session_state.vista = "public_appsview"
                        st.rerun()

    except Exception as e:
        st.error(f"Error al cargar el contenido: {str(e)}")
