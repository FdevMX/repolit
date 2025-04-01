import streamlit as st


def text_input_custom(label, type="default", key=None):
    """
    Componente personalizado para inputs de texto o password.
    """
    if type == "password":
        return st.text_input(label, type="password", key=key)
    else:
        return st.text_input(label, key=key)


def button_custom(label, key=None):
    """
    Componente personalizado para botones.
    """
    return st.button(label, key=key)

def edit_button(label, id=None, use_container_width=False):
    """
    Componente para botones de edición (amarillo).
    Usa el prefijo 'edit_' en la key para aplicar los estilos CSS.
    """
    # Asegura que la key comience con 'edit_' para que el CSS funcione
    key = f"edit_{id}" if id else f"edit_button_{label.lower().replace(' ', '_')}"
    return st.button(label, key=key, use_container_width=use_container_width)

def delete_button(label, id=None, use_container_width=False):
    """
    Componente para botones de eliminación (rojo).
    Usa el prefijo 'delete_' en la key para aplicar los estilos CSS.
    """
    key = f"delete_{id}" if id else f"delete_button_{label.lower().replace(' ', '_')}"
    return st.button(label, key=key, use_container_width=use_container_width)

def add_button(label, use_container_width=False):
    """
    Componente para botones de añadir (verde).
    """
    return st.button(label, key="add_category_button", use_container_width=use_container_width)

# Componentes adicionales para formularios
def form_container(content_func):
    """
    Contenedor para formularios con estilo consistente.
    """
    with st.container():
        with st.markdown(
            """
        <div style="
            background-color: #FBD8FD;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        ">
        """,
            unsafe_allow_html=True,
        ):
            content_func()
        st.markdown("</div>", unsafe_allow_html=True)
