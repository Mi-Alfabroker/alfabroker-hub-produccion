from flask import Blueprint, jsonify, request
from app.services.cliente_service import ClienteService
from flasgger import swag_from

cliente_bp = Blueprint('cliente', __name__, url_prefix='/api')

@cliente_bp.route('/clientes', methods=['GET'])
def get_clientes():
    """Obtener todos los clientes
    ---
    tags:
      - Clientes
    summary: Obtener lista de clientes
    description: Obtiene todos los clientes con filtro opcional por tipo (PERSONA o EMPRESA)
    parameters:
      - name: tipo
        in: query
        type: string
        enum: ['PERSONA', 'EMPRESA']
        description: Filtrar clientes por tipo
    responses:
      200:
        description: Lista de clientes obtenida exitosamente
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
                  tipo_cliente:
                    type: string
                    example: "PERSONA"
                  usuario:
                    type: string
                    example: "maria.gonzalez"
                  nombre:
                    type: string
                    example: "María González"
                    description: "Para personas naturales"
                  razon_social:
                    type: string
                    example: "Empresa XYZ S.A.S."
                    description: "Para empresas"
                  correo:
                    type: string
                    example: "maria@ejemplo.com"
                  telefono_movil:
                    type: string
                    example: "3001234567"
                  ciudad:
                    type: string
                    example: "Bogotá"
                  direccion:
                    type: string
                    example: "Calle 123 #45-67"
                  fecha_creacion:
                    type: string
                    format: date-time
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
              example: "El tipo debe ser PERSONA o EMPRESA"
      500:
        description: Error interno del servidor
    """
    try:
        tipo = request.args.get('tipo')  # Filtrar por tipo si se proporciona
        
        if tipo:
            if tipo not in ['PERSONA', 'EMPRESA']:
                return jsonify({
                    'status': 'error',
                    'message': 'El tipo debe ser PERSONA o EMPRESA'
                }), 400
            clientes = ClienteService.get_clientes_by_tipo(tipo)
        else:
            clientes = ClienteService.get_all_clientes()
            
        return jsonify({
            'status': 'success',
            'data': [cliente.to_dict() for cliente in clientes]
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@cliente_bp.route('/clientes/<int:cliente_id>', methods=['GET'])
def get_cliente(cliente_id):
    """Obtener un cliente por ID
    ---
    tags:
      - Clientes
    summary: Obtener cliente específico
    description: Obtiene los datos de un cliente específico por su ID
    parameters:
      - name: cliente_id
        in: path
        type: integer
        required: true
        description: ID del cliente a obtener
        example: 1
    responses:
      200:
        description: Cliente obtenido exitosamente
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
                tipo_cliente:
                  type: string
                  example: "PERSONA"
                usuario:
                  type: string
                  example: "maria.gonzalez"
                nombre:
                  type: string
                  example: "María González"
                  description: "Para personas naturales"
                razon_social:
                  type: string
                  example: "Empresa XYZ S.A.S."
                  description: "Para empresas"
                correo:
                  type: string
                  example: "maria@ejemplo.com"
                telefono_movil:
                  type: string
                  example: "3001234567"
                ciudad:
                  type: string
                  example: "Bogotá"
                direccion:
                  type: string
                  example: "Calle 123 #45-67"
                fecha_creacion:
                  type: string
                  format: date-time
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
        cliente = ClienteService.get_cliente_by_id(cliente_id)
        if cliente:
            return jsonify({
                'status': 'success',
                'data': cliente.to_dict()
            }), 200
        else:
            return jsonify({
                'status': 'error',
                'message': 'Cliente no encontrado'
            }), 404
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@cliente_bp.route('/clientes', methods=['POST'])
def create_cliente():
    """Crear un nuevo cliente
    ---
    tags:
      - Clientes
    summary: Crear nuevo cliente
    description: Crea un nuevo cliente (persona natural o empresa) en el sistema
    parameters:
      - name: cliente
        in: body
        required: true
        schema:
          type: object
          required:
            - tipo_cliente
            - usuario
            - clave
          properties:
            tipo_cliente:
              type: string
              enum: ['PERSONA', 'EMPRESA']
              example: "PERSONA"
              description: "Tipo de cliente a crear"
            usuario:
              type: string
              example: "maria.gonzalez"
              description: "Nombre de usuario único"
            clave:
              type: string
              example: "clave_segura"
              description: "Contraseña del cliente"
            nombre:
              type: string
              example: "María González"
              description: "Nombre completo (requerido para PERSONA)"
            razon_social:
              type: string
              example: "Empresa XYZ S.A.S."
              description: "Razón social (requerido para EMPRESA)"
            tipo_documento:
              type: string
              example: "CC"
              description: "Tipo de documento (para PERSONA)"
            numero_documento:
              type: string
              example: "12345678"
              description: "Número de documento (para PERSONA)"
            nit:
              type: string
              example: "900123456-7"
              description: "NIT (para EMPRESA)"
            correo:
              type: string
              format: email
              example: "maria@ejemplo.com"
              description: "Correo electrónico"
            telefono_movil:
              type: string
              example: "3001234567"
              description: "Número de teléfono móvil"
            ciudad:
              type: string
              example: "Bogotá"
              description: "Ciudad de residencia"
            direccion:
              type: string
              example: "Calle 123 #45-67"
              description: "Dirección completa"
            edad:
              type: integer
              example: 30
              description: "Edad (para PERSONA)"
            nombre_rep_legal:
              type: string
              example: "Juan Pérez"
              description: "Representante legal (para EMPRESA)"
    responses:
      201:
        description: Cliente creado exitosamente
        schema:
          type: object
          properties:
            status:
              type: string
              example: "success"
            message:
              type: string
              example: "Cliente creado exitosamente"
            data:
              type: object
              properties:
                id:
                  type: integer
                  example: 1
                tipo_cliente:
                  type: string
                  example: "PERSONA"
                usuario:
                  type: string
                  example: "maria.gonzalez"
                nombre:
                  type: string
                  example: "María González"
                correo:
                  type: string
                  example: "maria@ejemplo.com"
                fecha_creacion:
                  type: string
                  format: date-time
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
              example: "nombre es requerido para personas naturales"
      500:
        description: Error interno del servidor
    """
    try:
        data = request.get_json()
        
        # Validaciones básicas
        if not data:
            return jsonify({
                'status': 'error',
                'message': 'No se proporcionaron datos'
            }), 400
            
        if not data.get('tipo_cliente'):
            return jsonify({
                'status': 'error',
                'message': 'tipo_cliente es requerido'
            }), 400
            
        if not data.get('usuario'):
            return jsonify({
                'status': 'error',
                'message': 'usuario es requerido'
            }), 400
            
        if not data.get('clave'):
            return jsonify({
                'status': 'error',
                'message': 'clave es requerida'
            }), 400
        
        # Validaciones específicas por tipo
        tipo_cliente = data.get('tipo_cliente')
        if tipo_cliente == 'PERSONA':
            if not data.get('nombre'):
                return jsonify({
                    'status': 'error',
                    'message': 'nombre es requerido para personas naturales'
                }), 400
        elif tipo_cliente == 'EMPRESA':
            if not data.get('razon_social'):
                return jsonify({
                    'status': 'error',
                    'message': 'razon_social es requerida para empresas'
                }), 400
        else:
            return jsonify({
                'status': 'error',
                'message': 'tipo_cliente debe ser PERSONA o EMPRESA'
            }), 400
        
        cliente = ClienteService.create_cliente(data)
        return jsonify({
            'status': 'success',
            'message': 'Cliente creado exitosamente',
            'data': cliente.to_dict()
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

@cliente_bp.route('/clientes/<int:cliente_id>', methods=['PUT'])
def update_cliente(cliente_id):
    """Actualizar un cliente existente
    ---
    tags:
      - Clientes
    summary: Actualizar cliente existente
    description: Actualiza los datos de un cliente existente por su ID
    parameters:
      - name: cliente_id
        in: path
        type: integer
        required: true
        description: ID del cliente a actualizar
        example: 1
      - name: cliente
        in: body
        required: true
        schema:
          type: object
          properties:
            tipo_cliente:
              type: string
              enum: ['PERSONA', 'EMPRESA']
              example: "PERSONA"
              description: "Tipo de cliente"
            usuario:
              type: string
              example: "maria.gonzalez"
              description: "Nombre de usuario único"
            clave:
              type: string
              example: "nueva_clave"
              description: "Contraseña del cliente"
            nombre:
              type: string
              example: "María González"
              description: "Nombre completo (para PERSONA)"
            razon_social:
              type: string
              example: "Empresa XYZ S.A.S."
              description: "Razón social (para EMPRESA)"
            tipo_documento:
              type: string
              example: "CC"
              description: "Tipo de documento (para PERSONA)"
            numero_documento:
              type: string
              example: "12345678"
              description: "Número de documento (para PERSONA)"
            nit:
              type: string
              example: "900123456-7"
              description: "NIT (para EMPRESA)"
            correo:
              type: string
              format: email
              example: "maria@ejemplo.com"
              description: "Correo electrónico"
            telefono_movil:
              type: string
              example: "3001234567"
              description: "Número de teléfono móvil"
            ciudad:
              type: string
              example: "Bogotá"
              description: "Ciudad de residencia"
            direccion:
              type: string
              example: "Calle 123 #45-67"
              description: "Dirección completa"
            edad:
              type: integer
              example: 30
              description: "Edad (para PERSONA)"
            nombre_rep_legal:
              type: string
              example: "Juan Pérez"
              description: "Representante legal (para EMPRESA)"
    responses:
      200:
        description: Cliente actualizado exitosamente
        schema:
          type: object
          properties:
            status:
              type: string
              example: "success"
            message:
              type: string
              example: "Cliente actualizado exitosamente"
            data:
              type: object
              properties:
                id:
                  type: integer
                  example: 1
                tipo_cliente:
                  type: string
                  example: "PERSONA"
                usuario:
                  type: string
                  example: "maria.gonzalez"
                nombre:
                  type: string
                  example: "María González"
                correo:
                  type: string
                  example: "maria@ejemplo.com"
                fecha_creacion:
                  type: string
                  format: date-time
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
              example: "No se proporcionaron datos"
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
        data = request.get_json()
        if not data:
            return jsonify({
                'status': 'error',
                'message': 'No se proporcionaron datos'
            }), 400
        
        cliente = ClienteService.update_cliente(cliente_id, data)
        if cliente:
            return jsonify({
                'status': 'success',
                'message': 'Cliente actualizado exitosamente',
                'data': cliente.to_dict()
            }), 200
        else:
            return jsonify({
                'status': 'error',
                'message': 'Cliente no encontrado'
            }), 404
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@cliente_bp.route('/clientes/<int:cliente_id>', methods=['DELETE'])
def delete_cliente(cliente_id):
    """Eliminar un cliente
    ---
    tags:
      - Clientes
    summary: Eliminar cliente
    description: Elimina un cliente del sistema por su ID
    parameters:
      - name: cliente_id
        in: path
        type: integer
        required: true
        description: ID del cliente a eliminar
        example: 1
    responses:
      200:
        description: Cliente eliminado exitosamente
        schema:
          type: object
          properties:
            status:
              type: string
              example: "success"
            message:
              type: string
              example: "Cliente eliminado exitosamente"
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
        if ClienteService.delete_cliente(cliente_id):
            return jsonify({
                'status': 'success',
                'message': 'Cliente eliminado exitosamente'
            }), 200
        else:
            return jsonify({
                'status': 'error',
                'message': 'Cliente no encontrado'
            }), 404
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500 