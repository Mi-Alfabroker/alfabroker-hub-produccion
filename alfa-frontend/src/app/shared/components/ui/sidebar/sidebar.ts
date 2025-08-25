import { Component, Input, Output, EventEmitter, ChangeDetectionStrategy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router, RouterModule } from '@angular/router';

import { ElementoMenu, ConfiguracionSidebar } from '@core/models/sidebar.interface';

@Component({
  selector: 'app-sidebar',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './sidebar.html',
  styleUrls: ['./sidebar.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class SidebarComponent {
  /** Configuración del sidebar */
  @Input() configuracion: ConfiguracionSidebar | null = null;

  /** Evento emitido cuando se selecciona un elemento del menú */
  @Output() elementoSeleccionado = new EventEmitter<ElementoMenu>();

  /** Evento emitido cuando se cambia el estado de colapso */
  @Output() cambioColapso = new EventEmitter<boolean>();

  /** Evento emitido cuando se hace logout */
  @Output() cerrarSesion = new EventEmitter<void>();

  constructor(private router: Router) {}

  /**
   * Maneja la selección de un elemento del menú
   * @param elemento Elemento seleccionado
   */
  alSeleccionarElemento(elemento: ElementoMenu): void {
    if (elemento.deshabilitado) {
      return;
    }

    // Actualizar estado activo
    this.actualizarElementoActivo(elemento.id);

    // Navegar a la ruta
    this.router.navigate([elemento.ruta]);

    // Emitir evento
    this.elementoSeleccionado.emit(elemento);
  }

  /**
   * Alterna el estado de colapso del sidebar
   */
  alternarColapso(): void {
    if (this.configuracion) {
      this.configuracion.colapsado = !this.configuracion.colapsado;
      this.cambioColapso.emit(this.configuracion.colapsado);
    }
  }

  /**
   * Maneja el evento de cerrar sesión
   */
  alCerrarSesion(): void {
    this.cerrarSesion.emit();
  }

  /**
   * Actualiza el elemento activo en el menú
   * @param elementoId ID del elemento a activar
   */
  private actualizarElementoActivo(elementoId: string): void {
    if (!this.configuracion) return;

    // Desactivar todos los elementos
    this.configuracion.grupos.forEach(grupo => {
      grupo.elementos.forEach(elemento => {
        elemento.activo = elemento.id === elementoId;
      });
    });
  }

  /**
   * Verifica si la ruta actual coincide con un elemento del menú
   * @param ruta Ruta a verificar
   * @returns true si la ruta está activa
   */
  esRutaActiva(ruta: string): boolean {
    return this.router.url === ruta;
  }

  /**
   * Verifica si hay información de usuario disponible
   * @returns true si hay usuario configurado
   */
  tieneUsuario(): boolean {
    return !!(this.configuracion && this.configuracion.usuario);
  }
}
