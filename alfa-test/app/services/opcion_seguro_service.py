from app import db
from app.models import (
    OpcionSeguro, OpcionHogar, OpcionVehiculo, OpcionCopropiedad, OpcionOtro,
    Bien, Aseguradora, AseguradoraDeducible, AseguradoraCobertura, AseguradoraFinanciacion,
    Hogar, Vehiculo, Copropiedad, OtroBien
)
from sqlalchemy.exc import IntegrityError
from sqlalchemy import and_

class OpcionSeguroService:
    
    @staticmethod
    def crear_opcion_seguro(datos_opcion):
        """Crear una nueva opción de seguro (cotización)"""
        try:
            # Validar datos requeridos
            if not datos_opcion.get('bien_id'):
                return {'error': 'El ID del bien es requerido'}, 400
            if not datos_opcion.get('aseguradora_id'):
                return {'error': 'El ID de la aseguradora es requerido'}, 400
            if not datos_opcion.get('tipo_opcion'):
                return {'error': 'El tipo de opción es requerido'}, 400
            if not datos_opcion.get('valores_asegurados'):
                return {'error': 'Los valores asegurados son requeridos'}, 400
            
            # Validar que el bien existe
            bien = Bien.query.get(datos_opcion['bien_id'])
            if not bien:
                return {'error': 'El bien especificado no existe'}, 404
            
            # Validar que la aseguradora existe
            aseguradora = Aseguradora.query.get(datos_opcion['aseguradora_id'])
            if not aseguradora:
                return {'error': 'La aseguradora especificada no existe'}, 404
            
            # Validar que el tipo de opción coincide con el tipo de bien
            if datos_opcion['tipo_opcion'] != bien.tipo_bien:
                return {'error': 'El tipo de opción debe coincidir con el tipo de bien'}, 400
            
            # Crear la opción específica según el tipo
            opcion_especifica = OpcionSeguroService._crear_opcion_especifica(
                datos_opcion['tipo_opcion'],
                datos_opcion['valores_asegurados'],
                bien
            )
            
            if isinstance(opcion_especifica, tuple):  # Es un error
                return opcion_especifica
            
            # Crear la opción de seguro principal
            consecutivo = OpcionSeguro.generar_consecutivo()
            opcion_seguro = OpcionSeguro(
                consecutivo=consecutivo,
                bien_id=datos_opcion['bien_id'],
                aseguradora_id=datos_opcion['aseguradora_id'],
                tipo_opcion=datos_opcion['tipo_opcion'],
                opcion_especifica_id=opcion_especifica.id,
                valor_prima_total=datos_opcion.get('valor_prima_total'),
                financiacion_id=datos_opcion.get('financiacion_id')
            )
            
            db.session.add(opcion_seguro)
            db.session.flush()  # Para obtener el ID
            
            # Asociar deducibles seleccionados
            if datos_opcion.get('deducibles_seleccionados'):
                OpcionSeguroService._asociar_deducibles(
                    opcion_seguro.id,
                    datos_opcion['deducibles_seleccionados'],
                    datos_opcion['aseguradora_id'],
                    datos_opcion['tipo_opcion']
                )
            
            # Asociar coberturas seleccionadas
            if datos_opcion.get('coberturas_seleccionadas'):
                OpcionSeguroService._asociar_coberturas(
                    opcion_seguro.id,
                    datos_opcion['coberturas_seleccionadas'],
                    datos_opcion['aseguradora_id'],
                    datos_opcion['tipo_opcion']
                )
            
            db.session.commit()
            
            return {
                'message': 'Opción de seguro creada exitosamente',
                'opcion_seguro': opcion_seguro.to_dict()
            }, 201
            
        except IntegrityError as e:
            db.session.rollback()
            return {'error': 'Error de integridad en la base de datos'}, 400
        except Exception as e:
            db.session.rollback()
            return {'error': f'Error interno del servidor: {str(e)}'}, 500
    
    @staticmethod
    def _crear_opcion_especifica(tipo_opcion, valores_asegurados, bien):
        """Crear la opción específica según el tipo"""
        bien_especifico = bien.get_bien_especifico()
        if not bien_especifico:
            return {'error': 'No se pudo obtener información específica del bien'}, 400
        
        if tipo_opcion == 'HOGAR':
            return OpcionSeguroService._crear_opcion_hogar(valores_asegurados, bien_especifico)
        elif tipo_opcion == 'VEHICULO':
            return OpcionSeguroService._crear_opcion_vehiculo(valores_asegurados, bien_especifico)
        elif tipo_opcion == 'COPROPIEDAD':
            return OpcionSeguroService._crear_opcion_copropiedad(valores_asegurados, bien_especifico)
        elif tipo_opcion == 'OTRO':
            return OpcionSeguroService._crear_opcion_otro(valores_asegurados, bien_especifico)
        else:
            return {'error': 'Tipo de opción no válido'}, 400
    
    @staticmethod
    def _crear_opcion_hogar(valores_asegurados, hogar):
        """Crear opción específica para hogar"""
        opcion_hogar = OpcionHogar(
            valor_inmueble_asegurado=valores_asegurados.get('valor_inmueble_asegurado'),
            valor_contenidos_normales_asegurado=valores_asegurados.get('valor_contenidos_normales_asegurado'),
            valor_contenidos_especiales_asegurado=valores_asegurados.get('valor_contenidos_especiales_asegurado'),
            valor_equipo_electronico_asegurado=valores_asegurados.get('valor_equipo_electronico_asegurado'),
            valor_maquinaria_equipo_asegurado=valores_asegurados.get('valor_maquinaria_equipo_asegurado'),
            valor_rc_asegurado=valores_asegurados.get('valor_rc_asegurado')
        )
        
        # Validar que los valores no excedan los avalúos
        errores = opcion_hogar.validar_valores_asegurados(hogar)
        if errores:
            return {'error': f'Valores asegurados inválidos: {", ".join(errores)}'}, 400
        
        db.session.add(opcion_hogar)
        db.session.flush()
        return opcion_hogar
    
    @staticmethod
    def _crear_opcion_vehiculo(valores_asegurados, vehiculo):
        """Crear opción específica para vehículo"""
        opcion_vehiculo = OpcionVehiculo(
            valor_vehiculo_asegurado=valores_asegurados.get('valor_vehiculo_asegurado'),
            valor_accesorios_asegurado=valores_asegurados.get('valor_accesorios_asegurado'),
            valor_rc_asegurado=valores_asegurados.get('valor_rc_asegurado')
        )
        
        # Validar que los valores no excedan los avalúos
        errores = opcion_vehiculo.validar_valores_asegurados(vehiculo)
        if errores:
            return {'error': f'Valores asegurados inválidos: {", ".join(errores)}'}, 400
        
        db.session.add(opcion_vehiculo)
        db.session.flush()
        return opcion_vehiculo
    
    @staticmethod
    def _crear_opcion_copropiedad(valores_asegurados, copropiedad):
        """Crear opción específica para copropiedad"""
        opcion_copropiedad = OpcionCopropiedad(
            valor_area_comun_asegurado=valores_asegurados.get('valor_area_comun_asegurado'),
            valor_area_privada_asegurado=valores_asegurados.get('valor_area_privada_asegurado'),
            valor_maquinaria_equipo_asegurado=valores_asegurados.get('valor_maquinaria_equipo_asegurado'),
            valor_equipo_electronico_asegurado=valores_asegurados.get('valor_equipo_electronico_asegurado'),
            valor_muebles_asegurado=valores_asegurados.get('valor_muebles_asegurado'),
            valor_directores_asegurado=valores_asegurados.get('valor_directores_asegurado'),
            valor_rce_asegurado=valores_asegurados.get('valor_rce_asegurado'),
            valor_manejo_asegurado=valores_asegurados.get('valor_manejo_asegurado'),
            valor_transporte_valores_vigencia_asegurado=valores_asegurados.get('valor_transporte_valores_vigencia_asegurado'),
            valor_transporte_valores_despacho_asegurado=valores_asegurados.get('valor_transporte_valores_despacho_asegurado')
        )
        
        # Validar que los valores no excedan los avalúos
        errores = opcion_copropiedad.validar_valores_asegurados(copropiedad)
        if errores:
            return {'error': f'Valores asegurados inválidos: {", ".join(errores)}'}, 400
        
        db.session.add(opcion_copropiedad)
        db.session.flush()
        return opcion_copropiedad
    
    @staticmethod
    def _crear_opcion_otro(valores_asegurados, otro_bien):
        """Crear opción específica para otro bien"""
        opcion_otro = OpcionOtro(
            valor_asegurado=valores_asegurados.get('valor_asegurado')
        )
        
        # Validar que los valores no excedan los avalúos
        errores = opcion_otro.validar_valores_asegurados(otro_bien)
        if errores:
            return {'error': f'Valores asegurados inválidos: {", ".join(errores)}'}, 400
        
        db.session.add(opcion_otro)
        db.session.flush()
        return opcion_otro
    
    @staticmethod
    def _asociar_deducibles(opcion_seguro_id, deducibles_ids, aseguradora_id, tipo_opcion):
        """Asociar deducibles seleccionados a la opción de seguro"""
        for deducible_id in deducibles_ids:
            # Validar que el deducible existe y pertenece a la aseguradora
            deducible = AseguradoraDeducible.query.filter(
                and_(
                    AseguradoraDeducible.id == deducible_id,
                    AseguradoraDeducible.aseguradora_id == aseguradora_id,
                    AseguradoraDeducible.tipo_poliza == tipo_opcion
                )
            ).first()
            
            if deducible:
                # Usar SQL directo para la tabla de asociación
                db.session.execute(
                    "INSERT INTO opciones_seguro_deducibles (opcion_seguro_id, deducible_id) VALUES (:opcion_id, :deducible_id)",
                    {'opcion_id': opcion_seguro_id, 'deducible_id': deducible_id}
                )
    
    @staticmethod
    def _asociar_coberturas(opcion_seguro_id, coberturas_ids, aseguradora_id, tipo_opcion):
        """Asociar coberturas seleccionadas a la opción de seguro"""
        for cobertura_id in coberturas_ids:
            # Validar que la cobertura existe y pertenece a la aseguradora
            cobertura = AseguradoraCobertura.query.filter(
                and_(
                    AseguradoraCobertura.id == cobertura_id,
                    AseguradoraCobertura.aseguradora_id == aseguradora_id,
                    AseguradoraCobertura.tipo_poliza == tipo_opcion
                )
            ).first()
            
            if cobertura:
                # Usar SQL directo para la tabla de asociación
                db.session.execute(
                    "INSERT INTO opciones_seguro_coberturas (opcion_seguro_id, cobertura_id) VALUES (:opcion_id, :cobertura_id)",
                    {'opcion_id': opcion_seguro_id, 'cobertura_id': cobertura_id}
                )
    
    @staticmethod
    def obtener_opciones_seguro(bien_id=None, aseguradora_id=None, tipo_opcion=None):
        """Obtener opciones de seguro con filtros opcionales"""
        try:
            query = OpcionSeguro.query
            
            if bien_id:
                query = query.filter(OpcionSeguro.bien_id == bien_id)
            if aseguradora_id:
                query = query.filter(OpcionSeguro.aseguradora_id == aseguradora_id)
            if tipo_opcion:
                query = query.filter(OpcionSeguro.tipo_opcion == tipo_opcion)
            
            opciones = query.all()
            
            return {
                'opciones_seguro': [opcion.to_dict() for opcion in opciones]
            }, 200
            
        except Exception as e:
            return {'error': f'Error al obtener opciones de seguro: {str(e)}'}, 500
    
    @staticmethod
    def obtener_opcion_seguro_por_id(opcion_id):
        """Obtener una opción de seguro por ID"""
        try:
            opcion = OpcionSeguro.query.get(opcion_id)
            if not opcion:
                return {'error': 'Opción de seguro no encontrada'}, 404
            
            return {'opcion_seguro': opcion.to_dict()}, 200
            
        except Exception as e:
            return {'error': f'Error al obtener opción de seguro: {str(e)}'}, 500
    
    @staticmethod
    def obtener_opciones_por_bien(bien_id):
        """Obtener todas las opciones de seguro para un bien específico"""
        try:
            bien = Bien.query.get(bien_id)
            if not bien:
                return {'error': 'Bien no encontrado'}, 404
            
            opciones = OpcionSeguro.query.filter(OpcionSeguro.bien_id == bien_id).all()
            
            return {
                'bien': bien.to_dict(),
                'opciones_seguro': [opcion.to_dict() for opcion in opciones]
            }, 200
            
        except Exception as e:
            return {'error': f'Error al obtener opciones del bien: {str(e)}'}, 500
    
    @staticmethod
    def actualizar_valor_prima(opcion_id, nuevo_valor_prima):
        """Actualizar el valor de la prima de una opción"""
        try:
            opcion = OpcionSeguro.query.get(opcion_id)
            if not opcion:
                return {'error': 'Opción de seguro no encontrada'}, 404
            
            if opcion.poliza:
                return {'error': 'No se puede actualizar una opción que ya tiene póliza'}, 400
            
            opcion.valor_prima_total = nuevo_valor_prima
            db.session.commit()
            
            return {
                'message': 'Valor de prima actualizado exitosamente',
                'opcion_seguro': opcion.to_dict()
            }, 200
            
        except Exception as e:
            db.session.rollback()
            return {'error': f'Error interno del servidor: {str(e)}'}, 500
    
    @staticmethod
    def eliminar_opcion_seguro(opcion_id):
        """Eliminar una opción de seguro"""
        try:
            opcion = OpcionSeguro.query.get(opcion_id)
            if not opcion:
                return {'error': 'Opción de seguro no encontrada'}, 404
            
            if opcion.poliza:
                return {'error': 'No se puede eliminar una opción que ya tiene póliza'}, 400
            
            db.session.delete(opcion)
            db.session.commit()
            
            return {'message': 'Opción de seguro eliminada exitosamente'}, 200
            
        except Exception as e:
            db.session.rollback()
            return {'error': f'Error interno del servidor: {str(e)}'}, 500
    
    @staticmethod
    def calcular_simulacion_prima(datos_simulacion):
        """Calcular simulación de prima sin crear la opción"""
        try:
            # Obtener información necesaria
            bien = Bien.query.get(datos_simulacion.get('bien_id'))
            if not bien:
                return {'error': 'Bien no encontrado'}, 404
            
            aseguradora = Aseguradora.query.get(datos_simulacion.get('aseguradora_id'))
            if not aseguradora:
                return {'error': 'Aseguradora no encontrada'}, 404
            
            # Calcular valor asegurado total
            valores_asegurados = datos_simulacion.get('valores_asegurados', {})
            valor_total = sum(float(v) for v in valores_asegurados.values() if v)
            
            # Obtener comisión y sobrecomisión
            comision = aseguradora.get_comision_por_tipo(bien.tipo_bien) or 0
            sobrecomision = aseguradora.get_sobrecomision_por_tipo(bien.tipo_bien) or 0
            
            # Simulación básica (aquí se podría implementar lógica más compleja)
            prima_base = valor_total * 0.002  # 0.2% del valor asegurado
            prima_iva = prima_base * 0.19
            prima_total = prima_base + prima_iva
            comision_total = prima_base * (comision + sobrecomision)
            
            return {
                'simulacion': {
                    'bien_id': bien.id,
                    'aseguradora_id': aseguradora.id,
                    'valor_total_asegurado': valor_total,
                    'prima_base': prima_base,
                    'prima_iva': prima_iva,
                    'prima_total': prima_total,
                    'comision_porcentaje': (comision + sobrecomision) * 100,
                    'comision_total': comision_total
                }
            }, 200
            
        except Exception as e:
            return {'error': f'Error al calcular simulación: {str(e)}'}, 500 