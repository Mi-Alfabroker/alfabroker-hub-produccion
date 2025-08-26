import { Component, Input, Output, EventEmitter, OnInit, OnDestroy, ChangeDetectionStrategy, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Subject } from 'rxjs';
import { takeUntil } from 'rxjs/operators';

import { Aseguradora, CrearAseguradoraDto, ActualizarAseguradoraDto, ComisionesAseguradora } from '@core/models/aseguradora.interface';

@Component({
  selector: 'app-formulario-aseguradora',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './formulario-aseguradora.html',
  styleUrls: ['./formulario-aseguradora.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class FormularioAseguradoraComponent implements OnInit, OnDestroy {
  /** Aseguradora a editar (opcional, si no se proporciona es para crear) */
  @Input() aseguradora: Aseguradora | null = null;
  
  /** Si el formulario está en modo de solo lectura */
  @Input() soloLectura = false;
  
  /** Si mostrar el botón de cancelar */
  @Input() mostrarCancelar = true;
  
  /** Evento cuando se guarda la aseguradora */
  @Output() guardar = new EventEmitter<CrearAseguradoraDto | ActualizarAseguradoraDto>();
  
  /** Evento cuando se cancela la operación */
  @Output() cancelar = new EventEmitter<void>();
  
  /** Formulario reactivo */
  formulario!: FormGroup;
  
  /** Si el formulario se está enviando */
  enviando = false;
  
  /** Si el formulario se guardó exitosamente */
  guardadoExitoso = false;
  
  /** Si el botón de cancelar está deshabilitado */
  botonCancelarDeshabilitado = false;
  
  /** Si el botón de guardar está deshabilitado */
  botonGuardarDeshabilitado = false;
  
  /** Subject para manejar la destrucción del componente */
  private destruir$ = new Subject<void>();

  constructor(
    private fb: FormBuilder,
    private cdr: ChangeDetectorRef
  ) {
    this.crearFormulario();
  }

  ngOnInit(): void {
    if (this.aseguradora) {
      this.cargarDatosAseguradora();
    }
    
    if (this.soloLectura) {
      this.formulario.disable();
    }
    
    // Manejar el estado de los botones según el estado del formulario
    this.actualizarEstadoBotones();
    
    // Suscribirse a cambios del formulario para actualizar estado de botones
    this.formulario.statusChanges
      .pipe(takeUntil(this.destruir$))
      .subscribe(() => {
        this.actualizarEstadoBotones();
      });
  }

  ngOnDestroy(): void {
    this.destruir$.next();
    this.destruir$.complete();
  }

  /**
   * Crea el formulario reactivo
   */
  private crearFormulario(): void {
    this.formulario = this.fb.group({
      // Información básica
      nombre: ['', [Validators.required, Validators.maxLength(255)]],
      numeral_asistencia: ['', Validators.maxLength(255)],
      correo_comercial: ['', [Validators.email, Validators.maxLength(255)]],
      correo_reclamaciones: ['', [Validators.email, Validators.maxLength(255)]],
      oficina_direccion: [''],
      contacto_asignado: ['', Validators.maxLength(255)],
      logo_url: ['', Validators.maxLength(255)],
      pais_origen_bandera_url: ['', Validators.maxLength(255)],
      respaldo_internacional: [''],
      
      // Comisiones normales
      comision_hogar: [null, [Validators.min(0), Validators.max(1)]],
      comision_vehiculo: [null, [Validators.min(0), Validators.max(1)]],
      comision_copropiedad: [null, [Validators.min(0), Validators.max(1)]],
      comision_otro: [null, [Validators.min(0), Validators.max(1)]],
      
      // Sobrecomisiones
      sobrecomision_hogar: [null, [Validators.min(0), Validators.max(1)]],
      sobrecomision_vehiculo: [null, [Validators.min(0), Validators.max(1)]],
      sobrecomision_copropiedad: [null, [Validators.min(0), Validators.max(1)]],
      sobrecomision_otro: [null, [Validators.min(0), Validators.max(1)]],
      
      // Sublímites RC Vehículos
      sublimite_rc_veh_bienes_terceros: [null, [Validators.min(0), Validators.max(1)]],
      sublimite_rc_veh_amparo_patrimonial: [null, [Validators.min(0), Validators.max(1)]],
      sublimite_rc_veh_muerte_una_persona: [null, [Validators.min(0), Validators.max(1)]],
      sublimite_rc_veh_muerte_mas_personas: [null, [Validators.min(0), Validators.max(1)]],
      
      // Sublímites RCE Copropiedad
      sublimite_rce_cop_contratistas: [null, [Validators.min(0), Validators.max(1)]],
      sublimite_rce_cop_cruzada: [null, [Validators.min(0), Validators.max(1)]],
      sublimite_rce_cop_patronal: [null, [Validators.min(0), Validators.max(1)]],
      sublimite_rce_cop_parqueaderos: [null, [Validators.min(0), Validators.max(1)]],
      sublimite_rce_cop_gastos_medicos: [null, [Validators.min(0), Validators.max(1)]]
    });
  }

  /**
   * Carga los datos de la aseguradora en el formulario
   */
  private cargarDatosAseguradora(): void {
    if (!this.aseguradora) return;

    const datos = {
      nombre: this.aseguradora.nombre,
      numeral_asistencia: this.aseguradora.numeral_asistencia || '',
      correo_comercial: this.aseguradora.correo_comercial || '',
      correo_reclamaciones: this.aseguradora.correo_reclamaciones || '',
      oficina_direccion: this.aseguradora.oficina_direccion || '',
      contacto_asignado: this.aseguradora.contacto_asignado || '',
      logo_url: this.aseguradora.logo_url || '',
      pais_origen_bandera_url: this.aseguradora.pais_origen_bandera_url || '',
      respaldo_internacional: this.aseguradora.respaldo_internacional || '',
      
      // Comisiones normales
      comision_hogar: this.aseguradora.comisiones_normales?.HOGAR || null,
      comision_vehiculo: this.aseguradora.comisiones_normales?.VEHICULO || null,
      comision_copropiedad: this.aseguradora.comisiones_normales?.COPROPIEDAD || null,
      comision_otro: this.aseguradora.comisiones_normales?.OTRO || null,
      
      // Sobrecomisiones
      sobrecomision_hogar: this.aseguradora.sobrecomisiones?.HOGAR || null,
      sobrecomision_vehiculo: this.aseguradora.sobrecomisiones?.VEHICULO || null,
      sobrecomision_copropiedad: this.aseguradora.sobrecomisiones?.COPROPIEDAD || null,
      sobrecomision_otro: this.aseguradora.sobrecomisiones?.OTRO || null,
      
      // Sublímites
      sublimite_rc_veh_bienes_terceros: this.aseguradora.sublimite_rc_veh_bienes_terceros || null,
      sublimite_rc_veh_amparo_patrimonial: this.aseguradora.sublimite_rc_veh_amparo_patrimonial || null,
      sublimite_rc_veh_muerte_una_persona: this.aseguradora.sublimite_rc_veh_muerte_una_persona || null,
      sublimite_rc_veh_muerte_mas_personas: this.aseguradora.sublimite_rc_veh_muerte_mas_personas || null,
      sublimite_rce_cop_contratistas: this.aseguradora.sublimite_rce_cop_contratistas || null,
      sublimite_rce_cop_cruzada: this.aseguradora.sublimite_rce_cop_cruzada || null,
      sublimite_rce_cop_patronal: this.aseguradora.sublimite_rce_cop_patronal || null,
      sublimite_rce_cop_parqueaderos: this.aseguradora.sublimite_rce_cop_parqueaderos || null,
      sublimite_rce_cop_gastos_medicos: this.aseguradora.sublimite_rce_cop_gastos_medicos || null
    };

    this.formulario.patchValue(datos);
    this.cdr.markForCheck();
  }

  /**
   * Maneja el envío del formulario
   */
  alEnviarFormulario(): void {
    if (this.formulario.invalid || this.enviando) {
      this.marcarCamposComoTocados();
      return;
    }

    this.enviando = true;
    this.actualizarEstadoBotones();
    const valoresFormulario = this.formulario.value;
    
    // Construir objeto de comisiones normales
    const comisionesNormales: ComisionesAseguradora = {};
    if (valoresFormulario.comision_hogar !== null) comisionesNormales.HOGAR = valoresFormulario.comision_hogar;
    if (valoresFormulario.comision_vehiculo !== null) comisionesNormales.VEHICULO = valoresFormulario.comision_vehiculo;
    if (valoresFormulario.comision_copropiedad !== null) comisionesNormales.COPROPIEDAD = valoresFormulario.comision_copropiedad;
    if (valoresFormulario.comision_otro !== null) comisionesNormales.OTRO = valoresFormulario.comision_otro;
    
    // Construir objeto de sobrecomisiones
    const sobrecomisiones: ComisionesAseguradora = {};
    if (valoresFormulario.sobrecomision_hogar !== null) sobrecomisiones.HOGAR = valoresFormulario.sobrecomision_hogar;
    if (valoresFormulario.sobrecomision_vehiculo !== null) sobrecomisiones.VEHICULO = valoresFormulario.sobrecomision_vehiculo;
    if (valoresFormulario.sobrecomision_copropiedad !== null) sobrecomisiones.COPROPIEDAD = valoresFormulario.sobrecomision_copropiedad;
    if (valoresFormulario.sobrecomision_otro !== null) sobrecomisiones.OTRO = valoresFormulario.sobrecomision_otro;

    const datosAseguradora: CrearAseguradoraDto | ActualizarAseguradoraDto = {
      nombre: valoresFormulario.nombre,
      numeral_asistencia: valoresFormulario.numeral_asistencia || undefined,
      correo_comercial: valoresFormulario.correo_comercial || undefined,
      correo_reclamaciones: valoresFormulario.correo_reclamaciones || undefined,
      oficina_direccion: valoresFormulario.oficina_direccion || undefined,
      contacto_asignado: valoresFormulario.contacto_asignado || undefined,
      logo_url: valoresFormulario.logo_url || undefined,
      pais_origen_bandera_url: valoresFormulario.pais_origen_bandera_url || undefined,
      respaldo_internacional: valoresFormulario.respaldo_internacional || undefined,
      comisiones_normales: Object.keys(comisionesNormales).length > 0 ? comisionesNormales : undefined,
      sobrecomisiones: Object.keys(sobrecomisiones).length > 0 ? sobrecomisiones : undefined,
      sublimite_rc_veh_bienes_terceros: valoresFormulario.sublimite_rc_veh_bienes_terceros || undefined,
      sublimite_rc_veh_amparo_patrimonial: valoresFormulario.sublimite_rc_veh_amparo_patrimonial || undefined,
      sublimite_rc_veh_muerte_una_persona: valoresFormulario.sublimite_rc_veh_muerte_una_persona || undefined,
      sublimite_rc_veh_muerte_mas_personas: valoresFormulario.sublimite_rc_veh_muerte_mas_personas || undefined,
      sublimite_rce_cop_contratistas: valoresFormulario.sublimite_rce_cop_contratistas || undefined,
      sublimite_rce_cop_cruzada: valoresFormulario.sublimite_rce_cop_cruzada || undefined,
      sublimite_rce_cop_patronal: valoresFormulario.sublimite_rce_cop_patronal || undefined,
      sublimite_rce_cop_parqueaderos: valoresFormulario.sublimite_rce_cop_parqueaderos || undefined,
      sublimite_rce_cop_gastos_medicos: valoresFormulario.sublimite_rce_cop_gastos_medicos || undefined
    };

    this.guardar.emit(datosAseguradora);
  }

  /**
   * Maneja la cancelación del formulario
   */
  alCancelar(): void {
    if (this.botonCancelarDeshabilitado) {
      return;
    }
    this.cancelar.emit();
  }

  /**
   * Marca todos los campos como tocados para mostrar errores
   */
  private marcarCamposComoTocados(): void {
    Object.keys(this.formulario.controls).forEach(campo => {
      this.formulario.get(campo)?.markAsTouched();
    });
    this.cdr.markForCheck();
  }

  /**
   * Verifica si un campo tiene errores y ha sido tocado
   */
  tieneCampoError(nombreCampo: string): boolean {
    const campo = this.formulario.get(nombreCampo);
    return !!(campo && campo.invalid && campo.touched);
  }

  /**
   * Obtiene el mensaje de error para un campo
   */
  obtenerMensajeError(nombreCampo: string): string {
    const campo = this.formulario.get(nombreCampo);
    if (!campo || !campo.errors) return '';

    const errores = campo.errors;
    
    if (errores['required']) return 'Este campo es obligatorio';
    if (errores['email']) return 'Debe ser un correo electrónico válido';
    if (errores['maxlength']) return `Máximo ${errores['maxlength'].requiredLength} caracteres`;
    if (errores['min']) return `El valor mínimo es ${errores['min'].min}`;
    if (errores['max']) return `El valor máximo es ${errores['max'].max}`;
    
    return 'Campo inválido';
  }

  /**
   * Resetea el estado de envío
   */
  resetearEnvio(): void {
    this.enviando = false;
    this.guardadoExitoso = true;
    this.actualizarEstadoBotones();
    this.cdr.markForCheck();
    
    // Resetear el estado de éxito después de un momento
    setTimeout(() => {
      this.guardadoExitoso = false;
      this.cdr.markForCheck();
    }, 2000);
  }

  /**
   * Actualiza el estado de los botones según el estado del formulario
   */
  private actualizarEstadoBotones(): void {
    this.botonCancelarDeshabilitado = this.enviando;
    this.botonGuardarDeshabilitado = this.formulario.invalid || this.enviando;
    this.cdr.markForCheck();
  }

  /**
   * Getter para determinar si es modo edición
   */
  get esModoEdicion(): boolean {
    return !!this.aseguradora;
  }

  /**
   * Getter para el título del formulario
   */
  get tituloFormulario(): string {
    if (this.soloLectura) return 'Detalles de la Aseguradora';
    return this.esModoEdicion ? 'Editar Aseguradora' : 'Nueva Aseguradora';
  }
}
