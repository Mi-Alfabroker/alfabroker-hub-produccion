from app.models.bien_model import Bien
from app.models.hogar_model import Hogar
from app.models.vehiculo_model import Vehiculo
from app.models.copropiedad_model import Copropiedad
from app.models.otro_bien_model import OtroBien
from app.models.cliente_bien_model import ClienteBien
from app import db

class BienService:
    
    @staticmethod
    def get_all_bienes():
        """Obtener todos los bienes"""
        return Bien.query.all()
    
    @staticmethod
    def get_bien_by_id(bien_id):
        """Obtener un bien por ID"""
        return Bien.query.get(bien_id)
    
    @staticmethod
    def get_bienes_by_tipo(tipo_bien):
        """Obtener bienes por tipo"""
        return Bien.query.filter_by(tipo_bien=tipo_bien).all()
    
    @staticmethod
    def get_bienes_by_cliente(cliente_id):
        """Obtener todos los bienes de un cliente"""
        asignaciones = ClienteBien.query.filter_by(cliente_id=cliente_id).all()
        return [Bien.query.get(asig.bien_id) for asig in asignaciones]
    
    @staticmethod
    def create_bien(tipo_bien, data_especifico, data_general=None):
        """
        Crear un nuevo bien con patrón polimórfico
        
        Args:
            tipo_bien: 'HOGAR', 'VEHICULO', 'COPROPIEDAD', 'OTRO'
            data_especifico: Datos específicos según el tipo de bien
            data_general: Datos generales del bien (estado, comentarios, etc.)
        """
        if data_general is None:
            data_general = {}
            
        # Crear el bien específico primero
        bien_especifico = None
        
        try:
            if tipo_bien == 'HOGAR':
                bien_especifico = BienService._create_hogar(data_especifico)
            elif tipo_bien == 'VEHICULO':
                bien_especifico = BienService._create_vehiculo(data_especifico)
            elif tipo_bien == 'COPROPIEDAD':
                bien_especifico = BienService._create_copropiedad(data_especifico)
            elif tipo_bien == 'OTRO':
                bien_especifico = BienService._create_otro_bien(data_especifico)
            else:
                raise ValueError(f"Tipo de bien no válido: {tipo_bien}")
            
            # Crear el bien principal
            bien = Bien(
                tipo_bien=tipo_bien,
                bien_especifico_id=bien_especifico.id,
                estado=data_general.get('estado'),
                comentarios_generales=data_general.get('comentarios_generales'),
                vigencias_continuas=data_general.get('vigencias_continuas', False)
            )
            
            db.session.add(bien)
            db.session.commit()
            return bien
            
        except Exception as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def _create_hogar(data):
        """Crear un hogar específico"""
        hogar = Hogar(
            tipo_inmueble=data.get('tipo_inmueble'),
            ciudad_inmueble=data.get('ciudad_inmueble'),
            direccion_inmueble=data.get('direccion_inmueble'),
            numero_pisos=data.get('numero_pisos'),
            ano_construccion=data.get('ano_construccion'),
            valor_inmueble_avaluo=data.get('valor_inmueble_avaluo'),
            valor_contenidos_normales_avaluo=data.get('valor_contenidos_normales_avaluo'),
            valor_contenidos_especiales_avaluo=data.get('valor_contenidos_especiales_avaluo'),
            valor_equipo_electronico_avaluo=data.get('valor_equipo_electronico_avaluo'),
            valor_maquinaria_equipo_avaluo=data.get('valor_maquinaria_equipo_avaluo')
        )
        db.session.add(hogar)
        db.session.flush()  # Para obtener el ID
        return hogar
    
    @staticmethod
    def _create_vehiculo(data):
        """Crear un vehículo específico"""
        vehiculo = Vehiculo(
            tipo_vehiculo=data.get('tipo_vehiculo'),
            placa=data.get('placa'),
            marca=data.get('marca'),
            serie_referencia=data.get('serie_referencia'),
            ano_modelo=data.get('ano_modelo'),
            ano_nacimiento_conductor=data.get('ano_nacimiento_conductor'),
            codigo_fasecolda=data.get('codigo_fasecolda'),
            valor_vehiculo=data.get('valor_vehiculo'),
            valor_accesorios_avaluo=data.get('valor_accesorios_avaluo')
        )
        db.session.add(vehiculo)
        db.session.flush()  # Para obtener el ID
        return vehiculo
    
    @staticmethod
    def _create_copropiedad(data):
        """Crear una copropiedad específica"""
        copropiedad = Copropiedad(
            tipo_copropiedad=data.get('tipo_copropiedad'),
            ciudad=data.get('ciudad'),
            direccion=data.get('direccion'),
            estrato=data.get('estrato'),
            ano_construccion=data.get('ano_construccion'),
            numero_torres=data.get('numero_torres'),
            numero_maximo_pisos=data.get('numero_maximo_pisos'),
            numero_maximo_sotanos=data.get('numero_maximo_sotanos'),
            cantidad_unidades_casa=data.get('cantidad_unidades_casa'),
            cantidad_unidades_apartamentos=data.get('cantidad_unidades_apartamentos'),
            cantidad_unidades_locales=data.get('cantidad_unidades_locales'),
            cantidad_unidades_oficinas=data.get('cantidad_unidades_oficinas'),
            cantidad_unidades_otros=data.get('cantidad_unidades_otros'),
            valor_edificio_area_comun_avaluo=data.get('valor_edificio_area_comun_avaluo'),
            valor_edificio_area_privada_avaluo=data.get('valor_edificio_area_privada_avaluo'),
            valor_maquinaria_equipo_avaluo=data.get('valor_maquinaria_equipo_avaluo'),
            valor_equipo_electrico_electronico_avaluo=data.get('valor_equipo_electrico_electronico_avaluo'),
            valor_muebles_avaluo=data.get('valor_muebles_avaluo')
        )
        db.session.add(copropiedad)
        db.session.flush()  # Para obtener el ID
        return copropiedad
    
    @staticmethod
    def _create_otro_bien(data):
        """Crear otro tipo de bien específico"""
        otro_bien = OtroBien(
            tipo_seguro=data.get('tipo_seguro'),
            bien_asegurado=data.get('bien_asegurado'),
            valor_bien_asegurar=data.get('valor_bien_asegurar'),
            detalles_bien_asegurado=data.get('detalles_bien_asegurado')
        )
        db.session.add(otro_bien)
        db.session.flush()  # Para obtener el ID
        return otro_bien
    
    @staticmethod
    def update_bien(bien_id, data_general=None, data_especifico=None):
        """Actualizar un bien existente"""
        bien = Bien.query.get(bien_id)
        if not bien:
            return None
        
        try:
            # Actualizar datos generales si se proporcionan
            if data_general:
                bien.estado = data_general.get('estado', bien.estado)
                bien.comentarios_generales = data_general.get('comentarios_generales', bien.comentarios_generales)
                bien.vigencias_continuas = data_general.get('vigencias_continuas', bien.vigencias_continuas)
            
            # Actualizar bien específico si se proporcionan datos
            if data_especifico:
                bien_especifico = bien.get_bien_especifico()
                if bien_especifico:
                    BienService._update_bien_especifico(bien.tipo_bien, bien_especifico, data_especifico)
            
            db.session.commit()
            return bien
            
        except Exception as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def _update_bien_especifico(tipo_bien, bien_especifico, data):
        """Actualizar el bien específico según su tipo"""
        if tipo_bien == 'HOGAR':
            for key, value in data.items():
                if hasattr(bien_especifico, key):
                    setattr(bien_especifico, key, value)
        elif tipo_bien == 'VEHICULO':
            for key, value in data.items():
                if hasattr(bien_especifico, key):
                    setattr(bien_especifico, key, value)
        elif tipo_bien == 'COPROPIEDAD':
            for key, value in data.items():
                if hasattr(bien_especifico, key):
                    setattr(bien_especifico, key, value)
        elif tipo_bien == 'OTRO':
            for key, value in data.items():
                if hasattr(bien_especifico, key):
                    setattr(bien_especifico, key, value)
    
    @staticmethod
    def delete_bien(bien_id):
        """Eliminar un bien (esto también eliminará el bien específico)"""
        bien = Bien.query.get(bien_id)
        if not bien:
            return False
        
        try:
            # Eliminar primero el bien específico
            bien_especifico = bien.get_bien_especifico()
            if bien_especifico:
                db.session.delete(bien_especifico)
            
            # Eliminar el bien principal (esto eliminará automáticamente las relaciones)
            db.session.delete(bien)
            db.session.commit()
            return True
            
        except Exception as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def asignar_bien_a_cliente(cliente_id, bien_id):
        """Asignar un bien a un cliente"""
        # Verificar si la asignación ya existe
        asignacion_existente = ClienteBien.query.filter_by(
            cliente_id=cliente_id, 
            bien_id=bien_id
        ).first()
        
        if asignacion_existente:
            return asignacion_existente
        
        asignacion = ClienteBien(cliente_id=cliente_id, bien_id=bien_id)
        db.session.add(asignacion)
        db.session.commit()
        return asignacion
    
    @staticmethod
    def desasignar_bien_de_cliente(cliente_id, bien_id):
        """Desasignar un bien de un cliente"""
        asignacion = ClienteBien.query.filter_by(
            cliente_id=cliente_id, 
            bien_id=bien_id
        ).first()
        
        if asignacion:
            db.session.delete(asignacion)
            db.session.commit()
            return True
        return False 