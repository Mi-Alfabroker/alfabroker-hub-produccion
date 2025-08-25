from app import db
from datetime import datetime, date

class PolizaPlanPago(db.Model):
    __tablename__ = 'poliza_plan_pagos'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    poliza_id = db.Column(db.Integer, db.ForeignKey('polizas.id'), nullable=False)
    numero_cuota = db.Column(db.Integer, nullable=False)
    valor_a_pagar = db.Column(db.Numeric(15, 2), nullable=False)
    fecha_maxima_pago = db.Column(db.Date, nullable=False)
    estado_pago = db.Column(db.String(50), default='Pendiente de pago')
    link_portal_pagos = db.Column(db.String(255))
    
    # Campos adicionales para tracking
    fecha_pago_real = db.Column(db.Date)
    valor_pagado = db.Column(db.Numeric(15, 2))
    referencia_pago = db.Column(db.String(100))
    
    def __repr__(self):
        return f'<PolizaPlanPago {self.poliza_id}-{self.numero_cuota}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'poliza_id': self.poliza_id,
            'numero_cuota': self.numero_cuota,
            'valor_a_pagar': float(self.valor_a_pagar) if self.valor_a_pagar else None,
            'fecha_maxima_pago': self.fecha_maxima_pago.isoformat() if self.fecha_maxima_pago else None,
            'estado_pago': self.estado_pago,
            'link_portal_pagos': self.link_portal_pagos,
            'fecha_pago_real': self.fecha_pago_real.isoformat() if self.fecha_pago_real else None,
            'valor_pagado': float(self.valor_pagado) if self.valor_pagado else None,
            'referencia_pago': self.referencia_pago,
            'dias_hasta_vencimiento': self.calcular_dias_hasta_vencimiento(),
            'esta_vencido': self.esta_vencido(),
            'puede_pagarse': self.puede_pagarse()
        }
    
    def calcular_dias_hasta_vencimiento(self):
        """Calcular los días hasta el vencimiento"""
        if not self.fecha_maxima_pago:
            return None
        
        hoy = date.today()
        return (self.fecha_maxima_pago - hoy).days
    
    def esta_vencido(self):
        """Verificar si el pago está vencido"""
        if not self.fecha_maxima_pago:
            return False
        
        if self.estado_pago == 'Pagado':
            return False
        
        return date.today() > self.fecha_maxima_pago
    
    def puede_pagarse(self):
        """Verificar si el pago puede realizarse"""
        return self.estado_pago in ['Pendiente de pago', 'Vencido']
    
    def marcar_como_pagado(self, valor_pagado=None, referencia_pago=None, fecha_pago=None):
        """Marcar la cuota como pagada"""
        self.estado_pago = 'Pagado'
        self.fecha_pago_real = fecha_pago or date.today()
        self.valor_pagado = valor_pagado or self.valor_a_pagar
        self.referencia_pago = referencia_pago
    
    def marcar_como_vencido(self):
        """Marcar la cuota como vencida"""
        if self.esta_vencido() and self.estado_pago == 'Pendiente de pago':
            self.estado_pago = 'Vencido'
    
    def calcular_mora(self, tasa_mora_diaria=0.0015):
        """Calcular valor de mora si está vencido"""
        if not self.esta_vencido():
            return 0
        
        dias_mora = abs(self.calcular_dias_hasta_vencimiento())
        valor_capital = float(self.valor_a_pagar)
        
        return valor_capital * tasa_mora_diaria * dias_mora
    
    def generar_link_portal_pagos(self, base_url="https://pagos.aseguradora.com"):
        """Generar link para portal de pagos"""
        if not self.link_portal_pagos:
            import uuid
            token = str(uuid.uuid4())
            self.link_portal_pagos = f"{base_url}/pago/{self.poliza_id}/{self.numero_cuota}?token={token}"
        
        return self.link_portal_pagos
    
    @staticmethod
    def generar_plan_pagos(poliza_id, valor_prima_total, numero_cuotas, fecha_inicio_vigencia, 
                          tasa_financiacion=None, frecuencia_pago='mensual'):
        """Generar plan de pagos para una póliza"""
        from dateutil.relativedelta import relativedelta
        
        plan_pagos = []
        
        # Calcular valor de cada cuota
        if tasa_financiacion:
            # Con financiación
            if tasa_financiacion == 0:
                valor_cuota = valor_prima_total / numero_cuotas
            else:
                # Fórmula de cuota con tasa
                valor_cuota = valor_prima_total * (tasa_financiacion * (1 + tasa_financiacion)**numero_cuotas) / ((1 + tasa_financiacion)**numero_cuotas - 1)
        else:
            # Sin financiación
            valor_cuota = valor_prima_total / numero_cuotas
        
        # Generar cada cuota
        for i in range(numero_cuotas):
            if frecuencia_pago == 'mensual':
                fecha_vencimiento = fecha_inicio_vigencia + relativedelta(months=i)
            elif frecuencia_pago == 'trimestral':
                fecha_vencimiento = fecha_inicio_vigencia + relativedelta(months=i*3)
            elif frecuencia_pago == 'semestral':
                fecha_vencimiento = fecha_inicio_vigencia + relativedelta(months=i*6)
            else:  # anual
                fecha_vencimiento = fecha_inicio_vigencia + relativedelta(years=i)
            
            cuota = PolizaPlanPago(
                poliza_id=poliza_id,
                numero_cuota=i + 1,
                valor_a_pagar=valor_cuota,
                fecha_maxima_pago=fecha_vencimiento,
                estado_pago='Pendiente de pago'
            )
            plan_pagos.append(cuota)
        
        return plan_pagos 