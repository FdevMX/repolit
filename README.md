# Repolit - Repositorio Digital

Repolit es una aplicación web desarrollada con Streamlit que permite gestionar y compartir publicaciones digitales. El sistema cuenta con autenticación de usuarios, gestión de categorías y etiquetas, y soporte para diferentes tipos de archivos.

## Tabla de Contenidos

- [Repolit - Repositorio Digital](#repolit---repositorio-digital)
  - [Tabla de Contenidos](#tabla-de-contenidos)
  - [Características](#características)
  - [Requisitos del Sistema](#requisitos-del-sistema)
  - [Instalación](#instalación)
  - [Configuración](#configuración)
  - [Uso](#uso)
    - [Roles de Usuario](#roles-de-usuario)
      - [Usuario Público](#usuario-público)
      - [Usuario Registrado](#usuario-registrado)
      - [Administrador](#administrador)
  - [Estructura del Proyecto](#estructura-del-proyecto)
  - [Base de Datos](#base-de-datos)
    - [Tablas Principales](#tablas-principales)
    - [Esquema de Datos](#esquema-de-datos)
  - [Funcionalidades](#funcionalidades)
    - [Gestión de Publicaciones](#gestión-de-publicaciones)
    - [Sistema de Filtros](#sistema-de-filtros)
    - [Gestión de Archivos](#gestión-de-archivos)
  - [Licencia](#licencia)

## Características

- 🔐 Autenticación de usuarios
- 📁 Gestión de publicaciones
- 🏷️ Sistema de categorías y etiquetas
- 🔍 Búsqueda y filtrado avanzado
- 📄 Soporte para múltiples tipos de archivo
- 👥 Roles de usuario (admin/usuario)
- 🌐 Vista pública y privada

## Requisitos del Sistema

- Python 3.8 o superior
- PostgreSQL 12 o superior
- pip (gestor de paquetes de Python)
- Navegador web moderno

## Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/fdevmx/repolit.git
cd repolit
```

2. Crear y activar entorno virtual:
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

## Configuración

1. Crear archivo `.env` en la raíz del proyecto:
```env
# Database
DB_HOST=localhost
DB_PORT=5432
DB_NAME=repolit
DB_USER=your_user
DB_PASSWORD=your_password

# App
SECRET_KEY=your_secret_key
UPLOAD_FOLDER=uploads
```

2. Configurar base de datos:
```bash
# Crear base de datos en PostgreSQL
createdb repolit

# Ejecutar script de inicialización
psql -d repolit -f schema.sql
```

## Uso

1. Iniciar la aplicación:
```bash
streamlit run app.py
```

2. Acceder a la aplicación:
- Vista pública: `http://localhost:8501`
- Panel de administración: `http://localhost:8501/?vista=login`

### Roles de Usuario

#### Usuario Público
- Ver publicaciones públicas
- Filtrar por categorías y etiquetas
- Descargar archivos públicos

#### Usuario Registrado
- Crear publicaciones
- Gestionar publicaciones propias
- Acceso a panel personal

#### Administrador
- Gestionar categorías
- Gestionar etiquetas
- Acceso completo al sistema

## Estructura del Proyecto

```
repolit/
├── frontend/
│   ├── views/                 # Vistas de la aplicación
│   │   ├── view_private_general.py    # Panel principal
│   │   ├── view_public_apps.py        # Vista pública
│   │   └── ...
│   └── components/            # Componentes reutilizables
│       ├── sidebar_private_component.py
│       └── sidebar_public_component.py
├── backend/
│   ├── auth/                 # Autenticación
│   ├── data/                 # Acceso a datos
│   ├── storage/              # Gestión de archivos
│   └── db/                   # Conexión a base de datos
└── uploads/                  # Archivos subidos
```

## Base de Datos

### Tablas Principales
- `users`: Gestión de usuarios
- `publications`: Publicaciones
- `categories`: Categorías
- `tags`: Etiquetas
- `publication_tags`: Relación publicaciones-etiquetas

### Esquema de Datos
```sql

-- ...más tablas en schema.sql
```

## Funcionalidades

### Gestión de Publicaciones
- Crear, editar y eliminar publicaciones
- Asignar categorías y etiquetas
- Adjuntar archivos (PDF, imágenes, etc.)
- Marcar como destacado o privado

### Sistema de Filtros
- Búsqueda por título/descripción
- Filtrado por categorías
- Filtrado por etiquetas
- Vista de publicaciones propias

### Gestión de Archivos
- Soporte para múltiples formatos
- Previsualización de imágenes y PDFs
- Sistema de descarga segura
- Almacenamiento organizado

## Licencia

Este proyecto está licenciado bajo GNU v3. Ver archivo LICENSE para más detalles.