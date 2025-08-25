from app import db
from datetime import datetime
from enum import Enum

class RolEnum(Enum):
    SUPER_ADMIN = 'super_admin'  # Valor en DB: 'super_admin'
    ADMIN = 'admin'              # Valor en DB: 'admin' 
    AGENTE = 'agente'            # Valor en DB: 'agente'

class Agente(db.Model):
    __tablename__ = 'agente'  # Mantenemos el nombre como en la BD
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(150), nullable=False)
    correo = db.Column(db.String(100), unique=True, nullable=False)
    usuario = db.Column(db.String(50), unique=True, nullable=False)
    clave = db.Column(db.String(255), nullable=False)
    # Especificar explícitamente los valores del enum para MySQL
    rol = db.Column(db.Enum('super_admin', 'admin', 'agente', name='rol_enum'), nullable=False)
    activo = db.Column(db.Boolean, default=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relación con la tabla de asignaciones
    asignaciones_agente = db.relationship('AgenteCliente', 
                                         foreign_keys='AgenteCliente.agente_id', 
                                         backref='agente')
    
    @property
    def clientes(self):
        """Obtener clientes asignados a este agente"""
        from app.models.cliente_model import Cliente
        return [Cliente.query.get(asig.cliente_id) for asig in self.asignaciones_agente]
    
    def __repr__(self):
        return f'<Agente {self.nombre}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'correo': self.correo,
            'usuario': self.usuario,
            # No incluir la clave en la respuesta por seguridad
            'rol': self.rol,  # Devolver el valor directo de la BD
            'activo': self.activo,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None
        } 