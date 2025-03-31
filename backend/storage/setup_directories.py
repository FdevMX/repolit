# Script para crear la estructura de directorios para archivos subidos
import os

def create_files_directory():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    files_dir = os.path.join(base_dir, 'files')
    
    if not os.path.exists(files_dir):
        os.makedirs(files_dir)
        print(f"Directorio 'files' creado en: {files_dir}")
    else:
        print(f"El directorio 'files' ya existe en: {files_dir}")

if __name__ == "__main__":
    create_files_directory()