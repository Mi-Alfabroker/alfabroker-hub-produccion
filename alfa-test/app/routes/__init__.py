# Paquete routes
from .agente_routes import agente_bp
from .cliente_routes import cliente_bp
from .asignacion_routes import asignacion_bp
from .bien_routes import bien_bp
from .aseguradora_routes import aseguradora_bp
from .opcion_seguro_routes import opcion_seguro_bp
from .poliza_routes import poliza_bp

__all__ = ['agente_bp', 'cliente_bp', 'asignacion_bp', 'bien_bp', 'aseguradora_bp', 'opcion_seguro_bp', 'poliza_bp'] 