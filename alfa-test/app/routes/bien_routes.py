from flask import Blueprint, jsonify, request
from app.services.bien_service import BienService
from flasgger import swag_from

bien_bp = Blueprint('bien', __name__, url_prefix='/api')

@bien_bp.route('/bienes', methods=['GET'])
def get_bienes():
    """Obtener todos los bienes
    ---
    tags:
      - Bienes
    summary: Obtener lista de bienes asegurables
    description: Obtiene todos los bienes con filtros opcionales por tipo o cliente
    parameters:
      - name: tipo
        in: query
        type: string
        enum: ['HOGAR', 'VEHICULO', 'COPROPIEDAD', 'OTRO']
        description: Filtrar bienes por tipo
      - name: cliente_id
        in: query
        type: integer
        description: Filtrar bienes por cliente específico
    responses:
      200:
        description: Lista de bienes obtenida exitosamente
        schema:
          type: object
          properties:
            status:
              type: string
              example: "success"
            data:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                    example: 1
                  tipo_bien:
                    type: string
                    example: "HOGAR"
                  bien_especifico_id:
                    type: integer
                    example: 1
                  estado:
                    type: string
                    example: "Activo"
                  comentarios_generales:
                    type: string
                    example: "Casa principal de familia"
                  vigencias_continuas:
                    type: boolean
                    example: true
                  fecha_creacion:
                    type: string
                    format: date-time
                  bien_especifico:
                    type: object
                    description: "Datos específicos del bien según su tipo"
      400:
        description: Parámetros inválidos
        schema:
          type: object
          properties:
            status:
              type: string
              example: "error"
            message:
              type: string
              example: "El tipo debe ser HOGAR, VEHICULO, COPROPIEDAD o OTRO"
      500:
        description: Error interno del servidor
    """
    try:
        tipo = request.args.get('tipo')  # Filtrar por tipo si se proporciona
        cliente_id = request.args.get('cliente_id')  # Filtrar por cliente si se proporciona
        
        if cliente_id:
            try:
                cliente_id = int(cliente_id)
                bienes = BienService.get_bienes_by_cliente(cliente_id)
            except ValueError:
                return jsonify({
                    'status': 'error',
                    'message': 'cliente_id debe ser un número entero'
                }), 400
        elif tipo:
            if tipo not in ['HOGAR', 'VEHICULO', 'COPROPIEDAD', 'OTRO']:
                return jsonify({
                    'status': 'error',
                    'message': 'El tipo debe ser HOGAR, VEHICULO, COPROPIEDAD o OTRO'
                }), 400
            bienes = BienService.get_bienes_by_tipo(tipo)
        else:
            bienes = BienService.get_all_bienes()
            
        return jsonify({
            'status': 'success',
            'data': [bien.to_dict() for bien in bienes]
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@bien_bp.route('/bienes/<int:bien_id>', methods=['GET'])
def get_bien(bien_id):
    """Obtener un bien por ID
    ---
    tags:
      - Bienes
    summary: Obtener bien específico
    description: Obtiene los datos de un bien asegurable específico por su ID, incluyendo sus datos específicos según el tipo
    parameters:
      - name: bien_id
        in: path
        type: integer
        required: true
        description: ID del bien a obtener
        example: 1
    responses:
      200:
        description: Bien obtenido exitosamente
        schema:
          type: object
          properties:
            status:
              type: string
              example: "success"
            data:
              type: object
              properties:
                id:
                  type: integer
                  example: 1
                tipo_bien:
                  type: string
                  example: "HOGAR"
                bien_especifico_id:
                  type: integer
                  example: 1
                estado:
                  type: string
                  example: "Activo"
                comentarios_generales:
                  type: string
                  example: "Casa principal de familia"
                vigencias_continuas:
                  type: boolean
                  example: true
                fecha_creacion:
                  type: string
                  format: date-time
                bien_especifico:
                  type: object
                  description: "Datos específicos del bien según su tipo"
                  oneOf:
                    - title: "HOGAR"
                      properties:
                        tipo_inmueble:
                          type: string
                          example: "Casa"
                        ciudad_inmueble:
                          type: string
                          example: "Bogotá"
                        direccion_inmueble:
                          type: string
                          example: "Carrera 15 #45-23"
                        numero_pisos:
                          type: integer
                          example: 2
                        ano_construccion:
                          type: integer
                          example: 2015
                        valor_inmueble_avaluo:
                          type: number
                          example: 350000000.00
                    - title: "VEHICULO"
                      properties:
                        tipo_vehiculo:
                          type: string
                          example: "Automóvil"
                        placa:
                          type: string
                          example: "ABC123"
                        marca:
                          type: string
                          example: "Toyota"
                        serie_referencia:
                          type: string
                          example: "Corolla Cross XLI"
                        ano_modelo:
                          type: integer
                          example: 2023
                        valor_vehiculo:
                          type: number
                          example: 85000000.00
                    - title: "COPROPIEDAD"
                      properties:
                        tipo_copropiedad:
                          type: string
                          example: "Conjunto Residencial"
                        ciudad:
                          type: string
                          example: "Bogotá"
                        direccion:
                          type: string
                          example: "Carrera 7 #127-45"
                        estrato:
                          type: integer
                          example: 4
                        numero_torres:
                          type: integer
                          example: 3
                        cantidad_unidades_apartamentos:
                          type: integer
                          example: 180
                        valor_edificio_area_comun_avaluo:
                          type: number
                          example: 2500000000.00
                    - title: "OTRO"
                      properties:
                        tipo_seguro:
                          type: string
                          example: "Seguro de Transporte"
                        bien_asegurado:
                          type: string
                          example: "Mercancías en Tránsito"
                        valor_bien_asegurar:
                          type: number
                          example: 500000000.00
      404:
        description: Bien no encontrado
        schema:
          type: object
          properties:
            status:
              type: string
              example: "error"
            message:
              type: string
              example: "Bien no encontrado"
      500:
        description: Error interno del servidor
        schema:
          type: object
          properties:
            status:
              type: string
              example: "error"
            message:
              type: string
              example: "Error interno del servidor"
    """
    try:
        bien = BienService.get_bien_by_id(bien_id)
        if bien:
            return jsonify({
                'status': 'success',
                'data': bien.to_dict()
            }), 200
        else:
            return jsonify({
                'status': 'error',
                'message': 'Bien no encontrado'
            }), 404
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@bien_bp.route('/bienes', methods=['POST'])
def create_bien():
    """Crear un nuevo bien
    ---
    tags:
      - Bienes
    summary: Crear nuevo bien asegurable
    description: Crea un nuevo bien asegurable de cualquier tipo (HOGAR, VEHICULO, COPROPIEDAD, OTRO) y opcionalmente lo asigna a un cliente
    parameters:
      - name: bien
        in: body
        required: true
        schema:
          type: object
          required:
            - tipo_bien
            - data_especifico
          properties:
            tipo_bien:
              type: string
              enum: ['HOGAR', 'VEHICULO', 'COPROPIEDAD', 'OTRO']
              example: "HOGAR"
              description: "Tipo de bien a crear"
            data_especifico:
              type: object
              description: "Datos específicos según el tipo de bien"
              oneOf:
                - title: "HOGAR"
                  type: object
                  required: [tipo_inmueble]
                  properties:
                    tipo_inmueble:
                      type: string
                      example: "Casa"
                      description: "Tipo de inmueble (Casa, Apartamento, etc.)"
                    ciudad_inmueble:
                      type: string
                      example: "Bogotá"
                    direccion_inmueble:
                      type: string
                      example: "Carrera 15 #45-23"
                    numero_pisos:
                      type: integer
                      example: 2
                    ano_construccion:
                      type: integer
                      example: 2015
                    valor_inmueble_avaluo:
                      type: number
                      example: 350000000.00
                    valor_contenidos_normales_avaluo:
                      type: number
                      example: 25000000.00
                - title: "VEHICULO"
                  type: object
                  required: [placa]
                  properties:
                    tipo_vehiculo:
                      type: string
                      example: "Automóvil"
                    placa:
                      type: string
                      example: "ABC123"
                      description: "Placa del vehículo (requerido y único)"
                    marca:
                      type: string
                      example: "Toyota"
                    serie_referencia:
                      type: string
                      example: "Corolla Cross XLI"
                    ano_modelo:
                      type: integer
                      example: 2023
                    codigo_fasecolda:
                      type: string
                      example: "81042090"
                    valor_vehiculo:
                      type: number
                      example: 85000000.00
                - title: "COPROPIEDAD"
                  type: object
                  required: [tipo_copropiedad]
                  properties:
                    tipo_copropiedad:
                      type: string
                      example: "Conjunto Residencial"
                      description: "Tipo de copropiedad (requerido)"
                    ciudad:
                      type: string
                      example: "Bogotá"
                    direccion:
                      type: string
                      example: "Carrera 7 #127-45"
                    estrato:
                      type: integer
                      example: 4
                    numero_torres:
                      type: integer
                      example: 3
                    numero_maximo_pisos:
                      type: integer
                      example: 15
                    cantidad_unidades_apartamentos:
                      type: integer
                      example: 180
                    valor_edificio_area_comun_avaluo:
                      type: number
                      example: 2500000000.00
                - title: "OTRO"
                  type: object
                  required: [bien_asegurado]
                  properties:
                    tipo_seguro:
                      type: string
                      example: "Seguro de Transporte"
                    bien_asegurado:
                      type: string
                      example: "Mercancías en Tránsito"
                      description: "Descripción del bien asegurado (requerido)"
                    valor_bien_asegurar:
                      type: number
                      example: 500000000.00
                    detalles_bien_asegurado:
                      type: string
                      example: "Cobertura para mercancías transportadas"
            data_general:
              type: object
              description: "Datos generales del bien (opcional)"
              properties:
                estado:
                  type: string
                  example: "Activo"
                  description: "Estado del bien"
                comentarios_generales:
                  type: string
                  example: "Bien principal del cliente"
                  description: "Comentarios adicionales"
                vigencias_continuas:
                  type: boolean
                  example: true
                  description: "Indica si tiene vigencias continuas"
            cliente_id:
              type: integer
              example: 1
              description: "ID del cliente al cual asignar el bien (opcional)"
    responses:
      201:
        description: Bien creado exitosamente
        schema:
          type: object
          properties:
            status:
              type: string
              example: "success"
            message:
              type: string
              example: "Bien creado exitosamente"
            data:
              type: object
              properties:
                id:
                  type: integer
                  example: 1
                tipo_bien:
                  type: string
                  example: "HOGAR"
                bien_especifico_id:
                  type: integer
                  example: 1
                estado:
                  type: string
                  example: "Activo"
                comentarios_generales:
                  type: string
                  example: "Casa principal de familia"
                vigencias_continuas:
                  type: boolean
                  example: true
                fecha_creacion:
                  type: string
                  format: date-time
                bien_especifico:
                  type: object
                  description: "Datos específicos del bien creado"
      400:
        description: Datos inválidos o campos requeridos faltantes
        schema:
          type: object
          properties:
            status:
              type: string
              example: "error"
            message:
              type: string
              example: "tipo_bien es requerido"
      500:
        description: Error interno del servidor
        schema:
          type: object
          properties:
            status:
              type: string
              example: "error"
            message:
              type: string
              example: "Error interno del servidor"
    """
    try:
        data = request.get_json()
        
        # Validaciones básicas
        if not data:
            return jsonify({
                'status': 'error',
                'message': 'No se proporcionaron datos'
            }), 400
            
        if not data.get('tipo_bien'):
            return jsonify({
                'status': 'error',
                'message': 'tipo_bien es requerido'
            }), 400
            
        tipo_bien = data.get('tipo_bien')
        if tipo_bien not in ['HOGAR', 'VEHICULO', 'COPROPIEDAD', 'OTRO']:
            return jsonify({
                'status': 'error',
                'message': 'tipo_bien debe ser HOGAR, VEHICULO, COPROPIEDAD o OTRO'
            }), 400
            
        if not data.get('data_especifico'):
            return jsonify({
                'status': 'error',
                'message': 'data_especifico es requerido'
            }), 400
        
        # Validaciones específicas por tipo
        data_especifico = data.get('data_especifico')
        if tipo_bien == 'HOGAR':
            if not data_especifico.get('tipo_inmueble'):
                return jsonify({
                    'status': 'error',
                    'message': 'tipo_inmueble es requerido para hogares'
                }), 400
        elif tipo_bien == 'VEHICULO':
            if not data_especifico.get('placa'):
                return jsonify({
                    'status': 'error',
                    'message': 'placa es requerida para vehículos'
                }), 400
        elif tipo_bien == 'COPROPIEDAD':
            if not data_especifico.get('tipo_copropiedad'):
                return jsonify({
                    'status': 'error',
                    'message': 'tipo_copropiedad es requerido para copropiedades'
                }), 400
        elif tipo_bien == 'OTRO':
            if not data_especifico.get('bien_asegurado'):
                return jsonify({
                    'status': 'error',
                    'message': 'bien_asegurado es requerido para otros bienes'
                }), 400
        
        data_general = data.get('data_general', {})
        
        bien = BienService.create_bien(tipo_bien, data_especifico, data_general)
        
        # Si se proporciona cliente_id, asignar el bien al cliente
        cliente_id = data.get('cliente_id')
        if cliente_id:
            BienService.asignar_bien_a_cliente(cliente_id, bien.id)
        
        return jsonify({
            'status': 'success',
            'message': 'Bien creado exitosamente',
            'data': bien.to_dict()
        }), 201
        
    except ValueError as ve:
        return jsonify({
            'status': 'error',
            'message': str(ve)
        }), 400
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@bien_bp.route('/bienes/<int:bien_id>', methods=['PUT'])
def update_bien(bien_id):
    """Actualizar un bien existente
    ---
    tags:
      - Bienes
    summary: Actualizar bien asegurable
    description: Actualiza los datos de un bien asegurable existente (datos generales o específicos)
    parameters:
      - name: bien_id
        in: path
        type: integer
        required: true
        description: ID del bien a actualizar
        example: 1
      - name: bien
        in: body
        required: true
        schema:
          type: object
          properties:
            data_general:
              type: object
              description: "Datos generales del bien a actualizar"
              properties:
                estado:
                  type: string
                  example: "Activo"
                  description: "Estado del bien"
                comentarios_generales:
                  type: string
                  example: "Bien actualizado"
                  description: "Comentarios adicionales"
                vigencias_continuas:
                  type: boolean
                  example: true
                  description: "Indica si tiene vigencias continuas"
            data_especifico:
              type: object
              description: "Datos específicos del bien a actualizar según su tipo"
              properties:
                tipo_inmueble:
                  type: string
                  example: "Apartamento"
                  description: "Para bienes tipo HOGAR"
                valor_inmueble_avaluo:
                  type: number
                  example: 400000000.00
                  description: "Para bienes tipo HOGAR"
                placa:
                  type: string
                  example: "DEF456"
                  description: "Para bienes tipo VEHICULO"
                valor_vehiculo:
                  type: number
                  example: 90000000.00
                  description: "Para bienes tipo VEHICULO"
                tipo_copropiedad:
                  type: string
                  example: "Edificio Residencial"
                  description: "Para bienes tipo COPROPIEDAD"
                bien_asegurado:
                  type: string
                  example: "Equipos de Oficina"
                  description: "Para bienes tipo OTRO"
    responses:
      200:
        description: Bien actualizado exitosamente
        schema:
          type: object
          properties:
            status:
              type: string
              example: "success"
            message:
              type: string
              example: "Bien actualizado exitosamente"
            data:
              type: object
              properties:
                id:
                  type: integer
                  example: 1
                tipo_bien:
                  type: string
                  example: "HOGAR"
                bien_especifico_id:
                  type: integer
                  example: 1
                estado:
                  type: string
                  example: "Activo"
                comentarios_generales:
                  type: string
                  example: "Bien actualizado"
                vigencias_continuas:
                  type: boolean
                  example: true
                fecha_creacion:
                  type: string
                  format: date-time
                bien_especifico:
                  type: object
                  description: "Datos específicos actualizados"
      400:
        description: Datos inválidos o no se proporcionaron datos
        schema:
          type: object
          properties:
            status:
              type: string
              example: "error"
            message:
              type: string
              example: "Se debe proporcionar data_general o data_especifico"
      404:
        description: Bien no encontrado
        schema:
          type: object
          properties:
            status:
              type: string
              example: "error"
            message:
              type: string
              example: "Bien no encontrado"
      500:
        description: Error interno del servidor
        schema:
          type: object
          properties:
            status:
              type: string
              example: "error"
            message:
              type: string
              example: "Error interno del servidor"
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'status': 'error',
                'message': 'No se proporcionaron datos'
            }), 400
        
        data_general = data.get('data_general')
        data_especifico = data.get('data_especifico')
        
        if not data_general and not data_especifico:
            return jsonify({
                'status': 'error',
                'message': 'Se debe proporcionar data_general o data_especifico'
            }), 400
        
        bien = BienService.update_bien(bien_id, data_general, data_especifico)
        if bien:
            return jsonify({
                'status': 'success',
                'message': 'Bien actualizado exitosamente',
                'data': bien.to_dict()
            }), 200
        else:
            return jsonify({
                'status': 'error',
                'message': 'Bien no encontrado'
            }), 404
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@bien_bp.route('/bienes/<int:bien_id>', methods=['DELETE'])
def delete_bien(bien_id):
    """Eliminar un bien
    ---
    tags:
      - Bienes
    summary: Eliminar bien asegurable
    description: Elimina un bien asegurable del sistema por su ID
    parameters:
      - name: bien_id
        in: path
        type: integer
        required: true
        description: ID del bien a eliminar
        example: 1
    responses:
      200:
        description: Bien eliminado exitosamente
        schema:
          type: object
          properties:
            status:
              type: string
              example: "success"
            message:
              type: string
              example: "Bien eliminado exitosamente"
      404:
        description: Bien no encontrado
        schema:
          type: object
          properties:
            status:
              type: string
              example: "error"
            message:
              type: string
              example: "Bien no encontrado"
      500:
        description: Error interno del servidor
        schema:
          type: object
          properties:
            status:
              type: string
              example: "error"
            message:
              type: string
              example: "Error interno del servidor"
    """
    try:
        if BienService.delete_bien(bien_id):
            return jsonify({
                'status': 'success',
                'message': 'Bien eliminado exitosamente'
            }), 200
        else:
            return jsonify({
                'status': 'error',
                'message': 'Bien no encontrado'
            }), 404
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@bien_bp.route('/bienes/<int:bien_id>/asignar', methods=['POST'])
def asignar_bien_a_cliente(bien_id):
    """Asignar un bien a un cliente"""
    try:
        data = request.get_json()
        if not data or not data.get('cliente_id'):
            return jsonify({
                'status': 'error',
                'message': 'cliente_id es requerido'
            }), 400
        
        cliente_id = data.get('cliente_id')
        
        # Verificar que el bien existe
        bien = BienService.get_bien_by_id(bien_id)
        if not bien:
            return jsonify({
                'status': 'error',
                'message': 'Bien no encontrado'
            }), 404
        
        asignacion = BienService.asignar_bien_a_cliente(cliente_id, bien_id)
        return jsonify({
            'status': 'success',
            'message': 'Bien asignado exitosamente al cliente',
            'data': asignacion.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@bien_bp.route('/bienes/<int:bien_id>/desasignar', methods=['POST'])
def desasignar_bien_de_cliente(bien_id):
    """Desasignar un bien de un cliente"""
    try:
        data = request.get_json()
        if not data or not data.get('cliente_id'):
            return jsonify({
                'status': 'error',
                'message': 'cliente_id es requerido'
            }), 400
        
        cliente_id = data.get('cliente_id')
        
        if BienService.desasignar_bien_de_cliente(cliente_id, bien_id):
            return jsonify({
                'status': 'success',
                'message': 'Bien desasignado exitosamente del cliente'
            }), 200
        else:
            return jsonify({
                'status': 'error',
                'message': 'Asignación no encontrada'
            }), 404
            
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

# Rutas específicas para cada tipo de bien
@bien_bp.route('/bienes/tipos', methods=['GET'])
def get_tipos_bienes():
    """Obtener los tipos de bienes disponibles
    ---
    tags:
      - Bienes
    summary: Obtener tipos de bienes disponibles
    description: Retorna la lista de tipos de bienes que se pueden asegurar en el sistema
    responses:
      200:
        description: Tipos de bienes obtenidos exitosamente
        schema:
          type: object
          properties:
            status:
              type: string
              example: "success"
            data:
              type: object
              properties:
                tipos:
                  type: array
                  items:
                    type: string
                  example: ["HOGAR", "VEHICULO", "COPROPIEDAD", "OTRO"]
                descripciones:
                  type: object
                  properties:
                    HOGAR:
                      type: string
                      example: "Bienes inmuebles residenciales"
                    VEHICULO:
                      type: string
                      example: "Vehículos motorizados"
                    COPROPIEDAD:
                      type: string
                      example: "Propiedades horizontales o edificios"
                    OTRO:
                      type: string
                      example: "Otros tipos de bienes asegurables"
    """
    return jsonify({
        'status': 'success',
        'data': {
            'tipos': ['HOGAR', 'VEHICULO', 'COPROPIEDAD', 'OTRO'],
            'descripciones': {
                'HOGAR': 'Bienes inmuebles residenciales',
                'VEHICULO': 'Vehículos motorizados',
                'COPROPIEDAD': 'Propiedades horizontales o edificios',
                'OTRO': 'Otros tipos de bienes asegurables'
            }
        }
    }), 200

# Endpoint para obtener bienes de un cliente específico con detalles
@bien_bp.route('/clientes/<int:cliente_id>/bienes', methods=['GET'])
def get_bienes_cliente(cliente_id):
    """Obtener todos los bienes de un cliente específico
    ---
    tags:
      - Bienes
    summary: Obtener bienes de un cliente
    description: Obtiene la lista de todos los bienes asignados a un cliente específico
    parameters:
      - name: cliente_id
        in: path
        type: integer
        required: true
        description: ID del cliente del cual obtener los bienes
        example: 1
    responses:
      200:
        description: Lista de bienes del cliente obtenida exitosamente
        schema:
          type: object
          properties:
            status:
              type: string
              example: "success"
            data:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                    example: 1
                  tipo_bien:
                    type: string
                    example: "HOGAR"
                  bien_especifico_id:
                    type: integer
                    example: 1
                  estado:
                    type: string
                    example: "Activo"
                  comentarios_generales:
                    type: string
                    example: "Casa principal de familia"
                  vigencias_continuas:
                    type: boolean
                    example: true
                  fecha_creacion:
                    type: string
                    format: date-time
                  bien_especifico:
                    type: object
                    description: "Datos específicos del bien según su tipo"
            total:
              type: integer
              example: 3
              description: "Número total de bienes del cliente"
      404:
        description: Cliente no encontrado
        schema:
          type: object
          properties:
            status:
              type: string
              example: "error"
            message:
              type: string
              example: "Cliente no encontrado"
      500:
        description: Error interno del servidor
        schema:
          type: object
          properties:
            status:
              type: string
              example: "error"
            message:
              type: string
              example: "Error interno del servidor"
    """
    try:
        bienes = BienService.get_bienes_by_cliente(cliente_id)
        return jsonify({
            'status': 'success',
            'data': [bien.to_dict() for bien in bienes],
            'total': len(bienes)
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500 