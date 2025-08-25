// Interfaces para tabla dinámica reutilizable - Sistema Alfa

/** Tipos de datos que puede mostrar una columna */
export type TipoDatoColumna = 'texto' | 'numero' | 'fecha' | 'estado' | 'acciones' | 'checkbox' | 'icono';

/** Tipo de alineación del contenido de la columna */
export type AlineacionColumna = 'izquierda' | 'centro' | 'derecha';

/** Configuración de una columna de la tabla */
export interface ConfiguracionColumna {
  /** Clave del campo en los datos */
  clave: string;
  /** Título a mostrar en el header */
  titulo: string;
  /** Tipo de dato de la columna */
  tipo: TipoDatoColumna;
  /** Ancho de la columna (opcional) */
  ancho?: string;
  /** Si la columna es ordenable */
  ordenable?: boolean;
  /** Alineación del contenido */
  alineacion?: AlineacionColumna;
  /** Si la columna está oculta */
  oculta?: boolean;
  /** Configuración específica para diferentes tipos */
  configuracion?: ConfiguracionTipoColumna;
}

/** Configuración específica según el tipo de columna */
export interface ConfiguracionTipoColumna {
  /** Para tipo 'estado': mapeo de valores a estilos */
  estados?: {
    [valor: string]: {
      etiqueta: string;
      color: 'verde' | 'azul' | 'amarillo' | 'rojo' | 'gris';
      icono?: string;
    };
  };
  /** Para tipo 'fecha': formato de fecha */
  formatoFecha?: string;
  /** Para tipo 'numero': formato numérico */
  formatoNumero?: {
    decimales?: number;
    moneda?: boolean;
    separadorMiles?: boolean;
  };
  /** Para tipo 'acciones': botones disponibles */
  acciones?: AccionTabla[];
  /** Para tipo 'icono': configuración del ícono */
  icono?: {
    campo?: string; // Campo que determina qué ícono mostrar
    mapeoIconos?: { [valor: string]: string }; // Mapeo de valores a SVG
    colorPorDefecto?: string;
  };
}

/** Configuración de una acción en la tabla */
export interface AccionTabla {
  /** ID único de la acción */
  id: string;
  /** Etiqueta a mostrar */
  etiqueta: string;
  /** Ícono SVG */
  icono: string;
  /** Color del botón */
  color: 'primario' | 'secundario' | 'exito' | 'advertencia' | 'error';
  /** Si la acción está deshabilitada */
  deshabilitada?: (fila: any) => boolean;
  /** Tooltip a mostrar */
  tooltip?: string;
}

/** Configuración general de la tabla */
export interface ConfiguracionTabla {
  /** Columnas de la tabla */
  columnas: ConfiguracionColumna[];
  /** Si se puede seleccionar filas */
  seleccionable?: boolean;
  /** Si se pueden seleccionar múltiples filas */
  seleccionMultiple?: boolean;
  /** Si mostrar el paginador */
  paginacion?: boolean;
  /** Número de filas por página */
  filasPorPagina?: number;
  /** Si mostrar el buscador */
  buscador?: boolean;
  /** Placeholder del buscador */
  placeholderBuscador?: string;
  /** Si mostrar información de totales */
  mostrarInfo?: boolean;
  /** Altura máxima de la tabla */
  alturaMaxima?: string;
  /** Si la tabla es responsiva */
  responsiva?: boolean;
}

/** Evento de acción en una fila */
export interface EventoAccionFila {
  /** ID de la acción ejecutada */
  accion: string;
  /** Datos de la fila */
  fila: any;
  /** Índice de la fila */
  indice: number;
}

/** Evento de selección de filas */
export interface EventoSeleccionFila {
  /** Filas seleccionadas */
  filasSeleccionadas: any[];
  /** Índices de las filas seleccionadas */
  indicesSeleccionados: number[];
}

/** Evento de ordenamiento */
export interface EventoOrdenamiento {
  /** Columna por la que se ordena */
  columna: string;
  /** Dirección del ordenamiento */
  direccion: 'asc' | 'desc' | null;
}

/** Estado de ordenamiento de la tabla */
export interface EstadoOrdenamiento {
  /** Columna activa */
  columnaActiva: string | null;
  /** Dirección actual */
  direccion: 'asc' | 'desc' | null;
}
