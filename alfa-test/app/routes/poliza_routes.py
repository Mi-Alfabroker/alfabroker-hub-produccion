from flask import Blueprint, request, jsonify
from app.services.poliza_service import PolizaService
from app.models.poliza_model import Poliza

poliza_bp = Blueprint('poliza', __name__, url_prefix='/api')

# Crear una nueva póliza
@poliza_bp.route('/polizas', methods=['POST'])
def create_poliza():
    """
    Crear una nueva póliza
    ---
    tags:
      - Pólizas
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            opcion_seguro_id:
              type: integer
              description: ID de la opción de seguro a convertir en póliza
              example: 1
            tomador_id:
              type: integer
              description: ID del cliente tomador de la póliza
              example: 1
            beneficiario_id:
              type: integer
              description: ID del cliente beneficiario de la póliza
              example: 1
            asegurado_id:
              type: integer
              description: ID del cliente asegurado de la póliza
              example: 1
            fecha_inicio:
              type: string
              format: date
              description: Fecha de inicio de la póliza
              example: "2024-01-15"
            fecha_fin:
              type: string
              format: date
              description: Fecha de fin de la póliza
              example: "2025-01-15"
            forma_pago:
              type: string
              enum: [ANUAL, SEMESTRAL, TRIMESTRAL, MENSUAL]
              description: Forma de pago de la póliza
              example: "MENSUAL"
            observaciones:
              type: string
              description: Observaciones adicionales
              example: "Póliza con descuento por buen conductor"
          required:
            - opcion_seguro_id
            - tomador_id
            - beneficiario_id
            - asegurado_id
            - fecha_inicio
            - fecha_fin
            - forma_pago
    responses:
      201:
        description: Póliza creada exitosamente
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
            message:
              type: string
              example: "Póliza creada exitosamente"
            data:
              type: object
              properties:
                id:
                  type: integer
                  example: 1
                numero_poliza:
                  type: string
                  example: "POL-2024-001"
                opcion_seguro_id:
                  type: integer
                  example: 1
                tomador_id:
                  type: integer
                  example: 1
                beneficiario_id:
                  type: integer
                  example: 1
                asegurado_id:
                  type: integer
                  example: 1
                fecha_inicio:
                  type: string
                  format: date
                  example: "2024-01-15"
                fecha_fin:
                  type: string
                  format: date
                  example: "2025-01-15"
                forma_pago:
                  type: string
                  example: "MENSUAL"
                estado:
                  type: string
                  example: "ACTIVA"
                valor_prima:
                  type: number
                  format: float
                  example: 1200000.00
                valor_comision:
                  type: number
                  format: float
                  example: 120000.00
                fecha_creacion:
                  type: string
                  format: datetime
                  example: "2024-01-15T10:30:00"
                observaciones:
                  type: string
                  example: "Póliza con descuento por buen conductor"
      400:
        description: Error en los datos enviados
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: false
            message:
              type: string
              example: "La opción de seguro no existe"
      500:
        description: Error interno del servidor
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: false
            message:
              type: string
              example: "Error interno del servidor"
    """
    try:
        data = request.get_json()
        
        # Validar datos requeridos
        required_fields = ['opcion_seguro_id', 'tomador_id', 'beneficiario_id', 'asegurado_id', 'fecha_inicio', 'fecha_fin', 'forma_pago']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'message': f'El campo {field} es requerido'
                }), 400
        
        # Crear póliza
        poliza = PolizaService.create_poliza(data)
        
        if poliza:
            return jsonify({
                'success': True,
                'message': 'Póliza creada exitosamente',
                'data': poliza.to_dict()
            }), 201
        else:
            return jsonify({
                'success': False,
                'message': 'Error al crear la póliza'
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

# Obtener todas las pólizas
@poliza_bp.route('/polizas', methods=['GET'])
def get_all_polizas():
    """
    Obtener todas las pólizas
    ---
    tags:
      - Pólizas
    parameters:
      - in: query
        name: page
        type: integer
        description: Número de página (por defecto 1)
        example: 1
      - in: query
        name: per_page
        type: integer
        description: Cantidad de registros por página (por defecto 10)
        example: 10
      - in: query
        name: estado
        type: string
        enum: [ACTIVA, VENCIDA, CANCELADA, SUSPENDIDA]
        description: Filtrar por estado de póliza
        example: "ACTIVA"
      - in: query
        name: agente_id
        type: integer
        description: Filtrar por ID del agente
        example: 1
      - in: query
        name: aseguradora_id
        type: integer
        description: Filtrar por ID de la aseguradora
        example: 1
    responses:
      200:
        description: Lista de pólizas obtenida exitosamente
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
            message:
              type: string
              example: "Pólizas obtenidas exitosamente"
            data:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                    example: 1
                  numero_poliza:
                    type: string
                    example: "POL-2024-001"
                  opcion_seguro_id:
                    type: integer
                    example: 1
                  tomador_id:
                    type: integer
                    example: 1
                  beneficiario_id:
                    type: integer
                    example: 1
                  asegurado_id:
                    type: integer
                    example: 1
                  fecha_inicio:
                    type: string
                    format: date
                    example: "2024-01-15"
                  fecha_fin:
                    type: string
                    format: date
                    example: "2025-01-15"
                  forma_pago:
                    type: string
                    example: "MENSUAL"
                  estado:
                    type: string
                    example: "ACTIVA"
                  valor_prima:
                    type: number
                    format: float
                    example: 1200000.00
                  valor_comision:
                    type: number
                    format: float
                    example: 120000.00
                  fecha_creacion:
                    type: string
                    format: datetime
                    example: "2024-01-15T10:30:00"
                  observaciones:
                    type: string
                    example: "Póliza con descuento por buen conductor"
            pagination:
              type: object
              properties:
                page:
                  type: integer
                  example: 1
                per_page:
                  type: integer
                  example: 10
                total:
                  type: integer
                  example: 25
                pages:
                  type: integer
                  example: 3
      500:
        description: Error interno del servidor
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: false
            message:
              type: string
              example: "Error interno del servidor"
    """
    try:
        # Obtener parámetros de consulta
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        estado = request.args.get('estado')
        agente_id = request.args.get('agente_id', type=int)
        aseguradora_id = request.args.get('aseguradora_id', type=int)
        
        # Construir filtros
        filters = {}
        if estado:
            filters['estado'] = estado
        if agente_id:
            filters['agente_id'] = agente_id
        if aseguradora_id:
            filters['aseguradora_id'] = aseguradora_id
        
        # Obtener pólizas
        polizas_data = PolizaService.get_all_polizas(page, per_page, filters)
        
        return jsonify({
            'success': True,
            'message': 'Pólizas obtenidas exitosamente',
            'data': polizas_data['polizas'],
            'pagination': polizas_data['pagination']
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

# Obtener una póliza por ID
@poliza_bp.route('/polizas/<int:poliza_id>', methods=['GET'])
def get_poliza_by_id(poliza_id):
    """
    Obtener una póliza por ID
    ---
    tags:
      - Pólizas
    parameters:
      - in: path
        name: poliza_id
        type: integer
        required: true
        description: ID de la póliza
        example: 1
    responses:
      200:
        description: Póliza obtenida exitosamente
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
            message:
              type: string
              example: "Póliza obtenida exitosamente"
            data:
              type: object
              properties:
                id:
                  type: integer
                  example: 1
                numero_poliza:
                  type: string
                  example: "POL-2024-001"
                opcion_seguro_id:
                  type: integer
                  example: 1
                tomador_id:
                  type: integer
                  example: 1
                beneficiario_id:
                  type: integer
                  example: 1
                asegurado_id:
                  type: integer
                  example: 1
                fecha_inicio:
                  type: string
                  format: date
                  example: "2024-01-15"
                fecha_fin:
                  type: string
                  format: date
                  example: "2025-01-15"
                forma_pago:
                  type: string
                  example: "MENSUAL"
                estado:
                  type: string
                  example: "ACTIVA"
                valor_prima:
                  type: number
                  format: float
                  example: 1200000.00
                valor_comision:
                  type: number
                  format: float
                  example: 120000.00
                fecha_creacion:
                  type: string
                  format: datetime
                  example: "2024-01-15T10:30:00"
                observaciones:
                  type: string
                  example: "Póliza con descuento por buen conductor"
                opcion_seguro:
                  type: object
                  description: Detalles de la opción de seguro asociada
                planes_pago:
                  type: array
                  items:
                    type: object
                    description: Planes de pago asociados
      404:
        description: Póliza no encontrada
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: false
            message:
              type: string
              example: "Póliza no encontrada"
      500:
        description: Error interno del servidor
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: false
            message:
              type: string
              example: "Error interno del servidor"
    """
    try:
        poliza = PolizaService.get_poliza_by_id(poliza_id)
        
        if not poliza:
            return jsonify({
                'success': False,
                'message': 'Póliza no encontrada'
            }), 404
        
        return jsonify({
            'success': True,
            'message': 'Póliza obtenida exitosamente',
            'data': poliza.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

# Actualizar una póliza
@poliza_bp.route('/polizas/<int:poliza_id>', methods=['PUT'])
def update_poliza(poliza_id):
    """
    Actualizar una póliza
    ---
    tags:
      - Pólizas
    parameters:
      - in: path
        name: poliza_id
        type: integer
        required: true
        description: ID de la póliza
        example: 1
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            tomador_id:
              type: integer
              description: ID del cliente tomador de la póliza
              example: 1
            beneficiario_id:
              type: integer
              description: ID del cliente beneficiario de la póliza
              example: 1
            asegurado_id:
              type: integer
              description: ID del cliente asegurado de la póliza
              example: 1
            fecha_inicio:
              type: string
              format: date
              description: Fecha de inicio de la póliza
              example: "2024-01-15"
            fecha_fin:
              type: string
              format: date
              description: Fecha de fin de la póliza
              example: "2025-01-15"
            forma_pago:
              type: string
              enum: [ANUAL, SEMESTRAL, TRIMESTRAL, MENSUAL]
              description: Forma de pago de la póliza
              example: "MENSUAL"
            estado:
              type: string
              enum: [ACTIVA, VENCIDA, CANCELADA, SUSPENDIDA]
              description: Estado de la póliza
              example: "ACTIVA"
            observaciones:
              type: string
              description: Observaciones adicionales
              example: "Póliza con descuento por buen conductor"
    responses:
      200:
        description: Póliza actualizada exitosamente
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
            message:
              type: string
              example: "Póliza actualizada exitosamente"
            data:
              type: object
              properties:
                id:
                  type: integer
                  example: 1
                numero_poliza:
                  type: string
                  example: "POL-2024-001"
                opcion_seguro_id:
                  type: integer
                  example: 1
                tomador_id:
                  type: integer
                  example: 1
                beneficiario_id:
                  type: integer
                  example: 1
                asegurado_id:
                  type: integer
                  example: 1
                fecha_inicio:
                  type: string
                  format: date
                  example: "2024-01-15"
                fecha_fin:
                  type: string
                  format: date
                  example: "2025-01-15"
                forma_pago:
                  type: string
                  example: "MENSUAL"
                estado:
                  type: string
                  example: "ACTIVA"
                valor_prima:
                  type: number
                  format: float
                  example: 1200000.00
                valor_comision:
                  type: number
                  format: float
                  example: 120000.00
                fecha_creacion:
                  type: string
                  format: datetime
                  example: "2024-01-15T10:30:00"
                observaciones:
                  type: string
                  example: "Póliza con descuento por buen conductor"
      404:
        description: Póliza no encontrada
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: false
            message:
              type: string
              example: "Póliza no encontrada"
      500:
        description: Error interno del servidor
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: false
            message:
              type: string
              example: "Error interno del servidor"
    """
    try:
        data = request.get_json()
        
        poliza = PolizaService.update_poliza(poliza_id, data)
        
        if not poliza:
            return jsonify({
                'success': False,
                'message': 'Póliza no encontrada'
            }), 404
        
        return jsonify({
            'success': True,
            'message': 'Póliza actualizada exitosamente',
            'data': poliza.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

# Cancelar una póliza
@poliza_bp.route('/polizas/<int:poliza_id>/cancelar', methods=['POST'])
def cancel_poliza(poliza_id):
    """
    Cancelar una póliza
    ---
    tags:
      - Pólizas
    parameters:
      - in: path
        name: poliza_id
        type: integer
        required: true
        description: ID de la póliza
        example: 1
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            motivo:
              type: string
              description: Motivo de la cancelación
              example: "Solicitud del cliente"
            fecha_cancelacion:
              type: string
              format: date
              description: Fecha de cancelación (por defecto hoy)
              example: "2024-06-15"
          required:
            - motivo
    responses:
      200:
        description: Póliza cancelada exitosamente
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
            message:
              type: string
              example: "Póliza cancelada exitosamente"
            data:
              type: object
              properties:
                id:
                  type: integer
                  example: 1
                numero_poliza:
                  type: string
                  example: "POL-2024-001"
                estado:
                  type: string
                  example: "CANCELADA"
                fecha_cancelacion:
                  type: string
                  format: date
                  example: "2024-06-15"
                motivo_cancelacion:
                  type: string
                  example: "Solicitud del cliente"
      404:
        description: Póliza no encontrada
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: false
            message:
              type: string
              example: "Póliza no encontrada"
      400:
        description: Error en los datos enviados
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: false
            message:
              type: string
              example: "La póliza ya está cancelada"
      500:
        description: Error interno del servidor
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: false
            message:
              type: string
              example: "Error interno del servidor"
    """
    try:
        data = request.get_json()
        
        if not data or 'motivo' not in data:
            return jsonify({
                'success': False,
                'message': 'El motivo de cancelación es requerido'
            }), 400
        
        poliza = PolizaService.cancel_poliza(poliza_id, data['motivo'], data.get('fecha_cancelacion'))
        
        if not poliza:
            return jsonify({
                'success': False,
                'message': 'Póliza no encontrada'
            }), 404
        
        return jsonify({
            'success': True,
            'message': 'Póliza cancelada exitosamente',
            'data': poliza.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

# Obtener plan de pagos de una póliza
@poliza_bp.route('/polizas/<int:poliza_id>/plan-pagos', methods=['GET'])
def get_plan_pagos(poliza_id):
    """
    Obtener plan de pagos de una póliza
    ---
    tags:
      - Pólizas
    parameters:
      - in: path
        name: poliza_id
        type: integer
        required: true
        description: ID de la póliza
        example: 1
    responses:
      200:
        description: Plan de pagos obtenido exitosamente
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
            message:
              type: string
              example: "Plan de pagos obtenido exitosamente"
            data:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                    example: 1
                  poliza_id:
                    type: integer
                    example: 1
                  numero_cuota:
                    type: integer
                    example: 1
                  fecha_vencimiento:
                    type: string
                    format: date
                    example: "2024-02-15"
                  valor_cuota:
                    type: number
                    format: float
                    example: 100000.00
                  estado:
                    type: string
                    example: "PENDIENTE"
                  fecha_pago:
                    type: string
                    format: date
                    example: null
                  valor_pagado:
                    type: number
                    format: float
                    example: 0.00
                  observaciones:
                    type: string
                    example: "Primera cuota"
      404:
        description: Póliza no encontrada
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: false
            message:
              type: string
              example: "Póliza no encontrada"
      500:
        description: Error interno del servidor
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: false
            message:
              type: string
              example: "Error interno del servidor"
    """
    try:
        plan_pagos = PolizaService.get_plan_pagos(poliza_id)
        
        if plan_pagos is None:
            return jsonify({
                'success': False,
                'message': 'Póliza no encontrada'
            }), 404
        
        return jsonify({
            'success': True,
            'message': 'Plan de pagos obtenido exitosamente',
            'data': [pago.to_dict() for pago in plan_pagos]
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

# Registrar pago de una cuota
@poliza_bp.route('/polizas/<int:poliza_id>/pagos/<int:cuota_id>', methods=['POST'])
def register_payment(poliza_id, cuota_id):
    """
    Registrar pago de una cuota
    ---
    tags:
      - Pólizas
    parameters:
      - in: path
        name: poliza_id
        type: integer
        required: true
        description: ID de la póliza
        example: 1
      - in: path
        name: cuota_id
        type: integer
        required: true
        description: ID de la cuota
        example: 1
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            valor_pagado:
              type: number
              format: float
              description: Valor pagado
              example: 100000.00
            fecha_pago:
              type: string
              format: date
              description: Fecha del pago (por defecto hoy)
              example: "2024-02-15"
            observaciones:
              type: string
              description: Observaciones del pago
              example: "Pago realizado en efectivo"
          required:
            - valor_pagado
    responses:
      200:
        description: Pago registrado exitosamente
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
            message:
              type: string
              example: "Pago registrado exitosamente"
            data:
              type: object
              properties:
                id:
                  type: integer
                  example: 1
                poliza_id:
                  type: integer
                  example: 1
                numero_cuota:
                  type: integer
                  example: 1
                fecha_vencimiento:
                  type: string
                  format: date
                  example: "2024-02-15"
                valor_cuota:
                  type: number
                  format: float
                  example: 100000.00
                estado:
                  type: string
                  example: "PAGADA"
                fecha_pago:
                  type: string
                  format: date
                  example: "2024-02-15"
                valor_pagado:
                  type: number
                  format: float
                  example: 100000.00
                observaciones:
                  type: string
                  example: "Pago realizado en efectivo"
      404:
        description: Póliza o cuota no encontrada
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: false
            message:
              type: string
              example: "Cuota no encontrada"
      400:
        description: Error en los datos enviados
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: false
            message:
              type: string
              example: "El valor pagado es requerido"
      500:
        description: Error interno del servidor
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: false
            message:
              type: string
              example: "Error interno del servidor"
    """
    try:
        data = request.get_json()
        
        if not data or 'valor_pagado' not in data:
            return jsonify({
                'success': False,
                'message': 'El valor pagado es requerido'
            }), 400
        
        cuota = PolizaService.register_payment(poliza_id, cuota_id, data)
        
        if not cuota:
            return jsonify({
                'success': False,
                'message': 'Cuota no encontrada'
            }), 404
        
        return jsonify({
            'success': True,
            'message': 'Pago registrado exitosamente',
            'data': cuota.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

# Obtener pólizas vencidas
@poliza_bp.route('/polizas/vencidas', methods=['GET'])
def get_expired_polizas():
    """
    Obtener pólizas vencidas
    ---
    tags:
      - Pólizas
    parameters:
      - in: query
        name: dias_vencimiento
        type: integer
        description: Días de vencimiento para considerar (por defecto 30)
        example: 30
      - in: query
        name: agente_id
        type: integer
        description: Filtrar por ID del agente
        example: 1
    responses:
      200:
        description: Pólizas vencidas obtenidas exitosamente
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
            message:
              type: string
              example: "Pólizas vencidas obtenidas exitosamente"
            data:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                    example: 1
                  numero_poliza:
                    type: string
                    example: "POL-2024-001"
                  fecha_fin:
                    type: string
                    format: date
                    example: "2024-01-15"
                  dias_vencidos:
                    type: integer
                    example: 15
                  valor_prima:
                    type: number
                    format: float
                    example: 1200000.00
                  tomador:
                    type: object
                    description: Datos del tomador
                  agente:
                    type: object
                    description: Datos del agente
      500:
        description: Error interno del servidor
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: false
            message:
              type: string
              example: "Error interno del servidor"
    """
    try:
        dias_vencimiento = request.args.get('dias_vencimiento', 30, type=int)
        agente_id = request.args.get('agente_id', type=int)
        
        polizas_vencidas = PolizaService.get_expired_polizas(dias_vencimiento, agente_id)
        
        return jsonify({
            'success': True,
            'message': 'Pólizas vencidas obtenidas exitosamente',
            'data': [poliza.to_dict() for poliza in polizas_vencidas]
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

# Obtener estadísticas de pólizas
@poliza_bp.route('/polizas/estadisticas', methods=['GET'])
def get_polizas_statistics():
    """
    Obtener estadísticas de pólizas
    ---
    tags:
      - Pólizas
    parameters:
      - in: query
        name: fecha_inicio
        type: string
        format: date
        description: Fecha de inicio para el rango de estadísticas
        example: "2024-01-01"
      - in: query
        name: fecha_fin
        type: string
        format: date
        description: Fecha de fin para el rango de estadísticas
        example: "2024-12-31"
      - in: query
        name: agente_id
        type: integer
        description: Filtrar por ID del agente
        example: 1
      - in: query
        name: aseguradora_id
        type: integer
        description: Filtrar por ID de la aseguradora
        example: 1
    responses:
      200:
        description: Estadísticas obtenidas exitosamente
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
            message:
              type: string
              example: "Estadísticas obtenidas exitosamente"
            data:
              type: object
              properties:
                total_polizas:
                  type: integer
                  example: 150
                polizas_activas:
                  type: integer
                  example: 120
                polizas_vencidas:
                  type: integer
                  example: 20
                polizas_canceladas:
                  type: integer
                  example: 10
                valor_total_primas:
                  type: number
                  format: float
                  example: 180000000.00
                valor_total_comisiones:
                  type: number
                  format: float
                  example: 18000000.00
                por_tipo_bien:
                  type: object
                  properties:
                    hogar:
                      type: integer
                      example: 50
                    vehiculo:
                      type: integer
                      example: 80
                    copropiedad:
                      type: integer
                      example: 15
                    otro:
                      type: integer
                      example: 5
                por_aseguradora:
                  type: array
                  items:
                    type: object
                    properties:
                      aseguradora:
                        type: string
                        example: "Seguros Alfa"
                      cantidad:
                        type: integer
                        example: 75
                      porcentaje:
                        type: number
                        format: float
                        example: 50.0
      500:
        description: Error interno del servidor
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: false
            message:
              type: string
              example: "Error interno del servidor"
    """
    try:
        fecha_inicio = request.args.get('fecha_inicio')
        fecha_fin = request.args.get('fecha_fin')
        agente_id = request.args.get('agente_id', type=int)
        aseguradora_id = request.args.get('aseguradora_id', type=int)
        
        filtros = {}
        if fecha_inicio:
            filtros['fecha_inicio'] = fecha_inicio
        if fecha_fin:
            filtros['fecha_fin'] = fecha_fin
        if agente_id:
            filtros['agente_id'] = agente_id
        if aseguradora_id:
            filtros['aseguradora_id'] = aseguradora_id
        
        estadisticas = PolizaService.get_statistics(filtros)
        
        return jsonify({
            'success': True,
            'message': 'Estadísticas obtenidas exitosamente',
            'data': estadisticas
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500 