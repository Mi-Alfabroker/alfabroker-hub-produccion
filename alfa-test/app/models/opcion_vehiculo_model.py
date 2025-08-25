from app import db

class OpcionVehiculo(db.Model):
    __tablename__ = 'opcion_vehiculo'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    valor_vehiculo_asegurado = db.Column(db.Numeric(15, 2))
    valor_accesorios_asegurado = db.Column(db.Numeric(15, 2))
    valor_rc_asegurado = db.Column(db.Numeric(15, 2))
    
    def __repr__(self):
        return f'<OpcionVehiculo {self.id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'valor_vehiculo_asegurado': float(self.valor_vehiculo_asegurado) if self.valor_vehiculo_asegurado else None,
            'valor_accesorios_asegurado': float(self.valor_accesorios_asegurado) if self.valor_accesorios_asegurado else None,
            'valor_rc_asegurado': float(self.valor_rc_asegurado) if self.valor_rc_asegurado else None
        }
    
    def calcular_valor_total_asegurado(self):
        """Calcular el valor total asegurado (sin RC)"""
        total = 0
        if self.valor_vehiculo_asegurado:
            total += float(self.valor_vehiculo_asegurado)
        if self.valor_accesorios_asegurado:
            total += float(self.valor_accesorios_asegurado)
        return total
    
    def validar_valores_asegurados(self, vehiculo_avaluo):
        """Validar que los valores asegurados no excedan los avalúos del vehículo"""
        errores = []
        
        if self.valor_vehiculo_asegurado and vehiculo_avaluo.valor_vehiculo:
            if float(self.valor_vehiculo_asegurado) > float(vehiculo_avaluo.valor_vehiculo):
                errores.append("El valor del vehículo asegurado no puede exceder el avalúo")
        
        if self.valor_accesorios_asegurado and vehiculo_avaluo.valor_accesorios_avaluo:
            if float(self.valor_accesorios_asegurado) > float(vehiculo_avaluo.valor_accesorios_avaluo):
                errores.append("El valor de accesorios asegurado no puede exceder el avalúo")
        
        return errores
    
    def es_valor_minimo_rc_suficiente(self, sublimites_aseguradora):
        """Verificar si el valor RC cumple con los sublímites mínimos"""
        if not self.valor_rc_asegurado:
            return False, "Debe especificar un valor de RC"
        
        errores = []
        valor_rc = float(self.valor_rc_asegurado)
        
        # Verificar sublímites si están definidos
        if sublimites_aseguradora:
            if hasattr(sublimites_aseguradora, 'sublimite_rc_veh_bienes_terceros'):
                sublimite = sublimites_aseguradora.sublimite_rc_veh_bienes_terceros
                if sublimite and valor_rc * sublimite < 50000000:  # Ejemplo: mínimo 50M
                    errores.append("RC insuficiente para bienes de terceros")
        
        return len(errores) == 0, errores 