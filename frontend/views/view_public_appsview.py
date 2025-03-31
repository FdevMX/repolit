import streamlit as st

def view_public_appsview():
    st.markdown("## Como crear una app responsiva")
    st.write("En este documento se explica detalladamente cómo crear una aplicación responsiva usando HTML, CSS y Javascript como tecnologías principales. También nos enseña cómo usar buenas prácticas y obtener código puro sin errores.")
    st.write("")

    # Etiquetas como pills
    st.markdown("###### Etiquetas")
    tags = ["HTML", "Apps web", "Javascript"]

    # Corregido: añadir el parámetro 'label'
    st.pills(
        label="Etiquetas",
        options=tags, 
        label_visibility="collapsed", 
        key="tags_pills"
    )

    st.markdown("###### Fecha de publicación")
    st.write("29 de noviembre de 2024")
    # Contenido del archivo
    st.markdown("### Contenido del archivo")
    st.write("Contenido del PDF, video, imagen o archivo que se anexa al momento de la publicación.")
