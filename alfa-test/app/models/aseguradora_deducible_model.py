from app import db

class AseguradoraDeducible(db.Model):
    __tablename__ = 'aseguradora_deducibles'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    aseguradora_id = db.Column(db.Integer, db.ForeignKey('aseguradoras.id'), nullable=False)
    tipo_poliza = db.Column(db.Enum('HOGAR', 'VEHICULO', 'COPROPIEDAD', 'OTRO', name='tipo_poliza_deducible_enum'), nullable=False)
    categoria = db.Column(db.String(255), nullable=False)
    tipo_deducible = db.Column(db.String(100))
    valor_porcentaje = db.Column(db.Numeric(5, 4))
    valor_minimo = db.Column(db.Numeric(15, 2))
    
    # Relación con opciones de seguro (N:N)
    opciones_seguro = db.relationship('OpcionSeguro', 
                                     secondary='opciones_seguro_deducibles',
                                     back_populates='deducibles_seleccionados')
    
    def __repr__(self):
        return f'<AseguradoraDeducible {self.categoria} - {self.tipo_poliza}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'aseguradora_id': self.aseguradora_id,
            'tipo_poliza': self.tipo_poliza,
            'categoria': self.categoria,
            'tipo_deducible': self.tipo_deducible,
            'valor_porcentaje': float(self.valor_porcentaje) if self.valor_porcentaje else None,
            'valor_minimo': float(self.valor_minimo) if self.valor_minimo else None
        }
    
    def calcular_deducible(self, valor_asegurado_o_perdida):
        """Calcular el valor del deducible para un valor dado"""
        if self.valor_porcentaje:
            deducible_calculado = valor_asegurado_o_perdida * self.valor_porcentaje
            if self.valor_minimo:
                return max(deducible_calculado, self.valor_minimo)
            return deducible_calculado
        elif self.valor_minimo:
            return self.valor_minimo
        return 0 