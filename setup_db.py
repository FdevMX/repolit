# Archivo setup_db.py mejorado con verificación progresiva
import sys
from backend.db.test_db_connection import test_postgres_connection
from backend.db.init_db import create_tables, insert_initial_data, create_admin_user
from backend.config.settings import get_db_config
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def check_table_data():
    """Comprueba si hay datos en las tablas principales y retorna los resultados."""
    try:
        # Obtener configuración desde el módulo centralizado
        config = get_db_config()

        # Conectar a PostgreSQL
        conn = psycopg2.connect(
            host=config["host"],
            port=config["port"],
            dbname=config["dbname"],
            user=config["user"],
            password=config["password"],
            cursor_factory=RealDictCursor,
        )

        data_status = {
            "categories": 0,
            "tags": 0,
            "users": 0,
            "admin_users": 0
        }

        with conn.cursor() as cur:
            # Verificar categorías
            cur.execute("SELECT COUNT(*) as count FROM categories")
            data_status["categories"] = cur.fetchone()['count']
            print(f"📊 Hay {data_status['categories']} categorías en la base de datos")

            # Verificar etiquetas
            cur.execute("SELECT COUNT(*) as count FROM tags")
            data_status["tags"] = cur.fetchone()['count']
            print(f"📊 Hay {data_status['tags']} etiquetas en la base de datos")

            # Verificar usuarios
            cur.execute("SELECT COUNT(*) as count FROM users")
            data_status["users"] = cur.fetchone()['count']
            print(f"📊 Hay {data_status['users']} usuarios en la base de datos")

            # Verificar usuarios administradores
            cur.execute("SELECT COUNT(*) as count FROM users WHERE role = 'admin'")
            data_status["admin_users"] = cur.fetchone()['count']
            print(f"📊 Hay {data_status['admin_users']} usuarios administradores")

        conn.close()
        return True, data_status
    except Exception as e:
        print(f"❌ Error al verificar datos en tablas: {e}")
        return False, {}


if __name__ == "__main__":
    print("\n🚀 ==== INICIALIZACIÓN Y VERIFICACIÓN DE BASE DE DATOS ==== 🚀\n")

    # Paso 1: Verificar conexión a PostgreSQL
    print("\n📡 Verificando conexión a PostgreSQL...")
    connection_ok = test_postgres_connection()

    if not connection_ok:
        print("\n❌ Error: No se pudo conectar a PostgreSQL.")
        print("📋 Verifica las credenciales en el archivo .env y asegúrate que PostgreSQL esté en ejecución.")
        sys.exit(1)

    # Paso 2: Verificar si existen las tablas necesarias
    print("\n🔍 Verificando estructura de base de datos...")

    # Obtener configuración desde el módulo centralizado
    config = get_db_config()

    # Verificar tablas existentes
    try:
        conn = psycopg2.connect(
            host=config["host"],
            port=config["port"],
            dbname=config["dbname"],
            user=config["user"],
            password=config["password"],
            cursor_factory=RealDictCursor,
        )

        with conn.cursor() as cur:
            cur.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema='public' AND table_type='BASE TABLE'
            """)
            tables = [record['table_name'] for record in cur.fetchall()]

            expected_tables = ['users', 'categories', 'tags', 'publications', 'publication_tags']
            missing_tables = [table for table in expected_tables if table not in tables]

        conn.close()

        if missing_tables:
            print(f"⚠️ Faltan tablas: {', '.join(missing_tables)}")

            # Paso 2.1: Crear tablas faltantes
            print("\n🛠️ Creando tablas faltantes...")
            create_tables()
        else:
            print("✅ Todas las tablas necesarias existen!")

    except Exception as e:
        print(f"❌ Error al verificar tablas: {e}")
        sys.exit(1)

    # Paso 3: Verificar datos en las tablas
    print("\n🔍 Verificando datos existentes...")
    data_check_ok, data_status = check_table_data()

    if not data_check_ok:
        print("❌ Error al verificar datos en las tablas.")
        sys.exit(1)

    # Paso 4: Insertar datos iniciales si es necesario
    if data_status["categories"] == 0 or data_status["tags"] == 0:
        print("\n📥 Insertando datos iniciales...")
        insert_initial_data()
    else:
        print("✅ Ya existen datos básicos en la base de datos.")

    # Paso 5: Crear usuario administrador si no existe
    if data_status["admin_users"] == 0:
        print("\n👤 Creando usuario administrador...")
        create_admin_user()
    else:
        print("✅ Ya existe al menos un usuario administrador.")

    # Paso 6: Verificación final
    print("\n🔍 Realizando verificación final...")
    final_check_ok, final_status = check_table_data()

    if final_check_ok:
        if (final_status["categories"] > 0 and 
            final_status["tags"] > 0 and 
            final_status["admin_users"] > 0):
            print("\n✅ ¡Base de datos inicializada correctamente!")
        else:
            print("\n⚠️ La base de datos no se inicializó completamente.")
    else:
        print("\n❌ Error en la verificación final.")

    print("\n✨ Proceso completado ✨\n")
