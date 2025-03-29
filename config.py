# config.py

class Config:
    """Base configuration class."""
    SECRET_KEY = 'your_secret_key_here'
    DEBUG = False
    TESTING = False
    DATABASE_URI = 'sqlite:///your_database.db'  # Example for SQLite

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    DATABASE_URI = 'sqlite:///dev_database.db'

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    DATABASE_URI = 'sqlite:///test_database.db'

class ProductionConfig(Config):
    """Production configuration."""
    DATABASE_URI = 'postgresql://user:password@localhost/prod_database'  # Example for PostgreSQL

# You can add more configurations as needed based on your environment.