// Interfaces para Aseguradoras - Sistema Alfa

/** Datos de una aseguradora */
export interface Aseguradora {
  /** ID único de la aseguradora */
  id: number;
  /** Nombre de la aseguradora */
  nombre: string;
  /** Número de asistencia */
  numeral_asistencia?: string;
  /** Correo comercial */
  correo_comercial?: string;
  /** Correo para reclamaciones */
  correo_reclamaciones?: string;
  /** Dirección de la oficina principal */
  oficina_direccion?: string;
  /** Nombre del contacto asignado */
  contacto_asignado?: string;
  /** URL del logo de la aseguradora */
  logo_url?: string;
  /** URL de la bandera del país de origen */
  pais_origen_bandera_url?: string;
  /** Información sobre respaldo internacional */
  respaldo_internacional?: string;
  /** Comisiones normales por tipo de póliza */
  comisiones_normales?: ComisionesAseguradora;
  /** Sobrecomisiones por tipo de póliza */
  sobrecomisiones?: ComisionesAseguradora;
  /** Sublímite RC vehículos bienes terceros */
  sublimite_rc_veh_bienes_terceros?: number;
  /** Sublímite RC vehículos amparo patrimonial */
  sublimite_rc_veh_amparo_patrimonial?: number;
  /** Sublímite RC vehículos muerte una persona */
  sublimite_rc_veh_muerte_una_persona?: number;
  /** Sublímite RC vehículos muerte más personas */
  sublimite_rc_veh_muerte_mas_personas?: number;
  /** Sublímite RCE copropiedad contratistas */
  sublimite_rce_cop_contratistas?: number;
  /** Sublímite RCE copropiedad cruzada */
  sublimite_rce_cop_cruzada?: number;
  /** Sublímite RCE copropiedad patronal */
  sublimite_rce_cop_patronal?: number;
  /** Sublímite RCE copropiedad parqueaderos */
  sublimite_rce_cop_parqueaderos?: number;
  /** Sublímite RCE copropiedad gastos médicos */
  sublimite_rce_cop_gastos_medicos?: number;
  /** Deducibles (solo si se incluyen plantillas) */
  deducibles?: AseguradoraDeducible[];
  /** Coberturas (solo si se incluyen plantillas) */
  coberturas?: AseguradoraCobertura[];
  /** Financiaciones (solo si se incluyen plantillas) */
  financiaciones?: AseguradoraFinanciacion[];
}

/** Comisiones por tipo de póliza */
export interface ComisionesAseguradora {
  HOGAR?: number;
  VEHICULO?: number;
  COPROPIEDAD?: number;
  OTRO?: number;
}

/** Tipos de póliza disponibles */
export type TipoPoliza = 'HOGAR' | 'VEHICULO' | 'COPROPIEDAD' | 'OTRO';

/** Deducible de una aseguradora */
export interface AseguradoraDeducible {
  /** ID único del deducible */
  id: number;
  /** ID de la aseguradora */
  aseguradora_id: number;
  /** Tipo de póliza */
  tipo_poliza: TipoPoliza;
  /** Categoría del deducible */
  categoria: string;
  /** Tipo de deducible */
  tipo_deducible?: string;
  /** Valor porcentual */
  valor_porcentaje?: number;
  /** Valor mínimo */
  valor_minimo?: number;
}

/** Cobertura de una aseguradora */
export interface AseguradoraCobertura {
  /** ID único de la cobertura */
  id: number;
  /** ID de la aseguradora */
  aseguradora_id: number;
  /** Tipo de póliza */
  tipo_poliza: TipoPoliza;
  /** Tipo de item (COBERTURA, ASISTENCIA, DIFERENCIADOR) */
  tipo_item: 'COBERTURA' | 'ASISTENCIA' | 'DIFERENCIADOR';
  /** Nombre del item */
  nombre_item: string;
}

/** Financiación de una aseguradora */
export interface AseguradoraFinanciacion {
  /** ID único de la financiación */
  id: number;
  /** ID de la aseguradora */
  aseguradora_id: number;
  /** Nombre de la financiera */
  nombre_financiera: string;
  /** Tasa efectiva mensual */
  tasa_efectiva_mensual: number;
}

/** Datos para crear una nueva aseguradora */
export interface CrearAseguradoraDto {
  /** Nombre de la aseguradora */
  nombre: string;
  /** Número de asistencia */
  numeral_asistencia?: string;
  /** Correo comercial */
  correo_comercial?: string;
  /** Correo para reclamaciones */
  correo_reclamaciones?: string;
  /** Dirección de la oficina principal */
  oficina_direccion?: string;
  /** Nombre del contacto asignado */
  contacto_asignado?: string;
  /** URL del logo de la aseguradora */
  logo_url?: string;
  /** URL de la bandera del país de origen */
  pais_origen_bandera_url?: string;
  /** Información sobre respaldo internacional */
  respaldo_internacional?: string;
  /** Comisiones normales por tipo de póliza */
  comisiones_normales?: ComisionesAseguradora;
  /** Sobrecomisiones por tipo de póliza */
  sobrecomisiones?: ComisionesAseguradora;
  /** Sublímite RC vehículos bienes terceros */
  sublimite_rc_veh_bienes_terceros?: number;
  /** Sublímite RC vehículos amparo patrimonial */
  sublimite_rc_veh_amparo_patrimonial?: number;
  /** Sublímite RC vehículos muerte una persona */
  sublimite_rc_veh_muerte_una_persona?: number;
  /** Sublímite RC vehículos muerte más personas */
  sublimite_rc_veh_muerte_mas_personas?: number;
  /** Sublímite RCE copropiedad contratistas */
  sublimite_rce_cop_contratistas?: number;
  /** Sublímite RCE copropiedad cruzada */
  sublimite_rce_cop_cruzada?: number;
  /** Sublímite RCE copropiedad patronal */
  sublimite_rce_cop_patronal?: number;
  /** Sublímite RCE copropiedad parqueaderos */
  sublimite_rce_cop_parqueaderos?: number;
  /** Sublímite RCE copropiedad gastos médicos */
  sublimite_rce_cop_gastos_medicos?: number;
}

/** Datos para actualizar una aseguradora */
export interface ActualizarAseguradoraDto extends Partial<CrearAseguradoraDto> {}

/** Respuesta de la API para obtener aseguradoras */
export interface RespuestaAseguradoras {
  aseguradoras: Aseguradora[];
}

/** Respuesta de la API para obtener una aseguradora */
export interface RespuestaAseguradora {
  aseguradora: Aseguradora;
}

/** Respuesta de la API para crear una aseguradora */
export interface RespuestaCrearAseguradora {
  message: string;
  aseguradora: Aseguradora;
}
