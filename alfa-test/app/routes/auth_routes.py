from flask import Blueprint, request, jsonify
from flasgger import swag_from
from app.services.auth_service import AuthService

auth_bp = Blueprint('auth', __name__, url_prefix='/api')

@auth_bp.route('/auth/agente/login', methods=['POST'])
@swag_from({
    'tags': ['Autenticación'],
    'summary': 'Login de agente',
    'description': 'Autenticar un agente y obtener token JWT',
    'parameters': [
        {
            'name': 'credentials',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'required': ['usuario', 'password'],
                'properties': {
                    'usuario': {
                        'type': 'string',
                        'description': 'Nombre de usuario del agente',
                        'example': 'juan.perez'
                    },
                    'password': {
                        'type': 'string',
                        'description': 'Contraseña del agente',
                        'example': 'mi_password_seguro'
                    }
                }
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Login exitoso',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {
                        'type': 'boolean',
                        'example': True
                    },
                    'message': {
                        'type': 'string',
                        'example': 'Login exitoso'
                    },
                    'data': {
                        'type': 'object',
                        'properties': {
                            'agente': {
                                'type': 'object',
                                'properties': {
                                    'id': {'type': 'integer', 'example': 1},
                                    'nombre': {'type': 'string', 'example': 'Juan Pérez'},
                                    'correo': {'type': 'string', 'example': 'juan.perez@davivienda.com'},
                                    'usuario': {'type': 'string', 'example': 'juan.perez'},
                                    'rol': {'type': 'string', 'example': 'agente'},
                                    'activo': {'type': 'boolean', 'example': True},
                                    'fecha_creacion': {'type': 'string', 'format': 'date-time'}
                                }
                            },
                            'token': {
                                'type': 'string',
                                'example': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...'
                            },
                            'expires_in': {
                                'type': 'integer',
                                'example': 86400,
                                'description': 'Tiempo de expiración del token en segundos'
                            }
                        }
                    }
                }
            }
        },
        400: {
            'description': 'Datos faltantes o inválidos',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean', 'example': False},
                    'message': {'type': 'string', 'example': 'Usuario y contraseña son requeridos'}
                }
            }
        },
        401: {
            'description': 'Credenciales incorrectas',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean', 'example': False},
                    'message': {'type': 'string', 'example': 'Usuario no encontrado'}
                }
            }
        },
        500: {
            'description': 'Error interno del servidor'
        }
    }
})
def login_agente():
    """Login de agente"""
    try:
        data = request.get_json()
        
        # Validar datos requeridos
        if not data:
            return jsonify({
                'success': False,
                'message': 'No se proporcionaron datos'
            }), 400
        
        usuario = data.get('usuario')
        password = data.get('password')
        
        if not usuario or not password:
            return jsonify({
                'success': False,
                'message': 'Usuario y contraseña son requeridos'
            }), 400
        
        # Autenticar agente
        success, auth_data, message = AuthService.authenticate_agente(usuario, password)
        
        if success:
            return jsonify({
                'success': True,
                'message': message,
                'data': auth_data
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': message
            }), 401
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error interno del servidor: {str(e)}'
        }), 500

@auth_bp.route('/auth/cliente/login', methods=['POST'])
@swag_from({
    'tags': ['Autenticación'],
    'summary': 'Login de cliente',
    'description': 'Autenticar un cliente y obtener token JWT',
    'parameters': [
        {
            'name': 'credentials',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'required': ['usuario', 'password'],
                'properties': {
                    'usuario': {
                        'type': 'string',
                        'description': 'Nombre de usuario del cliente',
                        'example': 'maria.gonzalez'
                    },
                    'password': {
                        'type': 'string',
                        'description': 'Contraseña del cliente',
                        'example': 'mi_password_seguro'
                    }
                }
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Login exitoso',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {
                        'type': 'boolean',
                        'example': True
                    },
                    'message': {
                        'type': 'string',
                        'example': 'Login exitoso'
                    },
                    'data': {
                        'type': 'object',
                        'properties': {
                            'cliente': {
                                'type': 'object',
                                'properties': {
                                    'id': {'type': 'integer', 'example': 1},
                                    'tipo_cliente': {'type': 'string', 'example': 'PERSONA'},
                                    'usuario': {'type': 'string', 'example': 'maria.gonzalez'},
                                    'nombre': {'type': 'string', 'example': 'María González'},
                                    'razon_social': {'type': 'string', 'example': 'Empresa ABC S.A.S.'},
                                    'correo': {'type': 'string', 'example': 'maria@ejemplo.com'},
                                    'telefono_movil': {'type': 'string', 'example': '3001234567'},
                                    'ciudad': {'type': 'string', 'example': 'Bogotá'},
                                    'direccion': {'type': 'string', 'example': 'Calle 123 #45-67'},
                                    'fecha_creacion': {'type': 'string', 'format': 'date-time'}
                                }
                            },
                            'token': {
                                'type': 'string',
                                'example': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...'
                            },
                            'expires_in': {
                                'type': 'integer',
                                'example': 86400,
                                'description': 'Tiempo de expiración del token en segundos'
                            }
                        }
                    }
                }
            }
        },
        400: {
            'description': 'Datos faltantes o inválidos',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean', 'example': False},
                    'message': {'type': 'string', 'example': 'Usuario y contraseña son requeridos'}
                }
            }
        },
        401: {
            'description': 'Credenciales incorrectas',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean', 'example': False},
                    'message': {'type': 'string', 'example': 'Usuario no encontrado'}
                }
            }
        },
        500: {
            'description': 'Error interno del servidor'
        }
    }
})
def login_cliente():
    """Login de cliente"""
    try:
        data = request.get_json()
        
        # Validar datos requeridos
        if not data:
            return jsonify({
                'success': False,
                'message': 'No se proporcionaron datos'
            }), 400
        
        usuario = data.get('usuario')
        password = data.get('password')
        
        if not usuario or not password:
            return jsonify({
                'success': False,
                'message': 'Usuario y contraseña son requeridos'
            }), 400
        
        # Autenticar cliente
        success, auth_data, message = AuthService.authenticate_cliente(usuario, password)
        
        if success:
            return jsonify({
                'success': True,
                'message': message,
                'data': auth_data
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': message
            }), 401
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error interno del servidor: {str(e)}'
        }), 500

@auth_bp.route('/auth/token/refresh', methods=['POST'])
@swag_from({
    'tags': ['Autenticación'],
    'summary': 'Renovar token JWT',
    'description': 'Renovar un token JWT próximo a expirar',
    'parameters': [
        {
            'name': 'token_data',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'required': ['token'],
                'properties': {
                    'token': {
                        'type': 'string',
                        'description': 'Token JWT actual',
                        'example': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...'
                    }
                }
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Token renovado exitosamente',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean', 'example': True},
                    'message': {'type': 'string', 'example': 'Token renovado exitosamente'},
                    'token': {'type': 'string', 'example': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...'},
                    'expires_in': {'type': 'integer', 'example': 86400}
                }
            }
        },
        400: {
            'description': 'Token inválido o no necesita renovación'
        },
        500: {
            'description': 'Error interno del servidor'
        }
    }
})
def refresh_token():
    """Renovar token JWT"""
    try:
        data = request.get_json()
        
        if not data or not data.get('token'):
            return jsonify({
                'success': False,
                'message': 'Token es requerido'
            }), 400
        
        token = data.get('token')
        success, new_token, message = AuthService.refresh_token(token)
        
        if success:
            return jsonify({
                'success': True,
                'message': message,
                'token': new_token,
                'expires_in': AuthService.JWT_EXPIRATION_HOURS * 3600
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': message
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error interno del servidor: {str(e)}'
        }), 500

@auth_bp.route('/auth/token/decode', methods=['POST'])
@swag_from({
    'tags': ['Autenticación'],
    'summary': 'Decodificar token JWT',
    'description': 'Decodificar y validar un token JWT (útil para debugging)',
    'parameters': [
        {
            'name': 'token_data',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'required': ['token'],
                'properties': {
                    'token': {
                        'type': 'string',
                        'description': 'Token JWT a decodificar',
                        'example': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...'
                    }
                }
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Token decodificado exitosamente',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean', 'example': True},
                    'message': {'type': 'string', 'example': 'Token válido'},
                    'payload': {
                        'type': 'object',
                        'properties': {
                            'user_id': {'type': 'integer', 'example': 1},
                            'user_type': {'type': 'string', 'example': 'agente'},
                            'usuario': {'type': 'string', 'example': 'juan.perez'},
                            'nombre': {'type': 'string', 'example': 'Juan Pérez'},
                            'correo': {'type': 'string', 'example': 'juan.perez@davivienda.com'},
                            'rol': {'type': 'string', 'example': 'agente'},
                            'iat': {'type': 'integer', 'description': 'Timestamp de emisión'},
                            'exp': {'type': 'integer', 'description': 'Timestamp de expiración'}
                        }
                    }
                }
            }
        },
        400: {
            'description': 'Token inválido o expirado'
        },
        500: {
            'description': 'Error interno del servidor'
        }
    }
})
def decode_token():
    """Decodificar token JWT"""
    try:
        data = request.get_json()
        
        if not data or not data.get('token'):
            return jsonify({
                'success': False,
                'message': 'Token es requerido'
            }), 400
        
        token = data.get('token')
        payload = AuthService.decode_token(token)
        
        return jsonify({
            'success': True,
            'message': 'Token válido',
            'payload': payload
        }), 200
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error interno del servidor: {str(e)}'
        }), 500 