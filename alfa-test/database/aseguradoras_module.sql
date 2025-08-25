-- =================================================================
-- SCRIPT COMPLETO DE BASE DE DATOS: BIEN ASEGURADO
-- Este script crea la estructura y la puebla con datos de ejemplo.
-- =================================================================

-- =================================================================
-- SECCIÓN 1: BORRADO DE TABLAS (para ejecuciones limpias)
-- =================================================================
SET FOREIGN_KEY_CHECKS = 0;
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
SET FOREIGN_KEY_CHECKS = 1;

-- =================================================================
-- SECCIÓN 2: CREACIÓN DE TABLAS (DDL)
-- =================================================================

-- -----------------------------------------------------
-- Tabla `clientes`
-- -----------------------------------------------------
CREATE TABLE clientes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    tipo_cliente VARCHAR(10) NOT NULL, -- 'PERSONA' o 'EMPRESA'
    ciudad VARCHAR(100),
    direccion VARCHAR(255),
    telefono_movil VARCHAR(20),
    correo VARCHAR(100) UNIQUE,
    usuario VARCHAR(50) UNIQUE NOT NULL,
    clave VARCHAR(255) NOT NULL,
    tipo_documento VARCHAR(10),
    numero_documento VARCHAR(20),
    nombre VARCHAR(150),
    edad INT,
    nit VARCHAR(20),
    razon_social VARCHAR(255),
    nombre_rep_legal VARCHAR(150),
    documento_rep_legal VARCHAR(20),
    telefono_rep_legal VARCHAR(20),
    correo_rep_legal VARCHAR(100),
    contacto_alternativo VARCHAR(255)
);

-- -----------------------------------------------------
-- Tabla `agente`
-- -----------------------------------------------------
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

-- -----------------------------------------------------
-- Tabla `agentes_clientes`
-- -----------------------------------------------------
CREATE TABLE agentes_clientes (
    agente_id INT NOT NULL,
    cliente_id INT NOT NULL,
    fecha_asignacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (agente_id, cliente_id),
    FOREIGN KEY (agente_id) REFERENCES agente(id) ON DELETE CASCADE,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE CASCADE
);

-- -----------------------------------------------------
-- Tablas de Bienes Específicos
-- -----------------------------------------------------
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

CREATE TABLE otros_bienes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    tipo_seguro VARCHAR(255),
    bien_asegurado VARCHAR(255),
    valor_bien_asegurar DECIMAL(15, 2),
    detalles_bien_asegurado TEXT
);

-- -----------------------------------------------------
-- Tabla `bienes` (Ancla Polimórfica)
-- -----------------------------------------------------
CREATE TABLE bienes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    tipo_bien ENUM('HOGAR', 'VEHICULO', 'COPROPIEDAD', 'OTRO') NOT NULL,
    bien_especifico_id INT NOT NULL,
    estado VARCHAR(50),
    comentarios_generales TEXT,
    vigencias_continuas BOOLEAN DEFAULT FALSE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- -----------------------------------------------------
-- Tabla `clientes_bienes`
-- -----------------------------------------------------
CREATE TABLE clientes_bienes (
    cliente_id INT NOT NULL,
    bien_id INT NOT NULL,
    PRIMARY KEY (cliente_id, bien_id),
    FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE CASCADE,
    FOREIGN KEY (bien_id) REFERENCES bienes(id) ON DELETE CASCADE
);

-- -----------------------------------------------------
-- Tablas del Módulo de Aseguradoras
-- -----------------------------------------------------
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

CREATE TABLE aseguradora_coberturas (
    id INT PRIMARY KEY AUTO_INCREMENT,
    aseguradora_id INT NOT NULL,
    tipo_poliza ENUM('HOGAR', 'VEHICULO', 'COPROPIEDAD', 'OTRO') NOT NULL,
    tipo_item VARCHAR(50) NOT NULL, -- 'COBERTURA', 'ASISTENCIA', 'DIFERENCIADOR'
    nombre_item VARCHAR(255) NOT NULL,
    FOREIGN KEY (aseguradora_id) REFERENCES aseguradoras(id) ON DELETE CASCADE
);

CREATE TABLE aseguradora_financiacion (
    id INT PRIMARY KEY AUTO_INCREMENT,
    aseguradora_id INT NOT NULL,
    nombre_financiera VARCHAR(255) NOT NULL,
    tasa_efectiva_mensual DECIMAL(6, 5) NOT NULL,
    FOREIGN KEY (aseguradora_id) REFERENCES aseguradoras(id) ON DELETE CASCADE
);

-- -----------------------------------------------------
-- Tablas del Módulo de Opciones de Seguro (Cotizaciones)
-- -----------------------------------------------------
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

-- -----------------------------------------------------
-- Tablas del Módulo de Pólizas (Contrato Final)
-- -----------------------------------------------------
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


-- =================================================================
-- SECCIÓN 3: INSERCIÓN DE DATOS DE EJEMPLO (DML)
-- =================================================================

-- -----------------------------------------------------
-- Poblar `agente`
-- -----------------------------------------------------
INSERT INTO agente (nombre, correo, usuario, clave, rol) VALUES
('Ana García', 'agarcia@seguros.com', 'agarcia', 'hash_clave_segura_1', 'super_admin'),
('Carlos Mendoza', 'cmendoza@seguros.com', 'cmendoza', 'hash_clave_segura_2', 'admin'),
('Sofia Rojas', 'srojas@seguros.com', 'srojas', 'hash_clave_segura_3', 'agente');

-- -----------------------------------------------------
-- Poblar `clientes`
-- -----------------------------------------------------
INSERT INTO clientes (tipo_cliente, ciudad, direccion, telefono_movil, correo, usuario, clave, tipo_documento, numero_documento, nombre, edad) VALUES
('PERSONA', 'Bogotá', 'Calle 100 # 20-30', '3101234567', 'juan.perez@email.com', 'jperez', 'hash_clave_cliente_1', 'CC', '1020304050', 'Juan Pérez', 35);

INSERT INTO clientes (tipo_cliente, ciudad, direccion, telefono_movil, correo, usuario, clave, nit, razon_social, nombre_rep_legal, documento_rep_legal, telefono_rep_legal, correo_rep_legal, contacto_alternativo) VALUES
('EMPRESA', 'Medellín', 'Carrera 45 # 12-34', '3209876543', 'contacto@constructora-xyz.com', 'constrxyz', 'hash_clave_cliente_2', '900.123.456-7', 'Constructora XYZ S.A.S', 'Luisa Martinez', '50607080', '3151112233', 'luisa.martinez@constructora-xyz.com', 'Gerencia');

-- -----------------------------------------------------
-- Poblar `agentes_clientes`
-- -----------------------------------------------------
INSERT INTO agentes_clientes (agente_id, cliente_id) VALUES
(3, 1), -- Sofia Rojas atiende a Juan Pérez
(2, 2); -- Carlos Mendoza atiende a Constructora XYZ

-- -----------------------------------------------------
-- Poblar Bienes Específicos
-- -----------------------------------------------------
INSERT INTO hogares (tipo_inmueble, ciudad_inmueble, direccion_inmueble, numero_pisos, ano_construccion, valor_inmueble_avaluo, valor_contenidos_normales_avaluo, valor_contenidos_especiales_avaluo, valor_equipo_electronico_avaluo) VALUES
('Apartamento', 'Bogotá', 'Calle 100 # 20-30 Apto 501', 1, 2018, 500000000.00, 80000000.00, 150000000.00, 40000000.00);

INSERT INTO vehiculos (tipo_vehiculo, placa, marca, serie_referencia, ano_modelo, ano_nacimiento_conductor, codigo_fasecolda, valor_vehiculo, valor_accesorios_avaluo) VALUES
('Automóvil', 'FJC123', 'Mazda', 'CX-5 Grand Touring', 2022, 1989, '12345678', 130000000.00, 5000000.00);

INSERT INTO copropiedades (tipo_copropiedad, ciudad, direccion, estrato, ano_construccion, numero_torres, numero_maximo_pisos, numero_maximo_sotanos, cantidad_unidades_apartamentos, valor_edificio_area_comun_avaluo, valor_maquinaria_equipo_avaluo) VALUES
('Residencial', 'Medellín', 'Carrera 45 # 12-34', 5, 2020, 2, 15, 2, 120, 10000000000.00, 500000000.00);

-- -----------------------------------------------------
-- Poblar `bienes`
-- -----------------------------------------------------
INSERT INTO bienes (tipo_bien, bien_especifico_id, estado, comentarios_generales) VALUES
('HOGAR', 1, 'Activo', 'Apartamento de Juan Pérez'),
('VEHICULO', 1, 'Activo', 'Vehículo de Juan Pérez'),
('COPROPIEDAD', 1, 'Activo', 'Edificio de Constructora XYZ');

-- -----------------------------------------------------
-- Poblar `clientes_bienes`
-- -----------------------------------------------------
INSERT INTO clientes_bienes (cliente_id, bien_id) VALUES
(1, 1), -- Hogar de Juan
(1, 2), -- Vehículo de Juan
(2, 3); -- Copropiedad de Constructora XYZ

-- -----------------------------------------------------
-- Poblar `aseguradoras` y sus plantillas
-- -----------------------------------------------------
-- Aseguradora 1: Seguros Confianza
INSERT INTO aseguradoras (nombre, numeral_asistencia, correo_comercial, correo_reclamaciones, logo_url, comisiones_normales, sobrecomisiones) VALUES
('Seguros Confianza', '#321', 'comercial@confianza.com', 'reclamos@confianza.com', '/logos/confianza.png', '{"HOGAR": 0.20, "VEHICULO": 0.15, "COPROPIEDAD": 0.18}', '{"HOGAR": 0.05, "VEHICULO": 0.02}');

-- Deducibles para Seguros Confianza
INSERT INTO aseguradora_deducibles (aseguradora_id, tipo_poliza, categoria, tipo_deducible, valor_porcentaje, valor_minimo) VALUES
(1, 'HOGAR', 'Terremoto', 'Porcentaje sobre valor asegurado', 0.02, 5000000),
(1, 'HOGAR', 'Hurto Contenidos', 'Porcentaje sobre valor pérdida', 0.10, 1000000),
(1, 'VEHICULO', 'Daños Perdida Parcial', 'Valor Fijo SMMLV', NULL, 1200000);

-- Coberturas para Seguros Confianza
INSERT INTO aseguradora_coberturas (aseguradora_id, tipo_poliza, tipo_item, nombre_item) VALUES
(1, 'HOGAR', 'COBERTURA', 'Amparo Básico Incendio y Aliados'),
(1, 'HOGAR', 'ASISTENCIA', 'Plomería de Emergencia'),
(1, 'VEHICULO', 'ASISTENCIA', 'Grúa Nacional 24/7');

-- Financiación para Seguros Confianza
INSERT INTO aseguradora_financiacion (aseguradora_id, nombre_financiera, tasa_efectiva_mensual) VALUES
(1, 'Financiera Confianza', 0.015),
(1, 'Sufi Bancolombia', 0.018);

-- Aseguradora 2: Aseguradora Global
INSERT INTO aseguradoras (nombre, numeral_asistencia, correo_comercial, correo_reclamaciones, logo_url, comisiones_normales, sobrecomisiones) VALUES
('Aseguradora Global', '#987', 'ventas@global.com', 'siniestros@global.com', '/logos/global.png', '{"HOGAR": 0.22, "VEHICULO": 0.18, "COPROPIEDAD": 0.20}', '{"HOGAR": 0.06, "VEHICULO": 0.04}');

-- Deducibles para Aseguradora Global
INSERT INTO aseguradora_deducibles (aseguradora_id, tipo_poliza, categoria, tipo_deducible, valor_porcentaje, valor_minimo) VALUES
(2, 'HOGAR', 'Terremoto', 'Porcentaje sobre valor asegurado', 0.025, 6000000),
(2, 'HOGAR', 'Hurto Contenidos', 'Porcentaje sobre valor pérdida', 0.15, 1500000);

-- -----------------------------------------------------
-- Poblar Opciones de Seguro (Cotizaciones)
-- -----------------------------------------------------
-- Opción para el HOGAR de Juan Pérez con Seguros Confianza
INSERT INTO opcion_hogar (valor_inmueble_asegurado, valor_contenidos_normales_asegurado, valor_rc_asegurado) VALUES
(500000000.00, 80000000.00, 200000000.00);

INSERT INTO opciones_seguro (consecutivo, bien_id, aseguradora_id, tipo_opcion, opcion_especifica_id, valor_prima_total, financiacion_id) VALUES
('2025-CO-001-OPC-01', 1, 1, 'HOGAR', 1, 1250000.00, 1);

-- Seleccionar deducibles y coberturas para esta opción
INSERT INTO opciones_seguro_deducibles (opcion_seguro_id, deducible_id) VALUES
(1, 1), -- Deducible de Terremoto de Seguros Confianza
(1, 2); -- Deducible de Hurto de Seguros Confianza

INSERT INTO opciones_seguro_coberturas (opcion_seguro_id, cobertura_id) VALUES
(1, 1), -- Cobertura de Amparo Básico
(1, 2); -- Asistencia de Plomería

-- -----------------------------------------------------
-- Poblar Pólizas (Contrato Final)
-- -----------------------------------------------------
-- Juan Pérez acepta la opción de Seguros Confianza
INSERT INTO polizas (opcion_seguro_id, consecutivo_poliza, numero_poliza_aseguradora, fecha_inicio_vigencia, fecha_fin_vigencia, medio_pago, estado_cartera, valor_prima_neta, valor_otros_costos, valor_iva, ingreso_comision_percibido) VALUES
(1, '2025-CO-001', 'SC-HOG-98765', '2025-07-15', '2026-07-15', 'Financiación', 'Al Día', 1050420.17, 0, 199579.83, 262605.04); -- Prima Neta * (Comisión + Sobrecomisión)

-- -----------------------------------------------------
-- Poblar Plan de Pagos
-- -----------------------------------------------------
INSERT INTO poliza_plan_pagos (poliza_id, numero_cuota, valor_a_pagar, fecha_maxima_pago, estado_pago, link_portal_pagos) VALUES
(1, 1, 125000.00, '2025-07-15', 'Pagado', 'https://pagos.confianza.com/1'),
(1, 2, 125000.00, '2025-08-15', 'Pendiente de pago', 'https://pagos.confianza.com/1'),
(1, 3, 125000.00, '2025-09-15', 'Pendiente de pago', 'https://pagos.confianza.com/1');
-- ... se insertarían las demás cuotas

