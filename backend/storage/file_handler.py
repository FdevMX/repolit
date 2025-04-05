# Manejo de archivos
import os
import shutil
from pathlib import Path
import streamlit as st
import uuid
import logging
# Importar funciones de Supabase
from backend.storage.supabase_storage import (
    save_file_to_supabase,
    get_file_url,
    delete_file_from_supabase,
)


# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("file_handler")

def save_uploaded_file(file_obj, user_id):
    """Guarda un archivo subido por el usuario."""
    return save_file_to_supabase(file_obj, user_id)

def get_file_path(file_url, is_public=True):
    """Obtiene la ruta de acceso a un archivo."""
    return get_file_url(file_url, is_public)

def delete_file(file_url):
    """Elimina un archivo."""
    return delete_file_from_supabase(file_url)
