import streamlit as st
import time

def save_edit_category():
    msg = st.toast("Actualizando categoría...", icon = "🔄")
    time.sleep(2)
    msg.toast(f"Categoría {st.session_state.edit_category} actualizada", icon="✅")
    time.sleep(2)
    msg.toast("Redireccionando a categorias", icon = "🔄")


def confirm_delete_category():
    msg = st.toast("Eliminando categoría...", icon="🔄")
    time.sleep(2)
    msg.toast(f"Categoría {st.session_state.delete_category} eliminada", icon="✅")
    time.sleep(2)
    msg.toast("Redireccionando a categorias", icon="🔄")

def confirm_add_category():
    msg = st.toast("Agregando categoría...", icon="🔄")
    time.sleep(2)
    msg.toast(f"Categoría {st.session_state.new_category_input} agregada", icon="✅")
    time.sleep(2)
    msg.toast("Redireccionando a categorias", icon="🔄")


# Añadimos las funciones para tags
def save_edit_tag():
    msg = st.toast("Actualizando etiqueta...", icon="🔄")
    time.sleep(2)
    msg.toast(f"Etiqueta {st.session_state.edit_tag} actualizada", icon="✅")
    time.sleep(2)
    msg.toast("Redireccionando a etiquetas", icon="🔄")


def confirm_delete_tag():
    msg = st.toast("Eliminando etiqueta...", icon="🔄")
    time.sleep(2)
    msg.toast(f"Etiqueta {st.session_state.delete_tag} eliminada", icon="✅")
    time.sleep(2)
    msg.toast("Redireccionando a etiquetas", icon="🔄")


def confirm_add_tag():
    msg = st.toast("Agregando etiqueta...", icon="🔄")
    time.sleep(2)
    msg.toast(f"Etiqueta {st.session_state.new_tag_input} agregada", icon="✅")
    time.sleep(2)
    msg.toast("Redireccionando a etiquetas", icon="🔄")
