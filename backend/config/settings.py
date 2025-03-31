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
        return {
            "host": os.getenv("DB_HOST", "localhost"),
            "port": int(os.getenv("DB_PORT", "5432")),
            "dbname": os.getenv("DB_NAME", "repolit"),
            "user": os.getenv("DB_USER", "postgres"),
            "password": os.getenv("DB_PASSWORD", ""),
        }

# Valores de configuración
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
APP_NAME = os.getenv("APP_NAME", "Repolit")