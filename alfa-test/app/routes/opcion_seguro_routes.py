from flask import Blueprint, request, jsonify
from flasgger import swag_from
from app.services.opcion_seguro_service import OpcionSeguroService

opcion_seguro_bp = Blueprint('opcion_seguro', __name__, url_prefix='/api')

@opcion_seguro_bp.route('/opciones-seguro', methods=['POST'])
@swag_from({
    'tags': ['Opciones de Seguro'],
    'summary': 'Crear opción de seguro (cotización)',
    'description': 'Crear una nueva opción de seguro vinculada a un bien específico y una aseguradora',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'required': ['bien_id', 'aseguradora_id', 'tipo_opcion', 'valores_asegurados'],
                'properties': {
                    'bien_id': {
                        'type': 'integer',
                        'description': 'ID del bien a asegurar',
                        'example': 1
                    },
                    'aseguradora_id': {
                        'type': 'integer',
                        'description': 'ID de la aseguradora',
                        'example': 1
                    },
                    'tipo_opcion': {
                        'type': 'string',
                        'enum': ['HOGAR', 'VEHICULO', 'COPROPIEDAD', 'OTRO'],
                        'description': 'Tipo de opción (debe coincidir con el tipo de bien)'
                    },
                    'valores_asegurados': {
                        'type': 'object',
                        'description': 'Valores asegurados específicos según el tipo',
                        'oneOf': [
                            {
                                'title': 'Valores para HOGAR',
                                'properties': {
                                    'valor_inmueble_asegurado': {'type': 'number'},
                                    'valor_contenidos_normales_asegurado': {'type': 'number'},
                                    'valor_contenidos_especiales_asegurado': {'type': 'number'},
                                    'valor_equipo_electronico_asegurado': {'type': 'number'},
                                    'valor_maquinaria_equipo_asegurado': {'type': 'number'},
                                    'valor_rc_asegurado': {'type': 'number'}
                                }
                            },
                            {
                                'title': 'Valores para VEHICULO',
                                'properties': {
                                    'valor_vehiculo_asegurado': {'type': 'number'},
                                    'valor_accesorios_asegurado': {'type': 'number'},
                                    'valor_rc_asegurado': {'type': 'number'}
                                }
                            },
                            {
                                'title': 'Valores para OTRO',
                                'properties': {
                                    'valor_asegurado': {'type': 'number'}
                                }
                            }
                        ]
                    },
                    'valor_prima_total': {
                        'type': 'number',
                        'description': 'Valor total de la prima',
                        'example': 1500000
                    },
                    'financiacion_id': {
                        'type': 'integer',
                        'description': 'ID de la opción de financiación (opcional)'
                    },
                    'deducibles_seleccionados': {
                        'type': 'array',
                        'items': {'type': 'integer'},
                        'description': 'IDs de los deducibles seleccionados'
                    },
                    'coberturas_seleccionadas': {
                        'type': 'array',
                        'items': {'type': 'integer'},
                        'description': 'IDs de las coberturas seleccionadas'
                    }
                }
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Opción de seguro creada exitosamente',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string'},
                    'opcion_seguro': {
                        'type': 'object',
                        'description': 'Datos de la opción de seguro creada'
                    }
                }
            }
        },
        400: {
            'description': 'Error de validación'
        },
        404: {
            'description': 'Bien o aseguradora no encontrados'
        }
    }
})
def crear_opcion_seguro():
    """Crear opción de seguro"""
    try:
        datos = request.get_json()
        if not datos:
            return jsonify({'error': 'No se proporcionaron datos'}), 400
        
        resultado, codigo = OpcionSeguroService.crear_opcion_seguro(datos)
        return jsonify(resultado), codigo
        
    except Exception as e:
        return jsonify({'error': f'Error interno del servidor: {str(e)}'}), 500

@opcion_seguro_bp.route('/opciones-seguro', methods=['GET'])
@swag_from({
    'tags': ['Opciones de Seguro'],
    'summary': 'Obtener opciones de seguro',
    'description': 'Obtener lista de opciones de seguro con filtros opcionales',
    'parameters': [
        {
            'name': 'bien_id',
            'in': 'query',
            'type': 'integer',
            'description': 'Filtrar por ID del bien'
        },
        {
            'name': 'aseguradora_id',
            'in': 'query',
            'type': 'integer',
            'description': 'Filtrar por ID de la aseguradora'
        },
        {
            'name': 'tipo_opcion',
            'in': 'query',
            'type': 'string',
            'enum': ['HOGAR', 'VEHICULO', 'COPROPIEDAD', 'OTRO'],
            'description': 'Filtrar por tipo de opción'
        }
    ],
    'responses': {
        200: {
            'description': 'Lista de opciones de seguro obtenida exitosamente',
            'schema': {
                'type': 'object',
                'properties': {
                    'opciones_seguro': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'description': 'Datos de cada opción de seguro'
                        }
                    }
                }
            }
        }
    }
})
def obtener_opciones_seguro():
    """Obtener opciones de seguro"""
    try:
        bien_id = request.args.get('bien_id', type=int)
        aseguradora_id = request.args.get('aseguradora_id', type=int)
        tipo_opcion = request.args.get('tipo_opcion')
        
        resultado, codigo = OpcionSeguroService.obtener_opciones_seguro(bien_id, aseguradora_id, tipo_opcion)
        return jsonify(resultado), codigo
        
    except Exception as e:
        return jsonify({'error': f'Error interno del servidor: {str(e)}'}), 500

@opcion_seguro_bp.route('/opciones-seguro/<int:opcion_id>', methods=['GET'])
@swag_from({
    'tags': ['Opciones de Seguro'],
    'summary': 'Obtener opción de seguro por ID',
    'description': 'Obtener información detallada de una opción de seguro específica',
    'parameters': [
        {
            'name': 'opcion_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID de la opción de seguro'
        }
    ],
    'responses': {
        200: {
            'description': 'Opción de seguro encontrada',
            'schema': {
                'type': 'object',
                'properties': {
                    'opcion_seguro': {
                        'type': 'object',
                        'description': 'Datos completos de la opción de seguro'
                    }
                }
            }
        },
        404: {
            'description': 'Opción de seguro no encontrada'
        }
    }
})
def obtener_opcion_seguro_por_id(opcion_id):
    """Obtener opción de seguro por ID"""
    try:
        resultado, codigo = OpcionSeguroService.obtener_opcion_seguro_por_id(opcion_id)
        return jsonify(resultado), codigo
        
    except Exception as e:
        return jsonify({'error': f'Error interno del servidor: {str(e)}'}), 500

@opcion_seguro_bp.route('/bienes/<int:bien_id>/opciones-seguro', methods=['GET'])
@swag_from({
    'tags': ['Opciones de Seguro'],
    'summary': 'Obtener opciones de seguro por bien',
    'description': 'Obtener todas las opciones de seguro disponibles para un bien específico',
    'parameters': [
        {
            'name': 'bien_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID del bien'
        }
    ],
    'responses': {
        200: {
            'description': 'Opciones de seguro del bien obtenidas exitosamente',
            'schema': {
                'type': 'object',
                'properties': {
                    'bien': {
                        'type': 'object',
                        'description': 'Información del bien'
                    },
                    'opciones_seguro': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'description': 'Opciones de seguro disponibles'
                        }
                    }
                }
            }
        },
        404: {
            'description': 'Bien no encontrado'
        }
    }
})
def obtener_opciones_por_bien(bien_id):
    """Obtener opciones de seguro por bien"""
    try:
        resultado, codigo = OpcionSeguroService.obtener_opciones_por_bien(bien_id)
        return jsonify(resultado), codigo
        
    except Exception as e:
        return jsonify({'error': f'Error interno del servidor: {str(e)}'}), 500

@opcion_seguro_bp.route('/opciones-seguro/<int:opcion_id>/prima', methods=['PUT'])
@swag_from({
    'tags': ['Opciones de Seguro'],
    'summary': 'Actualizar valor de prima',
    'description': 'Actualizar el valor de la prima de una opción de seguro (solo si no tiene póliza)',
    'parameters': [
        {
            'name': 'opcion_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID de la opción de seguro'
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'required': ['valor_prima_total'],
                'properties': {
                    'valor_prima_total': {
                        'type': 'number',
                        'description': 'Nuevo valor de la prima total',
                        'example': 1800000
                    }
                }
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Valor de prima actualizado exitosamente'
        },
        400: {
            'description': 'No se puede actualizar una opción que ya tiene póliza'
        },
        404: {
            'description': 'Opción de seguro no encontrada'
        }
    }
})
def actualizar_valor_prima(opcion_id):
    """Actualizar valor de prima"""
    try:
        datos = request.get_json()
        if not datos or 'valor_prima_total' not in datos:
            return jsonify({'error': 'El valor_prima_total es requerido'}), 400
        
        resultado, codigo = OpcionSeguroService.actualizar_valor_prima(opcion_id, datos['valor_prima_total'])
        return jsonify(resultado), codigo
        
    except Exception as e:
        return jsonify({'error': f'Error interno del servidor: {str(e)}'}), 500

@opcion_seguro_bp.route('/opciones-seguro/<int:opcion_id>', methods=['DELETE'])
@swag_from({
    'tags': ['Opciones de Seguro'],
    'summary': 'Eliminar opción de seguro',
    'description': 'Eliminar una opción de seguro (solo si no tiene póliza asociada)',
    'parameters': [
        {
            'name': 'opcion_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID de la opción de seguro'
        }
    ],
    'responses': {
        200: {
            'description': 'Opción de seguro eliminada exitosamente'
        },
        400: {
            'description': 'No se puede eliminar una opción que ya tiene póliza'
        },
        404: {
            'description': 'Opción de seguro no encontrada'
        }
    }
})
def eliminar_opcion_seguro(opcion_id):
    """Eliminar opción de seguro"""
    try:
        resultado, codigo = OpcionSeguroService.eliminar_opcion_seguro(opcion_id)
        return jsonify(resultado), codigo
        
    except Exception as e:
        return jsonify({'error': f'Error interno del servidor: {str(e)}'}), 500

@opcion_seguro_bp.route('/simulacion-prima', methods=['POST'])
@swag_from({
    'tags': ['Opciones de Seguro'],
    'summary': 'Simular prima de seguro',
    'description': 'Calcular simulación de prima sin crear la opción de seguro',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'required': ['bien_id', 'aseguradora_id', 'valores_asegurados'],
                'properties': {
                    'bien_id': {
                        'type': 'integer',
                        'description': 'ID del bien a simular',
                        'example': 1
                    },
                    'aseguradora_id': {
                        'type': 'integer',
                        'description': 'ID de la aseguradora',
                        'example': 1
                    },
                    'valores_asegurados': {
                        'type': 'object',
                        'description': 'Valores a asegurar para la simulación',
                        'example': {
                            'valor_inmueble_asegurado': 500000000,
                            'valor_contenidos_normales_asegurado': 80000000,
                            'valor_rc_asegurado': 200000000
                        }
                    }
                }
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Simulación calculada exitosamente',
            'schema': {
                'type': 'object',
                'properties': {
                    'simulacion': {
                        'type': 'object',
                        'properties': {
                            'bien_id': {'type': 'integer'},
                            'aseguradora_id': {'type': 'integer'},
                            'valor_total_asegurado': {'type': 'number'},
                            'prima_base': {'type': 'number'},
                            'prima_iva': {'type': 'number'},
                            'prima_total': {'type': 'number'},
                            'comision_porcentaje': {'type': 'number'},
                            'comision_total': {'type': 'number'}
                        }
                    }
                }
            }
        },
        404: {
            'description': 'Bien o aseguradora no encontrados'
        }
    }
})
def calcular_simulacion_prima():
    """Calcular simulación de prima"""
    try:
        datos = request.get_json()
        if not datos:
            return jsonify({'error': 'No se proporcionaron datos'}), 400
        
        resultado, codigo = OpcionSeguroService.calcular_simulacion_prima(datos)
        return jsonify(resultado), codigo
        
    except Exception as e:
        return jsonify({'error': f'Error interno del servidor: {str(e)}'}), 500 