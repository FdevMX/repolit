import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Cargar variables de entorno
load_dotenv()

# Configuración de Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Inicializar cliente
supabase: Client = None

def get_supabase_client():
    """Obtiene o inicializa el cliente de Supabase."""
    global supabase
    if supabase is None:
        if not SUPABASE_URL or not SUPABASE_KEY:
            raise ValueError("SUPABASE_URL y SUPABASE_KEY deben estar configurados en el archivo .env")
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    return supabase