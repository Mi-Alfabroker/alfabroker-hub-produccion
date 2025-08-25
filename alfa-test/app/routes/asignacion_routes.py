from flask import Blueprint, jsonify, request
from app.services.agente_cliente_service import AgenteClienteService
from flasgger import swag_from

asignacion_bp = Blueprint('asignacion', __name__, url_prefix='/api')

@asignacion_bp.route('/asignaciones', methods=['GET'])
def get_all_asignaciones():
    """Obtener todas las asignaciones agente-cliente
    ---
    tags:
      - Asignaciones
    summary: Obtener todas las asignaciones
    description: Obtiene todas las asignaciones entre agentes y clientes del sistema
    responses:
      200:
        description: Lista de asignaciones obtenida exitosamente
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
                  agente:
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
                      rol:
                        type: string
                        example: "agente"
                  cliente:
                    type: object
                    properties:
                      id:
                        type: integer
                        example: 1
                      nombre:
                        type: string
                        example: "María González"
                      tipo_cliente:
                        type: string
                        example: "PERSONA"
                      correo:
                        type: string
                        example: "maria@ejemplo.com"
      500:
        description: Error interno del servidor
    """
    try:
        asignaciones = AgenteClienteService.get_all_asignaciones()
        return jsonify({
            'status': 'success',
            'data': [asignacion.to_dict() for asignacion in asignaciones]
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@asignacion_bp.route('/clientes/<int:cliente_id>/agentes', methods=['GET'])
def get_agentes_by_cliente(cliente_id):
    """Obtener todos los agentes asignados a un cliente
    ---
    tags:
      - Asignaciones
    summary: Obtener agentes asignados a un cliente
    description: Obtiene la lista de todos los agentes que están asignados a un cliente específico
    parameters:
      - name: cliente_id
        in: path
        type: integer
        required: true
        description: ID del cliente del cual obtener los agentes asignados
        example: 1
    responses:
      200:
        description: Lista de agentes asignados obtenida exitosamente
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
        agentes = AgenteClienteService.get_agentes_by_cliente(cliente_id)
        return jsonify({
            'status': 'success',
            'data': [agente.to_dict() for agente in agentes]
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@asignacion_bp.route('/asignaciones', methods=['POST'])
def crear_asignacion():
    """Crear una nueva asignación agente-cliente
    ---
    tags:
      - Asignaciones
    summary: Crear nueva asignación
    description: Crea una nueva asignación entre un agente y un cliente
    parameters:
      - name: asignacion
        in: body
        required: true
        schema:
          type: object
          required:
            - agente_id
            - cliente_id
          properties:
            agente_id:
              type: integer
              example: 1
              description: "ID del agente a asignar"
            cliente_id:
              type: integer
              example: 1
              description: "ID del cliente a asignar"
    responses:
      201:
        description: Asignación creada exitosamente
        schema:
          type: object
          properties:
            status:
              type: string
              example: "success"
            message:
              type: string
              example: "Asignación creada exitosamente"
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
        description: Datos inválidos o asignación ya existe
        schema:
          type: object
          properties:
            status:
              type: string
              example: "error"
            message:
              type: string
              example: "agente_id y cliente_id son requeridos"
      500:
        description: Error interno del servidor
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'status': 'error',
                'message': 'No se proporcionaron datos'
            }), 400
        
        agente_id = data.get('agente_id')
        cliente_id = data.get('cliente_id')
        
        if not agente_id or not cliente_id:
            return jsonify({
                'status': 'error',
                'message': 'agente_id y cliente_id son requeridos'
            }), 400
        
        asignacion = AgenteClienteService.crear_asignacion(agente_id, cliente_id)
        if asignacion:
            return jsonify({
                'status': 'success',
                'message': 'Asignación creada exitosamente',
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

@asignacion_bp.route('/asignaciones/<int:agente_id>/<int:cliente_id>', methods=['DELETE'])
def eliminar_asignacion(agente_id, cliente_id):
    """Eliminar una asignación específica
    ---
    tags:
      - Asignaciones
    summary: Eliminar asignación específica
    description: Elimina una asignación específica entre un agente y un cliente
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
        description: ID del cliente
        example: 1
    responses:
      200:
        description: Asignación eliminada exitosamente
        schema:
          type: object
          properties:
            status:
              type: string
              example: "success"
            message:
              type: string
              example: "Asignación eliminada exitosamente"
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
                'message': 'Asignación eliminada exitosamente'
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