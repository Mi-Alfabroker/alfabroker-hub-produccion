import { Component, OnInit, OnDestroy, ChangeDetectionStrategy, ChangeDetectorRef } from '@angular/core';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { Subject } from 'rxjs';
import { takeUntil } from 'rxjs/operators';

import { AuthService } from '@core/services/auth.service';
import { AgenteAutenticado } from '@core/models/auth.interface';
import { SidebarComponent } from '@shared/components/ui/sidebar/sidebar';
import { ConfiguracionSidebar, ElementoMenu } from '@core/models/sidebar.interface';
import { SidebarConfigService } from '@core/services/sidebar-config.service';
import { TablaDinamicaComponent } from '@shared/components/ui/tabla-dinamica/tabla-dinamica';
import { ConfiguracionTabla, EventoAccionFila } from '@shared/models/tabla-dinamica.interface';

@Component({
  selector: 'app-aseguradoras-page',
  standalone: true,
  imports: [CommonModule, SidebarComponent, TablaDinamicaComponent],
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
  datosAseguradoras: any[] = [];
  
  /** Estado de carga */
  cargandoTabla = false;
  
  /** Subject para manejar la destrucción del componente */
  private destruir$ = new Subject<void>();

  constructor(
    private servicioAuth: AuthService,
    private router: Router,
    private cdr: ChangeDetectorRef,
    private sidebarConfigService: SidebarConfigService
  ) {
    this.configurarTabla();
    this.cargarDatosEjemplo();
  }

  ngOnInit(): void {
    // Suscribirse a los datos del agente
    this.servicioAuth.agenteActual$
      .pipe(takeUntil(this.destruir$))
      .subscribe(agente => {
        this.agenteActual = agente;
        
        // Si no hay agente autenticado, redirigir al login
        if (!agente) {
          this.router.navigate(['/']);
        } else {
          // Configurar el sidebar con los datos del agente usando el servicio global
          this.sidebarConfigService.configurarSidebar(agente);
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
          clave: 'icono',
          titulo: '',
          tipo: 'icono',
          ancho: '60px',
          ordenable: false,
          alineacion: 'centro'
        },
        {
          clave: 'id',
          titulo: 'ID',
          tipo: 'texto',
          ancho: '100px',
          ordenable: true
        },
        {
          clave: 'aseguradora',
          titulo: 'Aseguradora',
          tipo: 'texto',
          ordenable: true
        },
        {
          clave: 'estado',
          titulo: 'Status',
          tipo: 'estado',
          ancho: '150px',
          ordenable: true,
          alineacion: 'centro',
          configuracion: {
            estados: {
              'FULFILLED': {
                etiqueta: 'Fulfilled',
                color: 'verde'
              },
              'CONFIRMED': {
                etiqueta: 'Confirmed',
                color: 'azul'
              },
              'WAITING_SHIPMENT': {
                etiqueta: 'Waiting Shipment',
                color: 'amarillo'
              }
            }
          }
        },
        {
          clave: 'monto',
          titulo: 'Budget',
          tipo: 'numero',
          ancho: '120px',
          ordenable: true,
          alineacion: 'derecha',
          configuracion: {
            formatoNumero: {
              decimales: 1,
              moneda: true,
              separadorMiles: true
            }
          }
        },
        {
          clave: 'fechaCreacion',
          titulo: 'Created',
          tipo: 'fecha',
          ancho: '120px',
          ordenable: true
        },
        {
          clave: 'fechaVencimiento',
          titulo: 'Expired',
          tipo: 'fecha',
          ancho: '120px',
          ordenable: true
        },
        {
          clave: 'acciones',
          titulo: '',
          tipo: 'acciones',
          ancho: '80px',
          ordenable: false,
          alineacion: 'centro',
          configuracion: {
            acciones: [
              {
                id: 'ver',
                etiqueta: 'Ver',
                icono: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
                  <circle cx="12" cy="12" r="3"/>
                </svg>`,
                color: 'primario',
                tooltip: 'Ver detalles'
              }
            ]
          }
        }
      ],
      seleccionable: true,
      seleccionMultiple: true,
      paginacion: true,
      filasPorPagina: 10,
      buscador: true,
      placeholderBuscador: 'Buscar aseguradoras...',
      mostrarInfo: true,
      responsiva: true
    };
  }

  /**
   * Carga datos de ejemplo para mostrar en la tabla
   */
  private cargarDatosEjemplo(): void {
    this.datosAseguradoras = [
      {
        id: '#SO-00003',
        icono: '🏢',
        aseguradora: 'Gaspar Arhanes',
        estado: 'FULFILLED',
        monto: 2874.56,
        fechaCreacion: new Date('2019-05-18'),
        fechaVencimiento: new Date()
      },
      {
        id: '#SO-00004',
        icono: '🏢',
        aseguradora: 'Tristique van Aertsen',
        estado: 'CONFIRMED',
        monto: 1478.48,
        fechaCreacion: new Date('2019-05-12'),
        fechaVencimiento: new Date('2019-05-13')
      },
      {
        id: '#SO-00005',
        icono: '🏢',
        aseguradora: 'Tristique Huitlord',
        estado: 'WAITING_SHIPMENT',
        monto: 243.12,
        fechaCreacion: new Date('2019-05-14'),
        fechaVencimiento: new Date('2019-06-12')
      },
      {
        id: '#SO-00006',
        icono: '🏢',
        aseguradora: 'Tongkiang Jun-Seo',
        estado: 'FULFILLED',
        monto: 123.16,
        fechaCreacion: new Date('2019-05-14'),
        fechaVencimiento: new Date('2019-06-14')
      },
      {
        id: '#SO-00007',
        icono: '🏢',
        aseguradora: 'Ngọ Hải Giang',
        estado: 'CONFIRMED',
        monto: 194.76,
        fechaCreacion: new Date('2019-05-16'),
        fechaVencimiento: new Date('2019-06-24')
      },
      {
        id: '#SO-00008',
        icono: '🏢',
        aseguradora: 'Mijenna Taotic',
        estado: 'CONFIRMED',
        monto: 18789.72,
        fechaCreacion: new Date('2019-05-18'),
        fechaVencimiento: new Date('2019-06-01')
      },
      {
        id: '#SO-00009',
        icono: '🏢',
        aseguradora: 'Lestée Moss',
        estado: 'WAITING_SHIPMENT',
        monto: 457.45,
        fechaCreacion: new Date('2019-05-19'),
        fechaVencimiento: new Date('2019-05-12')
      },
      {
        id: '#SO-00010',
        icono: '🏢',
        aseguradora: 'Jacqueline Lleski',
        estado: 'FULFILLED',
        monto: 4411.96,
        fechaCreacion: new Date('2019-05-18'),
        fechaVencimiento: new Date('2019-06-08')
      },
      {
        id: '#SO-00011',
        icono: '🏢',
        aseguradora: 'Dai Jiang',
        estado: 'FULFILLED',
        monto: 2794.23,
        fechaCreacion: new Date('2019-05-21'),
        fechaVencimiento: new Date('2019-06-24')
      }
    ];
  }

  /**
   * Maneja las acciones ejecutadas en las filas de la tabla
   * @param evento Evento de acción en fila
   */
  manejarAccionFila(evento: EventoAccionFila): void {
    switch (evento.accion) {
      case 'ver':
        console.log('Ver detalles de:', evento.fila);
        // Aquí iría la lógica para ver detalles
        break;
      default:
        console.log('Acción no reconocida:', evento.accion);
    }
  }
}
