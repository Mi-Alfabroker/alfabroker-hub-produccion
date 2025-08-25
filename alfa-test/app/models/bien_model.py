from app import db
from datetime import datetime

class Bien(db.Model):
    __tablename__ = 'bienes'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tipo_bien = db.Column(db.Enum('HOGAR', 'VEHICULO', 'COPROPIEDAD', 'OTRO', name='tipo_bien_enum'), nullable=False)
    bien_especifico_id = db.Column(db.Integer, nullable=False)
    estado = db.Column(db.String(50))
    comentarios_generales = db.Column(db.Text)
    vigencias_continuas = db.Column(db.Boolean, default=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relación con la tabla de asignaciones cliente-bien
    asignaciones_bien = db.relationship('ClienteBien', 
                                       foreign_keys='ClienteBien.bien_id', 
                                       backref='bien')
    
    @property
    def clientes(self):
        """Obtener clientes asignados a este bien"""
        from app.models.cliente_model import Cliente
        return [Cliente.query.get(asig.cliente_id) for asig in self.asignaciones_bien]
    
    def get_bien_especifico(self):
        """Obtener el bien específico basado en el tipo_bien"""
        if self.tipo_bien == 'HOGAR':
            from app.models.hogar_model import Hogar
            return Hogar.query.get(self.bien_especifico_id)
        elif self.tipo_bien == 'VEHICULO':
            from app.models.vehiculo_model import Vehiculo
            return Vehiculo.query.get(self.bien_especifico_id)
        elif self.tipo_bien == 'COPROPIEDAD':
            from app.models.copropiedad_model import Copropiedad
            return Copropiedad.query.get(self.bien_especifico_id)
        elif self.tipo_bien == 'OTRO':
            from app.models.otro_bien_model import OtroBien
            return OtroBien.query.get(self.bien_especifico_id)
        return None
    
    def __repr__(self):
        return f'<Bien {self.id} - {self.tipo_bien}>'
    
    def to_dict(self, include_specific=True):
        result = {
            'id': self.id,
            'tipo_bien': self.tipo_bien,
            'bien_especifico_id': self.bien_especifico_id,
            'estado': self.estado,
            'comentarios_generales': self.comentarios_generales,
            'vigencias_continuas': self.vigencias_continuas,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None
        }
        
        if include_specific:
            bien_especifico = self.get_bien_especifico()
            if bien_especifico:
                result['bien_especifico'] = bien_especifico.to_dict()
        
        return result 