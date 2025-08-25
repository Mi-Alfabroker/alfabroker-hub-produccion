from app import db

class OpcionHogar(db.Model):
    __tablename__ = 'opcion_hogar'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    valor_inmueble_asegurado = db.Column(db.Numeric(15, 2))
    valor_contenidos_normales_asegurado = db.Column(db.Numeric(15, 2))
    valor_contenidos_especiales_asegurado = db.Column(db.Numeric(15, 2))
    valor_equipo_electronico_asegurado = db.Column(db.Numeric(15, 2))
    valor_maquinaria_equipo_asegurado = db.Column(db.Numeric(15, 2))
    valor_rc_asegurado = db.Column(db.Numeric(15, 2))
    
    def __repr__(self):
        return f'<OpcionHogar {self.id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'valor_inmueble_asegurado': float(self.valor_inmueble_asegurado) if self.valor_inmueble_asegurado else None,
            'valor_contenidos_normales_asegurado': float(self.valor_contenidos_normales_asegurado) if self.valor_contenidos_normales_asegurado else None,
            'valor_contenidos_especiales_asegurado': float(self.valor_contenidos_especiales_asegurado) if self.valor_contenidos_especiales_asegurado else None,
            'valor_equipo_electronico_asegurado': float(self.valor_equipo_electronico_asegurado) if self.valor_equipo_electronico_asegurado else None,
            'valor_maquinaria_equipo_asegurado': float(self.valor_maquinaria_equipo_asegurado) if self.valor_maquinaria_equipo_asegurado else None,
            'valor_rc_asegurado': float(self.valor_rc_asegurado) if self.valor_rc_asegurado else None
        }
    
    def calcular_valor_total_asegurado(self):
        """Calcular el valor total asegurado (sin RC)"""
        total = 0
        if self.valor_inmueble_asegurado:
            total += float(self.valor_inmueble_asegurado)
        if self.valor_contenidos_normales_asegurado:
            total += float(self.valor_contenidos_normales_asegurado)
        if self.valor_contenidos_especiales_asegurado:
            total += float(self.valor_contenidos_especiales_asegurado)
        if self.valor_equipo_electronico_asegurado:
            total += float(self.valor_equipo_electronico_asegurado)
        if self.valor_maquinaria_equipo_asegurado:
            total += float(self.valor_maquinaria_equipo_asegurado)
        return total
    
    def validar_valores_asegurados(self, hogar_avaluo):
        """Validar que los valores asegurados no excedan los avalúos del hogar"""
        errores = []
        
        if self.valor_inmueble_asegurado and hogar_avaluo.valor_inmueble_avaluo:
            if float(self.valor_inmueble_asegurado) > float(hogar_avaluo.valor_inmueble_avaluo):
                errores.append("El valor inmueble asegurado no puede exceder el avalúo")
        
        if self.valor_contenidos_normales_asegurado and hogar_avaluo.valor_contenidos_normales_avaluo:
            if float(self.valor_contenidos_normales_asegurado) > float(hogar_avaluo.valor_contenidos_normales_avaluo):
                errores.append("El valor contenidos normales asegurado no puede exceder el avalúo")
        
        if self.valor_contenidos_especiales_asegurado and hogar_avaluo.valor_contenidos_especiales_avaluo:
            if float(self.valor_contenidos_especiales_asegurado) > float(hogar_avaluo.valor_contenidos_especiales_avaluo):
                errores.append("El valor contenidos especiales asegurado no puede exceder el avalúo")
        
        if self.valor_equipo_electronico_asegurado and hogar_avaluo.valor_equipo_electronico_avaluo:
            if float(self.valor_equipo_electronico_asegurado) > float(hogar_avaluo.valor_equipo_electronico_avaluo):
                errores.append("El valor equipo electrónico asegurado no puede exceder el avalúo")
        
        if self.valor_maquinaria_equipo_asegurado and hogar_avaluo.valor_maquinaria_equipo_avaluo:
            if float(self.valor_maquinaria_equipo_asegurado) > float(hogar_avaluo.valor_maquinaria_equipo_avaluo):
                errores.append("El valor maquinaria equipo asegurado no puede exceder el avalúo")
        
        return errores 