# Script para inicializar datos básicos en la base de datos existente
import psycopg2
from ..config.settings import get_db_config

def insert_initial_data():
    """Inserta datos iniciales en la base de datos."""
    # Obtener la configuración de la base de datos
    config = get_db_config()
    
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
            
            print("Categorías iniciales insertadas correctamente")
        else:
            print(f"Ya existen {count} categorías en la base de datos")
        
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
            
            print("Etiquetas iniciales insertadas correctamente")
        else:
            print(f"Ya existen {count} etiquetas en la base de datos")
        
        # Confirmar los cambios
        conn.commit()
    
    conn.close()

# Función opcional para crear un usuario administrador inicial
def create_admin_user(email="admin@repolit.com", name="Admin", apellidos="Sistema", password="admin123"):
    """Crea un usuario administrador si no existe ningún admin."""
    from ..utils.password_utils import hash_password
    
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
                INSERT INTO users (email, name, apellidos, password_hash, role)
                VALUES (%s, %s, %s, %s, 'admin')
            """, (email, name, apellidos, password_hash))
            
            conn.commit()
            print(f"Usuario administrador creado: {email}")
        else:
            print("Ya existe al menos un usuario administrador")
    
    conn.close()

if __name__ == "__main__":
    print("Inicializando datos básicos...")
    insert_initial_data()
    
    # Descomentar si deseas crear un usuario admin
    # create_admin_user()
    
    print("Inicialización completada")