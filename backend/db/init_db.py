# Script para inicializar datos básicos en la base de datos existente
import sys
import os
# Añadir el directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

# Ahora podemos importar usando rutas absolutas
from backend.config.settings import get_db_config
from backend.utils.password_utils import hash_password
import psycopg2

def create_tables():
    """Crea todas las tablas necesarias en la base de datos si no existen."""
    # Obtener la configuración de la base de datos
    config = get_db_config()

    print(f"🔌 Conectando a: {config['host']}:{config['port']}, DB: {config['dbname']}")

    # Conectar a PostgreSQL
    conn = psycopg2.connect(
        host=config["host"],
        port=config["port"],
        dbname=config["dbname"],
        user=config["user"],
        password=config["password"]
    )

    # Lista de tablas que vamos a verificar
    tables_to_check = ['users', 'categories', 'tags', 'publications', 'publication_tags']
    existing_tables = []

    # Verificar qué tablas ya existen
    with conn.cursor() as cur:
        cur.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema='public' AND table_type='BASE TABLE'
        """)
        existing_tables = [row[0] for row in cur.fetchall()]

    print(f"\n🔍 Verificando tablas existentes: {', '.join(existing_tables) if existing_tables else 'ninguna'}")

    # Crear tablas
    with conn.cursor() as cur:
        # Extensión para UUID (siempre intentamos crearla, es idempotente)
        print("\n🧩 Configurando extensiones...")
        cur.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')
        print("✅ Extensión UUID configurada")

        # Función para actualización automática (siempre la actualizamos)
        print("\n⏱️ Configurando función de actualización automática...")
        cur.execute('''
            CREATE OR REPLACE FUNCTION update_updated_at_column()
            RETURNS TRIGGER AS $$
            BEGIN
                NEW.updated_at = CURRENT_TIMESTAMP;
                RETURN NEW;
            END;
            $$ LANGUAGE plpgsql;
        ''')
        print("✅ Función temporal creada")

        # Tabla: users
        if 'users' not in existing_tables:
            print("\n👤 Creando tabla de usuarios...")
            cur.execute('''
                CREATE TABLE users (
                    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                    email VARCHAR(255) UNIQUE NOT NULL,
                    name VARCHAR(255) NOT NULL,
                    apellidos VARCHAR(255) NOT NULL,
                    password_hash TEXT NOT NULL,
                    role VARCHAR(50) DEFAULT 'user',
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                    last_login TIMESTAMP WITH TIME ZONE
                );
            ''')
            print("✅ Tabla users creada")
        else:
            print("ℹ️ La tabla users ya existe, omitiendo...")

        # Tabla: categories
        if 'categories' not in existing_tables:
            print("\n📋 Creando tabla de categorías...")
            cur.execute('''
                CREATE TABLE categories (
                    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                    name VARCHAR(255) UNIQUE NOT NULL,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                );
            ''')

            # Trigger para updated_at en categories
            cur.execute('''
                DROP TRIGGER IF EXISTS update_categories_updated_at ON categories;
                CREATE TRIGGER update_categories_updated_at
                BEFORE UPDATE ON categories
                FOR EACH ROW EXECUTE PROCEDURE update_updated_at_column();
            ''')
            print("✅ Tabla categories y trigger creados")
        else:
            print("ℹ️ La tabla categories ya existe, omitiendo...")
            # Asegurar que el trigger existe
            cur.execute('''
                DROP TRIGGER IF EXISTS update_categories_updated_at ON categories;
                CREATE TRIGGER update_categories_updated_at
                BEFORE UPDATE ON categories
                FOR EACH ROW EXECUTE PROCEDURE update_updated_at_column();
            ''')
            print("✅ Trigger de categories verificado")

        # Tabla: tags
        if 'tags' not in existing_tables:
            print("\n🏷️ Creando tabla de etiquetas...")
            cur.execute(
                """
                CREATE TABLE tags (
                    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                    name VARCHAR(100) UNIQUE NOT NULL,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                );
            """
            )
            print("✅ Tabla tags creada")
        else:
            print("ℹ️ La tabla tags ya existe, omitiendo...")

        # Tabla: publications
        if 'publications' not in existing_tables:
            print("\n📄 Creando tabla de publicaciones...")
            cur.execute(
                """
                CREATE TABLE publications (
                    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                    title VARCHAR(255) NOT NULL,
                    description TEXT,
                    file_url TEXT,
                    file_name VARCHAR(255),
                    file_type VARCHAR(100),
                    file_size BIGINT,
                    category_id UUID REFERENCES categories(id),
                    user_id UUID REFERENCES users(id),
                    is_featured BOOLEAN DEFAULT FALSE,
                    is_public BOOLEAN DEFAULT TRUE,
                    is_external BOOLEAN DEFAULT FALSE,
                    media_type VARCHAR(50),
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                );
            """
            )

            # Trigger para updated_at en publications
            cur.execute('''
                DROP TRIGGER IF EXISTS update_publications_updated_at ON publications;
                CREATE TRIGGER update_publications_updated_at
                BEFORE UPDATE ON publications
                FOR EACH ROW EXECUTE PROCEDURE update_updated_at_column();
            ''')
            print("✅ Tabla publications y trigger creados")
        else:
            print("ℹ️ La tabla publications ya existe, omitiendo...")
            # Asegurar que el trigger existe
            cur.execute('''
                DROP TRIGGER IF EXISTS update_publications_updated_at ON publications;
                CREATE TRIGGER update_publications_updated_at
                BEFORE UPDATE ON publications
                FOR EACH ROW EXECUTE PROCEDURE update_updated_at_column();
            ''')
            print("✅ Trigger de publications verificado")

        # Tabla: publication_tags
        if 'publication_tags' not in existing_tables:
            print("\n🔗 Creando tabla de relaciones entre publicaciones y etiquetas...")
            cur.execute('''
                CREATE TABLE publication_tags (
                    publication_id UUID REFERENCES publications(id) ON DELETE CASCADE,
                    tag_id UUID REFERENCES tags(id) ON DELETE CASCADE,
                    PRIMARY KEY (publication_id, tag_id)
                );
            ''')
            print("✅ Tabla publication_tags creada")
        else:
            print("ℹ️ La tabla publication_tags ya existe, omitiendo...")

        # Confirmar los cambios
        conn.commit()

    # Verificar nuevamente qué tablas existen ahora
    with conn.cursor() as cur:
        cur.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema='public' AND table_type='BASE TABLE'
        """)
        existing_tables = [row[0] for row in cur.fetchall()]

        # Verificar si todas las tablas necesarias existen
        all_tables_exist = all(table in existing_tables for table in tables_to_check)

        if all_tables_exist:
            print("\n✅ Todas las tablas necesarias están disponibles")
        else:
            missing = [table for table in tables_to_check if table not in existing_tables]
            print(f"\n⚠️ Advertencia: Faltan algunas tablas: {', '.join(missing)}")

    conn.close()

def insert_initial_data():
    """Inserta datos iniciales en la base de datos."""
    # Obtener la configuración de la base de datos
    config = get_db_config()
    
    print(f"🔌 Conectando a: {config['host']}:{config['port']}, DB: {config['dbname']}")
    
    # Conectar a PostgreSQL
    conn = psycopg2.connect(
        host=config["host"],
        port=config["port"],
        dbname=config["dbname"],
        user=config["user"],
        password=config["password"]
    )
    
    # Insertar categorías iniciales
    with conn.cursor() as cur:
        print("\n📋 Verificando categorías...")
        # Verificar si ya hay categorías
        cur.execute("SELECT COUNT(*) FROM categories")
        count = cur.fetchone()[0]
        
        if count == 0:
            # Insertar categorías
            categories = [
                "Seguridad en computo",
                "Desarrollo de apps móviles",
                "Inteligencia artificial",
                "Análisis de vulnerabilidades",
                "Redes y conmutadores",
                "Sistemas operativos"
            ]
            
            for category in categories:
                cur.execute(
                    "INSERT INTO categories (name) VALUES (%s)",
                    (category,)
                )
            
            print(f"✅ {len(categories)} categorías iniciales insertadas correctamente")
        else:
            print(f"ℹ️ Ya existen {count} categorías en la base de datos")
        
        print("\n🏷️ Verificando etiquetas...")
        # Verificar si ya hay etiquetas
        cur.execute("SELECT COUNT(*) FROM tags")
        count = cur.fetchone()[0]
        
        if count == 0:
            # Insertar tags
            tags = [
                "Redes", "Cisco", "IA", "VSCode", "HTML", "Javascript", 
                "Enrutamiento", "Switching", "LAN", "Programación", 
                "Python", "Windows", "Linux", "MacOS"
            ]
            
            for tag in tags:
                cur.execute(
                    "INSERT INTO tags (name) VALUES (%s)",
                    (tag,)
                )
            
            print(f"✅ {len(tags)} etiquetas iniciales insertadas correctamente")
        else:
            print(f"ℹ️ Ya existen {count} etiquetas en la base de datos")
        
        # Confirmar los cambios
        conn.commit()
    
    conn.close()

# Función opcional para crear un usuario administrador inicial
def create_admin_user(email="admin@repolit.com", name="Admin", apellidos="Sistema", password="admin123"):
    """Crea un usuario administrador si no existe ningún admin."""
    print("\n👤 Verificando usuario administrador...")
    
    config = get_db_config()
    conn = psycopg2.connect(
        host=config["host"],
        port=config["port"],
        dbname=config["dbname"],
        user=config["user"],
        password=config["password"]
    )
    
    with conn.cursor() as cur:
        # Verificar si ya hay algún usuario administrador
        cur.execute("SELECT COUNT(*) FROM users WHERE role = 'admin'")
        count = cur.fetchone()[0]
        
        if count == 0:
            # Hash de la contraseña
            password_hash = hash_password(password)
            
            # Insertar usuario administrador
            cur.execute("""
                INSERT INTO users (id, email, name, apellidos, password_hash, role)
                VALUES (uuid_generate_v4(), %s, %s, %s, %s, 'admin')
            """, (email, name, apellidos, password_hash))
            
            conn.commit()
            print(f"✅ Usuario administrador creado: {email}")
        else:
            print(f"ℹ️ Ya existe al menos un usuario administrador")
    
    conn.close()

if __name__ == "__main__":
    print("\n🚀 ==== INICIALIZACIÓN DE DATOS BÁSICOS ==== 🚀\n")
    
    # Crear tablas
    create_tables()
    
    # Insertar datos iniciales
    insert_initial_data()
    
    # Crear usuario administrador
    create_admin_user()
    
    print("\n✨ Inicialización completada con éxito ✨\n")
