from app import db

class Hogar(db.Model):
    __tablename__ = 'hogares'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tipo_inmueble = db.Column(db.String(100))
    ciudad_inmueble = db.Column(db.String(100))
    direccion_inmueble = db.Column(db.String(255))
    numero_pisos = db.Column(db.Integer)
    ano_construccion = db.Column(db.Integer)
    valor_inmueble_avaluo = db.Column(db.Numeric(15, 2))
    valor_contenidos_normales_avaluo = db.Column(db.Numeric(15, 2))
    valor_contenidos_especiales_avaluo = db.Column(db.Numeric(15, 2))
    valor_equipo_electronico_avaluo = db.Column(db.Numeric(15, 2))
    valor_maquinaria_equipo_avaluo = db.Column(db.Numeric(15, 2))
    
    def __repr__(self):
        return f'<Hogar {self.id} - {self.tipo_inmueble}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'tipo_inmueble': self.tipo_inmueble,
            'ciudad_inmueble': self.ciudad_inmueble,
            'direccion_inmueble': self.direccion_inmueble,
            'numero_pisos': self.numero_pisos,
            'ano_construccion': self.ano_construccion,
            'valor_inmueble_avaluo': float(self.valor_inmueble_avaluo) if self.valor_inmueble_avaluo else None,
            'valor_contenidos_normales_avaluo': float(self.valor_contenidos_normales_avaluo) if self.valor_contenidos_normales_avaluo else None,
            'valor_contenidos_especiales_avaluo': float(self.valor_contenidos_especiales_avaluo) if self.valor_contenidos_especiales_avaluo else None,
            'valor_equipo_electronico_avaluo': float(self.valor_equipo_electronico_avaluo) if self.valor_equipo_electronico_avaluo else None,
            'valor_maquinaria_equipo_avaluo': float(self.valor_maquinaria_equipo_avaluo) if self.valor_maquinaria_equipo_avaluo else None
        } 