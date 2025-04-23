import streamlit as st
import time
from datetime import datetime
from frontend.components.sidebar_private_component import show_sidebar
from backend.auth.auth_service import is_authenticated, get_current_user, is_admin
from backend.data.publication_data import (
    get_publications_with_tags,
    get_publications_by_user,
    get_publication_by_id,
    update_publication,
    delete_publication
)
from backend.data.category_data import get_categories, get_category_by_name
from backend.data.tag_data import get_tags, get_or_create_tags
from backend.storage.file_handler import save_uploaded_file

def format_date(date_str):
    """Formatea una fecha de PostgreSQL a un formato legible."""
    if not date_str:
        return ""
    try:
        date_obj = datetime.fromisoformat(str(date_str).replace('Z', '+00:00'))
        return date_obj.strftime("%d de %B de %Y")
    except:
        return str(date_str)

def view_private_general():
    # Verificar autenticación
    if not is_authenticated():
        st.warning("Debes iniciar sesión para acceder a esta página")
        st.session_state.vista = "login"
        st.rerun()
        return

    # Obtener datos del usuario
    user = get_current_user()

    # Configurar sidebar específico para usuario autenticado
    show_sidebar(user, "private_general")

    # Contenido principal de la vista
    st.title("Todas las Publicaciones")

    # Inicializar claves de filtro en session_state si no existen
    if 'private_filter_search' not in st.session_state:
        st.session_state.private_filter_search = ""
    if 'private_filter_category' not in st.session_state:
        st.session_state.private_filter_category = "Todas las categorías"
    if 'private_filter_tags' not in st.session_state:
        st.session_state.private_filter_tags = []
    if 'private_filter_only_mine' not in st.session_state:
        st.session_state.private_filter_only_mine = False

    # Filtros
    with st.expander("Filtros de búsqueda", expanded=False):
        col1, col2 = st.columns(2)

        with col1:
            # Usar el valor guardado como predeterminado
            search_query = st.text_input(
                "Buscar por título o descripción",
                value=st.session_state.private_filter_search,
                key="search_query",
            )
            # Guardar cambios en el estado de sesión
            st.session_state.private_filter_search = search_query

            # Obtener categorías de la base de datos
            try:
                categories = get_categories()
                category_names = ["Todas las categorías"] + [
                    cat["name"] for cat in categories
                ]
                selected_category = st.selectbox(
                    "Filtrar por categoría",
                    category_names,
                    index=(
                        category_names.index(st.session_state.private_filter_category)
                        if st.session_state.private_filter_category in category_names
                        else 0
                    ),
                )
                # Guardar cambios en el estado de sesión
                st.session_state.private_filter_category = selected_category
            except Exception as e:
                st.error(f"Error al cargar categorías: {e}")
                selected_category = "Todas las categorías"
                categories = []
                st.session_state.private_filter_category = selected_category

        with col2:
            # Obtener etiquetas de la base de datos
            try:
                tags = get_tags()
                tag_names = [tag["name"] for tag in tags] if tags else []

                # Filtrar etiquetas guardadas para asegurarse que existan en las etiquetas actuales
                valid_saved_tags = [
                    tag
                    for tag in st.session_state.private_filter_tags
                    if tag in tag_names
                ]

                selected_tags = st.multiselect(
                    "Filtrar por etiquetas", tag_names, default=valid_saved_tags
                )
                # Guardar cambios en el estado de sesión
                st.session_state.private_filter_tags = selected_tags
            except Exception as e:
                st.error(f"Error al cargar etiquetas: {e}")
                selected_tags = []
                st.session_state.private_filter_tags = []

            # Opción para ver solo mis publicaciones
            show_only_mine = st.checkbox(
                "Ver solo mis publicaciones",
                value=st.session_state.private_filter_only_mine,
            )
            # Guardar cambios en el estado de sesión
            st.session_state.private_filter_only_mine = show_only_mine

    # Obtener publicaciones según los filtros
    try:
        # Determinar qué publicaciones mostrar
        if show_only_mine:
            publications = get_publications_by_user(user['id'])
        else:
            publications = get_publications_with_tags()

        # Aplicar filtros adicionales (esto sería mejor hacerlo en la BD pero por ahora filtramos en memoria)
        if search_query:
            publications = [p for p in publications if 
                           search_query.lower() in p['title'].lower() or 
                           search_query.lower() in p['description'].lower()]

        if selected_category and selected_category != "Todas las categorías":
            publications = [p for p in publications if p['category_name'] == selected_category]

        if selected_tags:
            filtered_pubs = []
            for pub in publications:
                # Obtener nombres de etiquetas de la publicación
                pub_tag_names = [tag['name'] for tag in pub.get('tags', [])]
                # Verificar si alguna etiqueta seleccionada está en la publicación
                if any(tag in pub_tag_names for tag in selected_tags):
                    filtered_pubs.append(pub)
            publications = filtered_pubs

    except Exception as e:
        st.error(f"Error al cargar publicaciones: {e}")
        publications = []

    # Inicializar estados para modales
    if 'edit_pub_modal' not in st.session_state:
        st.session_state.edit_pub_modal = False
        st.session_state.edit_pub_id = None

    if 'delete_pub_modal' not in st.session_state:
        st.session_state.delete_pub_modal = False
        st.session_state.delete_pub_id = None

    # Título y descripción
    if publications:
        st.success(f"{len(publications)} publicaciones encontradas")
    else:
        st.info("No se encontraron publicaciones. ¡Crea una nueva!")

    # Mostrar modales si están activos
    if st.session_state.edit_pub_modal and st.session_state.edit_pub_id:
        try:
            # Obtener la publicación a editar
            publication = get_publication_by_id(st.session_state.edit_pub_id)

            if not publication:
                st.error("La publicación no existe o ha sido eliminada")
                st.session_state.edit_pub_modal = False
                st.rerun()

            st.markdown("### Editar publicación")
            with st.container():
                # Formulario pre-llenado con datos del archivo
                new_title = st.text_input("Título", value=publication["title"])
                new_description = st.text_area("Descripción", value=publication["description"])

                # Categorías y etiquetas
                categories = get_categories()
                category_names = [cat['name'] for cat in categories] if categories else []

                if category_names:
                    default_index = category_names.index(publication['category_name']) if publication['category_name'] in category_names else 0
                    new_category = st.selectbox("Categoría", category_names, index=default_index)
                else:
                    new_category = st.selectbox("Categoría", ["Sin categorías disponibles"])
                    st.warning("No hay categorías disponibles.")

                tags_data = get_tags()
                tag_names = [tag['name'] for tag in tags_data] if tags_data else []
                current_tag_names = [tag['name'] for tag in publication.get('tags', [])]

                if tag_names:
                    new_tags = st.multiselect("Etiquetas", tag_names, default=current_tag_names)
                else:
                    new_tags = st.multiselect("Etiquetas", ["Sin etiquetas disponibles"])
                    st.warning("No hay etiquetas disponibles.")

                # Opciones de publicación
                col_featured, col_public = st.columns(2)
                with col_featured:
                    is_featured = st.checkbox("Destacar publicación", value=publication.get('is_featured', False),
                                           help="Las publicaciones destacadas aparecen primero")
                with col_public:
                    is_public = st.checkbox("Publicación pública", value=publication.get('is_public', True),
                                         help="Si no se marca, quedará como borrador")

                # Determinar si la publicación actual es una URL externa o un archivo local
                is_external_content = publication.get('is_external', False)
                initial_content_type = "URL Externa" if is_external_content else "Archivo Local"
                
                # Opciones de tipo de contenido
                # st.write("**Tipo de contenido:**")
                content_type_options = ["Archivo Local", "URL Externa"]
                new_content_type = st.radio(
                    "Tipo de contenido",
                    options=content_type_options,
                    index=content_type_options.index(initial_content_type),
                    horizontal=True
                )
                
                # Manejar la entrada según el tipo de contenido seleccionado
                if new_content_type == "Archivo Local":
                    # Mostrar información del archivo actual si existe
                    if publication.get('file_name') and not is_external_content:
                        st.write(f"**Archivo actual:** {publication['file_name']}")
                    elif is_external_content:
                        st.warning("⚠️ Cambiar a archivo local eliminará la URL externa actual")
                    else:
                        st.write("**No hay archivo adjunto**")
                    
                    # Opción para subir un nuevo archivo
                    new_file = st.file_uploader("Seleccionar nuevo archivo (opcional)")
                    
                    # Mostrar vista previa si es una imagen en un expander
                    if publication.get('file_type') and publication['file_type'].startswith('image/') and not is_external_content:
                        with st.expander("Vista previa de la imagen actual", expanded=False):
                            try:
                                from PIL import Image
                                import os
                                from backend.storage.file_handler import get_file_path
                
                                file_path = get_file_path(publication['file_url'])
                                if os.path.exists(file_path):
                                    image = Image.open(file_path)
                                    st.image(image, caption="Imagen actual", width=300)
                            except Exception as e:
                                st.warning(f"No se pudo cargar la vista previa de la imagen: {e}")
                
                else:  # URL Externa
                    # Mostrar la URL actual si existe y es externa
                    current_url = publication.get('file_url', '') if is_external_content else ''
                    current_media_type = publication.get('media_type', 'video').capitalize() if is_external_content else 'Video'
                    
                    if is_external_content and current_url:
                        st.write(f"**URL actual:** {current_url}")
                    else:
                        st.warning("⚠️ Cambiar a URL externa eliminará el archivo local actual")
                    
                    # Campo para ingresar URL
                    new_content_url = st.text_input(
                        "URL del contenido", 
                        value=current_url,
                        placeholder="https://youtube.com/watch?v=...",
                        help="Ingresa la URL del video o sitio web que deseas enlazar"
                    )
                    
                    # Selector de tipo de contenido para URLs
                    new_media_type = st.selectbox(
                        "Tipo de contenido",
                        options=["Video", "Audio"],
                        index=0 if current_media_type == "Video" else 1,
                        help="Selecciona cómo se reproducirá este contenido"
                    )
                    
                    # Para mantener compatibilidad con el código existente
                    new_file = None
                
                    # Si es una URL de YouTube y el tipo es audio, mostrar información
                    if new_media_type == "Audio" and new_content_url:
                        from backend.storage.youtube_handler import is_youtube_url
                        if is_youtube_url(new_content_url):
                            st.info("ℹ️ El audio se extraerá del video de YouTube seleccionado")
                        else:
                            st.warning("⚠️ La reproducción como audio solo funciona con URLs de YouTube")

                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Guardar cambios", key="save_pub_edit", use_container_width=True):
                        with st.spinner("Actualizando publicación..."):
                            try:
                                # Procesar archivo o URL según el tipo de contenido
                                new_file_info = None
                                
                                if new_content_type == "Archivo Local" and new_file:
                                    # Subida de nuevo archivo local
                                    new_file_info = save_uploaded_file(new_file, user['id'])
                                    if not new_file_info:
                                        st.error("Error al guardar el archivo.")
                                        return
                                elif new_content_type == "URL Externa" and new_content_url:
                                    # Procesar URL externa
                                    if not new_content_url.startswith(('http://', 'https://')):
                                        st.error("Por favor, ingresa una URL válida que comience con http:// o https://")
                                        return
                                        
                                    # Si el tipo de medio es audio y es una URL de YouTube, extraer información de audio
                                    if new_media_type.lower() == "audio":
                                        from backend.storage.youtube_handler import is_youtube_url, extract_audio_from_youtube
                                        if is_youtube_url(new_content_url):
                                            # Obtener info del audio de YouTube
                                            youtube_info = extract_audio_from_youtube(new_content_url, user['id'])
                                            if not youtube_info:
                                                st.error("No se pudo procesar el audio del video de YouTube.")
                                                return
                                                
                                            # Normalizar los nombres de campo para que coincidan con lo que espera update_publication
                                            new_file_info = {
                                                "file_url": youtube_info.get("url", ""),
                                                "file_name": youtube_info.get("filename", "youtube_audio"),
                                                "file_type": youtube_info.get("content_type", "url"),
                                                "is_external": youtube_info.get("is_external", True),
                                                "media_type": youtube_info.get("media_type", "audio")
                                            }
                                        else:
                                            st.error("La reproducción como audio solo funciona con URLs de YouTube.")
                                            return
                                    else:
                                        # Para video o URLs que no son para audio
                                        new_file_info = {
                                            "file_url": new_content_url,
                                            "is_external": True,
                                            "file_name": "external_content",
                                            "file_type": "url",
                                            "media_type": new_media_type.lower()
                                        }
                                    
                                # Obtener id de categoría
                                category_obj = get_category_by_name(new_category)
                                if not category_obj:
                                    st.error(f"La categoría '{new_category}' no se encontró.")
                                    return
                        
                                # Datos a actualizar
                                update_data = {
                                    'title': new_title,
                                    'description': new_description,
                                    'category_id': category_obj['id'],
                                    'is_featured': is_featured,
                                    'is_public': is_public
                                }
                        
                                # Añadir mensaje de debug para ver qué se está enviando
                                # st.info(f"Actualizando con datos: {update_data} y archivo: {new_file_info}")
                                
                                # Actualizar publicación
                                updated = update_publication(
                                    st.session_state.edit_pub_id,
                                    update_data,
                                    new_file_info,
                                    new_tags
                                )
                        
                                if updated:
                                    st.success("Publicación actualizada correctamente.")
                                    time.sleep(1)
                                    st.session_state.edit_pub_modal = False
                                    st.rerun()
                                else:
                                    st.error("Error al actualizar la publicación.")
                            except Exception as e:
                                st.error(f"Error: {str(e)}")
                                
                with col2:
                    if st.button("Cancelar", key="cancel_pub_edit", use_container_width=True):
                        st.session_state.edit_pub_modal = False
                        st.rerun()

        except Exception as e:
            st.error(f"Error al cargar los detalles de la publicación: {e}")
            st.session_state.edit_pub_modal = False
            st.rerun()

    elif st.session_state.delete_pub_modal and st.session_state.delete_pub_id:
        try:
            # Obtener la publicación a eliminar
            publication = get_publication_by_id(st.session_state.delete_pub_id)

            if not publication:
                st.error("La publicación no existe o ya ha sido eliminada")
                st.session_state.delete_pub_modal = False
                st.rerun()

            st.markdown("### Confirmar eliminación")
            with st.container():
                st.write(f"¿Está seguro de que desea eliminar la publicación **{publication['title']}**?")
                st.write("Esta acción no se puede deshacer.")

                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Eliminar", key="confirm_pub_delete", use_container_width=True):
                        with st.spinner("Eliminando publicación..."):
                            try:
                                result = delete_publication(st.session_state.delete_pub_id)
                                if result:
                                    st.error(f"Publicación eliminada: {publication['title']}")
                                    time.sleep(1)
                                    st.session_state.delete_pub_modal = False
                                    st.rerun()
                                else:
                                    st.warning("No se pudo eliminar la publicación.")
                            except Exception as e:
                                st.error(f"Error: {str(e)}")

                with col2:
                    if st.button("Cancelar", key="cancel_pub_delete", use_container_width=True):
                        st.session_state.delete_pub_modal = False
                        st.rerun()

        except Exception as e:
            st.error(f"Error al cargar los detalles de la publicación: {e}")
            st.session_state.delete_pub_modal = False
            st.rerun()

    # Si no hay modales activos, mostrar la lista de publicaciones
    else:
        if not publications:
            st.markdown("""
            <div style="text-align: center; padding: 2rem;">
                <h3>No hay publicaciones disponibles</h3>
                <p>Utiliza el botón 'Crear nueva publicación' para añadir contenido.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Crear un diseño de grid con 4 columnas por fila
            cols = st.columns(3)
            for index, pub in enumerate(publications):
                with cols[index % 3]:  # Asignar cada publicación a una columna
                    # Contenido de la tarjeta
                    # Obtener datos para mostrar
                    title = pub['title'][:17] + "..." if len(pub['title']) > 17 else pub['title']
                    description = pub['description'][:80] + "..." if len(pub['description']) > 80 else pub['description']
                    category = pub['category_name']
                    tags = [tag['name'] for tag in pub.get('tags', [])]
                    tags_html = " ".join([f'<span class="tag">{tag}</span>' for tag in tags[:3]])
                    if len(tags) > 3:
                        tags_html += f' <span class="tag">+{len(tags)-3}</span>'

                    created = format_date(pub.get('created_at'))
                    updated = format_date(pub.get('updated_at'))

                    # Verificar si hay imagen para mostrar
                    has_image = pub.get('file_type') and 'image' in pub.get('file_type', '')

                    # HTML para la tarjeta
                    card_html = f"""
                    <div class="pub-card">
                        <h4>{title}</h4>
                        <p class="card-category">{category}</p>
                        <p class="card-desc">{description}</p>
                        <div class="card-tags">{tags_html}</div>
                        <p class="card-date">Creado: {created}</p>
                        <p class="card-date">Actualizado: {updated}</p>
                    </div>
                    """

                    st.markdown(card_html, unsafe_allow_html=True)

                    # Mostrar ícono si es una publicación destacada
                    status_featured = st.container()
                    with status_featured:
                        # Featured indicator
                        if pub.get('is_featured'):
                            st.markdown("📌 **Destacada**", help="Esta publicación está destacada")
                        else:
                            # Empty space placeholder to maintain consistent height
                            st.markdown("<div style='height: 42px;'></div>", unsafe_allow_html=True)

                    # Mostrar ícono si es un borrador (no público)
                    status_public = st.container()
                    with status_public:
                        if not pub.get('is_public'):
                            st.markdown("🎨 **Borrador**", help="Esta publicación es privada (solo visible para ti)")
                        else:
                            # Empty space placeholder to maintain consistent height
                            st.markdown("<div style='height: 42px;'></div>", unsafe_allow_html=True)

                    # Botones funcionales de Streamlit
                    col1, col2, col3 = st.columns(3)

                    # def create_view_link(pub_id):
                    #     return f"""
                    #     <a href="?id={pub_id}" target="_self" class="view-link">
                    #         Ver publicación
                    #     </a>
                    #     """

                    # Reemplaza el bloque del botón "Ver" con esto:
                    with col1:
                        # Este es una alternativa
                        # st.markdown(create_view_link(pub['id']), unsafe_allow_html=True)

                        if st.button("Ver", key=f"view_pub_{pub['id']}", use_container_width=True):
                            # Establecer el parámetro de URL
                            st.query_params['id'] = pub['id']
                            # Cambiar la vista
                            st.session_state.vista = "private_pub_view"
                            st.rerun()

                    with col2:
                        if st.button("Editar", key=f"edit_pub_{pub['id']}", use_container_width=True):
                            st.session_state.edit_pub_modal = True
                            st.session_state.edit_pub_id = pub['id']
                            st.rerun()

                    with col3:
                        if st.button("Eliminar", key=f"delete_pub_{pub['id']}", use_container_width=True):
                            st.session_state.delete_pub_modal = True
                            st.session_state.delete_pub_id = pub['id']
                            st.rerun()
