from app import db

class Copropiedad(db.Model):
    __tablename__ = 'copropiedades'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tipo_copropiedad = db.Column(db.String(100))
    ciudad = db.Column(db.String(100))
    direccion = db.Column(db.String(255))
    estrato = db.Column(db.Integer)
    ano_construccion = db.Column(db.Integer)
    numero_torres = db.Column(db.Integer)
    numero_maximo_pisos = db.Column(db.Integer)
    numero_maximo_sotanos = db.Column(db.Integer)
    cantidad_unidades_casa = db.Column(db.Integer)
    cantidad_unidades_apartamentos = db.Column(db.Integer)
    cantidad_unidades_locales = db.Column(db.Integer)
    cantidad_unidades_oficinas = db.Column(db.Integer)
    cantidad_unidades_otros = db.Column(db.Integer)
    valor_edificio_area_comun_avaluo = db.Column(db.Numeric(15, 2))
    valor_edificio_area_privada_avaluo = db.Column(db.Numeric(15, 2))
    valor_maquinaria_equipo_avaluo = db.Column(db.Numeric(15, 2))
    valor_equipo_electrico_electronico_avaluo = db.Column(db.Numeric(15, 2))
    valor_muebles_avaluo = db.Column(db.Numeric(15, 2))
    
    def __repr__(self):
        return f'<Copropiedad {self.id} - {self.tipo_copropiedad}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'tipo_copropiedad': self.tipo_copropiedad,
            'ciudad': self.ciudad,
            'direccion': self.direccion,
            'estrato': self.estrato,
            'ano_construccion': self.ano_construccion,
            'numero_torres': self.numero_torres,
            'numero_maximo_pisos': self.numero_maximo_pisos,
            'numero_maximo_sotanos': self.numero_maximo_sotanos,
            'cantidad_unidades_casa': self.cantidad_unidades_casa,
            'cantidad_unidades_apartamentos': self.cantidad_unidades_apartamentos,
            'cantidad_unidades_locales': self.cantidad_unidades_locales,
            'cantidad_unidades_oficinas': self.cantidad_unidades_oficinas,
            'cantidad_unidades_otros': self.cantidad_unidades_otros,
            'valor_edificio_area_comun_avaluo': float(self.valor_edificio_area_comun_avaluo) if self.valor_edificio_area_comun_avaluo else None,
            'valor_edificio_area_privada_avaluo': float(self.valor_edificio_area_privada_avaluo) if self.valor_edificio_area_privada_avaluo else None,
            'valor_maquinaria_equipo_avaluo': float(self.valor_maquinaria_equipo_avaluo) if self.valor_maquinaria_equipo_avaluo else None,
            'valor_equipo_electrico_electronico_avaluo': float(self.valor_equipo_electrico_electronico_avaluo) if self.valor_equipo_electrico_electronico_avaluo else None,
            'valor_muebles_avaluo': float(self.valor_muebles_avaluo) if self.valor_muebles_avaluo else None
        } 