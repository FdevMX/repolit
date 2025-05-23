import streamlit as st
import time
from frontend.components.sidebar_private_component import show_sidebar
from frontend.components.toast_components import save_edit_category, confirm_delete_category, confirm_add_category
from backend.auth.auth_service import is_authenticated, get_current_user, is_admin
from backend.data.category_data import (
    get_categories, 
    get_category_by_id, 
    create_category, 
    update_category, 
    delete_category
)

def view_manage_categories():
    # Verificar autenticación
    if not is_authenticated():
        st.warning("Debes iniciar sesión para acceder a esta página")
        st.session_state.vista = "login"
        st.rerun()
        return

    # Verificar si es administrador (solo los administradores pueden gestionar categorías)
    if not is_admin():
        st.warning("No tienes permisos para acceder a esta página")
        st.session_state.vista = "private_general"
        st.rerun()
        return

    # Obtener datos del usuario
    user = get_current_user()

    # Configurar sidebar específico para usuario autenticado
    show_sidebar(user, "manage_categories")    

    # Inicializar estados para modales
    if 'edit_modal' not in st.session_state:
        st.session_state.edit_modal = False
        st.session_state.edit_category = ""
        st.session_state.edit_category_id = ""

    if 'delete_modal' not in st.session_state:
        st.session_state.delete_modal = False
        st.session_state.delete_category = ""
        st.session_state.delete_category_id = ""

    if 'add_modal' not in st.session_state:
        st.session_state.add_modal = False

    # Título y descripción
    st.title("Gestión de Categorías")
    st.write("Administra las categorías disponibles para clasificar las publicaciones.")

    # Mostrar modales si están activos
    if st.session_state.edit_modal:
        st.markdown("### Editar categoría")
        with st.container():
            new_category_name = st.text_input(
                "Nombre de la categoría", 
                value=st.session_state.edit_category,
                key="edit_category_input"
            )

            col1, col2 = st.columns(2)
            with col1:
                if st.button("Guardar cambios", key="save_edit", use_container_width=True):
                    if new_category_name:
                        # Actualizar la categoría en la base de datos
                        result = update_category(st.session_state.edit_category_id, new_category_name)
                        if result:
                            save_edit_category()
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

            st.write(f"¿Está seguro de que desea eliminar la categoría **{st.session_state.delete_category}**?")
            st.write("**Nota:** No se puede eliminar si hay publicaciones asociadas a esta categoría.")

            col1, col2 = st.columns(2)
            with col1:
                if st.button("Eliminar", key="confirm_delete", use_container_width=True):
                    # Eliminar la categoría de la base de datos
                    result = delete_category(st.session_state.delete_category_id)
                    if result:
                        confirm_delete_category()
                        st.session_state.delete_modal = False
                        st.rerun()
                    else:
                        st.warning("No se pudo eliminar. La categoría podría estar en uso.")

            with col2:
                if st.button("Cancelar", key="cancel_delete", use_container_width=True):
                    st.session_state.delete_modal = False
                    st.rerun()
           

    elif st.session_state.add_modal:
        st.markdown("### Agregar nueva categoría")
        with st.container():
            new_category = st.text_input("Nombre de la categoría", key="new_category_input")

            col1, col2 = st.columns(2)
            with col1:
                if st.button("Agregar", key="confirm_add", use_container_width=True):
                    if new_category:
                        # Crear la categoría en la base de datos
                        result = create_category(new_category)
                        if result:
                            confirm_add_category()
                            st.session_state.add_modal = False
                            st.rerun()
                        else:
                            st.error("Error al agregar. El nombre ya podría existir.")
                    else:
                        st.warning("El nombre de la categoría no puede estar vacío.")

            with col2:
                if st.button("Cancelar", key="cancel_add", use_container_width=True):
                    st.session_state.add_modal = False
                    st.rerun()


    # Si no hay modales activos, mostrar la lista de categorías
    else:
        # Botón para agregar categoría (centrado)
        col1, col2, col3 = st.columns([3, 2, 2])
        with col1:
            if st.button("+ Agregar nueva categoría", key="add_category_button", use_container_width=True):
                st.session_state.add_modal = True
                st.rerun()
        
        # Separador visual después del botón
        st.markdown("<hr>", unsafe_allow_html=True)
        
        # Obtener categorías desde la base de datos
        categories = get_categories()

        if not categories:
            st.info("No hay categorías disponibles. ¡Agrega una nueva!")
        else:
            # Contenedor principal para categorías
            for category in categories:
                col1, col2, col3 = st.columns([5, 1, 1])

                with col1:
                    st.markdown(f"<div class='category-name'>{category['name']}</div>", unsafe_allow_html=True)

                with col2:
                    if st.button("Editar", key=f"edit_{category['id']}", use_container_width=True):
                        st.session_state.edit_modal = True
                        st.session_state.edit_category = category['name']
                        st.session_state.edit_category_id = category['id']
                        st.rerun()

                with col3:
                    if st.button("Eliminar", key=f"delete_{category['id']}", use_container_width=True):
                        st.session_state.delete_modal = True
                        st.session_state.delete_category = category['name']
                        st.session_state.delete_category_id = category['id']
                        st.rerun()

                # Línea divisoria
                # st.markdown("<hr class='category-divider'>", unsafe_allow_html=True)
