import streamlit as st
from frontend.components.card_component import card_component

def view_public_apps():
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