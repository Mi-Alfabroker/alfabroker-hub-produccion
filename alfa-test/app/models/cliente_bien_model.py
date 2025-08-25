from app import db
from datetime import datetime

class ClienteBien(db.Model):
    __tablename__ = 'clientes_bienes'
    
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id', ondelete='CASCADE'), primary_key=True)
    bien_id = db.Column(db.Integer, db.ForeignKey('bienes.id', ondelete='CASCADE'), primary_key=True)
    
    def __repr__(self):
        return f'<ClienteBien cliente_id={self.cliente_id}, bien_id={self.bien_id}>'
    
    def to_dict(self):
        return {
            'cliente_id': self.cliente_id,
            'bien_id': self.bien_id
        } 