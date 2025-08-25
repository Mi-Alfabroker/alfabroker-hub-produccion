// Interfaces para el sidebar - Sistema Alfa

/** Elemento individual del menú del sidebar */
export interface ElementoMenu {
  /** ID único del elemento */
  id: string;
  /** Etiqueta a mostrar */
  etiqueta: string;
  /** Ruta de navegación */
  ruta: string;
  /** Ícono SVG o nombre del ícono */
  icono: string;
  /** Indica si el elemento está activo */
  activo?: boolean;
  /** Indica si el elemento está deshabilitado */
  deshabilitado?: boolean;
  /** Badge de notificación (opcional) */
  badge?: number | string;
  /** Color del badge */
  colorBadge?: 'primary' | 'warning' | 'error' | 'success';
}

/** Grupo de elementos del menú */
export interface GrupoMenu {
  /** ID único del grupo */
  id: string;
  /** Título del grupo (opcional) */
  titulo?: string;
  /** Elementos del grupo */
  elementos: ElementoMenu[];
}

/** Configuración del sidebar */
export interface ConfiguracionSidebar {
  /** Indica si el sidebar está colapsado */
  colapsado: boolean;
  /** Logo de la aplicación */
  logo?: string;
  /** Título de la aplicación */
  tituloApp: string;
  /** Subtítulo de la aplicación */
  subtituloApp?: string;
  /** Grupos de menú */
  grupos: GrupoMenu[];
  /** Información del usuario */
  usuario?: {
    nombre: string;
    email: string;
    avatar?: string;
  } | null;
}
