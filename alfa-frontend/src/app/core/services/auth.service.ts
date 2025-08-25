import { Injectable, Inject, PLATFORM_ID } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { BehaviorSubject, Observable, of } from 'rxjs';
import { map, catchError, tap } from 'rxjs/operators';

import { 
  DatosLogin, 
  RespuestaLogin, 
  AgenteAutenticado, 
  DatosToken 
} from '@core/models/auth.interface';

/**
 * Servicio principal de autenticación
 * Maneja login, logout, almacenamiento de tokens y estado de sesión
 */
@Injectable({
  providedIn: 'root'
})
export class AuthService {
  /** URL base de la API */
  private readonly urlApi = 'http://18.188.89.220:5000/api';
  
  /** Clave para almacenar el token en localStorage */
  private readonly claveToken = 'token_agente';
  
  /** Clave para almacenar los datos del agente en localStorage */
  private readonly claveAgente = 'datos_agente';
  
  /** Subject para el estado de autenticación */
  private estaAutenticadoSubject = new BehaviorSubject<boolean>(false);
  
  /** Subject para los datos del agente actual */
  private agenteActualSubject = new BehaviorSubject<AgenteAutenticado | null>(null);

  /** Observable público del estado de autenticación */
  public readonly estaAutenticado$ = this.estaAutenticadoSubject.asObservable();
  
  /** Observable público de los datos del agente */
  public readonly agenteActual$ = this.agenteActualSubject.asObservable();

  constructor(
    private http: HttpClient,
    @Inject(PLATFORM_ID) private platformId: Object
  ) {
    // Verificar si hay una sesión existente al inicializar
    this.verificarSesionExistente();
  }

  /**
   * Realiza el login del agente
   * @param datosLogin Credenciales del usuario
   * @returns Observable con el resultado del login
   */
  iniciarSesion(datosLogin: DatosLogin): Observable<boolean> {
    const cabeceras = new HttpHeaders({
      'Content-Type': 'application/json'
    });

    return this.http.post<RespuestaLogin>(
      `${this.urlApi}/auth/agente/login`,
      datosLogin,
      { headers: cabeceras }
    ).pipe(
      map(respuesta => {
        if (respuesta.success) {
          // Guardar datos en localStorage
          this.guardarDatosSesion(respuesta.data);
          
          // Actualizar subjects
          this.estaAutenticadoSubject.next(true);
          this.agenteActualSubject.next(respuesta.data.agente);
          
          return true;
        } else {
          return false;
        }
      }),
      catchError(error => {
        console.error('Error en login:', error);
        return of(false);
      })
    );
  }

  /**
   * Cierra la sesión del usuario
   */
  cerrarSesion(): void {
    // Limpiar localStorage solo si estamos en el navegador
    if (isPlatformBrowser(this.platformId)) {
      localStorage.removeItem(this.claveToken);
      localStorage.removeItem(this.claveAgente);
    }
    
    // Actualizar subjects
    this.estaAutenticadoSubject.next(false);
    this.agenteActualSubject.next(null);
  }

  /**
   * Obtiene el token actual
   * @returns Token JWT o null si no existe
   */
  obtenerToken(): string | null {
    if (isPlatformBrowser(this.platformId)) {
      return localStorage.getItem(this.claveToken);
    }
    return null;
  }

  /**
   * Obtiene los datos del agente actual
   * @returns Datos del agente o null si no está autenticado
   */
  obtenerAgenteActual(): AgenteAutenticado | null {
    if (isPlatformBrowser(this.platformId)) {
      const datosAgente = localStorage.getItem(this.claveAgente);
      return datosAgente ? JSON.parse(datosAgente) : null;
    }
    return null;
  }

  /**
   * Verifica si el usuario está autenticado
   * @returns true si está autenticado, false en caso contrario
   */
  estaAutenticado(): boolean {
    return this.estaAutenticadoSubject.value;
  }

  /**
   * Verifica si hay una sesión existente al inicializar el servicio
   */
  private verificarSesionExistente(): void {
    const token = this.obtenerToken();
    const agente = this.obtenerAgenteActual();
    
    if (token && agente) {
      // TODO: Validar token con el servidor
      this.estaAutenticadoSubject.next(true);
      this.agenteActualSubject.next(agente);
    }
  }

  /**
   * Guarda los datos de la sesión en localStorage
   * @param datosToken Datos del token y agente
   */
  private guardarDatosSesion(datosToken: DatosToken): void {
    if (isPlatformBrowser(this.platformId)) {
      localStorage.setItem(this.claveToken, datosToken.token);
      localStorage.setItem(this.claveAgente, JSON.stringify(datosToken.agente));
    }
  }
}
