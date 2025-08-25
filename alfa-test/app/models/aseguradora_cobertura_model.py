from app import db

class AseguradoraCobertura(db.Model):
    __tablename__ = 'aseguradora_coberturas'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    aseguradora_id = db.Column(db.Integer, db.ForeignKey('aseguradoras.id'), nullable=False)
    tipo_poliza = db.Column(db.Enum('HOGAR', 'VEHICULO', 'COPROPIEDAD', 'OTRO', name='tipo_poliza_cobertura_enum'), nullable=False)
    tipo_item = db.Column(db.String(50), nullable=False)  # 'COBERTURA', 'ASISTENCIA', 'DIFERENCIADOR'
    nombre_item = db.Column(db.String(255), nullable=False)
    
    # Relación con opciones de seguro (N:N)
    opciones_seguro = db.relationship('OpcionSeguro', 
                                     secondary='opciones_seguro_coberturas',
                                     back_populates='coberturas_seleccionadas')
    
    def __repr__(self):
        return f'<AseguradoraCobertura {self.nombre_item} - {self.tipo_poliza}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'aseguradora_id': self.aseguradora_id,
            'tipo_poliza': self.tipo_poliza,
            'tipo_item': self.tipo_item,
            'nombre_item': self.nombre_item
        }
    
    @property
    def es_cobertura(self):
        """Verificar si es una cobertura principal"""
        return self.tipo_item == 'COBERTURA'
    
    @property
    def es_asistencia(self):
        """Verificar si es una asistencia"""
        return self.tipo_item == 'ASISTENCIA'
    
    @property
    def es_diferenciador(self):
        """Verificar si es un diferenciador"""
        return self.tipo_item == 'DIFERENCIADOR' 