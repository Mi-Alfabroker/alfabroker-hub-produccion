from app import db

class OtroBien(db.Model):
    __tablename__ = 'otros_bienes'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tipo_seguro = db.Column(db.String(255))
    bien_asegurado = db.Column(db.String(255))
    valor_bien_asegurar = db.Column(db.Numeric(15, 2))
    detalles_bien_asegurado = db.Column(db.Text)
    
    def __repr__(self):
        return f'<OtroBien {self.id} - {self.bien_asegurado}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'tipo_seguro': self.tipo_seguro,
            'bien_asegurado': self.bien_asegurado,
            'valor_bien_asegurar': float(self.valor_bien_asegurar) if self.valor_bien_asegurar else None,
            'detalles_bien_asegurado': self.detalles_bien_asegurado
        } 