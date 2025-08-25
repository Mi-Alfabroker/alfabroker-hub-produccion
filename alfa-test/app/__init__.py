from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flasgger import Swagger
from app.config import Config

# Inicializar extensiones
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Configuración de Swagger
    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": 'apispec_1',
                "route": '/apispec_1.json',
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/docs/"
    }
    
    swagger_template = {
        "swagger": "2.0",
        "info": {
            "title": "API de Seguros Davivienda",
            "description": "API RESTful para gestión de agentes, clientes, bienes asegurables y seguros",
            "version": "1.0.0",
            "contact": {
                "name": "Equipo de Desarrollo",
                "email": "desarrollo@davivienda.com"
            }
        },
        "host": "localhost:5000",
        "basePath": "/api",
        "schemes": ["http"],
        "consumes": ["application/json"],
        "produces": ["application/json"],
        "tags": [
            {
                "name": "Health",
                "description": "Endpoints de verificación de estado"
            },
            {
                "name": "Autenticación",
                "description": "Endpoints de autenticación y manejo de tokens JWT"
            },
            {
                "name": "Agentes",
                "description": "Gestión de agentes de seguros"
            },
            {
                "name": "Clientes",
                "description": "Gestión de clientes"
            },
            {
                "name": "Bienes",
                "description": "Gestión de bienes asegurables"
            },
            {
                "name": "Asignaciones",
                "description": "Gestión de asignaciones agente-cliente"
            },
            {
                "name": "Aseguradoras",
                "description": "Gestión de compañías aseguradoras y sus productos"
            },
            {
                "name": "Opciones de Seguro",
                "description": "Gestión de cotizaciones y opciones de seguro"
            },
            {
                "name": "Pólizas",
                "description": "Gestión de pólizas de seguro y pagos"
            }
        ]
    }
    
    # Configurar CORS
    CORS(app, 
         origins=app.config['CORS_ORIGINS'],
         allow_headers=app.config['CORS_ALLOW_HEADERS'],
         methods=app.config['CORS_METHODS'],
         supports_credentials=app.config['CORS_SUPPORTS_CREDENTIALS']
    )
    
    # Inicializar extensiones con la app
    db.init_app(app)
    Swagger(app, config=swagger_config, template=swagger_template)
    
    # Importar modelos para que SQLAlchemy los reconozca
    from app.models import (
        Agente, Cliente, AgenteCliente, 
        Bien, Hogar, Vehiculo, Copropiedad, OtroBien, ClienteBien,
        Aseguradora, AseguradoraDeducible, AseguradoraCobertura, AseguradoraFinanciacion,
        OpcionSeguro, OpcionHogar, OpcionVehiculo, OpcionCopropiedad, OpcionOtro,
        Poliza, PolizaPlanPago
    )
    
    # Registrar blueprints
    from app.routes.agente_routes import agente_bp
    from app.routes.cliente_routes import cliente_bp
    from app.routes.asignacion_routes import asignacion_bp
    from app.routes.bien_routes import bien_bp
    from app.routes.aseguradora_routes import aseguradora_bp
    from app.routes.opcion_seguro_routes import opcion_seguro_bp
    from app.routes.poliza_routes import poliza_bp
    from app.routes.auth_routes import auth_bp
    
    app.register_blueprint(agente_bp)
    app.register_blueprint(cliente_bp)
    app.register_blueprint(asignacion_bp)
    app.register_blueprint(bien_bp)
    app.register_blueprint(aseguradora_bp)
    app.register_blueprint(opcion_seguro_bp)
    app.register_blueprint(poliza_bp)
    app.register_blueprint(auth_bp)
    
    # Endpoint de salud y verificación CORS
    @app.route('/api/health', methods=['GET'])
    def health_check():
        """
        Endpoint de verificación de estado de la API
        ---
        tags:
          - Health
        responses:
          200:
            description: API funcionando correctamente
            schema:
              type: object
              properties:
                status:
                  type: string
                  example: "success"
                message:
                  type: string
                  example: "API de Seguros funcionando correctamente"
                cors_enabled:
                  type: boolean
                  example: true
                allowed_origins:
                  type: array
                  items:
                    type: string
                  example: ["http://localhost:4200"]
        """
        return {
            "status": "success",
            "message": "API de Seguros funcionando correctamente",
            "cors_enabled": True,
            "allowed_origins": app.config.get('CORS_ORIGINS', []),
            "timestamp": "2024-01-01T00:00:00Z"
        }, 200
    
    # No crear tablas automáticamente - ya existen en MySQL
    # Las tablas se crean mediante el script database/init.sql
    
    return app 