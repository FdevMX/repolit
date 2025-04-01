import streamlit as st
import time
from frontend.components.sidebar_private_component import show_sidebar
from frontend.components.toast_components import save_edit_tag, confirm_delete_tag, confirm_add_tag
from backend.auth.auth_service import is_authenticated, get_current_user, is_admin
from backend.data.tag_data import (
    get_tags, 
    get_tag_by_id, 
    create_tag, 
    update_tag, 
    delete_tag
)

def view_manage_tags():
    # Verificar autenticación
    if not is_authenticated():
        st.warning("Debes iniciar sesión para acceder a esta página")
        st.session_state.vista = "login"
        st.rerun()
        return

    # Verificar si es administrador (solo los administradores pueden gestionar etiquetas)
    if not is_admin():
        st.warning("No tienes permisos para acceder a esta página")
        st.session_state.vista = "private_general"
        st.rerun()
        return

    # Obtener datos del usuario
    user = get_current_user()

    # Configurar sidebar específico para usuario autenticado
    show_sidebar(user, "manage_tags")
    
    # Inicializar estados para modales
    if 'edit_modal' not in st.session_state:
        st.session_state.edit_modal = False
        st.session_state.edit_tag = ""
        st.session_state.edit_tag_id = ""

    if 'delete_modal' not in st.session_state:
        st.session_state.delete_modal = False
        st.session_state.delete_tag = ""
        st.session_state.delete_tag_id = ""

    if 'add_modal' not in st.session_state:
        st.session_state.add_modal = False

    # Título y descripción
    st.title("Gestión de Etiquetas")
    st.write("Administra las etiquetas disponibles para clasificar las publicaciones.")

    # Mostrar modales si están activos
    if st.session_state.edit_modal:
        st.markdown("### Editar etiqueta")
        with st.container():
            new_tag_name = st.text_input(
                "Nombre de la etiqueta", 
                value=st.session_state.edit_tag,
                key="edit_tag_input"
            )

            col1, col2 = st.columns(2)
            with col1:
                if st.button("Guardar cambios", key="save_edit", use_container_width=True):
                    if new_tag_name:
                        # Actualizar la etiqueta en la base de datos
                        result = update_tag(st.session_state.edit_tag_id, new_tag_name)
                        if result:
                            save_edit_tag()
                            st.session_state.edit_modal = False
                            st.rerun()
                        else:
                            st.error("Error al actualizar. El nombre podría estar duplicado.")
                    else:
                        st.warning("El nombre no puede estar vacío.")

            with col2:
                if st.button("Cancelar", key="cancel_edit", use_container_width=True):
                    st.session_state.edit_modal = False
                    st.rerun()

    elif st.session_state.delete_modal:
        st.markdown("### Confirmar eliminación")
        with st.container():
            st.write(f"¿Está seguro de que desea eliminar la etiqueta **{st.session_state.delete_tag}**?")
            st.write("**Nota:** No se puede eliminar si hay publicaciones asociadas a esta etiqueta.")

            col1, col2 = st.columns(2)
            with col1:
                if st.button("Eliminar", key="confirm_delete", use_container_width=True):
                    # Eliminar la etiqueta de la base de datos
                    result = delete_tag(st.session_state.delete_tag_id)
                    if result:
                        confirm_delete_tag()
                        st.session_state.delete_modal = False
                        st.rerun()
                    else:
                        st.warning("No se pudo eliminar. La etiqueta podría estar en uso.")

            with col2:
                if st.button("Cancelar", key="cancel_delete", use_container_width=True):
                    st.session_state.delete_modal = False
                    st.rerun()

    elif st.session_state.add_modal:
        st.markdown("### Agregar nueva etiqueta")
        with st.container():
            new_tag = st.text_input("Nombre de la etiqueta", key="new_tag_input")

            col1, col2 = st.columns(2)
            with col1:
                if st.button("Agregar", key="confirm_add", use_container_width=True):
                    if new_tag:
                        # Crear la etiqueta en la base de datos
                        result = create_tag(new_tag)
                        if result:
                            confirm_add_tag()
                            st.session_state.add_modal = False
                            st.rerun()
                        else:
                            st.error("Error al agregar. El nombre ya podría existir.")
                    else:
                        st.warning("El nombre de la etiqueta no puede estar vacío.")

            with col2:
                if st.button("Cancelar", key="cancel_add", use_container_width=True):
                    st.session_state.add_modal = False
                    st.rerun()

    # Si no hay modales activos, mostrar el botón de agregar etiqueta y la lista de etiquetas
    else:
        # MOVIDO: Botón para agregar etiqueta al principio (izquierda)
        col1, col2, col3 = st.columns([3, 2, 2])
        with col1:
            if st.button("+ Agregar nueva etiqueta", key="add_tag_button", use_container_width=True):
                st.session_state.add_modal = True
                st.rerun()

        # Separador visual después del botón
        st.markdown("<hr>", unsafe_allow_html=True)

        # Obtener etiquetas desde la base de datos
        tags = get_tags()

        if not tags:
            st.info("No hay etiquetas disponibles.")
        else:
            # Título de la sección de etiquetas
            st.subheader("Etiquetas existentes")

            # Contenedor principal para etiquetas
            for tag in tags:
                col1, col2, col3 = st.columns([5, 1, 1])

                with col1:
                    st.markdown(f"<div class='tags-name'>{tag['name']}</div>", unsafe_allow_html=True)

                with col2:
                    if st.button("Editar", key=f"edit_{tag['id']}", use_container_width=True):
                        st.session_state.edit_modal = True
                        st.session_state.edit_tag = tag['name']
                        st.session_state.edit_tag_id = tag['id']
                        st.rerun()

                with col3:
                    if st.button("Eliminar", key=f"delete_{tag['id']}", use_container_width=True):
                        st.session_state.delete_modal = True
                        st.session_state.delete_tag = tag['name']
                        st.session_state.delete_tag_id = tag['id']
                        st.rerun()

                # Línea divisoria entre etiquetas
                # st.markdown("<hr style='margin: 5px 0;'>", unsafe_allow_html=True)
