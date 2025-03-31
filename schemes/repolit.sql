-- Asegurarse de tener la extensión para generar UUIDs
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Función para actualizar automáticamente el campo updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = CURRENT_TIMESTAMP;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Tabla: users
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4 (),
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    apellidos VARCHAR(255) NOT NULL,
    password_hash TEXT NOT NULL,
    role VARCHAR(50) DEFAULT 'user',
    created_at TIMESTAMP
    WITH
        TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        last_login TIMESTAMP
    WITH
        TIME ZONE
);

-- Tabla: categories
CREATE TABLE categories (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4 (),
    name VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP
    WITH
        TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP
    WITH
        TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Trigger para actualizar updated_at en categories
CREATE TRIGGER update_categories_updated_at
BEFORE UPDATE ON categories
FOR EACH ROW EXECUTE PROCEDURE update_updated_at_column();

-- Tabla: tags
CREATE TABLE tags (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4 (),
    name VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP
    WITH
        TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Tabla: publications
CREATE TABLE publications (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4 (),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    file_url TEXT,
    file_name VARCHAR(255),
    file_type VARCHAR(100),
    file_size INTEGER,
    category_id UUID REFERENCES categories (id),
    user_id UUID REFERENCES users (id),
    created_at TIMESTAMP
    WITH
        TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP
    WITH
        TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Trigger para actualizar updated_at en publications
CREATE TRIGGER update_publications_updated_at
BEFORE UPDATE ON publications
FOR EACH ROW EXECUTE PROCEDURE update_updated_at_column();

-- Tabla: publication_tags (Relación muchos a muchos)
CREATE TABLE publication_tags (
    publication_id UUID REFERENCES publications (id) ON DELETE CASCADE,
    tag_id UUID REFERENCES tags (id) ON DELETE CASCADE,
    PRIMARY KEY (publication_id, tag_id)
);