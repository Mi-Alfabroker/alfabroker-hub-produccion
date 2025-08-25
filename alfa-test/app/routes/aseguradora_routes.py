from flask import Blueprint, request, jsonify
from flasgger import swag_from
from app.services.aseguradora_service import AseguradoraService

aseguradora_bp = Blueprint('aseguradora', __name__, url_prefix='/api')

@aseguradora_bp.route('/aseguradoras', methods=['POST'])
@swag_from({
    'tags': ['Aseguradoras'],
    'summary': 'Crear una nueva aseguradora',
    'description': 'Crear una nueva aseguradora con toda su información básica y sublímites',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'required': ['nombre'],
                'properties': {
                    'nombre': {
                        'type': 'string',
                        'description': 'Nombre de la aseguradora',
                        'example': 'Seguros Alfa S.A.'
                    },
                    'numeral_asistencia': {
                        'type': 'string',
                        'description': 'Número de asistencia',
                        'example': '#321'
                    },
                    'correo_comercial': {
                        'type': 'string',
                        'format': 'email',
                        'description': 'Correo comercial',
                        'example': 'comercial@segurosalfa.com'
                    },
                    'correo_reclamaciones': {
                        'type': 'string',
                        'format': 'email',
                        'description': 'Correo para reclamaciones',
                        'example': 'reclamos@segurosalfa.com'
                    },
                    'oficina_direccion': {
                        'type': 'string',
                        'description': 'Dirección de la oficina principal'
                    },
                    'contacto_asignado': {
                        'type': 'string',
                        'description': 'Nombre del contacto asignado'
                    },
                    'logo_url': {
                        'type': 'string',
                        'description': 'URL del logo de la aseguradora'
                    },
                    'comisiones_normales': {
                        'type': 'object',
                        'description': 'Comisiones normales por tipo de póliza',
                        'example': {
                            'HOGAR': 0.20,
                            'VEHICULO': 0.15,
                            'COPROPIEDAD': 0.18,
                            'OTRO': 0.12
                        }
                    },
                    'sobrecomisiones': {
                        'type': 'object',
                        'description': 'Sobrecomisiones por tipo de póliza',
                        'example': {
                            'HOGAR': 0.05,
                            'VEHICULO': 0.02
                        }
                    },
                    'sublimite_rc_veh_bienes_terceros': {
                        'type': 'number',
                        'format': 'float',
                        'description': 'Sublímite RC vehículos bienes terceros'
                    }
                }
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Aseguradora creada exitosamente',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string'},
                    'aseguradora': {
                        'type': 'object',
                        'description': 'Datos de la aseguradora creada'
                    }
                }
            }
        },
        400: {
            'description': 'Error de validación',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string'}
                }
            }
        }
    }
})
def crear_aseguradora():
    """Crear una nueva aseguradora"""
    try:
        datos = request.get_json()
        if not datos:
            return jsonify({'error': 'No se proporcionaron datos'}), 400
        
        resultado, codigo = AseguradoraService.crear_aseguradora(datos)
        return jsonify(resultado), codigo
        
    except Exception as e:
        return jsonify({'error': f'Error interno del servidor: {str(e)}'}), 500

@aseguradora_bp.route('/aseguradoras', methods=['GET'])
@swag_from({
    'tags': ['Aseguradoras'],
    'summary': 'Obtener todas las aseguradoras',
    'description': 'Obtener lista de todas las aseguradoras registradas',
    'parameters': [
        {
            'name': 'include_plantillas',
            'in': 'query',
            'type': 'boolean',
            'default': False,
            'description': 'Incluir deducibles, coberturas y financiaciones'
        }
    ],
    'responses': {
        200: {
            'description': 'Lista de aseguradoras obtenida exitosamente',
            'schema': {
                'type': 'object',
                'properties': {
                    'aseguradoras': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'description': 'Datos de cada aseguradora'
                        }
                    }
                }
            }
        }
    }
})
def obtener_aseguradoras():
    """Obtener todas las aseguradoras"""
    try:
        include_plantillas = request.args.get('include_plantillas', 'false').lower() == 'true'
        resultado, codigo = AseguradoraService.obtener_aseguradoras(include_plantillas)
        return jsonify(resultado), codigo
        
    except Exception as e:
        return jsonify({'error': f'Error interno del servidor: {str(e)}'}), 500

@aseguradora_bp.route('/aseguradoras/<int:aseguradora_id>', methods=['GET'])
@swag_from({
    'tags': ['Aseguradoras'],
    'summary': 'Obtener aseguradora por ID',
    'description': 'Obtener información detallada de una aseguradora específica',
    'parameters': [
        {
            'name': 'aseguradora_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID de la aseguradora'
        },
        {
            'name': 'include_plantillas',
            'in': 'query',
            'type': 'boolean',
            'default': True,
            'description': 'Incluir deducibles, coberturas y financiaciones'
        }
    ],
    'responses': {
        200: {
            'description': 'Aseguradora encontrada',
            'schema': {
                'type': 'object',
                'properties': {
                    'aseguradora': {
                        'type': 'object',
                        'description': 'Datos completos de la aseguradora'
                    }
                }
            }
        },
        404: {
            'description': 'Aseguradora no encontrada'
        }
    }
})
def obtener_aseguradora_por_id(aseguradora_id):
    """Obtener aseguradora por ID"""
    try:
        include_plantillas = request.args.get('include_plantillas', 'true').lower() == 'true'
        resultado, codigo = AseguradoraService.obtener_aseguradora_por_id(aseguradora_id, include_plantillas)
        return jsonify(resultado), codigo
        
    except Exception as e:
        return jsonify({'error': f'Error interno del servidor: {str(e)}'}), 500

@aseguradora_bp.route('/aseguradoras/<int:aseguradora_id>', methods=['PUT'])
@swag_from({
    'tags': ['Aseguradoras'],
    'summary': 'Actualizar aseguradora',
    'description': 'Actualizar información de una aseguradora existente',
    'parameters': [
        {
            'name': 'aseguradora_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID de la aseguradora'
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'nombre': {'type': 'string'},
                    'correo_comercial': {'type': 'string'},
                    'correo_reclamaciones': {'type': 'string'},
                    'comisiones_normales': {'type': 'object'},
                    'sobrecomisiones': {'type': 'object'}
                }
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Aseguradora actualizada exitosamente'
        },
        404: {
            'description': 'Aseguradora no encontrada'
        }
    }
})
def actualizar_aseguradora(aseguradora_id):
    """Actualizar aseguradora"""
    try:
        datos = request.get_json()
        if not datos:
            return jsonify({'error': 'No se proporcionaron datos'}), 400
        
        resultado, codigo = AseguradoraService.actualizar_aseguradora(aseguradora_id, datos)
        return jsonify(resultado), codigo
        
    except Exception as e:
        return jsonify({'error': f'Error interno del servidor: {str(e)}'}), 500

@aseguradora_bp.route('/aseguradoras/<int:aseguradora_id>', methods=['DELETE'])
@swag_from({
    'tags': ['Aseguradoras'],
    'summary': 'Eliminar aseguradora',
    'description': 'Eliminar una aseguradora (solo si no tiene opciones de seguro asociadas)',
    'parameters': [
        {
            'name': 'aseguradora_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID de la aseguradora'
        }
    ],
    'responses': {
        200: {
            'description': 'Aseguradora eliminada exitosamente'
        },
        400: {
            'description': 'No se puede eliminar porque tiene asociaciones'
        },
        404: {
            'description': 'Aseguradora no encontrada'
        }
    }
})
def eliminar_aseguradora(aseguradora_id):
    """Eliminar aseguradora"""
    try:
        resultado, codigo = AseguradoraService.eliminar_aseguradora(aseguradora_id)
        return jsonify(resultado), codigo
        
    except Exception as e:
        return jsonify({'error': f'Error interno del servidor: {str(e)}'}), 500

@aseguradora_bp.route('/aseguradoras/<int:aseguradora_id>/plantillas/<string:tipo_poliza>', methods=['GET'])
@swag_from({
    'tags': ['Aseguradoras'],
    'summary': 'Obtener plantillas por tipo de póliza',
    'description': 'Obtener deducibles, coberturas y financiaciones de una aseguradora para un tipo específico de póliza',
    'parameters': [
        {
            'name': 'aseguradora_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID de la aseguradora'
        },
        {
            'name': 'tipo_poliza',
            'in': 'path',
            'type': 'string',
            'required': True,
            'enum': ['HOGAR', 'VEHICULO', 'COPROPIEDAD', 'OTRO'],
            'description': 'Tipo de póliza'
        }
    ],
    'responses': {
        200: {
            'description': 'Plantillas obtenidas exitosamente',
            'schema': {
                'type': 'object',
                'properties': {
                    'aseguradora': {'type': 'object'},
                    'tipo_poliza': {'type': 'string'},
                    'deducibles': {
                        'type': 'array',
                        'items': {'type': 'object'}
                    },
                    'coberturas': {
                        'type': 'array',
                        'items': {'type': 'object'}
                    },
                    'financiaciones': {
                        'type': 'array',
                        'items': {'type': 'object'}
                    }
                }
            }
        },
        404: {
            'description': 'Aseguradora no encontrada'
        },
        400: {
            'description': 'Tipo de póliza no válido'
        }
    }
})
def obtener_plantillas_por_tipo(aseguradora_id, tipo_poliza):
    """Obtener plantillas por tipo de póliza"""
    try:
        resultado, codigo = AseguradoraService.obtener_plantillas_por_tipo(aseguradora_id, tipo_poliza)
        return jsonify(resultado), codigo
        
    except Exception as e:
        return jsonify({'error': f'Error interno del servidor: {str(e)}'}), 500

@aseguradora_bp.route('/aseguradoras/<int:aseguradora_id>/deducibles', methods=['POST'])
@swag_from({
    'tags': ['Aseguradoras'],
    'summary': 'Crear deducible',
    'description': 'Crear un nuevo deducible para una aseguradora',
    'parameters': [
        {
            'name': 'aseguradora_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID de la aseguradora'
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'required': ['tipo_poliza', 'categoria'],
                'properties': {
                    'tipo_poliza': {
                        'type': 'string',
                        'enum': ['HOGAR', 'VEHICULO', 'COPROPIEDAD', 'OTRO'],
                        'description': 'Tipo de póliza'
                    },
                    'categoria': {
                        'type': 'string',
                        'description': 'Categoría del deducible',
                        'example': 'Terremoto'
                    },
                    'tipo_deducible': {
                        'type': 'string',
                        'description': 'Tipo de deducible',
                        'example': 'Porcentaje sobre valor asegurado'
                    },
                    'valor_porcentaje': {
                        'type': 'number',
                        'format': 'float',
                        'description': 'Valor porcentual (ej: 0.02 para 2%)'
                    },
                    'valor_minimo': {
                        'type': 'number',
                        'format': 'float',
                        'description': 'Valor mínimo del deducible'
                    }
                }
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Deducible creado exitosamente'
        },
        404: {
            'description': 'Aseguradora no encontrada'
        }
    }
})
def crear_deducible(aseguradora_id):
    """Crear deducible"""
    try:
        datos = request.get_json()
        if not datos:
            return jsonify({'error': 'No se proporcionaron datos'}), 400
        
        resultado, codigo = AseguradoraService.crear_deducible(aseguradora_id, datos)
        return jsonify(resultado), codigo
        
    except Exception as e:
        return jsonify({'error': f'Error interno del servidor: {str(e)}'}), 500

@aseguradora_bp.route('/aseguradoras/<int:aseguradora_id>/coberturas', methods=['POST'])
@swag_from({
    'tags': ['Aseguradoras'],
    'summary': 'Crear cobertura',
    'description': 'Crear una nueva cobertura, asistencia o diferenciador para una aseguradora',
    'parameters': [
        {
            'name': 'aseguradora_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID de la aseguradora'
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'required': ['tipo_poliza', 'tipo_item', 'nombre_item'],
                'properties': {
                    'tipo_poliza': {
                        'type': 'string',
                        'enum': ['HOGAR', 'VEHICULO', 'COPROPIEDAD', 'OTRO'],
                        'description': 'Tipo de póliza'
                    },
                    'tipo_item': {
                        'type': 'string',
                        'enum': ['COBERTURA', 'ASISTENCIA', 'DIFERENCIADOR'],
                        'description': 'Tipo de item'
                    },
                    'nombre_item': {
                        'type': 'string',
                        'description': 'Nombre del item',
                        'example': 'Amparo Básico Incendio y Aliados'
                    }
                }
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Cobertura creada exitosamente'
        },
        404: {
            'description': 'Aseguradora no encontrada'
        }
    }
})
def crear_cobertura(aseguradora_id):
    """Crear cobertura"""
    try:
        datos = request.get_json()
        if not datos:
            return jsonify({'error': 'No se proporcionaron datos'}), 400
        
        resultado, codigo = AseguradoraService.crear_cobertura(aseguradora_id, datos)
        return jsonify(resultado), codigo
        
    except Exception as e:
        return jsonify({'error': f'Error interno del servidor: {str(e)}'}), 500

@aseguradora_bp.route('/aseguradoras/<int:aseguradora_id>/financiaciones', methods=['POST'])
@swag_from({
    'tags': ['Aseguradoras'],
    'summary': 'Crear opción de financiación',
    'description': 'Crear una nueva opción de financiación para una aseguradora',
    'parameters': [
        {
            'name': 'aseguradora_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID de la aseguradora'
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'required': ['nombre_financiera', 'tasa_efectiva_mensual'],
                'properties': {
                    'nombre_financiera': {
                        'type': 'string',
                        'description': 'Nombre de la financiera',
                        'example': 'Financiera Davivienda'
                    },
                    'tasa_efectiva_mensual': {
                        'type': 'number',
                        'format': 'float',
                        'description': 'Tasa efectiva mensual (ej: 0.015 para 1.5%)',
                        'example': 0.015
                    }
                }
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Financiación creada exitosamente'
        },
        404: {
            'description': 'Aseguradora no encontrada'
        }
    }
})
def crear_financiacion(aseguradora_id):
    """Crear financiación"""
    try:
        datos = request.get_json()
        if not datos:
            return jsonify({'error': 'No se proporcionaron datos'}), 400
        
        resultado, codigo = AseguradoraService.crear_financiacion(aseguradora_id, datos)
        return jsonify(resultado), codigo
        
    except Exception as e:
        return jsonify({'error': f'Error interno del servidor: {str(e)}'}), 500 