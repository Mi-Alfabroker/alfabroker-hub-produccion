from app import db

class OpcionOtro(db.Model):
    __tablename__ = 'opcion_otro'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    valor_asegurado = db.Column(db.Numeric(15, 2))
    
    def __repr__(self):
        return f'<OpcionOtro {self.id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'valor_asegurado': float(self.valor_asegurado) if self.valor_asegurado else None
        }
    
    def calcular_valor_total_asegurado(self):
        """Calcular el valor total asegurado"""
        return float(self.valor_asegurado) if self.valor_asegurado else 0
    
    def validar_valores_asegurados(self, otro_bien_avaluo):
        """Validar que el valor asegurado no exceda el avalúo del otro bien"""
        errores = []
        
        if self.valor_asegurado and otro_bien_avaluo.valor_bien_asegurar:
            if float(self.valor_asegurado) > float(otro_bien_avaluo.valor_bien_asegurar):
                errores.append("El valor asegurado no puede exceder el avalúo del bien")
        
        return errores
    
    def es_valor_minimo_suficiente(self, valor_minimo_requerido=1000000):
        """Verificar si el valor asegurado cumple con el mínimo requerido"""
        if not self.valor_asegurado:
            return False, "Debe especificar un valor asegurado"
        
        valor = float(self.valor_asegurado)
        if valor < valor_minimo_requerido:
            return False, f"El valor asegurado debe ser al menos {valor_minimo_requerido:,.0f}"
        
        return True, "Valor asegurado válido" 