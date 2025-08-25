from app import db
from datetime import datetime

class Cliente(db.Model):
    __tablename__ = 'clientes'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tipo_cliente = db.Column(db.String(10), nullable=False)  # 'PERSONA' o 'EMPRESA'
    
    # CAMPOS COMUNES Y DE LOGIN
    ciudad = db.Column(db.String(100))
    direccion = db.Column(db.String(255))
    telefono_movil = db.Column(db.String(20))
    correo = db.Column(db.String(100), unique=True)
    usuario = db.Column(db.String(50), unique=True, nullable=False)
    clave = db.Column(db.String(255), nullable=False)  # Se recomienda guardar la clave encriptada
    
    # CAMPOS PARA PERSONA NATURAL (serán NULL si es empresa)
    tipo_documento = db.Column(db.String(10))
    numero_documento = db.Column(db.String(20))
    nombre = db.Column(db.String(150))
    edad = db.Column(db.Integer)
    
    # CAMPOS PARA EMPRESA (serán NULL si es persona)
    nit = db.Column(db.String(20))
    razon_social = db.Column(db.String(255))
    nombre_rep_legal = db.Column(db.String(150))
    documento_rep_legal = db.Column(db.String(20))
    telefono_rep_legal = db.Column(db.String(20))
    correo_rep_legal = db.Column(db.String(100))
    contacto_alternativo = db.Column(db.String(255))
    
    # Relación con la tabla de asignaciones agente-cliente
    asignaciones_cliente = db.relationship('AgenteCliente', 
                                          foreign_keys='AgenteCliente.cliente_id', 
                                          backref='cliente')
    
    # Relación con la tabla de asignaciones cliente-bien
    asignaciones_bienes = db.relationship('ClienteBien', 
                                         foreign_keys='ClienteBien.cliente_id', 
                                         backref='cliente_propietario')
    
    @property
    def agentes(self):
        """Obtener agentes asignados a este cliente"""
        from app.models.agente_model import Agente
        return [Agente.query.get(asig.agente_id) for asig in self.asignaciones_cliente]
    
    @property
    def bienes(self):
        """Obtener bienes asignados a este cliente"""
        from app.models.bien_model import Bien
        return [Bien.query.get(asig.bien_id) for asig in self.asignaciones_bienes]
    
    def __repr__(self):
        if self.tipo_cliente == 'PERSONA':
            return f'<Cliente {self.nombre}>'
        else:
            return f'<Cliente {self.razon_social}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'tipo_cliente': self.tipo_cliente,
            'ciudad': self.ciudad,
            'direccion': self.direccion,
            'telefono_movil': self.telefono_movil,
            'correo': self.correo,
            'usuario': self.usuario,
            # No incluir la clave en la respuesta por seguridad
            'tipo_documento': self.tipo_documento,
            'numero_documento': self.numero_documento,
            'nombre': self.nombre,
            'edad': self.edad,
            'nit': self.nit,
            'razon_social': self.razon_social,
            'nombre_rep_legal': self.nombre_rep_legal,
            'documento_rep_legal': self.documento_rep_legal,
            'telefono_rep_legal': self.telefono_rep_legal,
            'correo_rep_legal': self.correo_rep_legal,
            'contacto_alternativo': self.contacto_alternativo
        } 