from app import db

class OpcionCopropiedad(db.Model):
    __tablename__ = 'opcion_copropiedad'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    valor_area_comun_asegurado = db.Column(db.Numeric(15, 2))
    valor_area_privada_asegurado = db.Column(db.Numeric(15, 2))
    valor_maquinaria_equipo_asegurado = db.Column(db.Numeric(15, 2))
    valor_equipo_electronico_asegurado = db.Column(db.Numeric(15, 2))
    valor_muebles_asegurado = db.Column(db.Numeric(15, 2))
    valor_directores_asegurado = db.Column(db.Numeric(15, 2))
    valor_rce_asegurado = db.Column(db.Numeric(15, 2))
    valor_manejo_asegurado = db.Column(db.Numeric(15, 2))
    valor_transporte_valores_vigencia_asegurado = db.Column(db.Numeric(15, 2))
    valor_transporte_valores_despacho_asegurado = db.Column(db.Numeric(15, 2))
    
    def __repr__(self):
        return f'<OpcionCopropiedad {self.id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'valor_area_comun_asegurado': float(self.valor_area_comun_asegurado) if self.valor_area_comun_asegurado else None,
            'valor_area_privada_asegurado': float(self.valor_area_privada_asegurado) if self.valor_area_privada_asegurado else None,
            'valor_maquinaria_equipo_asegurado': float(self.valor_maquinaria_equipo_asegurado) if self.valor_maquinaria_equipo_asegurado else None,
            'valor_equipo_electronico_asegurado': float(self.valor_equipo_electronico_asegurado) if self.valor_equipo_electronico_asegurado else None,
            'valor_muebles_asegurado': float(self.valor_muebles_asegurado) if self.valor_muebles_asegurado else None,
            'valor_directores_asegurado': float(self.valor_directores_asegurado) if self.valor_directores_asegurado else None,
            'valor_rce_asegurado': float(self.valor_rce_asegurado) if self.valor_rce_asegurado else None,
            'valor_manejo_asegurado': float(self.valor_manejo_asegurado) if self.valor_manejo_asegurado else None,
            'valor_transporte_valores_vigencia_asegurado': float(self.valor_transporte_valores_vigencia_asegurado) if self.valor_transporte_valores_vigencia_asegurado else None,
            'valor_transporte_valores_despacho_asegurado': float(self.valor_transporte_valores_despacho_asegurado) if self.valor_transporte_valores_despacho_asegurado else None
        }
    
    def calcular_valor_total_asegurado(self):
        """Calcular el valor total asegurado (sin coberturas especiales)"""
        total = 0
        if self.valor_area_comun_asegurado:
            total += float(self.valor_area_comun_asegurado)
        if self.valor_area_privada_asegurado:
            total += float(self.valor_area_privada_asegurado)
        if self.valor_maquinaria_equipo_asegurado:
            total += float(self.valor_maquinaria_equipo_asegurado)
        if self.valor_equipo_electronico_asegurado:
            total += float(self.valor_equipo_electronico_asegurado)
        if self.valor_muebles_asegurado:
            total += float(self.valor_muebles_asegurado)
        return total
    
    def calcular_valor_coberturas_especiales(self):
        """Calcular el valor de coberturas especiales"""
        total = 0
        if self.valor_directores_asegurado:
            total += float(self.valor_directores_asegurado)
        if self.valor_rce_asegurado:
            total += float(self.valor_rce_asegurado)
        if self.valor_manejo_asegurado:
            total += float(self.valor_manejo_asegurado)
        if self.valor_transporte_valores_vigencia_asegurado:
            total += float(self.valor_transporte_valores_vigencia_asegurado)
        if self.valor_transporte_valores_despacho_asegurado:
            total += float(self.valor_transporte_valores_despacho_asegurado)
        return total
    
    def validar_valores_asegurados(self, copropiedad_avaluo):
        """Validar que los valores asegurados no excedan los avalúos de la copropiedad"""
        errores = []
        
        if self.valor_area_comun_asegurado and copropiedad_avaluo.valor_edificio_area_comun_avaluo:
            if float(self.valor_area_comun_asegurado) > float(copropiedad_avaluo.valor_edificio_area_comun_avaluo):
                errores.append("El valor área común asegurado no puede exceder el avalúo")
        
        if self.valor_area_privada_asegurado and copropiedad_avaluo.valor_edificio_area_privada_avaluo:
            if float(self.valor_area_privada_asegurado) > float(copropiedad_avaluo.valor_edificio_area_privada_avaluo):
                errores.append("El valor área privada asegurado no puede exceder el avalúo")
        
        if self.valor_maquinaria_equipo_asegurado and copropiedad_avaluo.valor_maquinaria_equipo_avaluo:
            if float(self.valor_maquinaria_equipo_asegurado) > float(copropiedad_avaluo.valor_maquinaria_equipo_avaluo):
                errores.append("El valor maquinaria equipo asegurado no puede exceder el avalúo")
        
        if self.valor_equipo_electronico_asegurado and copropiedad_avaluo.valor_equipo_electrico_electronico_avaluo:
            if float(self.valor_equipo_electronico_asegurado) > float(copropiedad_avaluo.valor_equipo_electrico_electronico_avaluo):
                errores.append("El valor equipo electrónico asegurado no puede exceder el avalúo")
        
        if self.valor_muebles_asegurado and copropiedad_avaluo.valor_muebles_avaluo:
            if float(self.valor_muebles_asegurado) > float(copropiedad_avaluo.valor_muebles_avaluo):
                errores.append("El valor muebles asegurado no puede exceder el avalúo")
        
        return errores
    
    def validar_sublimites_rce(self, sublimites_aseguradora):
        """Validar que los valores RCE cumplan con los sublímites"""
        if not self.valor_rce_asegurado or not sublimites_aseguradora:
            return []
        
        errores = []
        valor_rce = float(self.valor_rce_asegurado)
        
        # Verificar sublímites específicos de RCE
        if hasattr(sublimites_aseguradora, 'sublimite_rce_cop_contratistas'):
            sublimite = sublimites_aseguradora.sublimite_rce_cop_contratistas
            if sublimite and valor_rce * sublimite < 100000000:  # Ejemplo
                errores.append("RCE insuficiente para contratistas")
        
        return errores 