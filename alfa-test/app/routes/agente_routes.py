from flask import Blueprint, jsonify, request
from app.services.agente_service import AgenteService
from app.services.agente_cliente_service import AgenteClienteService
from datetime import datetime
from flasgger import swag_from

agente_bp = Blueprint('agente', __name__, url_prefix='/api')

@agente_bp.route('/health', methods=['GET'])
def health_check():
    """Endpoint para verificar si la API está en línea
    ---
    tags:
      - Health
    summary: Verificar estado de la API
    description: Endpoint para comprobar que la API está funcionando correctamente
    responses:
      200:
        description: API funcionando correctamente
        schema:
          type: object
          properties:
            status:
              type: string
              example: "online"
            message:
              type: string
              example: "API está funcionando correctamente"
            timestamp:
              type: string
              format: date-time
              example: "2024-01-15T10:30:00.000000"
            version:
              type: string
              example: "1.0.0"
    """
    return jsonify({
        'status': 'online',
        'message': 'API está funcionando correctamente',
        'timestamp': datetime.utcnow().isoformat(),
        'version': '1.0.0'
    }), 200

@agente_bp.route('/agentes', methods=['GET'])
def get_agentes():
    """Obtener todos los agentes
    ---
    tags:
      - Agentes
    summary: Obtener lista de agentes
    description: Obtiene todos los agentes con filtros opcionales por rol o estado activo
    parameters:
      - name: rol
        in: query
        type: string
        enum: ['super_admin', 'admin', 'agente']
        description: Filtrar agentes por rol
      - name: activo
        in: query
        type: string
        enum: ['true', 'false']
        description: Filtrar solo agentes activos (true) o todos (false)
    responses:
      200:
        description: Lista de agentes obtenida exitosamente
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
                  nombre:
                    type: string
                    example: "Juan Pérez"
                  correo:
                    type: string
                    example: "juan.perez@davivienda.com"
                  usuario:
                    type: string
                    example: "juan.perez"
                  rol:
                    type: string
                    example: "agente"
                  activo:
                    type: boolean
                    example: true
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
              example: "El rol debe ser super_admin, admin o agente"
      500:
        description: Error interno del servidor
    """
    try:
        rol = request.args.get('rol')  # Filtrar por rol si se proporciona
        activo = request.args.get('activo')  # Filtrar por estado activo
        
        if rol:
            if rol not in ['super_admin', 'admin', 'agente']:
                return jsonify({
                    'status': 'error',
                    'message': 'El rol debe ser super_admin, admin o agente'
                }), 400
            agentes = AgenteService.get_agentes_by_rol(rol)
        elif activo == 'true':
            agentes = AgenteService.get_agentes_activos()
        else:
            agentes = AgenteService.get_all_agentes()
            
        return jsonify({
            'status': 'success',
            'data': [agente.to_dict() for agente in agentes]
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@agente_bp.route('/agentes/<int:agente_id>', methods=['GET'])
def get_agente(agente_id):
    """Obtener un agente por ID
    ---
    tags:
      - Agentes
    summary: Obtener agente específico
    description: Obtiene los datos de un agente específico por su ID
    parameters:
      - name: agente_id
        in: path
        type: integer
        required: true
        description: ID del agente a obtener
        example: 1
    responses:
      200:
        description: Agente obtenido exitosamente
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
                nombre:
                  type: string
                  example: "Juan Pérez"
                correo:
                  type: string
                  example: "juan.perez@davivienda.com"
                usuario:
                  type: string
                  example: "juan.perez"
                rol:
                  type: string
                  example: "agente"
                activo:
                  type: boolean
                  example: true
                fecha_creacion:
                  type: string
                  format: date-time
      404:
        description: Agente no encontrado
        schema:
          type: object
          properties:
            status:
              type: string
              example: "error"
            message:
              type: string
              example: "Agente no encontrado"
      500:
        description: Error interno del servidor
    """
    try:
        agente = AgenteService.get_agente_by_id(agente_id)
        if agente:
            return jsonify({
                'status': 'success',
                'data': agente.to_dict()
            }), 200
        else:
            return jsonify({
                'status': 'error',
                'message': 'Agente no encontrado'
            }), 404
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@agente_bp.route('/agentes', methods=['POST'])
def create_agente():
    """Crear un nuevo agente
    ---
    tags:
      - Agentes
    summary: Crear nuevo agente
    description: Crea un nuevo agente de seguros en el sistema
    parameters:
      - name: agente
        in: body
        required: true
        schema:
          type: object
          required:
            - nombre
            - correo
            - usuario
            - clave
            - rol
          properties:
            nombre:
              type: string
              example: "Juan Pérez"
              description: "Nombre completo del agente"
            correo:
              type: string
              format: email
              example: "juan.perez@davivienda.com"
              description: "Correo electrónico único del agente"
            usuario:
              type: string
              example: "juan.perez"
              description: "Nombre de usuario único"
            clave:
              type: string
              example: "mi_clave_segura"
              description: "Contraseña del agente"
            rol:
              type: string
              enum: ['super_admin', 'admin', 'agente']
              example: "agente"
              description: "Rol del agente en el sistema"
            activo:
              type: boolean
              example: true
              description: "Estado activo del agente (opcional, por defecto true)"
    responses:
      201:
        description: Agente creado exitosamente
        schema:
          type: object
          properties:
            status:
              type: string
              example: "success"
            message:
              type: string
              example: "Agente creado exitosamente"
            data:
              type: object
              properties:
                id:
                  type: integer
                  example: 1
                nombre:
                  type: string
                  example: "Juan Pérez"
                correo:
                  type: string
                  example: "juan.perez@davivienda.com"
                usuario:
                  type: string
                  example: "juan.perez"
                rol:
                  type: string
                  example: "agente"
                activo:
                  type: boolean
                  example: true
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
              example: "nombre es requerido"
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
            
        required_fields = ['nombre', 'correo', 'usuario', 'clave', 'rol']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'status': 'error',
                    'message': f'{field} es requerido'
                }), 400
        
        agente = AgenteService.create_agente(data)
        return jsonify({
            'status': 'success',
            'message': 'Agente creado exitosamente',
            'data': agente.to_dict()
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

@agente_bp.route('/agentes/<int:agente_id>', methods=['PUT'])
def update_agente(agente_id):
    """Actualizar un agente existente
    ---
    tags:
      - Agentes
    summary: Actualizar agente existente
    description: Actualiza los datos de un agente existente por su ID
    parameters:
      - name: agente_id
        in: path
        type: integer
        required: true
        description: ID del agente a actualizar
        example: 1
      - name: agente
        in: body
        required: true
        schema:
          type: object
          properties:
            nombre:
              type: string
              example: "Juan Pérez Actualizado"
              description: "Nombre completo del agente"
            correo:
              type: string
              format: email
              example: "juan.perez.nuevo@davivienda.com"
              description: "Correo electrónico del agente"
            usuario:
              type: string
              example: "juan.perez.nuevo"
              description: "Nombre de usuario único"
            clave:
              type: string
              example: "nueva_clave_segura"
              description: "Nueva contraseña del agente"
            telefono:
              type: string
              example: "3001234567"
              description: "Número de teléfono"
            rol:
              type: string
              enum: ['super_admin', 'admin', 'agente']
              example: "admin"
              description: "Rol del agente en el sistema"
            activo:
              type: boolean
              example: true
              description: "Estado activo del agente"
    responses:
      200:
        description: Agente actualizado exitosamente
        schema:
          type: object
          properties:
            status:
              type: string
              example: "success"
            message:
              type: string
              example: "Agente actualizado exitosamente"
            data:
              type: object
              properties:
                id:
                  type: integer
                  example: 1
                nombre:
                  type: string
                  example: "Juan Pérez Actualizado"
                correo:
                  type: string
                  example: "juan.perez.nuevo@davivienda.com"
                usuario:
                  type: string
                  example: "juan.perez.nuevo"
                rol:
                  type: string
                  example: "admin"
                activo:
                  type: boolean
                  example: true
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
        description: Agente no encontrado
        schema:
          type: object
          properties:
            status:
              type: string
              example: "error"
            message:
              type: string
              example: "Agente no encontrado"
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
        
        agente = AgenteService.update_agente(agente_id, data)
        if agente:
            return jsonify({
                'status': 'success',
                'message': 'Agente actualizado exitosamente',
                'data': agente.to_dict()
            }), 200
        else:
            return jsonify({
                'status': 'error',
                'message': 'Agente no encontrado'
            }), 404
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@agente_bp.route('/agentes/<int:agente_id>', methods=['DELETE'])
def delete_agente(agente_id):
    """Eliminar un agente
    ---
    tags:
      - Agentes
    summary: Eliminar agente
    description: Elimina un agente del sistema por su ID
    parameters:
      - name: agente_id
        in: path
        type: integer
        required: true
        description: ID del agente a eliminar
        example: 1
    responses:
      200:
        description: Agente eliminado exitosamente
        schema:
          type: object
          properties:
            status:
              type: string
              example: "success"
            message:
              type: string
              example: "Agente eliminado exitosamente"
      404:
        description: Agente no encontrado
        schema:
          type: object
          properties:
            status:
              type: string
              example: "error"
            message:
              type: string
              example: "Agente no encontrado"
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
        if AgenteService.delete_agente(agente_id):
            return jsonify({
                'status': 'success',
                'message': 'Agente eliminado exitosamente'
            }), 200
        else:
            return jsonify({
                'status': 'error',
                'message': 'Agente no encontrado'
            }), 404
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

# Endpoints para manejo de asignaciones agente-cliente
@agente_bp.route('/agentes/<int:agente_id>/clientes', methods=['GET'])
def get_clientes_agente(agente_id):
    """Obtener todos los clientes asignados a un agente
    ---
    tags:
      - Agentes
    summary: Obtener clientes asignados a un agente
    description: Obtiene la lista de todos los clientes que están asignados a un agente específico
    parameters:
      - name: agente_id
        in: path
        type: integer
        required: true
        description: ID del agente del cual obtener los clientes asignados
        example: 1
    responses:
      200:
        description: Lista de clientes asignados obtenida exitosamente
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
      404:
        description: Agente no encontrado
        schema:
          type: object
          properties:
            status:
              type: string
              example: "error"
            message:
              type: string
              example: "Agente no encontrado"
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
        clientes = AgenteClienteService.get_clientes_by_agente(agente_id)
        return jsonify({
            'status': 'success',
            'data': [cliente.to_dict() for cliente in clientes]
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@agente_bp.route('/agentes/<int:agente_id>/clientes/<int:cliente_id>', methods=['POST'])
def asignar_cliente(agente_id, cliente_id):
    """Asignar un cliente a un agente
    ---
    tags:
      - Agentes
    summary: Asignar cliente a agente
    description: Crea una asignación entre un agente y un cliente específico
    parameters:
      - name: agente_id
        in: path
        type: integer
        required: true
        description: ID del agente
        example: 1
      - name: cliente_id
        in: path
        type: integer
        required: true
        description: ID del cliente a asignar
        example: 1
    responses:
      201:
        description: Cliente asignado exitosamente
        schema:
          type: object
          properties:
            status:
              type: string
              example: "success"
            message:
              type: string
              example: "Cliente asignado exitosamente"
            data:
              type: object
              properties:
                agente_id:
                  type: integer
                  example: 1
                cliente_id:
                  type: integer
                  example: 1
                fecha_asignacion:
                  type: string
                  format: date-time
                  example: "2024-01-15T10:30:00"
      400:
        description: Error en la asignación (ya existe o agente/cliente no encontrado)
        schema:
          type: object
          properties:
            status:
              type: string
              example: "error"
            message:
              type: string
              example: "No se pudo crear la asignación (ya existe o agente/cliente no encontrado)"
      500:
        description: Error interno del servidor
    """
    try:
        asignacion = AgenteClienteService.crear_asignacion(agente_id, cliente_id)
        if asignacion:
            return jsonify({
                'status': 'success',
                'message': 'Cliente asignado exitosamente',
                'data': asignacion.to_dict()
            }), 201
        else:
            return jsonify({
                'status': 'error',
                'message': 'No se pudo crear la asignación (ya existe o agente/cliente no encontrado)'
            }), 400
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@agente_bp.route('/agentes/<int:agente_id>/clientes/<int:cliente_id>', methods=['DELETE'])
def desasignar_cliente(agente_id, cliente_id):
    """Desasignar un cliente de un agente
    ---
    tags:
      - Agentes
    summary: Desasignar cliente de agente
    description: Elimina la asignación entre un agente y un cliente específico
    parameters:
      - name: agente_id
        in: path
        type: integer
        required: true
        description: ID del agente
        example: 1
      - name: cliente_id
        in: path
        type: integer
        required: true
        description: ID del cliente a desasignar
        example: 1
    responses:
      200:
        description: Cliente desasignado exitosamente
        schema:
          type: object
          properties:
            status:
              type: string
              example: "success"
            message:
              type: string
              example: "Cliente desasignado exitosamente"
      404:
        description: Asignación no encontrada
        schema:
          type: object
          properties:
            status:
              type: string
              example: "error"
            message:
              type: string
              example: "Asignación no encontrada"
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
        if AgenteClienteService.eliminar_asignacion(agente_id, cliente_id):
            return jsonify({
                'status': 'success',
                'message': 'Cliente desasignado exitosamente'
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