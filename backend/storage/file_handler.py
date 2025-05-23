# Manejo de archivos
import os
import shutil
from pathlib import Path
import streamlit as st
import uuid
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("file_handler")

def ensure_files_directory():
    """Asegura que el directorio de files exista."""
    files_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'files')
    if not os.path.exists(files_dir):
        os.makedirs(files_dir)
        logger.info(f"Directorio 'files' creado en: {files_dir}")
    return files_dir

def save_uploaded_file(uploaded_file, user_id):
    """
    Guarda un archivo subido por el usuario en la estructura de carpetas.
    
    Args:
        uploaded_file: El objeto de archivo de Streamlit
        user_id: UUID del usuario que sube el archivo
        
    Returns:
        dict: Información del archivo guardado incluyendo URL, nombre, tipo y tamaño
    """
    if uploaded_file is None:
        logger.warning("Se intentó guardar un archivo None")
        return None
    
    try:
        # Crear la carpeta para el usuario si no existe
        files_dir = ensure_files_directory()
        user_dir = os.path.join(files_dir, str(user_id))
        
        if not os.path.exists(user_dir):
            os.makedirs(user_dir)
            logger.info(f"Directorio para usuario {user_id} creado")
        
        # Generar un nombre único para el archivo
        file_extension = Path(uploaded_file.name).suffix
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = os.path.join(user_dir, unique_filename)
        
        # Guardar el archivo
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Crear la URL relativa para acceder al archivo
        relative_path = os.path.join("files", str(user_id), unique_filename)
        
        logger.info(f"Archivo guardado: {relative_path}")
        
        # Devolver información del archivo
        return {
            "file_url": relative_path,
            "file_name": uploaded_file.name,
            "file_type": uploaded_file.type,
            "file_size": uploaded_file.size
        }
    except Exception as e:
        logger.error(f"Error al guardar archivo: {e}")
        return None

def delete_file(file_url):
    """
    Elimina un archivo del sistema de archivos.
    
    Args:
        file_url: URL relativa del archivo a eliminar
        
    Returns:
        bool: True si se eliminó correctamente, False si hubo un error
    """
    try:
        # La URL relativa incluye "files/user_id/filename"
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        file_path = os.path.join(base_dir, file_url)
        
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.info(f"Archivo eliminado: {file_url}")
            return True
        
        logger.warning(f"Archivo no encontrado para eliminar: {file_url}")
        return False
    except Exception as e:
        logger.error(f"Error eliminando archivo {file_url}: {e}")
        return False

def get_file_path(file_url):
    """
    Obtiene la ruta absoluta de un archivo a partir de su URL relativa.
    
    Args:
        file_url: URL relativa del archivo
        
    Returns:
        str: Ruta absoluta del archivo
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    return os.path.join(base_dir, file_url)