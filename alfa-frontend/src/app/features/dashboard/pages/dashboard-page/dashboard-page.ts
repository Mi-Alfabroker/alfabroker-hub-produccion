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
  selector: 'app-dashboard-page',
  standalone: true,
  imports: [CommonModule, SidebarComponent],
  templateUrl: './dashboard-page.html',
  styleUrls: ['./dashboard-page.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class DashboardPageComponent implements OnInit, OnDestroy {
  /** Datos del agente autenticado */
  agenteActual: AgenteAutenticado | null = null;
  
  /** Configuración del sidebar */
  configuracionSidebar: ConfiguracionSidebar | null = null;
  
  /** Subject para manejar la destrucción del componente */
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
}
