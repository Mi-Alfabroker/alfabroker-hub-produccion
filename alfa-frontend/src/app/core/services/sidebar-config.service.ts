import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { BehaviorSubject, Observable } from 'rxjs';

import { ConfiguracionSidebar } from '@core/models/sidebar.interface';
import { AgenteAutenticado } from '@core/models/auth.interface';

@Injectable({
  providedIn: 'root'
})
export class SidebarConfigService {
  private configuracionSubject = new BehaviorSubject<ConfiguracionSidebar | null>(null);
  
  /** Observable de la configuración del sidebar */
  configuracion$: Observable<ConfiguracionSidebar | null> = this.configuracionSubject.asObservable();

  constructor(private router: Router) {}

  /**
   * Obtiene la configuración actual del sidebar
   */
  obtenerConfiguracion(): ConfiguracionSidebar | null {
    return this.configuracionSubject.value;
  }

  /**
   * Configura el sidebar con los datos del agente autenticado
   * @param agente Datos del agente autenticado
   */
  configurarSidebar(agente: AgenteAutenticado): void {
    const configuracion: ConfiguracionSidebar = {
      colapsado: false,
      tituloApp: 'Alfa Broker Hub',
      subtituloApp: 'Panel de Control - Agente',
      grupos: [
        {
          id: 'principal',
          elementos: [
            {
              id: 'dashboard',
              etiqueta: 'Dashboard',
              ruta: '/dashboard',
              icono: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
                <path d="M9 9h6v6H9z"></path>
              </svg>`,
              activo: this.router.url === '/dashboard'
            },
            {
              id: 'aseguradoras',
              etiqueta: 'Aseguradoras',
              ruta: '/aseguradoras',
              icono: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"></path>
              </svg>`,
              activo: this.router.url === '/aseguradoras'
            },
            {
              id: 'mis-clientes',
              etiqueta: 'Mis Clientes',
              ruta: '/mis-clientes',
              icono: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
                <circle cx="9" cy="7" r="4"></circle>
                <path d="m22 21-3-3"></path>
                <circle cx="16" cy="11" r="3"></circle>
              </svg>`,
              activo: this.router.url === '/mis-clientes'
            }
          ]
        }
      ],
      usuario: {
        nombre: agente.nombre,
        email: agente.correo
      }
    };

    this.configuracionSubject.next(configuracion);
  }

  /**
   * Actualiza el estado activo de los elementos del menú basado en la ruta actual
   */
  actualizarRutaActiva(): void {
    const configuracionActual = this.configuracionSubject.value;
    
    if (configuracionActual) {
      // Actualizar el estado activo de todos los elementos
      configuracionActual.grupos.forEach(grupo => {
        grupo.elementos.forEach(elemento => {
          elemento.activo = this.router.url === elemento.ruta;
        });
      });

      this.configuracionSubject.next(configuracionActual);
    }
  }

  /**
   * Cambia el estado de colapso del sidebar
   * @param colapsado Nuevo estado de colapso
   */
  cambiarColapso(colapsado: boolean): void {
    const configuracionActual = this.configuracionSubject.value;
    
    if (configuracionActual) {
      configuracionActual.colapsado = colapsado;
      this.configuracionSubject.next(configuracionActual);
    }
  }

  /**
   * Limpia la configuración del sidebar (útil al cerrar sesión)
   */
  limpiarConfiguracion(): void {
    this.configuracionSubject.next(null);
  }
}
