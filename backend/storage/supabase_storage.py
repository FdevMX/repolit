import os
import uuid
from dotenv import load_dotenv
from supabase import create_client, Client
from datetime import timedelta

# Cargar variables de entorno
load_dotenv()

# Configuración de Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_BUCKET = os.getenv("SUPABASE_BUCKET", "datelit")

# Inicializar cliente de Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def save_file_to_supabase(file_obj, user_id, original_filename=None):
    """
    Guarda un archivo en Supabase Storage.
    
    Args:
        file_obj: Objeto de archivo (de streamlit)
        user_id: ID del usuario que sube el archivo
        original_filename: Nombre original del archivo (opcional)
        
    Returns:
        dict: Información del archivo guardado o None si hay error
    """
    try:
        # Generar nombre único para el archivo
        filename = original_filename or file_obj.name
        file_extension = os.path.splitext(filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        
        # Estructura de carpetas: user_id/año/mes/archivo
        from datetime import datetime
        now = datetime.now()
        path = f"{user_id}/{now.year}/{now.month}/{unique_filename}"
        
        # Subir archivo a Supabase
        result = supabase.storage.from_(SUPABASE_BUCKET).upload(
            path,
            file_obj.getvalue(),
            file_options={"content-type": file_obj.type}
        )
        
        # Construir URL pública (temporal) para confirmar la subida
        file_url = supabase.storage.from_(SUPABASE_BUCKET).get_public_url(path)
        
        # Devolver información del archivo
        return {
            "file_url": path,  # Guardamos la ruta interna, no la URL completa
            "file_name": filename,
            "file_type": file_obj.type,
            "file_size": len(file_obj.getvalue())
        }
    except Exception as e:
        print(f"Error al subir archivo a Supabase: {str(e)}")
        return None

def get_file_url(file_path, is_public=True, expires_in=3600):
    """
    Obtiene la URL de un archivo en Supabase Storage.
    
    Args:
        file_path: Ruta del archivo en Supabase
        is_public: Si el archivo es público
        expires_in: Tiempo de expiración del link en segundos (para archivos privados)
        
    Returns:
        str: URL del archivo
    """
    try:
        if is_public:
            return supabase.storage.from_(SUPABASE_BUCKET).get_public_url(file_path)
        else:
            # Para archivos privados, generar URL firmada con tiempo de expiración
            return supabase.storage.from_(SUPABASE_BUCKET).create_signed_url(
                file_path, 
                expires_in=expires_in
            )
    except Exception as e:
        print(f"Error al obtener URL del archivo: {str(e)}")
        return None

def delete_file_from_supabase(file_path):
    """Elimina un archivo de Supabase Storage."""
    try:
        supabase.storage.from_(SUPABASE_BUCKET).remove([file_path])
        return True
    except Exception as e:
        print(f"Error al eliminar archivo de Supabase: {str(e)}")
        return False