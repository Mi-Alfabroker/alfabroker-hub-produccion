from app import db
from app.models import Poliza, PolizaPlanPago, OpcionSeguro
from sqlalchemy.exc import IntegrityError
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

class PolizaService:
    
    @staticmethod
    def crear_poliza_desde_opcion(opcion_seguro_id, datos_poliza):
        """Crear una póliza a partir de una opción de seguro aceptada"""
        try:
            # Validar que la opción de seguro existe
            opcion = OpcionSeguro.query.get(opcion_seguro_id)
            if not opcion:
                return {'error': 'Opción de seguro no encontrada'}, 404
            
            # Validar que la opción puede convertirse a póliza
            if not opcion.puede_convertirse_a_poliza():
                return {'error': 'La opción de seguro no puede convertirse a póliza'}, 400
            
            # Validar datos requeridos
            if not datos_poliza.get('fecha_inicio_vigencia'):
                return {'error': 'La fecha de inicio de vigencia es requerida'}, 400
            if not datos_poliza.get('fecha_fin_vigencia'):
                return {'error': 'La fecha de fin de vigencia es requerida'}, 400
            if not datos_poliza.get('medio_pago'):
                return {'error': 'El medio de pago es requerido'}, 400
            
            # Parsear fechas
            fecha_inicio = datetime.strptime(datos_poliza['fecha_inicio_vigencia'], '%Y-%m-%d').date()
            fecha_fin = datetime.strptime(datos_poliza['fecha_fin_vigencia'], '%Y-%m-%d').date()
            
            if fecha_fin <= fecha_inicio:
                return {'error': 'La fecha de fin debe ser posterior a la fecha de inicio'}, 400
            
            # Calcular valores financieros
            valores_calculados = PolizaService._calcular_valores_poliza(opcion, datos_poliza)
            
            # Crear la póliza
            consecutivo = Poliza.generar_consecutivo()
            poliza = Poliza(
                opcion_seguro_id=opcion_seguro_id,
                consecutivo_poliza=consecutivo,
                numero_poliza_aseguradora=datos_poliza.get('numero_poliza_aseguradora'),
                fecha_inicio_vigencia=fecha_inicio,
                fecha_fin_vigencia=fecha_fin,
                medio_pago=datos_poliza['medio_pago'],
                estado_cartera=datos_poliza.get('estado_cartera', 'Al Día'),
                valor_prima_neta=valores_calculados['valor_prima_neta'],
                valor_otros_costos=valores_calculados['valor_otros_costos'],
                valor_iva=valores_calculados['valor_iva'],
                ingreso_comision_percibido=valores_calculados['ingreso_comision_percibido']
            )
            
            db.session.add(poliza)
            db.session.flush()  # Para obtener el ID
            
            # Crear plan de pagos si se especifica
            if datos_poliza.get('generar_plan_pagos', True):
                plan_pagos = PolizaService._generar_plan_pagos(
                    poliza.id,
                    valores_calculados['valor_prima_total'],
                    datos_poliza.get('numero_cuotas', 1),
                    fecha_inicio,
                    opcion.financiacion_seleccionada,
                    datos_poliza.get('frecuencia_pago', 'mensual')
                )
                
                for cuota in plan_pagos:
                    db.session.add(cuota)
            
            db.session.commit()
            
            return {
                'message': 'Póliza creada exitosamente',
                'poliza': poliza.to_dict(include_plan_pagos=True)
            }, 201
            
        except ValueError as e:
            return {'error': f'Error en formato de fecha: {str(e)}'}, 400
        except IntegrityError as e:
            db.session.rollback()
            return {'error': 'Error de integridad en la base de datos'}, 400
        except Exception as e:
            db.session.rollback()
            return {'error': f'Error interno del servidor: {str(e)}'}, 500
    
    @staticmethod
    def _calcular_valores_poliza(opcion, datos_poliza):
        """Calcular valores financieros de la póliza"""
        # Usar el valor de prima de la opción o el especificado
        valor_prima_total = datos_poliza.get('valor_prima_total') or opcion.valor_prima_total
        if not valor_prima_total:
            raise ValueError("No se pudo determinar el valor de la prima")
        
        valor_prima_total = float(valor_prima_total)
        
        # Calcular IVA (19%)
        valor_prima_neta = valor_prima_total / 1.19
        valor_iva = valor_prima_total - valor_prima_neta
        
        # Otros costos
        valor_otros_costos = float(datos_poliza.get('valor_otros_costos', 0))
        
        # Calcular comisión total
        ingreso_comision_percibido = opcion.calcular_comision_total()
        
        return {
            'valor_prima_neta': valor_prima_neta,
            'valor_iva': valor_iva,
            'valor_otros_costos': valor_otros_costos,
            'valor_prima_total': valor_prima_total,
            'ingreso_comision_percibido': ingreso_comision_percibido
        }
    
    @staticmethod
    def _generar_plan_pagos(poliza_id, valor_prima_total, numero_cuotas, fecha_inicio, 
                           financiacion=None, frecuencia_pago='mensual'):
        """Generar plan de pagos para la póliza"""
        tasa_financiacion = None
        if financiacion:
            tasa_financiacion = float(financiacion.tasa_efectiva_mensual)
        
        return PolizaPlanPago.generar_plan_pagos(
            poliza_id, valor_prima_total, numero_cuotas, fecha_inicio,
            tasa_financiacion, frecuencia_pago
        )
    
    @staticmethod
    def obtener_polizas(include_plan_pagos=False, filtros=None):
        """Obtener todas las pólizas con filtros opcionales"""
        try:
            query = Poliza.query
            
            if filtros:
                if filtros.get('estado_cartera'):
                    query = query.filter(Poliza.estado_cartera == filtros['estado_cartera'])
                if filtros.get('fecha_desde'):
                    fecha_desde = datetime.strptime(filtros['fecha_desde'], '%Y-%m-%d').date()
                    query = query.filter(Poliza.fecha_inicio_vigencia >= fecha_desde)
                if filtros.get('fecha_hasta'):
                    fecha_hasta = datetime.strptime(filtros['fecha_hasta'], '%Y-%m-%d').date()
                    query = query.filter(Poliza.fecha_inicio_vigencia <= fecha_hasta)
                if filtros.get('vigentes_solo'):
                    hoy = date.today()
                    query = query.filter(
                        Poliza.fecha_inicio_vigencia <= hoy,
                        Poliza.fecha_fin_vigencia >= hoy
                    )
            
            polizas = query.all()
            
            return {
                'polizas': [poliza.to_dict(include_plan_pagos=include_plan_pagos) for poliza in polizas]
            }, 200
            
        except ValueError as e:
            return {'error': f'Error en formato de fecha: {str(e)}'}, 400
        except Exception as e:
            return {'error': f'Error al obtener pólizas: {str(e)}'}, 500
    
    @staticmethod
    def obtener_poliza_por_id(poliza_id, include_plan_pagos=True):
        """Obtener una póliza por ID"""
        try:
            poliza = Poliza.query.get(poliza_id)
            if not poliza:
                return {'error': 'Póliza no encontrada'}, 404
            
            return {'poliza': poliza.to_dict(include_plan_pagos=include_plan_pagos)}, 200
            
        except Exception as e:
            return {'error': f'Error al obtener póliza: {str(e)}'}, 500
    
    @staticmethod
    def obtener_poliza_por_consecutivo(consecutivo_poliza, include_plan_pagos=True):
        """Obtener una póliza por consecutivo"""
        try:
            poliza = Poliza.query.filter(Poliza.consecutivo_poliza == consecutivo_poliza).first()
            if not poliza:
                return {'error': 'Póliza no encontrada'}, 404
            
            return {'poliza': poliza.to_dict(include_plan_pagos=include_plan_pagos)}, 200
            
        except Exception as e:
            return {'error': f'Error al obtener póliza: {str(e)}'}, 500
    
    @staticmethod
    def actualizar_estado_cartera(poliza_id, nuevo_estado):
        """Actualizar el estado de cartera de una póliza"""
        try:
            poliza = Poliza.query.get(poliza_id)
            if not poliza:
                return {'error': 'Póliza no encontrada'}, 404
            
            estados_validos = ['Al Día', 'Vencida', 'En Mora', 'Cancelada']
            if nuevo_estado not in estados_validos:
                return {'error': f'Estado no válido. Estados permitidos: {", ".join(estados_validos)}'}, 400
            
            poliza.estado_cartera = nuevo_estado
            db.session.commit()
            
            return {
                'message': 'Estado de cartera actualizado exitosamente',
                'poliza': poliza.to_dict()
            }, 200
            
        except Exception as e:
            db.session.rollback()
            return {'error': f'Error interno del servidor: {str(e)}'}, 500
    
    @staticmethod
    def procesar_pago_cuota(poliza_id, numero_cuota, datos_pago):
        """Procesar el pago de una cuota específica"""
        try:
            # Buscar la cuota
            cuota = PolizaPlanPago.query.filter(
                PolizaPlanPago.poliza_id == poliza_id,
                PolizaPlanPago.numero_cuota == numero_cuota
            ).first()
            
            if not cuota:
                return {'error': 'Cuota no encontrada'}, 404
            
            if not cuota.puede_pagarse():
                return {'error': 'La cuota no puede ser pagada'}, 400
            
            # Validar datos del pago
            if not datos_pago.get('valor_pagado'):
                return {'error': 'El valor pagado es requerido'}, 400
            
            valor_pagado = float(datos_pago['valor_pagado'])
            if valor_pagado <= 0:
                return {'error': 'El valor pagado debe ser mayor a cero'}, 400
            
            # Marcar como pagado
            cuota.marcar_como_pagado(
                valor_pagado=valor_pagado,
                referencia_pago=datos_pago.get('referencia_pago'),
                fecha_pago=datetime.strptime(datos_pago['fecha_pago'], '%Y-%m-%d').date() if datos_pago.get('fecha_pago') else None
            )
            
            # Actualizar estado de cartera de la póliza si es necesario
            poliza = cuota.poliza
            cuotas_pendientes = [c for c in poliza.plan_pagos if c.estado_pago != 'Pagado']
            cuotas_vencidas = [c for c in cuotas_pendientes if c.esta_vencido()]
            
            if not cuotas_pendientes:
                poliza.estado_cartera = 'Al Día'
            elif cuotas_vencidas:
                poliza.estado_cartera = 'Vencida'
            else:
                poliza.estado_cartera = 'Al Día'
            
            db.session.commit()
            
            return {
                'message': 'Pago procesado exitosamente',
                'cuota': cuota.to_dict(),
                'poliza_estado': poliza.estado_cartera
            }, 200
            
        except ValueError as e:
            return {'error': f'Error en formato de fecha o valor: {str(e)}'}, 400
        except Exception as e:
            db.session.rollback()
            return {'error': f'Error interno del servidor: {str(e)}'}, 500
    
    @staticmethod
    def obtener_cuotas_vencidas():
        """Obtener todas las cuotas vencidas del sistema"""
        try:
            hoy = date.today()
            cuotas_vencidas = PolizaPlanPago.query.filter(
                PolizaPlanPago.fecha_maxima_pago < hoy,
                PolizaPlanPago.estado_pago.in_(['Pendiente de pago', 'Vencido'])
            ).all()
            
            # Marcar como vencidas las que aún no estén marcadas
            for cuota in cuotas_vencidas:
                cuota.marcar_como_vencido()
            
            db.session.commit()
            
            return {
                'cuotas_vencidas': [cuota.to_dict() for cuota in cuotas_vencidas],
                'total_cuotas_vencidas': len(cuotas_vencidas),
                'valor_total_vencido': sum(float(cuota.valor_a_pagar) for cuota in cuotas_vencidas)
            }, 200
            
        except Exception as e:
            return {'error': f'Error al obtener cuotas vencidas: {str(e)}'}, 500
    
    @staticmethod
    def obtener_reporte_cartera():
        """Obtener reporte general del estado de cartera"""
        try:
            polizas_activas = Poliza.query.filter(
                Poliza.fecha_fin_vigencia >= date.today()
            ).all()
            
            resumen = {
                'total_polizas_activas': len(polizas_activas),
                'polizas_al_dia': 0,
                'polizas_vencidas': 0,
                'polizas_en_mora': 0,
                'valor_total_prima': 0,
                'valor_total_comisiones': 0,
                'cuotas_pendientes': 0,
                'valor_pendiente_cobro': 0
            }
            
            for poliza in polizas_activas:
                resumen['valor_total_prima'] += poliza.calcular_valor_prima_total()
                resumen['valor_total_comisiones'] += float(poliza.ingreso_comision_percibido or 0)
                
                if poliza.estado_cartera == 'Al Día':
                    resumen['polizas_al_dia'] += 1
                elif poliza.estado_cartera == 'Vencida':
                    resumen['polizas_vencidas'] += 1
                elif poliza.estado_cartera == 'En Mora':
                    resumen['polizas_en_mora'] += 1
                
                # Sumar cuotas pendientes
                for cuota in poliza.plan_pagos:
                    if cuota.estado_pago != 'Pagado':
                        resumen['cuotas_pendientes'] += 1
                        resumen['valor_pendiente_cobro'] += float(cuota.valor_a_pagar)
            
            return {'reporte_cartera': resumen}, 200
            
        except Exception as e:
            return {'error': f'Error al generar reporte de cartera: {str(e)}'}, 500
    
    @staticmethod
    def cancelar_poliza(poliza_id, motivo_cancelacion):
        """Cancelar una póliza"""
        try:
            poliza = Poliza.query.get(poliza_id)
            if not poliza:
                return {'error': 'Póliza no encontrada'}, 404
            
            puede_cancelarse, mensaje = poliza.puede_cancelarse()
            if not puede_cancelarse:
                return {'error': mensaje}, 400
            
            poliza.estado_cartera = 'Cancelada'
            
            # Marcar todas las cuotas pendientes como canceladas
            for cuota in poliza.plan_pagos:
                if cuota.estado_pago in ['Pendiente de pago', 'Vencido']:
                    cuota.estado_pago = 'Cancelado'
            
            db.session.commit()
            
            return {
                'message': 'Póliza cancelada exitosamente',
                'motivo': motivo_cancelacion,
                'poliza': poliza.to_dict(include_plan_pagos=True)
            }, 200
            
        except Exception as e:
            db.session.rollback()
            return {'error': f'Error interno del servidor: {str(e)}'}, 500 