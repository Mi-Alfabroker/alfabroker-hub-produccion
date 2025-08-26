import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError, map } from 'rxjs/operators';

import { 
  Aseguradora, 
  CrearAseguradoraDto, 
  ActualizarAseguradoraDto,
  RespuestaAseguradoras,
  RespuestaAseguradora,
  RespuestaCrearAseguradora,
  TipoPoliza
} from '@core/models/aseguradora.interface';

@Injectable({
  providedIn: 'root'
})
export class AseguradoraService {
  private readonly urlBase = '/api';

  constructor(private http: HttpClient) {}

  /**
   * Obtiene todas las aseguradoras
   * @param incluirPlantillas Si incluir deducibles, coberturas y financiaciones
   * @returns Observable con la lista de aseguradoras
   */
  obtenerAseguradoras(incluirPlantillas: boolean = false): Observable<Aseguradora[]> {
    let parametros = new HttpParams();
    if (incluirPlantillas) {
      parametros = parametros.set('include_plantillas', 'true');
    }

    const url = `${this.urlBase}/aseguradoras`;
    console.log('AseguradoraService - Realizando petición GET a:', url);
    console.log('AseguradoraService - Parámetros:', parametros.toString());

    return this.http.get<RespuestaAseguradoras>(url, { params: parametros })
      .pipe(
        map(respuesta => {
          console.log('AseguradoraService - Respuesta recibida:', respuesta);
          return respuesta.aseguradoras;
        }),
        catchError(error => {
          console.error('AseguradoraService - Error en petición:', error);
          return this.manejarError(error);
        })
      );
  }

  /**
   * Obtiene una aseguradora por ID
   * @param id ID de la aseguradora
   * @param incluirPlantillas Si incluir deducibles, coberturas y financiaciones
   * @returns Observable con los datos de la aseguradora
   */
  obtenerAseguradoraPorId(id: number, incluirPlantillas: boolean = true): Observable<Aseguradora> {
    let parametros = new HttpParams();
    if (incluirPlantillas) {
      parametros = parametros.set('include_plantillas', 'true');
    }

    return this.http.get<RespuestaAseguradora>(`${this.urlBase}/aseguradoras/${id}`, { params: parametros })
      .pipe(
        map(respuesta => respuesta.aseguradora),
        catchError(this.manejarError)
      );
  }

  /**
   * Crea una nueva aseguradora
   * @param datosAseguradora Datos de la aseguradora a crear
   * @returns Observable con los datos de la aseguradora creada
   */
  crearAseguradora(datosAseguradora: CrearAseguradoraDto): Observable<Aseguradora> {
    return this.http.post<RespuestaCrearAseguradora>(`${this.urlBase}/aseguradoras`, datosAseguradora)
      .pipe(
        map(respuesta => respuesta.aseguradora),
        catchError(this.manejarError)
      );
  }

  /**
   * Actualiza una aseguradora existente
   * @param id ID de la aseguradora
   * @param datosAseguradora Datos a actualizar
   * @returns Observable con los datos de la aseguradora actualizada
   */
  actualizarAseguradora(id: number, datosAseguradora: ActualizarAseguradoraDto): Observable<Aseguradora> {
    return this.http.put<RespuestaAseguradora>(`${this.urlBase}/aseguradoras/${id}`, datosAseguradora)
      .pipe(
        map(respuesta => respuesta.aseguradora),
        catchError(this.manejarError)
      );
  }

  /**
   * Elimina una aseguradora
   * @param id ID de la aseguradora a eliminar
   * @returns Observable con el resultado de la operación
   */
  eliminarAseguradora(id: number): Observable<{ message: string }> {
    return this.http.delete<{ message: string }>(`${this.urlBase}/aseguradoras/${id}`)
      .pipe(
        catchError(this.manejarError)
      );
  }

  /**
   * Obtiene las plantillas (deducibles, coberturas, financiaciones) por tipo de póliza
   * @param aseguradoraId ID de la aseguradora
   * @param tipoPoliza Tipo de póliza
   * @returns Observable con las plantillas
   */
  obtenerPlantillasPorTipo(aseguradoraId: number, tipoPoliza: TipoPoliza): Observable<any> {
    return this.http.get(`${this.urlBase}/aseguradoras/${aseguradoraId}/plantillas/${tipoPoliza}`)
      .pipe(
        catchError(this.manejarError)
      );
  }

  /**
   * Crea un deducible para una aseguradora
   * @param aseguradoraId ID de la aseguradora
   * @param datosDeducible Datos del deducible
   * @returns Observable con el resultado
   */
  crearDeducible(aseguradoraId: number, datosDeducible: any): Observable<any> {
    return this.http.post(`${this.urlBase}/aseguradoras/${aseguradoraId}/deducibles`, datosDeducible)
      .pipe(
        catchError(this.manejarError)
      );
  }

  /**
   * Crea una cobertura para una aseguradora
   * @param aseguradoraId ID de la aseguradora
   * @param datosCobertura Datos de la cobertura
   * @returns Observable con el resultado
   */
  crearCobertura(aseguradoraId: number, datosCobertura: any): Observable<any> {
    return this.http.post(`${this.urlBase}/aseguradoras/${aseguradoraId}/coberturas`, datosCobertura)
      .pipe(
        catchError(this.manejarError)
      );
  }

  /**
   * Crea una financiación para una aseguradora
   * @param aseguradoraId ID de la aseguradora
   * @param datosFinanciacion Datos de la financiación
   * @returns Observable con el resultado
   */
  crearFinanciacion(aseguradoraId: number, datosFinanciacion: any): Observable<any> {
    return this.http.post(`${this.urlBase}/aseguradoras/${aseguradoraId}/financiaciones`, datosFinanciacion)
      .pipe(
        catchError(this.manejarError)
      );
  }

  /**
   * Maneja los errores de las peticiones HTTP
   * @param error Error de la petición
   * @returns Observable con el error procesado
   */
  private manejarError(error: any): Observable<never> {
    let mensajeError = 'Ha ocurrido un error desconocido';
    
    console.error('AseguradoraService - Error completo:', error);
    console.error('AseguradoraService - Status:', error.status);
    console.error('AseguradoraService - StatusText:', error.statusText);
    console.error('AseguradoraService - URL:', error.url);
    
    if (error.error instanceof ErrorEvent) {
      // Error del lado del cliente
      mensajeError = `Error del cliente: ${error.error.message}`;
    } else {
      // Error del lado del servidor
      if (error.status === 0) {
        mensajeError = 'No se puede conectar con el servidor. Verifique que la API esté funcionando.';
      } else if (error.error && error.error.error) {
        mensajeError = error.error.error;
      } else if (error.error && error.error.message) {
        mensajeError = error.error.message;
      } else if (error.message) {
        mensajeError = error.message;
      } else {
        mensajeError = `Código de error: ${error.status}, mensaje: ${error.statusText}`;
      }
    }
    
    console.error('Error en AseguradoraService:', error);
    return throwError(() => new Error(mensajeError));
  }
}
