import { Component, OnInit, OnDestroy, ChangeDetectionStrategy, ChangeDetectorRef, ViewChild } from '@angular/core';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { Subject } from 'rxjs';
import { takeUntil, finalize } from 'rxjs/operators';

import { AuthService } from '@core/services/auth.service';
import { AgenteAutenticado } from '@core/models/auth.interface';
import { SidebarComponent } from '@shared/components/ui/sidebar/sidebar';
import { ConfiguracionSidebar, ElementoMenu } from '@core/models/sidebar.interface';
import { SidebarConfigService } from '@core/services/sidebar-config.service';
import { TablaDinamicaComponent } from '@shared/components/ui/tabla-dinamica/tabla-dinamica';
import { ConfiguracionTabla, EventoAccionFila } from '@shared/models/tabla-dinamica.interface';
import { FormularioAseguradoraComponent } from '@shared/components/ui/formulario-aseguradora/formulario-aseguradora';
import { AseguradoraService } from '@core/services/aseguradora.service';
import { Aseguradora, CrearAseguradoraDto, ActualizarAseguradoraDto } from '@core/models/aseguradora.interface';

@Component({
  selector: 'app-aseguradoras-page',
  standalone: true,
  imports: [CommonModule, SidebarComponent, TablaDinamicaComponent, FormularioAseguradoraComponent],
  templateUrl: './aseguradoras-page.html',
  styleUrls: ['./aseguradoras-page.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class AseguradorasPageComponent implements OnInit, OnDestroy {
  /** Título de la página */
  tituloPagina = 'Aseguradoras';
  
  /** Descripción de la página */
  descripcionPagina = 'Gestiona las compañías aseguradoras y sus productos';
  
  /** Datos del agente autenticado */
  agenteActual: AgenteAutenticado | null = null;
  
  /** Configuración del sidebar */
  configuracionSidebar: ConfiguracionSidebar | null = null;
  
  /** Configuración de la tabla de aseguradoras */
  configuracionTabla!: ConfiguracionTabla;
  
  /** Datos de las aseguradoras */
  datosAseguradoras: Aseguradora[] = [];
  
  /** Estado de carga */
  cargandoTabla = false;
  
  /** Si mostrar el formulario */
  mostrarFormulario = false;
  
  /** Si el botón de agregar está deshabilitado */
  botonAgregarDeshabilitado = false;
  
  /** ID de la aseguradora que se está eliminando */
  eliminandoAseguradoraId: number | null = null;
  
  /** Aseguradora seleccionada para editar */
  aseguradoraSeleccionada: Aseguradora | null = null;
  
  /** Mensaje de error */
  mensajeError: string | null = null;
  
  /** Mensaje de éxito */
  mensajeExito: string | null = null;
  
  /** Referencia al componente del formulario */
  @ViewChild('formularioAseguradora') formularioAseguradora: any;
  
  /** Subject para manejar la destrucción del componente */
  private destruir$ = new Subject<void>();

  constructor(
    private servicioAuth: AuthService,
    private router: Router,
    private cdr: ChangeDetectorRef,
    private sidebarConfigService: SidebarConfigService,
    private aseguradoraService: AseguradoraService
  ) {
    this.configurarTabla();
  }

  ngOnInit(): void {
    console.log('AseguradorasPageComponent - ngOnInit iniciado');
    
    // Suscribirse a los datos del agente
    this.servicioAuth.agenteActual$
      .pipe(takeUntil(this.destruir$))
      .subscribe(agente => {
        console.log('AseguradorasPageComponent - Agente recibido:', agente);
        this.agenteActual = agente;
        
        // Si no hay agente autenticado, redirigir al login
        if (!agente) {
          console.log('AseguradorasPageComponent - No hay agente, redirigiendo al login');
          this.router.navigate(['/']);
        } else {
          console.log('AseguradorasPageComponent - Agente válido, configurando sidebar y cargando aseguradoras');
          // Configurar el sidebar con los datos del agente usando el servicio global
          this.sidebarConfigService.configurarSidebar(agente);
          // Cargar las aseguradoras cuando el agente esté autenticado
          this.cargarAseguradoras();
        }
        
        this.cdr.markForCheck();
      });

    // Suscribirse a la configuración del sidebar
    this.sidebarConfigService.configuracion$
      .pipe(takeUntil(this.destruir$))
      .subscribe(configuracion => {
        this.configuracionSidebar = configuracion;
        this.cdr.markForCheck();
      });

    // Actualizar la ruta activa cuando se navega
    this.sidebarConfigService.actualizarRutaActiva();
    
    // Fallback: Si después de 2 segundos no se ha cargado el agente, cargar aseguradoras de todos modos
    setTimeout(() => {
      if (!this.agenteActual && this.datosAseguradoras.length === 0) {
        console.log('AseguradorasPageComponent - Fallback: Cargando aseguradoras sin agente');
        this.cargarAseguradoras();
      }
    }, 2000);
  }



  /**
   * Maneja la selección de un elemento del menú
   * @param elemento Elemento seleccionado
   */
  alSeleccionarElementoMenu(elemento: ElementoMenu): void {
    // La navegación ya se maneja en el componente sidebar
    this.cdr.markForCheck();
  }

  /**
   * Maneja el cambio de estado de colapso del sidebar
   * @param colapsado Estado de colapso
   */
  alCambiarColapso(colapsado: boolean): void {
    this.sidebarConfigService.cambiarColapso(colapsado);
  }

  /**
   * Maneja el cierre de sesión
   */
  cerrarSesion(): void {
    this.sidebarConfigService.limpiarConfiguracion();
    this.servicioAuth.cerrarSesion();
    this.router.navigate(['/']);
  }

  ngOnDestroy(): void {
    this.destruir$.next();
    this.destruir$.complete();
  }

  /**
   * Configura la tabla de aseguradoras
   */
  private configurarTabla(): void {
    this.configuracionTabla = {
      columnas: [
        {
          clave: 'id',
          titulo: 'ID',
          tipo: 'texto',
          ancho: '80px',
          ordenable: true
        },
        {
          clave: 'nombre',
          titulo: 'Nombre',
          tipo: 'texto',
          ordenable: true
        },
        {
          clave: 'correo_comercial',
          titulo: 'Correo Comercial',
          tipo: 'texto',
          ancho: '200px',
          ordenable: true
        },
        {
          clave: 'contacto_asignado',
          titulo: 'Contacto',
          tipo: 'texto',
          ancho: '150px',
          ordenable: true
        },
        {
          clave: 'numeral_asistencia',
          titulo: 'Asistencia',
          tipo: 'texto',
          ancho: '120px',
          ordenable: true,
          alineacion: 'centro'
        },
        {
          clave: 'acciones',
          titulo: 'Acciones',
          tipo: 'acciones',
          ancho: '120px',
          ordenable: false,
          alineacion: 'centro',
          configuracion: {
            acciones: [
              {
                id: 'editar',
                etiqueta: 'Editar',
                icono: 'icono-editar',
                color: 'primario',
                tooltip: 'Editar aseguradora'
              },
              {
                id: 'eliminar',
                etiqueta: 'Eliminar',
                icono: 'icono-eliminar',
                color: 'error',
                tooltip: 'Eliminar aseguradora'
              }
            ]
          }
        }
      ],
      seleccionable: false,
      seleccionMultiple: false,
      paginacion: true,
      filasPorPagina: 10,
      buscador: true,
      placeholderBuscador: 'Buscar aseguradoras...',
      mostrarInfo: true,
      responsiva: true
    };
  }

  /**
   * Carga las aseguradoras desde la API
   */
  private cargarAseguradoras(): void {
    console.log('AseguradorasPageComponent - Iniciando carga de aseguradoras');
    this.cargandoTabla = true;
    this.botonAgregarDeshabilitado = true;
    this.mensajeError = null;
    this.cdr.markForCheck();

    this.aseguradoraService.obtenerAseguradoras(false)
      .pipe(
        takeUntil(this.destruir$),
        finalize(() => {
          console.log('AseguradorasPageComponent - Finalizando carga de aseguradoras');
          this.cargandoTabla = false;
          this.botonAgregarDeshabilitado = false;
          this.cdr.markForCheck();
        })
      )
      .subscribe({
        next: (aseguradoras) => {
          console.log('AseguradorasPageComponent - Aseguradoras recibidas:', aseguradoras);
          this.datosAseguradoras = aseguradoras;
          this.cdr.markForCheck();
        },
        error: (error) => {
          console.error('AseguradorasPageComponent - Error al cargar aseguradoras:', error);
          this.mensajeError = `Error al cargar aseguradoras: ${error.message}`;
          this.datosAseguradoras = [];
          this.cdr.markForCheck();
        }
      });
  }

  /**
   * Abre el formulario para crear una nueva aseguradora
   */
  abrirFormularioCrear(): void {
    if (this.botonAgregarDeshabilitado) {
      return;
    }
    
    this.aseguradoraSeleccionada = null;
    this.mostrarFormulario = true;
    this.mensajeError = null;
    this.mensajeExito = null;
    this.cdr.markForCheck();
  }

  /**
   * Abre el formulario para editar una aseguradora
   */
  abrirFormularioEditar(aseguradora: Aseguradora): void {
    this.aseguradoraSeleccionada = aseguradora;
    this.mostrarFormulario = true;
    this.mensajeError = null;
    this.mensajeExito = null;
    this.cdr.markForCheck();
  }

  /**
   * Cierra el formulario
   */
  cerrarFormulario(): void {
    this.mostrarFormulario = false;
    this.aseguradoraSeleccionada = null;
    this.mensajeError = null;
    this.mensajeExito = null;
    this.cdr.markForCheck();
  }

  /**
   * Guarda una aseguradora (crear o actualizar)
   */
  guardarAseguradora(datosAseguradora: CrearAseguradoraDto | ActualizarAseguradoraDto): void {
    const esEdicion = !!this.aseguradoraSeleccionada;
    const operacion = esEdicion 
      ? this.aseguradoraService.actualizarAseguradora(this.aseguradoraSeleccionada!.id, datosAseguradora as ActualizarAseguradoraDto)
      : this.aseguradoraService.crearAseguradora(datosAseguradora as CrearAseguradoraDto);

    operacion
      .pipe(takeUntil(this.destruir$))
      .subscribe({
        next: (aseguradora) => {
          // Resetear el estado del formulario
          if (this.formularioAseguradora) {
            this.formularioAseguradora.resetearEnvio();
          }
          
          this.mensajeExito = esEdicion 
            ? 'Aseguradora actualizada exitosamente' 
            : 'Aseguradora creada exitosamente';
          
          // Esperar un momento antes de cerrar para mostrar el mensaje
          setTimeout(() => {
            this.cerrarFormulario();
          }, 1500);
          
          this.cargarAseguradoras(); // Recargar la tabla
          this.limpiarMensajes();
        },
        error: (error) => {
          // Resetear el estado del formulario también en caso de error
          if (this.formularioAseguradora) {
            this.formularioAseguradora.resetearEnvio();
          }
          
          this.mensajeError = `Error al ${esEdicion ? 'actualizar' : 'crear'} aseguradora: ${error.message}`;
          this.cdr.markForCheck();
        }
      });
  }

  /**
   * Elimina una aseguradora
   */
  eliminarAseguradora(aseguradora: Aseguradora): void {
    if (!confirm(`¿Está seguro de que desea eliminar la aseguradora "${aseguradora.nombre}"?`)) {
      return;
    }

    // Establecer estado de eliminación
    this.eliminandoAseguradoraId = aseguradora.id;
    this.mensajeError = null;
    this.mensajeExito = null;
    this.cdr.markForCheck();

    this.aseguradoraService.eliminarAseguradora(aseguradora.id)
      .pipe(
        takeUntil(this.destruir$),
        finalize(() => {
          // Limpiar estado de eliminación
          this.eliminandoAseguradoraId = null;
          this.cdr.markForCheck();
        })
      )
      .subscribe({
        next: () => {
          console.log('✅ Aseguradora eliminada exitosamente');
          this.mensajeExito = 'Aseguradora eliminada exitosamente';
          this.cargarAseguradoras(); // Recargar la tabla
          this.cdr.markForCheck();
          
          // Limpiar mensaje después de 3 segundos
          setTimeout(() => {
            this.mensajeExito = null;
            this.cdr.markForCheck();
          }, 3000);
        },
        error: (error) => {
          console.error('❌ Error al eliminar aseguradora:', error);
          this.mensajeError = `Error al eliminar aseguradora: ${error.message}`;
          this.cdr.markForCheck();
          
          // Limpiar mensaje de error después de 5 segundos
          setTimeout(() => {
            this.mensajeError = null;
            this.cdr.markForCheck();
          }, 5000);
        }
      });
  }

  /**
   * Limpia los mensajes después de un tiempo
   */
  private limpiarMensajes(): void {
    setTimeout(() => {
      this.mensajeError = null;
      this.mensajeExito = null;
      this.cdr.markForCheck();
    }, 5000);
  }

  /**
   * Maneja las acciones ejecutadas en las filas de la tabla
   * @param evento Evento de acción en fila
   */
  manejarAccionFila(evento: EventoAccionFila): void {
    const aseguradora = evento.fila as Aseguradora;
    
    switch (evento.accion) {
      case 'editar':
        this.abrirFormularioEditar(aseguradora);
        break;
      case 'eliminar':
        this.eliminarAseguradora(aseguradora);
        break;
      default:
        console.log('Acción no reconocida:', evento.accion);
    }
  }
}
