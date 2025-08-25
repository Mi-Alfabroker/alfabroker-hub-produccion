from app.models.cliente_model import Cliente
from app import db

class ClienteService:
    
    @staticmethod
    def get_all_clientes():
        """Obtener todos los clientes"""
        return Cliente.query.all()
    
    @staticmethod
    def get_cliente_by_id(cliente_id):
        """Obtener un cliente por ID"""
        return Cliente.query.get(cliente_id)
    
    @staticmethod
    def get_clientes_by_tipo(tipo_cliente):
        """Obtener clientes por tipo (PERSONA o EMPRESA)"""
        return Cliente.query.filter_by(tipo_cliente=tipo_cliente).all()
    
    @staticmethod
    def create_cliente(data):
        """Crear un nuevo cliente"""
        from app.services.auth_service import AuthService
        
        # Validar tipo de cliente
        tipo_cliente = data.get('tipo_cliente')
        if tipo_cliente not in ['PERSONA', 'EMPRESA']:
            raise ValueError("tipo_cliente debe ser 'PERSONA' o 'EMPRESA'")
        
        # Hashear la contraseña
        password = data.get('clave')
        if not password:
            raise ValueError("clave es requerida")
        
        hashed_password = AuthService.hash_password(password)
        
        cliente = Cliente(
            tipo_cliente=tipo_cliente,
            ciudad=data.get('ciudad'),
            direccion=data.get('direccion'),
            telefono_movil=data.get('telefono_movil'),
            correo=data.get('correo'),
            usuario=data.get('usuario'),
            clave=hashed_password,  # Contraseña hasheada
            # Campos para persona natural
            tipo_documento=data.get('tipo_documento'),
            numero_documento=data.get('numero_documento'),
            nombre=data.get('nombre'),
            edad=data.get('edad'),
            # Campos para empresa
            nit=data.get('nit'),
            razon_social=data.get('razon_social'),
            nombre_rep_legal=data.get('nombre_rep_legal'),
            documento_rep_legal=data.get('documento_rep_legal'),
            telefono_rep_legal=data.get('telefono_rep_legal'),
            correo_rep_legal=data.get('correo_rep_legal'),
            contacto_alternativo=data.get('contacto_alternativo')
        )
        
        db.session.add(cliente)
        db.session.commit()
        return cliente
    
    @staticmethod
    def update_cliente(cliente_id, data):
        """Actualizar un cliente existente"""
        cliente = Cliente.query.get(cliente_id)
        if cliente:
            # Campos comunes
            cliente.ciudad = data.get('ciudad', cliente.ciudad)
            cliente.direccion = data.get('direccion', cliente.direccion)
            cliente.telefono_movil = data.get('telefono_movil', cliente.telefono_movil)
            cliente.correo = data.get('correo', cliente.correo)
            cliente.usuario = data.get('usuario', cliente.usuario)
            
            # Solo actualizar clave si se proporciona
            if data.get('clave'):
                from app.services.auth_service import AuthService
                hashed_password = AuthService.hash_password(data.get('clave'))
                cliente.clave = hashed_password  # Contraseña hasheada
            
            # Campos específicos según el tipo
            if cliente.tipo_cliente == 'PERSONA':
                cliente.tipo_documento = data.get('tipo_documento', cliente.tipo_documento)
                cliente.numero_documento = data.get('numero_documento', cliente.numero_documento)
                cliente.nombre = data.get('nombre', cliente.nombre)
                cliente.edad = data.get('edad', cliente.edad)
            elif cliente.tipo_cliente == 'EMPRESA':
                cliente.nit = data.get('nit', cliente.nit)
                cliente.razon_social = data.get('razon_social', cliente.razon_social)
                cliente.nombre_rep_legal = data.get('nombre_rep_legal', cliente.nombre_rep_legal)
                cliente.documento_rep_legal = data.get('documento_rep_legal', cliente.documento_rep_legal)
                cliente.telefono_rep_legal = data.get('telefono_rep_legal', cliente.telefono_rep_legal)
                cliente.correo_rep_legal = data.get('correo_rep_legal', cliente.correo_rep_legal)
                cliente.contacto_alternativo = data.get('contacto_alternativo', cliente.contacto_alternativo)
            
            db.session.commit()
        return cliente
    
    @staticmethod
    def delete_cliente(cliente_id):
        """Eliminar un cliente"""
        cliente = Cliente.query.get(cliente_id)
        if cliente:
            db.session.delete(cliente)
            db.session.commit()
            return True
        return False 