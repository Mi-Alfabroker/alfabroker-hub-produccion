import { Component, Input, Output, EventEmitter, OnInit, OnChanges, SimpleChanges, ChangeDetectionStrategy, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { 
  ConfiguracionTabla, 
  ConfiguracionColumna, 
  EventoAccionFila, 
  EventoSeleccionFila, 
  EventoOrdenamiento,
  EstadoOrdenamiento,
  TipoDatoColumna
} from '@shared/models/tabla-dinamica.interface';

@Component({
  selector: 'app-tabla-dinamica',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './tabla-dinamica.html',
  styleUrls: ['./tabla-dinamica.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class TablaDinamicaComponent implements OnInit, OnChanges {
  /** Configuración de la tabla */
  @Input() configuracion!: ConfiguracionTabla;
  
  /** Datos a mostrar en la tabla */
  @Input() datos: any[] = [];
  
  /** Si la tabla está cargando datos */
  @Input() cargando = false;
  
  /** ID del elemento que se está eliminando (para mostrar spinner) */
  @Input() eliminandoElementoId: number | string | null = null;
  
  /** Mensaje cuando no hay datos */
  @Input() mensajeSinDatos = 'No hay datos disponibles';
  
  /** Evento cuando se ejecuta una acción en una fila */
  @Output() accionFila = new EventEmitter<EventoAccionFila>();
  
  /** Evento cuando se seleccionan filas */
  @Output() seleccionFila = new EventEmitter<EventoSeleccionFila>();
  
  /** Evento cuando se cambia el ordenamiento */
  @Output() cambioOrdenamiento = new EventEmitter<EventoOrdenamiento>();
  
  /** Datos filtrados y procesados para mostrar */
  datosVista: any[] = [];
  
  /** Término de búsqueda actual */
  terminoBusqueda = '';
  
  /** Estado del ordenamiento */
  estadoOrdenamiento: EstadoOrdenamiento = {
    columnaActiva: null,
    direccion: null
  };
  
  /** Filas seleccionadas */
  filasSeleccionadas: Set<number> = new Set();
  
  /** Si todas las filas están seleccionadas */
  todasSeleccionadas = false;
  
  /** Paginación */
  paginaActual = 1;
  totalPaginas = 1;
  
  constructor(private cdr: ChangeDetectorRef) {}

  ngOnInit(): void {
    console.log('TablaDinamicaComponent - ngOnInit');
    console.log('TablaDinamicaComponent - Configuración:', this.configuracion);
    console.log('TablaDinamicaComponent - Datos:', this.datos);
    this.procesarDatos();
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['datos'] || changes['configuracion']) {
      this.procesarDatos();
    }
  }

  /**
   * Procesa los datos según filtros, ordenamiento y paginación
   */
  private procesarDatos(): void {
    if (!this.datos) {
      this.datosVista = [];
      return;
    }

    let datosProcesados = [...this.datos];

    // Aplicar filtro de búsqueda
    if (this.terminoBusqueda.trim()) {
      datosProcesados = this.filtrarDatos(datosProcesados);
    }

    // Aplicar ordenamiento
    if (this.estadoOrdenamiento.columnaActiva && this.estadoOrdenamiento.direccion) {
      datosProcesados = this.ordenarDatos(datosProcesados);
    }

    // Calcular paginación
    if (this.configuracion?.paginacion) {
      const filasPorPagina = this.configuracion.filasPorPagina || 10;
      this.totalPaginas = Math.ceil(datosProcesados.length / filasPorPagina);
      
      const inicio = (this.paginaActual - 1) * filasPorPagina;
      const fin = inicio + filasPorPagina;
      datosProcesados = datosProcesados.slice(inicio, fin);
    }

    this.datosVista = datosProcesados;
    this.cdr.markForCheck();
  }

  /**
   * Filtra los datos según el término de búsqueda
   */
  private filtrarDatos(datos: any[]): any[] {
    const termino = this.terminoBusqueda.toLowerCase();
    const columnasVisibles = this.configuracion.columnas.filter(col => !col.oculta);

    return datos.filter(fila => {
      return columnasVisibles.some(columna => {
        const valor = this.obtenerValorCelda(fila, columna);
        return String(valor).toLowerCase().includes(termino);
      });
    });
  }

  /**
   * Ordena los datos según la columna y dirección especificadas
   */
  private ordenarDatos(datos: any[]): any[] {
    const columna = this.estadoOrdenamiento.columnaActiva!;
    const direccion = this.estadoOrdenamiento.direccion!;

    return datos.sort((a, b) => {
      const valorA = this.obtenerValorParaOrdenamiento(a[columna]);
      const valorB = this.obtenerValorParaOrdenamiento(b[columna]);

      if (valorA < valorB) return direccion === 'asc' ? -1 : 1;
      if (valorA > valorB) return direccion === 'asc' ? 1 : -1;
      return 0;
    });
  }

  /**
   * Obtiene el valor de una celda formateado para mostrar
   */
  obtenerValorCelda(fila: any, columna: ConfiguracionColumna): any {
    const valor = fila[columna.clave];

    switch (columna.tipo) {
      case 'fecha':
        return this.formatearFecha(valor, columna.configuracion?.formatoFecha);
      case 'numero':
        return this.formatearNumero(valor, columna.configuracion?.formatoNumero);
      case 'estado':
        return this.formatearEstado(valor, columna.configuracion?.estados);
      default:
        return valor;
    }
  }

  /**
   * Obtiene el valor preparado para ordenamiento
   */
  private obtenerValorParaOrdenamiento(valor: any): any {
    if (valor === null || valor === undefined) return '';
    if (valor instanceof Date) return valor.getTime();
    if (typeof valor === 'string') return valor.toLowerCase();
    return valor;
  }

  /**
   * Formatea una fecha según el formato especificado
   */
  private formatearFecha(fecha: any, formato?: string): string {
    if (!fecha) return '';
    
    const fechaObj = fecha instanceof Date ? fecha : new Date(fecha);
    if (isNaN(fechaObj.getTime())) return '';

    // Formato por defecto: DD/MM/YYYY
    const dia = fechaObj.getDate().toString().padStart(2, '0');
    const mes = (fechaObj.getMonth() + 1).toString().padStart(2, '0');
    const año = fechaObj.getFullYear();

    return `${dia}/${mes}/${año}`;
  }

  /**
   * Formatea un número según la configuración especificada
   */
  private formatearNumero(numero: any, config?: any): string {
    if (numero === null || numero === undefined || isNaN(numero)) return '';

    const opciones: Intl.NumberFormatOptions = {};
    
    if (config?.decimales !== undefined) {
      opciones.minimumFractionDigits = config.decimales;
      opciones.maximumFractionDigits = config.decimales;
    }
    
    if (config?.separadorMiles) {
      opciones.useGrouping = true;
    }
    
    if (config?.moneda) {
      opciones.style = 'currency';
      opciones.currency = 'USD';
    }

    return new Intl.NumberFormat('es-ES', opciones).format(numero);
  }

  /**
   * Formatea un estado según la configuración
   */
  formatearEstado(valor: any, estados?: any): any {
    if (!estados || !estados[valor]) {
      return { etiqueta: valor, color: 'gris' };
    }
    return estados[valor];
  }

  /**
   * Maneja el cambio de ordenamiento de una columna
   */
  ordenarPor(columna: ConfiguracionColumna): void {
    if (!columna.ordenable) return;

    let nuevaDireccion: 'asc' | 'desc' | null = 'asc';

    if (this.estadoOrdenamiento.columnaActiva === columna.clave) {
      if (this.estadoOrdenamiento.direccion === 'asc') {
        nuevaDireccion = 'desc';
      } else if (this.estadoOrdenamiento.direccion === 'desc') {
        nuevaDireccion = null;
      }
    }

    this.estadoOrdenamiento = {
      columnaActiva: nuevaDireccion ? columna.clave : null,
      direccion: nuevaDireccion
    };

    this.cambioOrdenamiento.emit({
      columna: columna.clave,
      direccion: nuevaDireccion
    });

    this.procesarDatos();
  }

  /**
   * Ejecuta una acción en una fila
   */
  ejecutarAccion(accionId: string, fila: any, indice: number): void {
    console.log('TablaDinamicaComponent - Ejecutando acción:', accionId, 'en fila:', fila);
    this.accionFila.emit({
      accion: accionId,
      fila,
      indice
    });
  }

  /**
   * Alterna la selección de una fila
   */
  alternarSeleccionFila(indice: number): void {
    if (this.filasSeleccionadas.has(indice)) {
      this.filasSeleccionadas.delete(indice);
    } else {
      this.filasSeleccionadas.add(indice);
    }

    this.actualizarSeleccion();
  }

  /**
   * Alterna la selección de todas las filas
   */
  alternarSeleccionTodas(): void {
    if (this.todasSeleccionadas) {
      this.filasSeleccionadas.clear();
    } else {
      this.datosVista.forEach((_, indice) => {
        this.filasSeleccionadas.add(indice);
      });
    }

    this.actualizarSeleccion();
  }

  /**
   * Actualiza el estado de selección y emite el evento
   */
  private actualizarSeleccion(): void {
    this.todasSeleccionadas = this.datosVista.length > 0 && 
      this.filasSeleccionadas.size === this.datosVista.length;

    const filasSeleccionadas = Array.from(this.filasSeleccionadas).map(indice => this.datosVista[indice]);
    const indicesSeleccionados = Array.from(this.filasSeleccionadas);

    this.seleccionFila.emit({
      filasSeleccionadas,
      indicesSeleccionados
    });

    this.cdr.markForCheck();
  }

  /**
   * Maneja la búsqueda
   */
  buscar(): void {
    this.paginaActual = 1;
    this.procesarDatos();
  }

  /**
   * Cambia de página
   */
  cambiarPagina(pagina: number): void {
    if (pagina >= 1 && pagina <= this.totalPaginas) {
      this.paginaActual = pagina;
      this.procesarDatos();
    }
  }

  /**
   * Verifica si una acción está deshabilitada para una fila
   */
  esAccionDeshabilitada(accion: any, fila: any): boolean {
    // Si se está eliminando este elemento, deshabilitar todas las acciones
    if (this.eliminandoElementoId !== null && fila.id === this.eliminandoElementoId) {
      return true;
    }
    
    return accion.deshabilitada ? accion.deshabilitada(fila) : false;
  }

  /**
   * Verifica si una acción específica está cargando
   */
  esAccionCargando(accion: any, fila: any): boolean {
    return this.eliminandoElementoId !== null && 
           fila.id === this.eliminandoElementoId && 
           accion.id === 'eliminar';
  }

  /**
   * Obtiene las columnas visibles
   */
  get columnasVisibles(): ConfiguracionColumna[] {
    return this.configuracion?.columnas?.filter(col => !col.oculta) || [];
  }
}