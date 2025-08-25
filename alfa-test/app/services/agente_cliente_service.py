from app.models.agente_cliente_model import AgenteCliente
from app.models.agente_model import Agente
from app.models.cliente_model import Cliente
from app import db
from datetime import datetime

class AgenteClienteService:
    
    @staticmethod
    def get_all_asignaciones():
        """Obtener todas las asignaciones agente-cliente"""
        return AgenteCliente.query.all()
    
    @staticmethod
    def get_clientes_by_agente(agente_id):
        """Obtener todos los clientes asignados a un agente"""
        agente = Agente.query.get(agente_id)
        return agente.clientes if agente else []
    
    @staticmethod
    def get_agentes_by_cliente(cliente_id):
        """Obtener todos los agentes asignados a un cliente"""
        cliente = Cliente.query.get(cliente_id)
        return cliente.agentes if cliente else []
    
    @staticmethod
    def crear_asignacion(agente_id, cliente_id):
        """Crear una nueva asignación agente-cliente"""
        # Verificar que no exista ya la asignación
        asignacion_existente = AgenteCliente.query.filter_by(
            agente_id=agente_id, 
            cliente_id=cliente_id
        ).first()
        
        if asignacion_existente:
            return None  # Ya existe
        
        # Verificar que existan el agente y cliente
        agente = Agente.query.get(agente_id)
        cliente = Cliente.query.get(cliente_id)
        
        if not agente or not cliente:
            return None  # Agente o cliente no existen
        
        asignacion = AgenteCliente(
            agente_id=agente_id,
            cliente_id=cliente_id,
            fecha_asignacion=datetime.utcnow()
        )
        
        db.session.add(asignacion)
        db.session.commit()
        return asignacion
    
    @staticmethod
    def eliminar_asignacion(agente_id, cliente_id):
        """Eliminar una asignación agente-cliente"""
        asignacion = AgenteCliente.query.filter_by(
            agente_id=agente_id, 
            cliente_id=cliente_id
        ).first()
        
        if asignacion:
            db.session.delete(asignacion)
            db.session.commit()
            return True
        return False
    
    @staticmethod
    def get_asignacion(agente_id, cliente_id):
        """Obtener una asignación específica"""
        return AgenteCliente.query.filter_by(
            agente_id=agente_id, 
            cliente_id=cliente_id
        ).first() 