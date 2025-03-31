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
