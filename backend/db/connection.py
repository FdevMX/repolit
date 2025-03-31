# Conexión a PostgreSQL
import psycopg2
from psycopg2.extras import RealDictCursor
import streamlit as st
from ..config.settings import get_db_config

@st.cache_resource
def get_db_connection():
    """
    Obtiene una conexión a la base de datos PostgreSQL.
    La conexión se almacena en caché para evitar múltiples conexiones.
    
    Returns:
        connection: Conexión a PostgreSQL
    """
    config = get_db_config()
    try:
        conn = psycopg2.connect(
            host=config["host"],
            port=config["port"],
            dbname=config["dbname"],
            user=config["user"],
            password=config["password"],
            cursor_factory=RealDictCursor  # Para obtener resultados como diccionarios
        )
        return conn
    except Exception as e:
        st.error(f"Error al conectar a PostgreSQL: {e}")
        raise

def execute_query(query, params=None, fetchone=False, commit=False):
    """
    Ejecuta una consulta SQL y devuelve los resultados.
    
    Args:
        query (str): Consulta SQL a ejecutar
        params (tuple, opcional): Parámetros para la consulta
        fetchone (bool, opcional): Si es True, devuelve solo el primer resultado
        commit (bool, opcional): Si es True, hace commit de los cambios
        
    Returns:
        list or dict: Resultados de la consulta
    """
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(query, params)
            
            if commit:
                conn.commit()
                return True
                
            if fetchone:
                return cur.fetchone()
            return cur.fetchall()
    except Exception as e:
        if commit:
            conn.rollback()
        st.error(f"Error en la consulta: {e}")
        raise

def test_connection():
    """
    Prueba la conexión a PostgreSQL.
    
    Returns:
        bool: True si la conexión es exitosa, False en caso contrario
    """
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            cur.execute("SELECT 1")
            result = cur.fetchone()
        print("Conexión exitosa a PostgreSQL")
        return True
    except Exception as e:
        print(f"Error al conectar a PostgreSQL: {e}")
        return False

if __name__ == "__main__":
    test_connection()