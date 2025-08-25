import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

class Config:
    """Configuración base"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'clave-secreta-por-defecto'
    
    # Configuración para MySQL en Docker
    DB_HOST = os.environ.get('DB_HOST') or 'localhost'
    DB_PORT = os.environ.get('DB_PORT') or '3306'
    DB_USER = os.environ.get('DB_USER') or 'alfa_user'
    DB_PASSWORD = os.environ.get('DB_PASSWORD') or 'alfa_password'
    DB_NAME = os.environ.get('DB_NAME') or 'alfa_db'
    
    # Configuración CORS - Orígenes permitidos
    CORS_ORIGINS = [
        "http://localhost:4200",     # Angular dev server
        "http://127.0.0.1:4200",    # Angular dev server (alternativo)
        "http://localhost:3000",     # Otros frameworks de desarrollo
        "http://127.0.0.1:3000",    # Otros frameworks de desarrollo (alternativo)
    ]
    
    # Headers permitidos para CORS
    CORS_ALLOW_HEADERS = [
        'Content-Type',
        'Authorization',
        'Access-Control-Allow-Credentials',
        'Access-Control-Allow-Headers',
        'Access-Control-Allow-Methods',
        'Access-Control-Allow-Origin',
        'X-Requested-With'
    ]
    
    # Métodos HTTP permitidos
    CORS_METHODS = ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS']
    
    # Permitir cookies/credenciales
    CORS_SUPPORTS_CREDENTIALS = True
    
    # URL de conexión a MySQL
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
        'connect_args': {
            'charset': 'utf8mb4'
        }
    }

class DevelopmentConfig(Config):
    """Configuración para desarrollo"""
    DEBUG = True
    
    # CORS más permisivo para desarrollo
    CORS_ORIGINS = [
        "http://localhost:4200",     # Angular dev server
        "http://127.0.0.1:4200",    # Angular dev server (alternativo)
        "http://localhost:3000",     # React/Vue dev servers
        "http://127.0.0.1:3000",    # React/Vue dev servers (alternativo)
        "http://localhost:8080",     # Vue CLI dev server
        "http://127.0.0.1:8080",    # Vue CLI dev server (alternativo)
        "http://localhost:5173",     # Vite dev server
        "http://127.0.0.1:5173",    # Vite dev server (alternativo)
    ]

class ProductionConfig(Config):
    """Configuración para producción"""
    DEBUG = False
    # En producción, usar variables de entorno para credenciales
    DB_HOST = os.environ.get('DB_HOST') or 'mysql'  # Nombre del servicio en Docker
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{Config.DB_USER}:{Config.DB_PASSWORD}@{DB_HOST}:{Config.DB_PORT}/{Config.DB_NAME}"
    )
    
    # CORS restrictivo para producción - solo dominios específicos
    CORS_ORIGINS = [
        # Agregar aquí los dominios de producción cuando estén disponibles
        # "https://alfabroker.com",
        # "https://www.alfabroker.com",
        # "https://app.alfabroker.com",
    ]

class TestingConfig(Config):
    """Configuración para testing"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

# Configuración por defecto
Config = DevelopmentConfig 