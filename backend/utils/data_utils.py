# Utilidades para manipulación de datos
import os
import json
import uuid
from datetime import datetime, timezone

def ensure_data_directory():
    """Asegura que el directorio data exista para almacenar los archivos JSON."""
    data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data')
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    return data_dir

def load_json(filename):
    """Carga datos desde un archivo JSON."""
    data_dir = ensure_data_directory()
    file_path = os.path.join(data_dir, f"{filename}.json")
    
    if not os.path.exists(file_path):
        # Si el archivo no existe, crear uno vacío
        with open(file_path, 'w') as f:
            json.dump([], f)
        return []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        # Si hay un error al decodificar, devolver una lista vacía
        return []

def save_json(filename, data):
    """Guarda datos en un archivo JSON."""
    data_dir = ensure_data_directory()
    file_path = os.path.join(data_dir, f"{filename}.json")
    
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def generate_uuid():
    """Genera un UUID único."""
    return str(uuid.uuid4())

def get_current_timestamp():
    """Obtiene la marca de tiempo actual en formato ISO."""
    return datetime.now(timezone.utc).isoformat()