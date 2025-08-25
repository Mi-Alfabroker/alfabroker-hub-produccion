import { Component, OnInit, OnDestroy, ChangeDetectionStrategy, ChangeDetectorRef } from '@angular/core';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { Subject } from 'rxjs';
import { takeUntil } from 'rxjs/operators';

import { AuthService } from '@core/services/auth.service';
import { DatosLogin } from '@core/models/auth.interface';

@Component({
  selector: 'app-login-page',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './login-page.html',
  styleUrls: ['./login-page.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class LoginPageComponent implements OnInit, OnDestroy {
  /** Formulario reactivo para el login */
  formularioLogin: FormGroup;
  
  /** Indica si se está procesando el login */
  cargandoLogin = false;
  
  /** Mensaje de error para mostrar al usuario */
  mensajeError = '';
  
  /** Subject para manejar la destrucción del componente */
  private destruir$ = new Subject<void>();

  constructor(
    private constructorFormulario: FormBuilder,
    private servicioAuth: AuthService,
    private router: Router,
    private cdr: ChangeDetectorRef
  ) {
    // Crear formulario con validaciones
    this.formularioLogin = this.constructorFormulario.group({
      usuario: ['', [Validators.required]],
      password: ['', [Validators.required, Validators.minLength(6)]]
    });
  }

  ngOnInit(): void {
    // Verificar si ya está autenticado
    if (this.servicioAuth.estaAutenticado()) {
      this.router.navigate(['/dashboard']);
    }
  }

  /**
   * Maneja el envío del formulario de login
   */
  alEnviarLogin(): void {
    if (this.formularioLogin.valid && !this.cargandoLogin) {
      this.cargandoLogin = true;
      this.mensajeError = '';
      this.cdr.markForCheck();

      const datosLogin: DatosLogin = {
        usuario: this.formularioLogin.value.usuario,
        password: this.formularioLogin.value.password
      };

      this.servicioAuth.iniciarSesion(datosLogin)
        .pipe(takeUntil(this.destruir$))
        .subscribe({
          next: (exito) => {
            this.cargandoLogin = false;
            
            if (exito) {
              // Login exitoso - redirigir al dashboard
              this.router.navigate(['/dashboard']);
            } else {
              // Mostrar error
              this.mensajeError = 'Usuario o contraseña incorrectos';
              this.cdr.markForCheck();
            }
          },
          error: (error) => {
            this.cargandoLogin = false;
            this.mensajeError = 'Error de conexión. Intente nuevamente.';
            console.error('Error en login:', error);
            this.cdr.markForCheck();
          }
        });
    } else {
      this.marcarCamposTocados();
    }
  }

  /**
   * Marca todos los campos del formulario como tocados para mostrar errores
   */
  private marcarCamposTocados(): void {
    Object.keys(this.formularioLogin.controls).forEach(clave => {
      const control = this.formularioLogin.get(clave);
      control?.markAsTouched();
    });
    this.cdr.markForCheck();
  }

  /**
   * Verifica si un campo específico tiene errores y ha sido tocado
   * @param nombreCampo Nombre del campo a verificar
   * @returns true si el campo tiene errores y ha sido tocado
   */
  tieneErrorCampo(nombreCampo: string): boolean {
    const control = this.formularioLogin.get(nombreCampo);
    return !!(control?.invalid && control?.touched);
  }

  /**
   * Obtiene el mensaje de error para un campo específico
   * @param nombreCampo Nombre del campo
   * @returns Mensaje de error o cadena vacía
   */
  obtenerMensajeErrorCampo(nombreCampo: string): string {
    const control = this.formularioLogin.get(nombreCampo);
    
    if (!control?.errors || !control?.touched) {
      return '';
    }

    if (control.errors['required']) {
      return nombreCampo === 'usuario' 
        ? 'El usuario es requerido' 
        : 'La contraseña es requerida';
    }

    if (control.errors['minlength']) {
      return 'La contraseña debe tener al menos 6 caracteres';
    }

    return 'Campo inválido';
  }

  ngOnDestroy(): void {
    this.destruir$.next();
    this.destruir$.complete();
  }
}
