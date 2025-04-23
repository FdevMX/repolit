import streamlit as st
import time
import os
from backend.auth.auth_service import is_authenticated, get_current_user, is_admin
from backend.data.category_data import get_categories, get_category_by_name
from backend.data.tag_data import get_tags
from backend.data.publication_data import create_publication
from backend.storage.file_handler import save_uploaded_file
from frontend.components.sidebar_private_component import show_sidebar
from backend.storage.youtube_handler import extract_audio_from_youtube, is_youtube_url


def view_create_publication():
    # Verificar autenticación
    if not is_authenticated():
        st.warning("Debes iniciar sesión para acceder a esta página")
        st.session_state.vista = "login"
        st.rerun()
        return

    # Obtener datos del usuario
    user = get_current_user()

    # AÑADIR: Verificar que el usuario realmente existe en la base de datos
    from backend.db.connection import execute_query
    try:
        user_check = execute_query("SELECT id FROM users WHERE id = %s", (user['id'],), fetchone=True)
        if not user_check:
            st.error(f"Error de autenticación: La sesión contiene un ID de usuario inválido.")
            st.warning("Por favor, cierra sesión e inicia sesión nuevamente.")
            # Forzar cierre de sesión
            st.session_state.vista = "logout"
            time.sleep(3)
            st.rerun()
            return
    except Exception as e:
        st.error(f"Error al verificar usuario: {e}")
        st.session_state.vista = "logout"
        st.rerun()
        return

    # Configurar sidebar específico para usuario autenticado
    show_sidebar(user, "create_publication")

    # Contenido principal
    st.title("Crear nueva publicación")
    st.write("Completa el formulario para crear una nueva publicación.")

    # Obtener categorías y tags dinámicamente de la base de datos
    try:
        categories = get_categories()
        category_names = [category['name'] for category in categories] if categories else []

        tags_data = get_tags()
        tag_names = [tag['name'] for tag in tags_data] if tags_data else []
    except Exception as e:
        st.error(f"Error al cargar datos: {e}")
        category_names = []
        tag_names = []

    # Opciones de contenido (fuera del formulario)
    subtitle = st.subheader("Antes de continuar selecciona el tipo de archivo")
    options = ["Archivo Local", "URL Externa"]
    selection = st.segmented_control(
        "Tipo de contenido", options, selection_mode="single",
        key="pub_content_type",
    )

    # Formulario para crear una nueva publicación
    with st.form("publication_form"):
        title = st.text_input("Título", key="pub_title", placeholder="Escribe un título descriptivo")
        description = st.text_area("Descripción", key="pub_desc", placeholder="Describe el contenido de la publicación")

        # Usar datos dinámicos de la BD
        if category_names:
            category = st.selectbox("Categoría", category_names, key="pub_category")
        else:
            category = st.selectbox("Categoría", ["Sin categorías disponibles"], key="pub_category")
            st.warning("No hay categorías disponibles. Contacta al administrador.")

        if tag_names:
            selected_tags = st.multiselect("Etiquetas", tag_names, key="pub_tags", 
                                          placeholder="Selecciona o escribe etiquetas para clasificar tu publicación")
        else:
            selected_tags = st.multiselect("Etiquetas", ["Sin etiquetas disponibles"], key="pub_tags")
            st.warning("No hay etiquetas disponibles. Contacta al administrador.")

        # Dentro del formulario, usar la variable selection directamente
        if selection == "Archivo Local":
            # Subida de archivo
            file_help = "Puedes subir documentos (.pdf, .doc, .docx), imágenes (.jpg, .png), videos (.mp4, .mov, .avi) u otros archivos relacionados"
            uploaded_file = st.file_uploader(
                "Seleccionar archivo", key="pub_file", help=file_help
            )

            # Vista previa del archivo si es una imagen
            if uploaded_file and uploaded_file.type.startswith("image/"):
                st.image(uploaded_file, caption="Vista previa de la imagen", width=300)
            content_url = None
        else:
            # Enlace URL
            content_url = st.text_input(
                "URL del contenido",
                key="pub_url",
                placeholder="https://youtube.com/jkkhjkh",
                help="Ingresa la URL del video o sitio web que deseas enlazar",
            )
            
            # Selector de tipo de contenido para URLs
            media_type = st.selectbox(
                "Tipo de contenido",
                options=["Video", "Audio"],
                key="pub_media_type",
                help="Selecciona cómo se reproducirá este contenido"
            )
            
            uploaded_file = None

        # Opciones de publicación
        col1, col2 = st.columns(2)
        with col1:
            is_featured = st.checkbox("Destacar publicación", key="pub_featured", 
                                     help="Las publicaciones destacadas aparecen primero en la página principal")
        with col2:
            is_public = st.checkbox("Publicar inmediatamente", value=True, key="pub_public",
                                   help="Si no se marca, la publicación quedará como borrador")

        # Botones de acción
        col_submit, col_cancel = st.columns(2)
        with col_submit:
            submit_button = st.form_submit_button("Crear publicación", use_container_width=True)
        with col_cancel:
            cancel_button = st.form_submit_button("Cancelar", use_container_width=True)

    # Lógica para manejar la creación de publicación
    if submit_button:
        if not title or not description or category == "Sin categorías disponibles":
            st.error("Por favor completa los campos obligatorios: título, descripción y categoría.")
        else:
            with st.spinner("Guardando publicación..."):
                try:
                    # Verificar user_id nuevamente antes de crear
                    user_current = get_current_user()
                    if not user_current or not user_current.get('id'):
                        st.error("No se pudo obtener información del usuario. Por favor, inicia sesión nuevamente.")
                        st.session_state.vista = "logout"
                        st.rerun()
                        return

                    # Mostrar ID para depuración (quitar en producción)
                    st.info(f"DEBUG - Usando user_id: {user_current['id']}")

                    # 1. Procesar archivo subido o URL
                    file_info = None
                    content_type = "Archivo" if st.session_state.pub_content_type == "Archivo Local" else "URL de video/sitio web"
                    
                    if content_type == "Archivo" and uploaded_file:
                        file_info = save_uploaded_file(uploaded_file, user['id'])
                        if not file_info:
                            st.error("Error al guardar el archivo. Inténtalo de nuevo.")
                            return
                        
                    # Dentro del bloque donde procesas la URL:
                    elif content_type == "URL de video/sitio web" and content_url:
                        # Verificar si es una URL válida
                        if not content_url.startswith(('http://', 'https://')):
                            st.error("Por favor, ingresa una URL válida que comience con http:// o https://")
                            return
                            
                        # Si el tipo de medio es audio y es una URL de YouTube, extraer audio
                        if media_type.lower() == "audio" and is_youtube_url(content_url):
                            file_info = extract_audio_from_youtube(content_url, user['id'])
                            if not file_info:
                                st.error("No se pudo extraer el audio del video de YouTube.")
                                return
                        else:
                            # Para video o URLs que no son de YouTube, guardar la URL directamente
                            file_info = {
                                "url": content_url,
                                "is_external": True,
                                "filename": "external_content",
                                "content_type": "url",
                                "media_type": media_type.lower()
                            }
                    else:
                        # Validación para cuando no hay archivo o URL
                        if content_type == "Archivo":
                            st.error("Por favor, selecciona un archivo para subir.")
                        else:
                            st.error("Por favor, ingresa una URL válida.")
                        return

                    # 2. Obtener ID de categoría
                    category_obj = get_category_by_name(category)
                    if not category_obj:
                        st.error(f"La categoría '{category}' no se encontró en la base de datos.")
                        return

                    # 3. Crear la publicación
                    result = create_publication(
                        title=title,
                        description=description,
                        category_id=category_obj['id'],
                        user_id=user['id'],
                        is_featured=is_featured,
                        is_public=is_public,
                        file_info=file_info,
                        tag_names=selected_tags
                    )

                    if result:
                        st.success(f"Publicación '{title}' creada exitosamente.")
                        st.balloons()
                        # Esperar un poco para que el usuario vea el mensaje
                        time.sleep(2)
                        st.session_state.vista = "private_general"
                        st.rerun()
                    else:
                        st.error("Error al crear la publicación. Por favor intenta de nuevo.")

                except Exception as e:
                    st.error(f"Error inesperado: {str(e)}")

    if cancel_button:
        st.warning("Creación de publicación cancelada.")
        st.session_state.vista = "private_general"
        st.rerun()
