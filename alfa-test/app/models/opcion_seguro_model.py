from app import db
from datetime import datetime

class OpcionSeguro(db.Model):
    __tablename__ = 'opciones_seguro'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    consecutivo = db.Column(db.String(50), unique=True, nullable=False)
    bien_id = db.Column(db.Integer, db.ForeignKey('bienes.id'), nullable=False)
    aseguradora_id = db.Column(db.Integer, db.ForeignKey('aseguradoras.id'), nullable=False)
    tipo_opcion = db.Column(db.Enum('HOGAR', 'VEHICULO', 'COPROPIEDAD', 'OTRO', name='tipo_opcion_enum'), nullable=False)
    opcion_especifica_id = db.Column(db.Integer, nullable=False)
    valor_prima_total = db.Column(db.Numeric(15, 2))
    financiacion_id = db.Column(db.Integer, db.ForeignKey('aseguradora_financiacion.id'))
    
    # Relación con el bien
    bien = db.relationship('Bien', foreign_keys=[bien_id], backref='opciones_seguro')
    
    # Relaciones N:N con deducibles y coberturas
    deducibles_seleccionados = db.relationship('AseguradoraDeducible', 
                                              secondary='opciones_seguro_deducibles',
                                              back_populates='opciones_seguro')
    
    coberturas_seleccionadas = db.relationship('AseguradoraCobertura', 
                                              secondary='opciones_seguro_coberturas',
                                              back_populates='opciones_seguro')
    
    # Relación con póliza (1:1)
    poliza = db.relationship('Poliza', 
                           foreign_keys='Poliza.opcion_seguro_id',
                           backref='opcion_seguro_origen',
                           uselist=False)
    
    def __repr__(self):
        return f'<OpcionSeguro {self.consecutivo}>'
    
    def to_dict(self, include_detalles=True):
        result = {
            'id': self.id,
            'consecutivo': self.consecutivo,
            'bien_id': self.bien_id,
            'aseguradora_id': self.aseguradora_id,
            'tipo_opcion': self.tipo_opcion,
            'opcion_especifica_id': self.opcion_especifica_id,
            'valor_prima_total': float(self.valor_prima_total) if self.valor_prima_total else None,
            'financiacion_id': self.financiacion_id,
            'aseguradora_nombre': self.aseguradora.nombre if self.aseguradora else None,
            'bien_info': self.bien.to_dict(include_specific=False) if self.bien else None,
            'tiene_poliza': self.poliza is not None
        }
        
        if include_detalles:
            # Incluir detalles específicos del tipo de opción
            opcion_especifica = self.get_opcion_especifica()
            if opcion_especifica:
                result['opcion_especifica'] = opcion_especifica.to_dict()
            
            # Incluir deducibles y coberturas seleccionadas
            result['deducibles_seleccionados'] = [d.to_dict() for d in self.deducibles_seleccionados]
            result['coberturas_seleccionadas'] = [c.to_dict() for c in self.coberturas_seleccionadas]
            
            # Incluir información de financiación si existe
            if self.financiacion_seleccionada:
                result['financiacion'] = self.financiacion_seleccionada.to_dict()
        
        return result
    
    def get_opcion_especifica(self):
        """Obtener el detalle específico basado en el tipo de opción"""
        if self.tipo_opcion == 'HOGAR':
            return OpcionHogar.query.get(self.opcion_especifica_id)
        elif self.tipo_opcion == 'VEHICULO':
            return OpcionVehiculo.query.get(self.opcion_especifica_id)
        elif self.tipo_opcion == 'COPROPIEDAD':
            return OpcionCopropiedad.query.get(self.opcion_especifica_id)
        elif self.tipo_opcion == 'OTRO':
            return OpcionOtro.query.get(self.opcion_especifica_id)
        return None
    
    def puede_convertirse_a_poliza(self):
        """Verificar si esta opción puede convertirse a póliza"""
        return self.poliza is None and self.valor_prima_total is not None
    
    def calcular_comision_total(self):
        """Calcular comisión total (normal + sobrecomisión)"""
        if not self.aseguradora or not self.valor_prima_total:
            return 0
        
        comision_normal = self.aseguradora.get_comision_por_tipo(self.tipo_opcion) or 0
        sobrecomision = self.aseguradora.get_sobrecomision_por_tipo(self.tipo_opcion) or 0
        
        return float(self.valor_prima_total) * (comision_normal + sobrecomision)
    
    @staticmethod
    def generar_consecutivo():
        """Generar consecutivo único para la opción"""
        import uuid
        from datetime import datetime
        año = datetime.now().year
        mes = datetime.now().month
        return f"{año}-{mes:02d}-OPC-{str(uuid.uuid4())[:8].upper()}"


# Tablas de relación N:N
opciones_seguro_deducibles = db.Table('opciones_seguro_deducibles',
    db.Column('opcion_seguro_id', db.Integer, db.ForeignKey('opciones_seguro.id'), primary_key=True),
    db.Column('deducible_id', db.Integer, db.ForeignKey('aseguradora_deducibles.id'), primary_key=True)
)

opciones_seguro_coberturas = db.Table('opciones_seguro_coberturas',
    db.Column('opcion_seguro_id', db.Integer, db.ForeignKey('opciones_seguro.id'), primary_key=True),
    db.Column('cobertura_id', db.Integer, db.ForeignKey('aseguradora_coberturas.id'), primary_key=True)
)

# Importación diferida para evitar dependencias circulares
from .opcion_hogar_model import OpcionHogar
from .opcion_vehiculo_model import OpcionVehiculo
from .opcion_copropiedad_model import OpcionCopropiedad
from .opcion_otro_model import OpcionOtro 