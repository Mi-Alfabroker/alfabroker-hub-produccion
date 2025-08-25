from app import db
from datetime import datetime
import json

class Aseguradora(db.Model):
    __tablename__ = 'aseguradoras'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(255), nullable=False)
    numeral_asistencia = db.Column(db.String(255))
    correo_comercial = db.Column(db.String(255))
    correo_reclamaciones = db.Column(db.String(255))
    oficina_direccion = db.Column(db.Text)
    contacto_asignado = db.Column(db.String(255))
    logo_url = db.Column(db.String(255))
    pais_origen_bandera_url = db.Column(db.String(255))
    respaldo_internacional = db.Column(db.Text)
    
    # Campos JSON para comisiones
    comisiones_normales = db.Column(db.JSON)
    sobrecomisiones = db.Column(db.JSON)
    
    # Sublímites para RC Vehículos
    sublimite_rc_veh_bienes_terceros = db.Column(db.Numeric(5, 4))
    sublimite_rc_veh_amparo_patrimonial = db.Column(db.Numeric(5, 4))
    sublimite_rc_veh_muerte_una_persona = db.Column(db.Numeric(5, 4))
    sublimite_rc_veh_muerte_mas_personas = db.Column(db.Numeric(5, 4))
    
    # Sublímites para RCE Copropiedad
    sublimite_rce_cop_contratistas = db.Column(db.Numeric(5, 4))
    sublimite_rce_cop_cruzada = db.Column(db.Numeric(5, 4))
    sublimite_rce_cop_patronal = db.Column(db.Numeric(5, 4))
    sublimite_rce_cop_parqueaderos = db.Column(db.Numeric(5, 4))
    sublimite_rce_cop_gastos_medicos = db.Column(db.Numeric(5, 4))
    
    # Relaciones con las tablas de plantillas
    deducibles = db.relationship('AseguradoraDeducible', 
                                foreign_keys='AseguradoraDeducible.aseguradora_id',
                                backref='aseguradora',
                                cascade='all, delete-orphan')
    
    coberturas = db.relationship('AseguradoraCobertura', 
                                foreign_keys='AseguradoraCobertura.aseguradora_id',
                                backref='aseguradora',
                                cascade='all, delete-orphan')
    
    financiaciones = db.relationship('AseguradoraFinanciacion', 
                                    foreign_keys='AseguradoraFinanciacion.aseguradora_id',
                                    backref='aseguradora',
                                    cascade='all, delete-orphan')
    
    # Relación con opciones de seguro
    opciones_seguro = db.relationship('OpcionSeguro', 
                                     foreign_keys='OpcionSeguro.aseguradora_id',
                                     backref='aseguradora')
    
    def __repr__(self):
        return f'<Aseguradora {self.nombre}>'
    
    def to_dict(self, include_plantillas=False):
        result = {
            'id': self.id,
            'nombre': self.nombre,
            'numeral_asistencia': self.numeral_asistencia,
            'correo_comercial': self.correo_comercial,
            'correo_reclamaciones': self.correo_reclamaciones,
            'oficina_direccion': self.oficina_direccion,
            'contacto_asignado': self.contacto_asignado,
            'logo_url': self.logo_url,
            'pais_origen_bandera_url': self.pais_origen_bandera_url,
            'respaldo_internacional': self.respaldo_internacional,
            'comisiones_normales': self.comisiones_normales,
            'sobrecomisiones': self.sobrecomisiones,
            'sublimite_rc_veh_bienes_terceros': float(self.sublimite_rc_veh_bienes_terceros) if self.sublimite_rc_veh_bienes_terceros else None,
            'sublimite_rc_veh_amparo_patrimonial': float(self.sublimite_rc_veh_amparo_patrimonial) if self.sublimite_rc_veh_amparo_patrimonial else None,
            'sublimite_rc_veh_muerte_una_persona': float(self.sublimite_rc_veh_muerte_una_persona) if self.sublimite_rc_veh_muerte_una_persona else None,
            'sublimite_rc_veh_muerte_mas_personas': float(self.sublimite_rc_veh_muerte_mas_personas) if self.sublimite_rc_veh_muerte_mas_personas else None,
            'sublimite_rce_cop_contratistas': float(self.sublimite_rce_cop_contratistas) if self.sublimite_rce_cop_contratistas else None,
            'sublimite_rce_cop_cruzada': float(self.sublimite_rce_cop_cruzada) if self.sublimite_rce_cop_cruzada else None,
            'sublimite_rce_cop_patronal': float(self.sublimite_rce_cop_patronal) if self.sublimite_rce_cop_patronal else None,
            'sublimite_rce_cop_parqueaderos': float(self.sublimite_rce_cop_parqueaderos) if self.sublimite_rce_cop_parqueaderos else None,
            'sublimite_rce_cop_gastos_medicos': float(self.sublimite_rce_cop_gastos_medicos) if self.sublimite_rce_cop_gastos_medicos else None
        }
        
        if include_plantillas:
            result['deducibles'] = [d.to_dict() for d in self.deducibles]
            result['coberturas'] = [c.to_dict() for c in self.coberturas]
            result['financiaciones'] = [f.to_dict() for f in self.financiaciones]
        
        return result
    
    def get_deducibles_por_tipo(self, tipo_poliza):
        """Obtener deducibles disponibles para un tipo de póliza específico"""
        return [d for d in self.deducibles if d.tipo_poliza == tipo_poliza]
    
    def get_coberturas_por_tipo(self, tipo_poliza):
        """Obtener coberturas disponibles para un tipo de póliza específico"""
        return [c for c in self.coberturas if c.tipo_poliza == tipo_poliza]
    
    def get_comision_por_tipo(self, tipo_poliza):
        """Obtener comisión normal para un tipo de póliza"""
        if self.comisiones_normales and tipo_poliza in self.comisiones_normales:
            return self.comisiones_normales[tipo_poliza]
        return None
    
    def get_sobrecomision_por_tipo(self, tipo_poliza):
        """Obtener sobrecomisión para un tipo de póliza"""
        if self.sobrecomisiones and tipo_poliza in self.sobrecomisiones:
            return self.sobrecomisiones[tipo_poliza]
        return None 