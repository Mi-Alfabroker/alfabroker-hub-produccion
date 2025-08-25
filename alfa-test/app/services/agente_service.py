from app.models.agente_model import Agente, RolEnum
from app.models.agente_cliente_model import AgenteCliente
from app import db

class AgenteService:
    
    @staticmethod
    def get_all_agentes():
        """Obtener todos los agentes"""
        return Agente.query.all()
    
    @staticmethod
    def get_agente_by_id(agente_id):
        """Obtener un agente por ID"""
        return Agente.query.get(agente_id)
    
    @staticmethod
    def get_agentes_by_rol(rol):
        """Obtener agentes por rol"""
        # Usar el valor string directamente
        return Agente.query.filter_by(rol=rol).all()
    
    @staticmethod
    def get_agentes_activos():
        """Obtener solo agentes activos"""
        return Agente.query.filter_by(activo=True).all()
    
    @staticmethod
    def create_agente(data):
        """Crear un nuevo agente"""
        from app.services.auth_service import AuthService
        
        # Validar rol
        rol_str = data.get('rol')
        if rol_str not in ['super_admin', 'admin', 'agente']:
            raise ValueError("rol debe ser 'super_admin', 'admin' o 'agente'")
        
        # Hashear la contraseña
        password = data.get('clave')
        if not password:
            raise ValueError("clave es requerida")
        
        hashed_password = AuthService.hash_password(password)
        
        agente = Agente(
            nombre=data.get('nombre'),
            correo=data.get('correo'),
            usuario=data.get('usuario'),
            clave=hashed_password,  # Contraseña hasheada
            rol=rol_str,  # Usar el string directamente
            activo=data.get('activo', True)
        )
        
        db.session.add(agente)
        db.session.commit()
        return agente
    
    @staticmethod
    def update_agente(agente_id, data):
        """Actualizar un agente existente"""
        agente = Agente.query.get(agente_id)
        if agente:
            agente.nombre = data.get('nombre', agente.nombre)
            agente.correo = data.get('correo', agente.correo)
            agente.usuario = data.get('usuario', agente.usuario)
            
            # Solo actualizar clave si se proporciona
            if data.get('clave'):
                from app.services.auth_service import AuthService
                hashed_password = AuthService.hash_password(data.get('clave'))
                agente.clave = hashed_password  # Contraseña hasheada
            
            # Actualizar rol si se proporciona
            if data.get('rol'):
                rol_str = data.get('rol')
                if rol_str in ['super_admin', 'admin', 'agente']:
                    agente.rol = rol_str  # Usar string directamente
            
            agente.activo = data.get('activo', agente.activo)
            db.session.commit()
        return agente
    
    @staticmethod
    def delete_agente(agente_id):
        """Eliminar un agente"""
        agente = Agente.query.get(agente_id)
        if agente:
            # Las asignaciones se eliminarán automáticamente por CASCADE
            db.session.delete(agente)
            db.session.commit()
            return True
        return False
    
    @staticmethod
    def asignar_cliente(agente_id, cliente_id):
        """Asignar un cliente a un agente"""
        from app.models.cliente_model import Cliente
        
        # Verificar que existan el agente y cliente
        agente = Agente.query.get(agente_id)
        cliente = Cliente.query.get(cliente_id)
        
        if not agente or not cliente:
            return False
        
        # Verificar que no exista ya la asignación
        asignacion_existente = AgenteCliente.query.filter_by(
            agente_id=agente_id, 
            cliente_id=cliente_id
        ).first()
        
        if asignacion_existente:
            return False  # Ya existe
        
        # Crear nueva asignación
        asignacion = AgenteCliente(
            agente_id=agente_id,
            cliente_id=cliente_id
        )
        
        db.session.add(asignacion)
        db.session.commit()
        return True
    
    @staticmethod
    def desasignar_cliente(agente_id, cliente_id):
        """Desasignar un cliente de un agente"""
        asignacion = AgenteCliente.query.filter_by(
            agente_id=agente_id, 
            cliente_id=cliente_id
        ).first()
        
        if asignacion:
            db.session.delete(asignacion)
            db.session.commit()
            return True
        return False 