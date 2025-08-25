from app import db

class AseguradoraFinanciacion(db.Model):
    __tablename__ = 'aseguradora_financiacion'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    aseguradora_id = db.Column(db.Integer, db.ForeignKey('aseguradoras.id'), nullable=False)
    nombre_financiera = db.Column(db.String(255), nullable=False)
    tasa_efectiva_mensual = db.Column(db.Numeric(6, 5), nullable=False)
    
    # Relación con opciones de seguro
    opciones_seguro = db.relationship('OpcionSeguro', 
                                     foreign_keys='OpcionSeguro.financiacion_id',
                                     backref='financiacion_seleccionada')
    
    def __repr__(self):
        return f'<AseguradoraFinanciacion {self.nombre_financiera}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'aseguradora_id': self.aseguradora_id,
            'nombre_financiera': self.nombre_financiera,
            'tasa_efectiva_mensual': float(self.tasa_efectiva_mensual) if self.tasa_efectiva_mensual else None
        }
    
    def calcular_cuota_mensual(self, valor_prima, numero_cuotas):
        """Calcular cuota mensual usando la tasa efectiva"""
        if not self.tasa_efectiva_mensual or numero_cuotas <= 0:
            return 0
        
        tasa = float(self.tasa_efectiva_mensual)
        if tasa == 0:
            return valor_prima / numero_cuotas
        
        # Fórmula de cuota mensual con tasa efectiva
        cuota = valor_prima * (tasa * (1 + tasa)**numero_cuotas) / ((1 + tasa)**numero_cuotas - 1)
        return cuota
    
    def calcular_total_financiado(self, valor_prima, numero_cuotas):
        """Calcular el total a pagar con financiación"""
        cuota_mensual = self.calcular_cuota_mensual(valor_prima, numero_cuotas)
        return cuota_mensual * numero_cuotas
    
    def calcular_costo_financiero(self, valor_prima, numero_cuotas):
        """Calcular el costo adicional por financiación"""
        total_financiado = self.calcular_total_financiado(valor_prima, numero_cuotas)
        return total_financiado - valor_prima 