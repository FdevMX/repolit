# Archivo para probar la conexión a PostgreSQL
import sys
import os
# Añadir el directorio raíz al path para importar correctamente los módulos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from backend.config.settings import get_db_config
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor

# Cargar variables de entorno
load_dotenv()

def test_postgres_connection():
    """Prueba la conexión directa a PostgreSQL"""
    try:
        # Obtener configuración desde el módulo centralizado
        config = get_db_config()

        # Intentar la conexión
        print(
            f"Conectando a PostgreSQL en {config['host']}:{config['port']}, DB: {config['dbname']}, Usuario: {config['user']}"
        )
        conn = psycopg2.connect(
            host=config["host"],
            port=config["port"],
            dbname=config["dbname"],
            user=config["user"],
            password=config["password"],
            cursor_factory=RealDictCursor,
        )

        print("✅ Conexión exitosa a PostgreSQL!")

        # Probar si existen las tablas necesarias
        with conn.cursor() as cur:
            cur.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema='public'
            """)
            tables = [record['table_name'] for record in cur.fetchall()]

            expected_tables = ['users', 'categories', 'tags', 'publications', 'publication_tags']
            missing_tables = [table for table in expected_tables if table not in tables]

            if missing_tables:
                print(f"❌ Faltan las siguientes tablas: {', '.join(missing_tables)}")
            else:
                print("✅ Todas las tablas necesarias existen!")

            # Verificar categorías
            if 'categories' in tables:
                cur.execute("SELECT COUNT(*) as count FROM categories")
                count = cur.fetchone()['count']
                print(f"👉 Hay {count} categorías en la base de datos.")

            # Verificar etiquetas
            if 'tags' in tables:
                cur.execute("SELECT COUNT(*) as count FROM tags")
                count = cur.fetchone()['count']
                print(f"👉 Hay {count} etiquetas en la base de datos.")

            # Verificar usuarios
            if 'users' in tables:
                cur.execute("SELECT COUNT(*) as count FROM users")
                count = cur.fetchone()['count']
                print(f"👉 Hay {count} usuarios en la base de datos.")

        conn.close()
        return True

    except Exception as e:
        print(f"❌ Error al conectar a PostgreSQL: {e}")
        return False

if __name__ == "__main__":
    print("\n==== PRUEBA DE CONEXIÓN A POSTGRESQL ====\n")
    test_postgres_connection()
    print("\n========================================\n")
