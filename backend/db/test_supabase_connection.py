import sys
import os
# Añadir el directorio raíz al path para importar correctamente los módulos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from dotenv import load_dotenv
from supabase import create_client, Client
import os

# Cargar variables de entorno
load_dotenv()

def test_supabase_connection():
    """Prueba la conexión a Supabase"""
    try:
        # Obtener configuración de Supabase desde variables de entorno
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_KEY")
        
        if not supabase_url or not supabase_key:
            print("❌ Error: No se encontraron las variables SUPABASE_URL o SUPABASE_KEY en el archivo .env")
            return False
        
        print(f"Conectando a Supabase: {supabase_url}")
        
        # Crear cliente de Supabase
        supabase: Client = create_client(supabase_url, supabase_key)
        
        # Probar una consulta simple para verificar la conexión
        print("Probando conexión con una consulta simple...")
        
        # Consultar tablas existentes usando la API REST de Supabase
        # Esto es diferente de PostgreSQL directo - usamos select() en vez de SQL raw
        result = supabase.table("categories").select("*").execute()
        
        print("✅ Conexión exitosa a Supabase!")
        
        # Mostrar información de las tablas
        tables_to_check = ['users', 'categories', 'tags', 'publications', 'publication_tags']
        for table in tables_to_check:
            try:
                count_result = supabase.table(table).select("*", count='exact').execute()
                count = len(count_result.data)
                print(f"👉 Hay {count} registros en la tabla {table}.")
            except Exception as table_error:
                print(f"❌ No se pudo acceder a la tabla {table}: {str(table_error)}")
        
        # Prueba de storage
        try:
            bucket_name = os.getenv("SUPABASE_BUCKET")
            bucket_result = supabase.storage.list_buckets()
            print(f"✅ Storage conectado correctamente. Buckets disponibles: {[b['name'] for b in bucket_result]}")
            
            if bucket_name:
                # Verificar si el bucket existe
                if any(b['name'] == bucket_name for b in bucket_result):
                    print(f"✅ El bucket '{bucket_name}' existe.")
                else:
                    print(f"⚠️ El bucket '{bucket_name}' no existe en Supabase.")
        except Exception as storage_error:
            print(f"❌ Error al acceder al storage: {str(storage_error)}")
            
        return True
    
    except Exception as e:
        print(f"❌ Error al conectar a Supabase: {str(e)}")
        return False

if __name__ == "__main__":
    print("\n==== PRUEBA DE CONEXIÓN A SUPABASE ====\n")
    test_supabase_connection()
    print("\n=======================================\n")