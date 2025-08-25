from app import db
from datetime import datetime, date

class Poliza(db.Model):
    __tablename__ = 'polizas'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    opcion_seguro_id = db.Column(db.Integer, db.ForeignKey('opciones_seguro.id'), unique=True, nullable=False)
    consecutivo_poliza = db.Column(db.String(50), unique=True, nullable=False)
    numero_poliza_aseguradora = db.Column(db.String(100))
    fecha_inicio_vigencia = db.Column(db.Date, nullable=False)
    fecha_fin_vigencia = db.Column(db.Date, nullable=False)
    medio_pago = db.Column(db.String(50))
    estado_cartera = db.Column(db.String(50))
    valor_prima_neta = db.Column(db.Numeric(15, 2))
    valor_otros_costos = db.Column(db.Numeric(15, 2))
    valor_iva = db.Column(db.Numeric(15, 2))
    ingreso_comision_percibido = db.Column(db.Numeric(15, 2))
    
    # Relación con plan de pagos
    plan_pagos = db.relationship('PolizaPlanPago', 
                                foreign_keys='PolizaPlanPago.poliza_id',
                                backref='poliza',
                                cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Poliza {self.consecutivo_poliza}>'
    
    def to_dict(self, include_plan_pagos=False):
        result = {
            'id': self.id,
            'opcion_seguro_id': self.opcion_seguro_id,
            'consecutivo_poliza': self.consecutivo_poliza,
            'numero_poliza_aseguradora': self.numero_poliza_aseguradora,
            'fecha_inicio_vigencia': self.fecha_inicio_vigencia.isoformat() if self.fecha_inicio_vigencia else None,
            'fecha_fin_vigencia': self.fecha_fin_vigencia.isoformat() if self.fecha_fin_vigencia else None,
            'medio_pago': self.medio_pago,
            'estado_cartera': self.estado_cartera,
            'valor_prima_neta': float(self.valor_prima_neta) if self.valor_prima_neta else None,
            'valor_otros_costos': float(self.valor_otros_costos) if self.valor_otros_costos else None,
            'valor_iva': float(self.valor_iva) if self.valor_iva else None,
            'ingreso_comision_percibido': float(self.ingreso_comision_percibido) if self.ingreso_comision_percibido else None,
            'valor_prima_total': self.calcular_valor_prima_total(),
            'dias_vigencia': self.calcular_dias_vigencia(),
            'esta_vigente': self.esta_vigente(),
            'porcentaje_comision': self.calcular_porcentaje_comision()
        }
        
        if include_plan_pagos:
            result['plan_pagos'] = [pago.to_dict() for pago in self.plan_pagos]
            result['resumen_pagos'] = self.get_resumen_pagos()
        
        return result
    
    def calcular_valor_prima_total(self):
        """Calcular el valor total de la prima (neta + IVA + otros costos)"""
        total = 0
        if self.valor_prima_neta:
            total += float(self.valor_prima_neta)
        if self.valor_iva:
            total += float(self.valor_iva)
        if self.valor_otros_costos:
            total += float(self.valor_otros_costos)
        return total
    
    def calcular_dias_vigencia(self):
        """Calcular los días de vigencia de la póliza"""
        if self.fecha_inicio_vigencia and self.fecha_fin_vigencia:
            return (self.fecha_fin_vigencia - self.fecha_inicio_vigencia).days
        return 0
    
    def esta_vigente(self):
        """Verificar si la póliza está vigente"""
        if not self.fecha_inicio_vigencia or not self.fecha_fin_vigencia:
            return False
        
        hoy = date.today()
        return self.fecha_inicio_vigencia <= hoy <= self.fecha_fin_vigencia
    
    def calcular_porcentaje_comision(self):
        """Calcular el porcentaje de comisión sobre la prima neta"""
        if not self.valor_prima_neta or not self.ingreso_comision_percibido:
            return 0
        
        prima_neta = float(self.valor_prima_neta)
        if prima_neta == 0:
            return 0
        
        return (float(self.ingreso_comision_percibido) / prima_neta) * 100
    
    def get_resumen_pagos(self):
        """Obtener resumen del plan de pagos"""
        if not self.plan_pagos:
            return {
                'total_cuotas': 0,
                'cuotas_pagadas': 0,
                'cuotas_pendientes': 0,
                'valor_total_plan': 0,
                'valor_pagado': 0,
                'valor_pendiente': 0
            }
        
        cuotas_pagadas = [p for p in self.plan_pagos if p.estado_pago == 'Pagado']
        cuotas_pendientes = [p for p in self.plan_pagos if p.estado_pago != 'Pagado']
        
        return {
            'total_cuotas': len(self.plan_pagos),
            'cuotas_pagadas': len(cuotas_pagadas),
            'cuotas_pendientes': len(cuotas_pendientes),
            'valor_total_plan': sum(float(p.valor_a_pagar) for p in self.plan_pagos),
            'valor_pagado': sum(float(p.valor_a_pagar) for p in cuotas_pagadas),
            'valor_pendiente': sum(float(p.valor_a_pagar) for p in cuotas_pendientes)
        }
    
    def puede_cancelarse(self):
        """Verificar si la póliza puede cancelarse"""
        # Solo se puede cancelar si está vigente y no tiene pagos pendientes
        if not self.esta_vigente():
            return False, "La póliza no está vigente"
        
        if self.estado_cartera == 'Vencida':
            return False, "La póliza tiene cartera vencida"
        
        return True, "La póliza puede cancelarse"
    
    @staticmethod
    def generar_consecutivo():
        """Generar consecutivo único para la póliza"""
        import uuid
        from datetime import datetime
        año = datetime.now().year
        mes = datetime.now().month
        return f"{año}-{mes:02d}-POL-{str(uuid.uuid4())[:8].upper()}" 