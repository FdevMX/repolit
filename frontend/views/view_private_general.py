import streamlit as st
from backend.auth.auth_service import is_authenticated, get_current_user, is_admin

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
    with st.sidebar:
        st.title(f"Bienvenido, {user['name']}")

        # Opciones de navegación para usuarios autenticados
        opciones = ["Todas las publicaciones", "Crear nueva publicación", 
                    "Ir a la página pública", "Cerrar sesión"]

        # Añadir opción de gestionar categorías solo para administradores
        if is_admin():
            opciones.insert(2, "Gestionar categorías")

        opcion = st.radio("Opciones:", opciones)

        # Navegación basada en la selección
        if opcion == "Crear nueva publicación":
            st.session_state.vista = "create_publication"
            st.rerun()
        elif opcion == "Gestionar categorías" and is_admin():
            st.session_state.vista = "manage_categories"
            st.rerun()
        elif opcion == "Ir a la página pública":
            st.session_state.vista = "public_apps"
            st.rerun()
        elif opcion == "Cerrar sesión":
            st.session_state.vista = "logout"
            st.rerun()

    # Contenido principal de la vista
    st.title("Todas las Publicaciones")
    # Aquí va el contenido principal de la vista...

    # Inicializar estados para modales
    if 'edit_file_modal' not in st.session_state:
        st.session_state.edit_file_modal = False
        st.session_state.edit_file_index = -1

    if 'delete_file_modal' not in st.session_state:
        st.session_state.delete_file_modal = False
        st.session_state.delete_file_index = -1

    # Título y descripción
    st.markdown("## Archivos disponibles")
    st.write("")

    # Archivos disponibles
    files = [
        {
            "title": "Como enrutar redes en una área local",
            "description": "Guía completa sobre enrutamiento de redes locales y configuración de dispositivos.",
            "category": "Redes y conmutadores",
            "tags": ["Redes", "Cisco", "Enrutamiento"],
            "date_created": "12 de enero de 2025",
            "date_updated": "12 de enero de 2025",
        },
        {
            "title": "Conceptos básicos de switching y LAN",
            "description": "Explicación de conceptos fundamentales de switching y LAN para principiantes.",
            "category": "Redes y conmutadores",
            "tags": ["Redes", "Switching", "LAN"],
            "date_created": "27 de diciembre de 2024",
            "date_updated": "27 de diciembre de 2024",
        },
        {
            "title": "Mejores lenguajes de programación",
            "description": "Análisis de los lenguajes de programación más utilizados en la actualidad.",
            "category": "Desarrollo de apps móviles",
            "tags": ["Programación", "Javascript", "Python"],
            "date_created": "12 de diciembre de 2024",
            "date_updated": "12 de diciembre de 2024",
        },
        {
            "title": "Sistemas operativos más populares",
            "description": "Comparativa entre los sistemas operativos más populares del mercado.",
            "category": "Sistemas operativos",
            "tags": ["Windows", "Linux", "MacOS"],
            "date_created": "30 de noviembre de 2024",
            "date_updated": "30 de noviembre de 2024",
        },
        {
            "title": "Mejores lenguajes de programación",
            "description": "Análisis de los lenguajes de programación más utilizados en la actualidad.",
            "category": "Desarrollo de apps móviles",
            "tags": ["Programación", "Javascript", "Python"],
            "date_created": "12 de diciembre de 2024",
            "date_updated": "12 de diciembre de 2024",
        },
        {
            "title": "Sistemas operativos más populares",
            "description": "Comparativa entre los sistemas operativos más populares del mercado.",
            "category": "Sistemas operativos",
            "tags": ["Windows", "Linux", "MacOS"],
            "date_created": "30 de noviembre de 2024",
            "date_updated": "30 de noviembre de 2024",
        },
    ]

    # Mostrar modales si están activos
    if st.session_state.edit_file_modal and st.session_state.edit_file_index >= 0:
        file = files[st.session_state.edit_file_index]
        st.markdown("### Editar publicación")
        with st.container():
            st.markdown(f"<div class='modal-section'>", unsafe_allow_html=True)

            # Formulario pre-llenado con datos del archivo
            new_title = st.text_input("Título", value=file["title"])
            new_description = st.text_area("Descripción", value=file["description"])
            new_category = st.selectbox("Categoría", 
                                      ["Seguridad en computo", "Desarrollo de apps móviles", "Inteligencia artificial", 
                                       "Análisis de vulnerabilidades", "Redes y conmutadores", "Sistemas operativos"],
                                      index=["Seguridad en computo", "Desarrollo de apps móviles", "Inteligencia artificial", 
                                             "Análisis de vulnerabilidades", "Redes y conmutadores", "Sistemas operativos"].index(file["category"]))
            new_tags = st.multiselect("Tags", 
                                    ["Redes", "Cisco", "IA", "VSCode", "HTML", "Javascript", "Enrutamiento", "Switching", "LAN", "Programación", "Python", "Windows", "Linux", "MacOS"],
                                    default=file["tags"])

            # Opción para reemplazar el archivo
            st.write("**Archivo actual:** archivo.pdf")
            new_file = st.file_uploader("Reemplazar archivo (opcional)")

            col1, col2 = st.columns(2)
            with col1:
                if st.button("Guardar cambios", key="save_file_edit", use_container_width=True):
                    st.success("Publicación actualizada correctamente.")
                    st.session_state.edit_file_modal = False
                    st.rerun()

            with col2:
                if st.button("Cancelar", key="cancel_file_edit", use_container_width=True):
                    st.session_state.edit_file_modal = False
                    st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

    elif st.session_state.delete_file_modal and st.session_state.delete_file_index >= 0:
        file = files[st.session_state.delete_file_index]
        st.markdown("### Confirmar eliminación")
        with st.container():
            st.markdown(f"<div class='modal-section'>", unsafe_allow_html=True)
            st.write(f"¿Está seguro de que desea eliminar la publicación **{file['title']}**?")
            st.write("Esta acción no se puede deshacer.")

            col1, col2 = st.columns(2)
            with col1:
                if st.button("Eliminar", key="confirm_file_delete", use_container_width=True):
                    st.error(f"Publicación eliminada: {file['title']}")
                    st.session_state.delete_file_modal = False
                    st.rerun()

            with col2:
                if st.button("Cancelar", key="cancel_file_delete", use_container_width=True):
                    st.session_state.delete_file_modal = False
                    st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

    # Si no hay modales activos, mostrar la lista de archivos
    else:
        # Crear un diseño de grid con 4 columnas por fila
        cols = st.columns(4)
        for index, file in enumerate(files):
            with cols[index % 4]:  # Asignar cada archivo a una columna
                # Contenido de la tarjeta
                st.markdown(
                    f"""<div class="card">
                        <div class="card-content">
                            <h4>{file['title']}</h4>
                            <p class="card-date">Creado: {file['date_created']}</p>
                            <p class="card-date">Actualizado: {file['date_updated']}</p>
                        </div>
                    """, 
                    unsafe_allow_html=True
                )

                # Botones funcionales de Streamlit en lugar de HTML
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Editar", key=f"edit_file_{index}", use_container_width=True):
                        st.session_state.edit_file_modal = True
                        st.session_state.edit_file_index = index
                        st.rerun()

                with col2:
                    if st.button("Eliminar", key=f"delete_file_{index}", use_container_width=True):
                        st.session_state.delete_file_modal = True
                        st.session_state.delete_file_index = index
                        st.rerun()

                # Cerrar div de la tarjeta
                st.markdown("</div>", unsafe_allow_html=True)
