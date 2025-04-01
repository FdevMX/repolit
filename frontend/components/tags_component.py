# NO SE ESTA USANDO, SOLO ES DE PRUEBA PARA COMPONENTE DE TAGS PERSONALIZADOS
# Este componente se puede usar para mostrar etiquetas personalizadas en Streamlit.

import streamlit as st

def tags_component(tags):
    st.markdown(
        f"""
        <div style="background-color: #FBD8FD; border-radius: 10px; padding: 0.5rem; margin-bottom: 0.5rem; text-align: center;">
            <span style="color: #000; font-weight: bold;">{tags}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
