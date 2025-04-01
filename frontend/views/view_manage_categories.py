import streamlit as st
from backend.auth.auth_service import is_authenticated, get_current_user, is_admin

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
    with st.sidebar:
        st.title(f"Bienvenido, {user['name']}")

        # Opciones de navegación para usuarios autenticados
        opciones = [
            "Todas las publicaciones",
            "Crear nueva publicación",
            "Ir a la página pública",
            "Cerrar sesión",
        ]

        # Añadir opción de gestionar categorías (ya la tenemos, pero la resaltamos como activa)
        opciones.insert(2, "Gestionar categorías")

        # Usar índice para marcar la opción actual como seleccionada
        index = opciones.index("Gestionar categorías")
        opcion = st.radio("Opciones:", opciones, index=index)

        # Navegación basada en la selección
        if opcion == "Todas las publicaciones":
            st.session_state.vista = "private_general"
            st.rerun()
        elif opcion == "Crear nueva publicación":
            st.session_state.vista = "create_publication"
            st.rerun()
        elif opcion == "Ir a la página pública":
            st.session_state.vista = "public_apps"
            st.rerun()
        elif opcion == "Cerrar sesión":
            st.session_state.vista = "logout"
            st.rerun()

    # Inicializar estados para modales
    if 'edit_modal' not in st.session_state:
        st.session_state.edit_modal = False
        st.session_state.edit_category = ""

    if 'delete_modal' not in st.session_state:
        st.session_state.delete_modal = False
        st.session_state.delete_category = ""

    if 'add_modal' not in st.session_state:
        st.session_state.add_modal = False

    # Título y descripción
    st.title("Gestión de Categorías")
    st.write("Administra las categorías disponibles para clasificar las publicaciones.")

    # Mostrar modales si están activos
    if st.session_state.edit_modal:
        st.markdown("### Editar categoría")
        with st.container():
            st.markdown(f"<div class='modal-section'>", unsafe_allow_html=True)
            new_category_name = st.text_input(
                "Nombre de la categoría", 
                value=st.session_state.edit_category,
                key="edit_category_input"
            )

            col1, col2 = st.columns(2)
            with col1:
                if st.button("Guardar cambios", key="save_edit", use_container_width=True):
                    st.success(f"Categoría actualizada: {new_category_name}")
                    st.session_state.edit_modal = False
                    st.rerun()

            with col2:
                if st.button("Cancelar", key="cancel_edit", use_container_width=True):
                    st.session_state.edit_modal = False
                    st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

    elif st.session_state.delete_modal:
        st.markdown("### Confirmar eliminación")
        with st.container():
            st.markdown(f"<div class='modal-section'>", unsafe_allow_html=True)
            st.write(f"¿Está seguro de que desea eliminar la categoría **{st.session_state.delete_category}**?")

            col1, col2 = st.columns(2)
            with col1:
                if st.button("Eliminar", key="confirm_delete", use_container_width=True):
                    st.error(f"Categoría eliminada: {st.session_state.delete_category}")
                    st.session_state.delete_modal = False
                    st.rerun()

            with col2:
                if st.button("Cancelar", key="cancel_delete", use_container_width=True):
                    st.session_state.delete_modal = False
                    st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

    elif st.session_state.add_modal:
        st.markdown("### Agregar nueva categoría")
        with st.container():
            st.markdown(f"<div class='modal-section'>", unsafe_allow_html=True)
            new_category = st.text_input("Nombre de la categoría", key="new_category_input")

            col1, col2 = st.columns(2)
            with col1:
                if st.button("Agregar", key="confirm_add", use_container_width=True):
                    st.success(f"Nueva categoría agregada: {new_category}")
                    st.session_state.add_modal = False
                    st.rerun()

            with col2:
                if st.button("Cancelar", key="cancel_add", use_container_width=True):
                    st.session_state.add_modal = False
                    st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

    # Si no hay modales activos, mostrar la lista de categorías
    else:
        # Categorías existentes
        categories = [
            "Seguridad en computo",
            "Desarrollo de apps móviles",
            "Inteligencia artificial",
            "Análisis de vulnerabilidades",
            "Redes y conmutadores",
            "Sistemas operativos",
        ]

        # Contenedor principal para categorías
        for category in categories:
            col1, col2, col3 = st.columns([6, 1, 1])

            with col1:
                st.markdown(f"<div class='category-name'>{category}</div>", unsafe_allow_html=True)

            with col2:
                if st.button("Editar", key=f"edit_{category}", use_container_width=True):
                    st.session_state.edit_modal = True
                    st.session_state.edit_category = category
                    st.rerun()

            with col3:
                if st.button("Eliminar", key=f"delete_{category}", use_container_width=True):
                    st.session_state.delete_modal = True
                    st.session_state.delete_category = category
                    st.rerun()

            # Línea divisoria
            st.markdown("<hr class='category-divider'>", unsafe_allow_html=True)

        # Botón para agregar categoría (centrado)
        col1, col2, col3 = st.columns([3, 2, 3])
        with col2:
            if st.button("+ Agregar nueva categoría", key="add_category_button", use_container_width=True):
                st.session_state.add_modal = True
                st.rerun()
