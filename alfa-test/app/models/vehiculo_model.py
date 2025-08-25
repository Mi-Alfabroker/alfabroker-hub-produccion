from app import db

class Vehiculo(db.Model):
    __tablename__ = 'vehiculos'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tipo_vehiculo = db.Column(db.String(100))
    placa = db.Column(db.String(10), unique=True)
    marca = db.Column(db.String(100))
    serie_referencia = db.Column(db.String(100))
    ano_modelo = db.Column(db.Integer)
    ano_nacimiento_conductor = db.Column(db.Integer)
    codigo_fasecolda = db.Column(db.String(50))
    valor_vehiculo = db.Column(db.Numeric(15, 2))
    valor_accesorios_avaluo = db.Column(db.Numeric(15, 2))
    
    def __repr__(self):
        return f'<Vehiculo {self.id} - {self.placa}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'tipo_vehiculo': self.tipo_vehiculo,
            'placa': self.placa,
            'marca': self.marca,
            'serie_referencia': self.serie_referencia,
            'ano_modelo': self.ano_modelo,
            'ano_nacimiento_conductor': self.ano_nacimiento_conductor,
            'codigo_fasecolda': self.codigo_fasecolda,
            'valor_vehiculo': float(self.valor_vehiculo) if self.valor_vehiculo else None,
            'valor_accesorios_avaluo': float(self.valor_accesorios_avaluo) if self.valor_accesorios_avaluo else None
        } 