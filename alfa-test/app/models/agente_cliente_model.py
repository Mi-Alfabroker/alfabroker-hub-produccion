from app import db
from datetime import datetime

class AgenteCliente(db.Model):
    """Modelo para manejar la relación entre agentes y clientes con campos adicionales"""
    __tablename__ = 'agentes_clientes'
    
    agente_id = db.Column(db.Integer, db.ForeignKey('agente.id'), primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), primary_key=True)
    fecha_asignacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<AgenteCliente agente_id={self.agente_id} cliente_id={self.cliente_id}>'
    
    def to_dict(self):
        return {
            'agente_id': self.agente_id,
            'cliente_id': self.cliente_id,
            'fecha_asignacion': self.fecha_asignacion.isoformat() if self.fecha_asignacion else None
        } 