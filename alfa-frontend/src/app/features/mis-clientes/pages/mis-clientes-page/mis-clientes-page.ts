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

@Component({
  selector: 'app-mis-clientes-page',
  standalone: true,
  imports: [CommonModule, SidebarComponent],
  templateUrl: './mis-clientes-page.html',
  styleUrls: ['./mis-clientes-page.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class MisClientesPageComponent implements OnInit, OnDestroy {
  tituloPagina = 'Mis Clientes';
  descripcionPagina = 'Gestiona y administra tu cartera de clientes';
  
  agenteActual: AgenteAutenticado | null = null;
  configuracionSidebar: ConfiguracionSidebar | null = null;
  
  private destruir$ = new Subject<void>();

  constructor(
    private servicioAuth: AuthService,
    private router: Router,
    private cdr: ChangeDetectorRef,
    private sidebarConfigService: SidebarConfigService
  ) {}

  ngOnInit(): void {
    // Suscribirse a los datos del agente
    this.servicioAuth.agenteActual$
      .pipe(takeUntil(this.destruir$))
      .subscribe({
        next: (agente) => {
          if (agente) {
            this.agenteActual = agente;
            // Configurar el sidebar con los datos del agente usando el servicio global
            this.sidebarConfigService.configurarSidebar(agente);
            this.cdr.markForCheck();
          } else {
            this.router.navigate(['/']);
          }
        },
        error: (error) => {
          console.error('Error al obtener agente actual:', error);
          this.router.navigate(['/']);
        }
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

  ngOnDestroy(): void {
    this.destruir$.next();
    this.destruir$.complete();
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
   * Cierra la sesión del usuario
   */
  cerrarSesion(): void {
    this.sidebarConfigService.limpiarConfiguracion();
    this.servicioAuth.cerrarSesion();
    this.router.navigate(['/']);
  }
}
