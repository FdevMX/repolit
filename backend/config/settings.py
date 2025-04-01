# Configuración y carga de variables de entorno
import os
from dotenv import load_dotenv
import streamlit as st

# Cargar variables de entorno desde .env
load_dotenv()

# Configuración de base de datos PostgreSQL
def get_db_config():
    """
    Obtener la configuración de PostgreSQL desde secrets de Streamlit o variables de entorno.
    """
    try:
        # Intentar obtener desde secrets de Streamlit
        return {
            "host": st.secrets["postgres"]["host"],
            "port": st.secrets["postgres"]["port"],
            "dbname": st.secrets["postgres"]["dbname"],
            "user": st.secrets["postgres"]["user"],
            "password": st.secrets["postgres"]["password"],
        }
    except:
        # Fallback a variables de entorno
        use_database = os.getenv("USE_DATABASE", "false").lower() == "true"
        if not use_database:
            return None
            
        # Verificar que existan las variables requeridas
        required_vars = ["DB_HOST", "DB_PORT", "DB_NAME", "DB_USER", "DB_PASSWORD"]
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        
        if missing_vars:
            raise EnvironmentError(f"Faltan variables de entorno requeridas: {', '.join(missing_vars)}")
            
        return {
            "host": os.getenv("DB_HOST"),
            "port": int(os.getenv("DB_PORT")),
            "dbname": os.getenv("DB_NAME"),
            "user": os.getenv("DB_USER"),
            "password": os.getenv("DB_PASSWORD"),
        }

# Valores de configuración
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
APP_NAME = os.getenv("APP_NAME", "Repolit")