import streamlit as st

def view_create_publication():
    st.markdown("## Crear nueva publicación")
    st.write("")

    # Formulario para crear una nueva publicación
    title = st.text_input("Título")
    description = st.text_area("Descripción")
    category = st.selectbox("Categoría", ["Seguridad en computo", "Desarrollo de apps móviles", "Inteligencia artificial"])
    tags = st.multiselect("Tags", ["Redes", "Cisco", "IA", "VSCode", "HTML", "Javascript"])
    
    # Subida de archivo (ahora a ancho completo sin la opción de enlace)
    file = st.file_uploader("Seleccionar archivo")

    st.write("")  # Espacio antes de los botones
    
    # Botones de acción centrados
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # Contenedor para botones centrados
        button_col1, button_col2 = st.columns(2)
        with button_col1:
            if st.button("Crear publicación", use_container_width=True):
                st.success("Publicación creada exitosamente.")
        with button_col2:
            if st.button("Cancelar publicación", use_container_width=True):
                st.warning("Publicación cancelada.")