-- =============================================================================
-- SCRIPT DEFINITIVO DE INICIALIZACIÓN DE BASE DE DATOS - SISTEMA ALFA
-- Sistema de Gestión de Seguros - Davivienda
-- 
-- Este script crea la estructura completa de la base de datos desde cero
-- Incluye todas las tablas necesarias para el sistema de seguros
-- =============================================================================

-- Crear base de datos si no existe
CREATE DATABASE IF NOT EXISTS alfa_db;
USE alfa_db;

-- Deshabilitar verificación de claves foráneas temporalmente
SET FOREIGN_KEY_CHECKS = 0;

-- =============================================================================
-- ELIMINACIÓN DE TABLAS EXISTENTES (RESET COMPLETO)
-- =============================================================================
DROP TABLE IF EXISTS poliza_plan_pagos;
DROP TABLE IF EXISTS polizas;
DROP TABLE IF EXISTS opciones_seguro_deducibles;
DROP TABLE IF EXISTS opciones_seguro_coberturas;
DROP TABLE IF EXISTS opcion_hogar;
DROP TABLE IF EXISTS opcion_vehiculo;
DROP TABLE IF EXISTS opcion_copropiedad;
DROP TABLE IF EXISTS opcion_otro;
DROP TABLE IF EXISTS opciones_seguro;
DROP TABLE IF EXISTS aseguradora_financiacion;
DROP TABLE IF EXISTS aseguradora_coberturas;
DROP TABLE IF EXISTS aseguradora_deducibles;
DROP TABLE IF EXISTS aseguradoras;
DROP TABLE IF EXISTS clientes_bienes;
DROP TABLE IF EXISTS agentes_clientes;
DROP TABLE IF EXISTS hogares;
DROP TABLE IF EXISTS vehiculos;
DROP TABLE IF EXISTS copropiedades;
DROP TABLE IF EXISTS otros_bienes;
DROP TABLE IF EXISTS bienes;
DROP TABLE IF EXISTS agente;
DROP TABLE IF EXISTS clientes;

-- Rehabilitar verificación de claves foráneas
SET FOREIGN_KEY_CHECKS = 1;

-- =============================================================================
-- CREACIÓN DE TABLAS PRINCIPALES
-- =============================================================================

-- -----------------------------------------------------------------------------
-- Tabla de clientes (personas naturales y empresas)
-- -----------------------------------------------------------------------------
CREATE TABLE clientes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    tipo_cliente VARCHAR(10) NOT NULL, -- 'PERSONA' o 'EMPRESA'

    -- CAMPOS COMUNES Y DE LOGIN
    ciudad VARCHAR(100),
    direccion VARCHAR(255),
    telefono_movil VARCHAR(20),
    correo VARCHAR(100) UNIQUE,
    usuario VARCHAR(50) UNIQUE NOT NULL,
    clave VARCHAR(255) NOT NULL,

    -- CAMPOS PARA PERSONA NATURAL (serán NULL si es empresa)
    tipo_documento VARCHAR(10),
    numero_documento VARCHAR(20),
    nombre VARCHAR(150),
    edad INT,

    -- CAMPOS PARA EMPRESA (serán NULL si es persona)
    nit VARCHAR(20),
    razon_social VARCHAR(255),
    nombre_rep_legal VARCHAR(150),
    documento_rep_legal VARCHAR(20),
    telefono_rep_legal VARCHAR(20),
    correo_rep_legal VARCHAR(100),
    contacto_alternativo VARCHAR(255)
);

-- -----------------------------------------------------------------------------
-- Tabla de agentes
-- -----------------------------------------------------------------------------
CREATE TABLE agente (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(150) NOT NULL,
    correo VARCHAR(100) UNIQUE NOT NULL,
    usuario VARCHAR(50) UNIQUE NOT NULL,
    clave VARCHAR(255) NOT NULL,
    rol ENUM('super_admin', 'admin', 'agente') NOT NULL,
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- -----------------------------------------------------------------------------
-- Tabla de relación agente-cliente (N:N)
-- -----------------------------------------------------------------------------
CREATE TABLE agentes_clientes (
    agente_id INT NOT NULL,
    cliente_id INT NOT NULL,
    fecha_asignacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (agente_id, cliente_id),
    FOREIGN KEY (agente_id) REFERENCES agente(id) ON DELETE CASCADE,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE CASCADE
);

-- =============================================================================
-- TABLAS DE BIENES ESPECÍFICOS
-- =============================================================================

-- -----------------------------------------------------------------------------
-- Tabla de hogares
-- -----------------------------------------------------------------------------
CREATE TABLE hogares (
    id INT PRIMARY KEY AUTO_INCREMENT,
    tipo_inmueble VARCHAR(100),
    ciudad_inmueble VARCHAR(100),
    direccion_inmueble VARCHAR(255),
    numero_pisos INT,
    ano_construccion INT,
    valor_inmueble_avaluo DECIMAL(15, 2),
    valor_contenidos_normales_avaluo DECIMAL(15, 2),
    valor_contenidos_especiales_avaluo DECIMAL(15, 2),
    valor_equipo_electronico_avaluo DECIMAL(15, 2),
    valor_maquinaria_equipo_avaluo DECIMAL(15, 2)
);

-- -----------------------------------------------------------------------------
-- Tabla de vehículos
-- -----------------------------------------------------------------------------
CREATE TABLE vehiculos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    tipo_vehiculo VARCHAR(100),
    placa VARCHAR(10) UNIQUE,
    marca VARCHAR(100),
    serie_referencia VARCHAR(100),
    ano_modelo INT,
    ano_nacimiento_conductor INT,
    codigo_fasecolda VARCHAR(50),
    valor_vehiculo DECIMAL(15, 2),
    valor_accesorios_avaluo DECIMAL(15, 2)
);

-- -----------------------------------------------------------------------------
-- Tabla de copropiedades
-- -----------------------------------------------------------------------------
CREATE TABLE copropiedades (
    id INT PRIMARY KEY AUTO_INCREMENT,
    tipo_copropiedad VARCHAR(100),
    ciudad VARCHAR(100),
    direccion VARCHAR(255),
    estrato INT,
    ano_construccion INT,
    numero_torres INT,
    numero_maximo_pisos INT,
    numero_maximo_sotanos INT,
    cantidad_unidades_casa INT,
    cantidad_unidades_apartamentos INT,
    cantidad_unidades_locales INT,
    cantidad_unidades_oficinas INT,
    cantidad_unidades_otros INT,
    valor_edificio_area_comun_avaluo DECIMAL(15, 2),
    valor_edificio_area_privada_avaluo DECIMAL(15, 2),
    valor_maquinaria_equipo_avaluo DECIMAL(15, 2),
    valor_equipo_electrico_electronico_avaluo DECIMAL(15, 2),
    valor_muebles_avaluo DECIMAL(15, 2)
);

-- -----------------------------------------------------------------------------
-- Tabla de otros bienes
-- -----------------------------------------------------------------------------
CREATE TABLE otros_bienes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    tipo_seguro VARCHAR(255),
    bien_asegurado VARCHAR(255),
    valor_bien_asegurar DECIMAL(15, 2),
    detalles_bien_asegurado TEXT
);

-- -----------------------------------------------------------------------------
-- Tabla principal de bienes (polimórfica)
-- -----------------------------------------------------------------------------
CREATE TABLE bienes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    tipo_bien ENUM('HOGAR', 'VEHICULO', 'COPROPIEDAD', 'OTRO') NOT NULL,
    bien_especifico_id INT NOT NULL,
    estado VARCHAR(50),
    comentarios_generales TEXT,
    vigencias_continuas BOOLEAN DEFAULT FALSE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- -----------------------------------------------------------------------------
-- Tabla de relación cliente-bien (N:N)
-- -----------------------------------------------------------------------------
CREATE TABLE clientes_bienes (
    cliente_id INT NOT NULL,
    bien_id INT NOT NULL,
    PRIMARY KEY (cliente_id, bien_id),
    FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE CASCADE,
    FOREIGN KEY (bien_id) REFERENCES bienes(id) ON DELETE CASCADE
);

-- =============================================================================
-- MÓDULO DE ASEGURADORAS
-- =============================================================================

-- -----------------------------------------------------------------------------
-- Tabla principal de aseguradoras
-- -----------------------------------------------------------------------------
CREATE TABLE aseguradoras (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(255) NOT NULL,
    numeral_asistencia VARCHAR(255),
    correo_comercial VARCHAR(255),
    correo_reclamaciones VARCHAR(255),
    oficina_direccion TEXT,
    contacto_asignado VARCHAR(255),
    logo_url VARCHAR(255),
    pais_origen_bandera_url VARCHAR(255),
    respaldo_internacional TEXT,
    comisiones_normales JSON,
    sobrecomisiones JSON,
    sublimite_rc_veh_bienes_terceros DECIMAL(5, 4),
    sublimite_rc_veh_amparo_patrimonial DECIMAL(5, 4),
    sublimite_rc_veh_muerte_una_persona DECIMAL(5, 4),
    sublimite_rc_veh_muerte_mas_personas DECIMAL(5, 4),
    sublimite_rce_cop_contratistas DECIMAL(5, 4),
    sublimite_rce_cop_cruzada DECIMAL(5, 4),
    sublimite_rce_cop_patronal DECIMAL(5, 4),
    sublimite_rce_cop_parqueaderos DECIMAL(5, 4),
    sublimite_rce_cop_gastos_medicos DECIMAL(5, 4)
);

-- -----------------------------------------------------------------------------
-- Tabla de deducibles por aseguradora
-- -----------------------------------------------------------------------------
CREATE TABLE aseguradora_deducibles (
    id INT PRIMARY KEY AUTO_INCREMENT,
    aseguradora_id INT NOT NULL,
    tipo_poliza ENUM('HOGAR', 'VEHICULO', 'COPROPIEDAD', 'OTRO') NOT NULL,
    categoria VARCHAR(255) NOT NULL,
    tipo_deducible VARCHAR(100),
    valor_porcentaje DECIMAL(5, 4),
    valor_minimo DECIMAL(15, 2),
    FOREIGN KEY (aseguradora_id) REFERENCES aseguradoras(id) ON DELETE CASCADE
);

-- -----------------------------------------------------------------------------
-- Tabla de coberturas por aseguradora
-- -----------------------------------------------------------------------------
CREATE TABLE aseguradora_coberturas (
    id INT PRIMARY KEY AUTO_INCREMENT,
    aseguradora_id INT NOT NULL,
    tipo_poliza ENUM('HOGAR', 'VEHICULO', 'COPROPIEDAD', 'OTRO') NOT NULL,
    tipo_item VARCHAR(50) NOT NULL, -- 'COBERTURA', 'ASISTENCIA', 'DIFERENCIADOR'
    nombre_item VARCHAR(255) NOT NULL,
    FOREIGN KEY (aseguradora_id) REFERENCES aseguradoras(id) ON DELETE CASCADE
);

-- -----------------------------------------------------------------------------
-- Tabla de financiación por aseguradora
-- -----------------------------------------------------------------------------
CREATE TABLE aseguradora_financiacion (
    id INT PRIMARY KEY AUTO_INCREMENT,
    aseguradora_id INT NOT NULL,
    nombre_financiera VARCHAR(255) NOT NULL,
    tasa_efectiva_mensual DECIMAL(6, 5) NOT NULL,
    FOREIGN KEY (aseguradora_id) REFERENCES aseguradoras(id) ON DELETE CASCADE
);

-- =============================================================================
-- MÓDULO DE OPCIONES DE SEGURO (COTIZACIONES)
-- =============================================================================

-- -----------------------------------------------------------------------------
-- Tabla principal de opciones de seguro
-- -----------------------------------------------------------------------------
CREATE TABLE opciones_seguro (
    id INT PRIMARY KEY AUTO_INCREMENT,
    consecutivo VARCHAR(50) UNIQUE NOT NULL,
    bien_id INT NOT NULL,
    aseguradora_id INT NOT NULL,
    tipo_opcion ENUM('HOGAR', 'VEHICULO', 'COPROPIEDAD', 'OTRO') NOT NULL,
    opcion_especifica_id INT NOT NULL,
    valor_prima_total DECIMAL(15, 2),
    financiacion_id INT,
    FOREIGN KEY (bien_id) REFERENCES bienes(id) ON DELETE CASCADE,
    FOREIGN KEY (aseguradora_id) REFERENCES aseguradoras(id),
    FOREIGN KEY (financiacion_id) REFERENCES aseguradora_financiacion(id)
);

-- -----------------------------------------------------------------------------
-- Tablas de opciones específicas por tipo de bien
-- -----------------------------------------------------------------------------
CREATE TABLE opcion_hogar (
    id INT PRIMARY KEY AUTO_INCREMENT,
    valor_inmueble_asegurado DECIMAL(15, 2),
    valor_contenidos_normales_asegurado DECIMAL(15, 2),
    valor_contenidos_especiales_asegurado DECIMAL(15, 2),
    valor_equipo_electronico_asegurado DECIMAL(15, 2),
    valor_maquinaria_equipo_asegurado DECIMAL(15, 2),
    valor_rc_asegurado DECIMAL(15, 2)
);

CREATE TABLE opcion_vehiculo (
    id INT PRIMARY KEY AUTO_INCREMENT,
    valor_vehiculo_asegurado DECIMAL(15, 2),
    valor_accesorios_asegurado DECIMAL(15, 2),
    valor_rc_asegurado DECIMAL(15, 2)
);

CREATE TABLE opcion_copropiedad (
    id INT PRIMARY KEY AUTO_INCREMENT,
    valor_area_comun_asegurado DECIMAL(15, 2),
    valor_area_privada_asegurado DECIMAL(15, 2),
    valor_maquinaria_equipo_asegurado DECIMAL(15, 2),
    valor_equipo_electronico_asegurado DECIMAL(15, 2),
    valor_muebles_asegurado DECIMAL(15, 2),
    valor_directores_asegurado DECIMAL(15, 2),
    valor_rce_asegurado DECIMAL(15, 2),
    valor_manejo_asegurado DECIMAL(15, 2),
    valor_transporte_valores_vigencia_asegurado DECIMAL(15, 2),
    valor_transporte_valores_despacho_asegurado DECIMAL(15, 2)
);

CREATE TABLE opcion_otro (
    id INT PRIMARY KEY AUTO_INCREMENT,
    valor_asegurado DECIMAL(15, 2)
);

-- -----------------------------------------------------------------------------
-- Tablas de relación para opciones de seguro
-- -----------------------------------------------------------------------------
CREATE TABLE opciones_seguro_deducibles (
    opcion_seguro_id INT NOT NULL,
    deducible_id INT NOT NULL,
    PRIMARY KEY (opcion_seguro_id, deducible_id),
    FOREIGN KEY (opcion_seguro_id) REFERENCES opciones_seguro(id) ON DELETE CASCADE,
    FOREIGN KEY (deducible_id) REFERENCES aseguradora_deducibles(id)
);

CREATE TABLE opciones_seguro_coberturas (
    opcion_seguro_id INT NOT NULL,
    cobertura_id INT NOT NULL,
    PRIMARY KEY (opcion_seguro_id, cobertura_id),
    FOREIGN KEY (opcion_seguro_id) REFERENCES opciones_seguro(id) ON DELETE CASCADE,
    FOREIGN KEY (cobertura_id) REFERENCES aseguradora_coberturas(id)
);

-- =============================================================================
-- MÓDULO DE PÓLIZAS (CONTRATO FINAL)
-- =============================================================================

-- -----------------------------------------------------------------------------
-- Tabla principal de pólizas
-- -----------------------------------------------------------------------------
CREATE TABLE polizas (
    id INT PRIMARY KEY AUTO_INCREMENT,
    opcion_seguro_id INT UNIQUE NOT NULL,
    consecutivo_poliza VARCHAR(50) UNIQUE NOT NULL,
    numero_poliza_aseguradora VARCHAR(100),
    fecha_inicio_vigencia DATE NOT NULL,
    fecha_fin_vigencia DATE NOT NULL,
    medio_pago VARCHAR(50),
    estado_cartera VARCHAR(50),
    valor_prima_neta DECIMAL(15, 2),
    valor_otros_costos DECIMAL(15, 2),
    valor_iva DECIMAL(15, 2),
    ingreso_comision_percibido DECIMAL(15, 2),
    FOREIGN KEY (opcion_seguro_id) REFERENCES opciones_seguro(id)
);

-- -----------------------------------------------------------------------------
-- Tabla de plan de pagos de pólizas
-- -----------------------------------------------------------------------------
CREATE TABLE poliza_plan_pagos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    poliza_id INT NOT NULL,
    numero_cuota INT NOT NULL,
    valor_a_pagar DECIMAL(15, 2) NOT NULL,
    fecha_maxima_pago DATE NOT NULL,
    estado_pago VARCHAR(50) DEFAULT 'Pendiente de pago',
    link_portal_pagos VARCHAR(255),
    FOREIGN KEY (poliza_id) REFERENCES polizas(id) ON DELETE CASCADE
);

-- =============================================================================
-- ÍNDICES PARA OPTIMIZACIÓN
-- =============================================================================

-- Índices para mejorar el rendimiento de consultas frecuentes
CREATE INDEX idx_clientes_tipo ON clientes(tipo_cliente);
CREATE INDEX idx_clientes_usuario ON clientes(usuario);
CREATE INDEX idx_agente_rol ON agente(rol);
CREATE INDEX idx_agente_activo ON agente(activo);
CREATE INDEX idx_bienes_tipo ON bienes(tipo_bien);
CREATE INDEX idx_bienes_estado ON bienes(estado);
CREATE INDEX idx_aseguradoras_nombre ON aseguradoras(nombre);
CREATE INDEX idx_opciones_seguro_consecutivo ON opciones_seguro(consecutivo);
CREATE INDEX idx_polizas_consecutivo ON polizas(consecutivo_poliza);
CREATE INDEX idx_polizas_vigencia ON polizas(fecha_inicio_vigencia, fecha_fin_vigencia);

-- =============================================================================
-- SCRIPT COMPLETADO EXITOSAMENTE
-- 
-- ESTRUCTURA CREADA:
-- • Módulo de Clientes y Agentes (3 tablas)
-- • Módulo de Bienes (6 tablas)
-- • Módulo de Aseguradoras (4 tablas)
-- • Módulo de Opciones de Seguro (8 tablas)
-- • Módulo de Pólizas (2 tablas)
-- • Total: 23 tablas + índices de optimización
-- 
-- La base de datos está lista para recibir datos dummy
-- =============================================================================

