from app import db
from app.models import (
    Aseguradora, AseguradoraDeducible, AseguradoraCobertura, 
    AseguradoraFinanciacion
)
from sqlalchemy.exc import IntegrityError
from sqlalchemy import and_

class AseguradoraService:
    
    @staticmethod
    def crear_aseguradora(datos_aseguradora):
        """Crear una nueva aseguradora"""
        try:
            # Validar datos requeridos
            if not datos_aseguradora.get('nombre'):
                return {'error': 'El nombre de la aseguradora es requerido'}, 400
            
            # Crear aseguradora
            aseguradora = Aseguradora(
                nombre=datos_aseguradora['nombre'],
                numeral_asistencia=datos_aseguradora.get('numeral_asistencia'),
                correo_comercial=datos_aseguradora.get('correo_comercial'),
                correo_reclamaciones=datos_aseguradora.get('correo_reclamaciones'),
                oficina_direccion=datos_aseguradora.get('oficina_direccion'),
                contacto_asignado=datos_aseguradora.get('contacto_asignado'),
                logo_url=datos_aseguradora.get('logo_url'),
                pais_origen_bandera_url=datos_aseguradora.get('pais_origen_bandera_url'),
                respaldo_internacional=datos_aseguradora.get('respaldo_internacional'),
                comisiones_normales=datos_aseguradora.get('comisiones_normales'),
                sobrecomisiones=datos_aseguradora.get('sobrecomisiones'),
                sublimite_rc_veh_bienes_terceros=datos_aseguradora.get('sublimite_rc_veh_bienes_terceros'),
                sublimite_rc_veh_amparo_patrimonial=datos_aseguradora.get('sublimite_rc_veh_amparo_patrimonial'),
                sublimite_rc_veh_muerte_una_persona=datos_aseguradora.get('sublimite_rc_veh_muerte_una_persona'),
                sublimite_rc_veh_muerte_mas_personas=datos_aseguradora.get('sublimite_rc_veh_muerte_mas_personas'),
                sublimite_rce_cop_contratistas=datos_aseguradora.get('sublimite_rce_cop_contratistas'),
                sublimite_rce_cop_cruzada=datos_aseguradora.get('sublimite_rce_cop_cruzada'),
                sublimite_rce_cop_patronal=datos_aseguradora.get('sublimite_rce_cop_patronal'),
                sublimite_rce_cop_parqueaderos=datos_aseguradora.get('sublimite_rce_cop_parqueaderos'),
                sublimite_rce_cop_gastos_medicos=datos_aseguradora.get('sublimite_rce_cop_gastos_medicos')
            )
            
            db.session.add(aseguradora)
            db.session.commit()
            
            return {'message': 'Aseguradora creada exitosamente', 'aseguradora': aseguradora.to_dict()}, 201
            
        except IntegrityError as e:
            db.session.rollback()
            return {'error': 'Error de integridad en la base de datos'}, 400
        except Exception as e:
            db.session.rollback()
            return {'error': f'Error interno del servidor: {str(e)}'}, 500
    
    @staticmethod
    def obtener_aseguradoras(include_plantillas=False):
        """Obtener todas las aseguradoras"""
        try:
            aseguradoras = Aseguradora.query.all()
            return {
                'aseguradoras': [aseg.to_dict(include_plantillas=include_plantillas) for aseg in aseguradoras]
            }, 200
        except Exception as e:
            return {'error': f'Error al obtener aseguradoras: {str(e)}'}, 500
    
    @staticmethod
    def obtener_aseguradora_por_id(aseguradora_id, include_plantillas=True):
        """Obtener una aseguradora por ID"""
        try:
            aseguradora = Aseguradora.query.get(aseguradora_id)
            if not aseguradora:
                return {'error': 'Aseguradora no encontrada'}, 404
            
            return {'aseguradora': aseguradora.to_dict(include_plantillas=include_plantillas)}, 200
        except Exception as e:
            return {'error': f'Error al obtener aseguradora: {str(e)}'}, 500
    
    @staticmethod
    def actualizar_aseguradora(aseguradora_id, datos_actualizacion):
        """Actualizar una aseguradora"""
        try:
            aseguradora = Aseguradora.query.get(aseguradora_id)
            if not aseguradora:
                return {'error': 'Aseguradora no encontrada'}, 404
            
            # Actualizar campos permitidos
            campos_permitidos = [
                'nombre', 'numeral_asistencia', 'correo_comercial', 'correo_reclamaciones',
                'oficina_direccion', 'contacto_asignado', 'logo_url', 'pais_origen_bandera_url',
                'respaldo_internacional', 'comisiones_normales', 'sobrecomisiones',
                'sublimite_rc_veh_bienes_terceros', 'sublimite_rc_veh_amparo_patrimonial',
                'sublimite_rc_veh_muerte_una_persona', 'sublimite_rc_veh_muerte_mas_personas',
                'sublimite_rce_cop_contratistas', 'sublimite_rce_cop_cruzada',
                'sublimite_rce_cop_patronal', 'sublimite_rce_cop_parqueaderos',
                'sublimite_rce_cop_gastos_medicos'
            ]
            
            for campo in campos_permitidos:
                if campo in datos_actualizacion:
                    setattr(aseguradora, campo, datos_actualizacion[campo])
            
            db.session.commit()
            
            return {'message': 'Aseguradora actualizada exitosamente', 'aseguradora': aseguradora.to_dict()}, 200
            
        except IntegrityError as e:
            db.session.rollback()
            return {'error': 'Error de integridad en la base de datos'}, 400
        except Exception as e:
            db.session.rollback()
            return {'error': f'Error interno del servidor: {str(e)}'}, 500
    
    @staticmethod
    def eliminar_aseguradora(aseguradora_id):
        """Eliminar una aseguradora"""
        try:
            aseguradora = Aseguradora.query.get(aseguradora_id)
            if not aseguradora:
                return {'error': 'Aseguradora no encontrada'}, 404
            
            # Verificar si tiene opciones de seguro o pólizas activas
            if aseguradora.opciones_seguro:
                return {'error': 'No se puede eliminar la aseguradora porque tiene opciones de seguro asociadas'}, 400
            
            db.session.delete(aseguradora)
            db.session.commit()
            
            return {'message': 'Aseguradora eliminada exitosamente'}, 200
            
        except Exception as e:
            db.session.rollback()
            return {'error': f'Error interno del servidor: {str(e)}'}, 500
    
    @staticmethod
    def obtener_plantillas_por_tipo(aseguradora_id, tipo_poliza):
        """Obtener deducibles y coberturas de una aseguradora para un tipo de póliza"""
        try:
            aseguradora = Aseguradora.query.get(aseguradora_id)
            if not aseguradora:
                return {'error': 'Aseguradora no encontrada'}, 404
            
            if tipo_poliza not in ['HOGAR', 'VEHICULO', 'COPROPIEDAD', 'OTRO']:
                return {'error': 'Tipo de póliza no válido'}, 400
            
            deducibles = AseguradoraDeducible.query.filter(
                and_(
                    AseguradoraDeducible.aseguradora_id == aseguradora_id,
                    AseguradoraDeducible.tipo_poliza == tipo_poliza
                )
            ).all()
            
            coberturas = AseguradoraCobertura.query.filter(
                and_(
                    AseguradoraCobertura.aseguradora_id == aseguradora_id,
                    AseguradoraCobertura.tipo_poliza == tipo_poliza
                )
            ).all()
            
            financiaciones = AseguradoraFinanciacion.query.filter(
                AseguradoraFinanciacion.aseguradora_id == aseguradora_id
            ).all()
            
            return {
                'aseguradora': aseguradora.to_dict(),
                'tipo_poliza': tipo_poliza,
                'deducibles': [d.to_dict() for d in deducibles],
                'coberturas': [c.to_dict() for c in coberturas],
                'financiaciones': [f.to_dict() for f in financiaciones]
            }, 200
            
        except Exception as e:
            return {'error': f'Error al obtener plantillas: {str(e)}'}, 500
    
    @staticmethod
    def crear_deducible(aseguradora_id, datos_deducible):
        """Crear un deducible para una aseguradora"""
        try:
            aseguradora = Aseguradora.query.get(aseguradora_id)
            if not aseguradora:
                return {'error': 'Aseguradora no encontrada'}, 404
            
            # Validar datos requeridos
            if not datos_deducible.get('tipo_poliza'):
                return {'error': 'El tipo de póliza es requerido'}, 400
            if not datos_deducible.get('categoria'):
                return {'error': 'La categoría es requerida'}, 400
            
            deducible = AseguradoraDeducible(
                aseguradora_id=aseguradora_id,
                tipo_poliza=datos_deducible['tipo_poliza'],
                categoria=datos_deducible['categoria'],
                tipo_deducible=datos_deducible.get('tipo_deducible'),
                valor_porcentaje=datos_deducible.get('valor_porcentaje'),
                valor_minimo=datos_deducible.get('valor_minimo')
            )
            
            db.session.add(deducible)
            db.session.commit()
            
            return {'message': 'Deducible creado exitosamente', 'deducible': deducible.to_dict()}, 201
            
        except Exception as e:
            db.session.rollback()
            return {'error': f'Error interno del servidor: {str(e)}'}, 500
    
    @staticmethod
    def crear_cobertura(aseguradora_id, datos_cobertura):
        """Crear una cobertura para una aseguradora"""
        try:
            aseguradora = Aseguradora.query.get(aseguradora_id)
            if not aseguradora:
                return {'error': 'Aseguradora no encontrada'}, 404
            
            # Validar datos requeridos
            if not datos_cobertura.get('tipo_poliza'):
                return {'error': 'El tipo de póliza es requerido'}, 400
            if not datos_cobertura.get('tipo_item'):
                return {'error': 'El tipo de item es requerido'}, 400
            if not datos_cobertura.get('nombre_item'):
                return {'error': 'El nombre del item es requerido'}, 400
            
            cobertura = AseguradoraCobertura(
                aseguradora_id=aseguradora_id,
                tipo_poliza=datos_cobertura['tipo_poliza'],
                tipo_item=datos_cobertura['tipo_item'],
                nombre_item=datos_cobertura['nombre_item']
            )
            
            db.session.add(cobertura)
            db.session.commit()
            
            return {'message': 'Cobertura creada exitosamente', 'cobertura': cobertura.to_dict()}, 201
            
        except Exception as e:
            db.session.rollback()
            return {'error': f'Error interno del servidor: {str(e)}'}, 500
    
    @staticmethod
    def crear_financiacion(aseguradora_id, datos_financiacion):
        """Crear una opción de financiación para una aseguradora"""
        try:
            aseguradora = Aseguradora.query.get(aseguradora_id)
            if not aseguradora:
                return {'error': 'Aseguradora no encontrada'}, 404
            
            # Validar datos requeridos
            if not datos_financiacion.get('nombre_financiera'):
                return {'error': 'El nombre de la financiera es requerido'}, 400
            if not datos_financiacion.get('tasa_efectiva_mensual'):
                return {'error': 'La tasa efectiva mensual es requerida'}, 400
            
            financiacion = AseguradoraFinanciacion(
                aseguradora_id=aseguradora_id,
                nombre_financiera=datos_financiacion['nombre_financiera'],
                tasa_efectiva_mensual=datos_financiacion['tasa_efectiva_mensual']
            )
            
            db.session.add(financiacion)
            db.session.commit()
            
            return {'message': 'Financiación creada exitosamente', 'financiacion': financiacion.to_dict()}, 201
            
        except Exception as e:
            db.session.rollback()
            return {'error': f'Error interno del servidor: {str(e)}'}, 500 