// Interfaces para autenticación - Sistema Alfa

/** Datos requeridos para el login */
export interface DatosLogin {
  /** Nombre de usuario del agente */
  usuario: string;
  /** Contraseña del agente */
  password: string;
}

/** Información del agente autenticado */
export interface AgenteAutenticado {
  /** ID único del agente */
  id: number;
  /** Nombre completo del agente */
  nombre: string;
  /** Correo electrónico corporativo */
  correo: string;
  /** Nombre de usuario */
  usuario: string;
  /** Rol del agente en el sistema */
  rol: string;
  /** Estado activo del agente */
  activo: boolean;
  /** Fecha de creación del agente */
  fecha_creacion: string;
}

/** Datos del token JWT */
export interface DatosToken {
  /** Agente autenticado */
  agente: AgenteAutenticado;
  /** Token JWT */
  token: string;
  /** Tiempo de expiración en segundos */
  expires_in: number;
}

/** Respuesta exitosa de la API */
export interface RespuestaExitosa<T> {
  /** Indica si la operación fue exitosa */
  success: true;
  /** Mensaje descriptivo */
  message: string;
  /** Datos de respuesta */
  data: T;
}

/** Respuesta de error de la API */
export interface RespuestaError {
  /** Indica que la operación falló */
  success: false;
  /** Mensaje de error */
  message: string;
  /** Detalles adicionales del error */
  error?: string;
}

/** Unión de tipos para respuestas de la API */
export type RespuestaApi<T> = RespuestaExitosa<T> | RespuestaError;

/** Respuesta específica del login */
export type RespuestaLogin = RespuestaApi<DatosToken>;
