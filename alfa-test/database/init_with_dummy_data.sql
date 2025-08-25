-- =============================================================================
-- INICIALIZACION COMPLETA DE BASE DE DATOS CON DATOS DUMMY - SISTEMA ALFA
-- Sistema de Gestión de Seguros - Davivienda
-- =============================================================================

-- Crear base de datos si no existe
CREATE DATABASE IF NOT EXISTS alfa_db;
USE alfa_db;

-- Deshabilitar verificación de claves foráneas temporalmente
SET FOREIGN_KEY_CHECKS = 0;

-- Eliminar todas las tablas existentes para reinicio limpio
DROP TABLE IF EXISTS clientes_bienes;
DROP TABLE IF EXISTS agentes_clientes;
DROP TABLE IF EXISTS bienes;
DROP TABLE IF EXISTS hogares;
DROP TABLE IF EXISTS vehiculos;
DROP TABLE IF EXISTS copropiedades;
DROP TABLE IF EXISTS otros_bienes;
DROP TABLE IF EXISTS clientes;
DROP TABLE IF EXISTS agente;

-- Rehabilitar verificación de claves foráneas
SET FOREIGN_KEY_CHECKS = 1;

-- =============================================================================
-- CREAR ESTRUCTURA DE TABLAS
-- =============================================================================

-- Tabla de clientes (personas naturales y empresas)
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

-- Tabla de agentes
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

-- Tabla de relación agente-cliente (N:N)
CREATE TABLE agentes_clientes (
    agente_id INT NOT NULL,
    cliente_id INT NOT NULL,
    fecha_asignacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (agente_id, cliente_id),
    FOREIGN KEY (agente_id) REFERENCES agente(id) ON DELETE CASCADE,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE CASCADE
);

-- Tabla principal de bienes (polimórfica)
CREATE TABLE bienes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    tipo_bien ENUM('HOGAR', 'VEHICULO', 'COPROPIEDAD', 'OTRO') NOT NULL,
    bien_especifico_id INT NOT NULL,
    estado VARCHAR(50),
    comentarios_generales TEXT,
    vigencias_continuas BOOLEAN DEFAULT FALSE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de relación cliente-bien (N:N)
CREATE TABLE clientes_bienes (
    cliente_id INT NOT NULL,
    bien_id INT NOT NULL,
    PRIMARY KEY (cliente_id, bien_id),
    FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE CASCADE,
    FOREIGN KEY (bien_id) REFERENCES bienes(id) ON DELETE CASCADE
);

-- Tablas específicas de bienes
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

-- =============================================================================
-- INSERTAR DATOS DUMMY - AGENTES
-- =============================================================================

INSERT INTO agente (nombre, correo, usuario, clave, rol, activo) VALUES
-- Super Administrador
('Admin Principal', 'admin@davivienda.com', 'admin', 'admin123', 'super_admin', TRUE),

-- Administradores
('Carlos Rodríguez Mendoza', 'carlos.rodriguez@davivienda.com', 'carlos.rodriguez', 'admin456', 'admin', TRUE),
('Ana Sofía Mendoza Torres', 'ana.mendoza@davivienda.com', 'ana.mendoza', 'admin789', 'admin', TRUE),
('Luis Fernando Torres Ruiz', 'luis.torres@davivienda.com', 'luis.torres', 'admin321', 'admin', FALSE),
('Gloria Patricia Ramírez', 'gloria.ramirez@davivienda.com', 'gloria.ramirez', 'admin654', 'admin', TRUE),

-- Agentes de Seguros
('Juan Pérez Gómez', 'juan.perez@davivienda.com', 'juan.perez', 'agente123', 'agente', TRUE),
('María García Hernández', 'maria.garcia@davivienda.com', 'maria.garcia', 'agente456', 'agente', TRUE),
('Patricia Jiménez Villa', 'patricia.jimenez@davivienda.com', 'patricia.jimenez', 'agente789', 'agente', TRUE),
('Roberto Castillo Mora', 'roberto.castillo@davivienda.com', 'roberto.castillo', 'agente321', 'agente', TRUE),
('Mónica Vargas Sánchez', 'monica.vargas@davivienda.com', 'monica.vargas', 'agente654', 'agente', TRUE),
('Daniel Herrera Castro', 'daniel.herrera@davivienda.com', 'daniel.herrera', 'agente987', 'agente', TRUE),
('Isabella Cruz Delgado', 'isabella.cruz@davivienda.com', 'isabella.cruz', 'agente147', 'agente', FALSE),
('Alejandro Morales Vega', 'alejandro.morales@davivienda.com', 'alejandro.morales', 'agente258', 'agente', TRUE),
('Valentina Ospina Rueda', 'valentina.ospina@davivienda.com', 'valentina.ospina', 'agente369', 'agente', TRUE),
('Sebastián Torres Aguilar', 'sebastian.torres@davivienda.com', 'sebastian.torres', 'agente741', 'agente', TRUE);

-- =============================================================================
-- INSERTAR DATOS DUMMY - CLIENTES PERSONAS NATURALES
-- =============================================================================

INSERT INTO clientes (tipo_cliente, usuario, clave, nombre, tipo_documento, numero_documento, correo, telefono_movil, ciudad, direccion, edad) VALUES
('PERSONA', 'carlos.lopez', 'cliente123', 'Carlos López Martínez', 'CC', '12345678', 'carlos.lopez@gmail.com', '3001234567', 'Bogotá', 'Carrera 15 #85-32 Apto 501', 35),
('PERSONA', 'ana.martinez', 'cliente456', 'Ana Martínez Rodríguez', 'CC', '87654321', 'ana.martinez@hotmail.com', '3009876543', 'Medellín', 'Calle 70 #45-12 Casa 45', 28),
('PERSONA', 'felipe.santos', 'cliente789', 'Felipe Santos Restrepo', 'CC', '98765432', 'felipe.santos@yahoo.com', '3012345678', 'Bogotá', 'Avenida 19 #123-45', 42),
('PERSONA', 'laura.ramirez', 'cliente321', 'Laura Ramírez Vélez', 'CC', '11223344', 'laura.ramirez@gmail.com', '3023456789', 'Medellín', 'Carrera 43A #5-67 Apto 802', 31),
('PERSONA', 'diego.moreno', 'cliente654', 'Diego Moreno Castro', 'CC', '55667788', 'diego.moreno@outlook.com', '3034567890', 'Cali', 'Calle 5 #70-23 Casa 12', 39),
('PERSONA', 'camila.torres', 'cliente987', 'Camila Torres Giraldo', 'CC', '99887766', 'camila.torres@gmail.com', '3045678901', 'Barranquilla', 'Carrera 44 #32-76', 26),
('PERSONA', 'andres.lopez', 'cliente147', 'Andrés López Fernández', 'CE', '123456789', 'andres.lopez@hotmail.com', '3056789012', 'Cartagena', 'Calle 30 #45-67 Apto 304', 33),
('PERSONA', 'sofia.martinez', 'cliente258', 'Sofía Martínez Ruiz', 'CC', '77788899', 'sofia.martinez@yahoo.com', '3067890123', 'Bucaramanga', 'Avenida 15 #34-56', 29),
('PERSONA', 'miguel.hernan', 'cliente369', 'Miguel Hernández Silva', 'CC', '44455566', 'miguel.hernan@gmail.com', '3078901234', 'Pereira', 'Carrera 27 #65-43', 45),
('PERSONA', 'natalia.gomez', 'cliente741', 'Natalia Gómez Aguilar', 'CC', '66677788', 'natalia.gomez@outlook.com', '3089012345', 'Manizales', 'Calle 23 #12-34', 27),
('PERSONA', 'sebastian.cruz', 'cliente852', 'Sebastián Cruz Delgado', 'TI', '1234567890', 'sebastian.cruz@gmail.com', '3090123456', 'Santa Marta', 'Avenida del Río #45-78', 22),
('PERSONA', 'gabriela.vega', 'cliente963', 'Gabriela Vega Montoya', 'CC', '33344455', 'gabriela.vega@hotmail.com', '3101234567', 'Ibagué', 'Carrera 5 #33-78 Casa 23', 36),
('PERSONA', 'ricardo.silva', 'cliente174', 'Ricardo Silva Orozco', 'CC', '22233344', 'ricardo.silva@yahoo.com', '3112345678', 'Cúcuta', 'Calle 10 #15-67', 41),
('PERSONA', 'elena.vargas', 'cliente285', 'Elena Vargas Morales', 'CC', '55544433', 'elena.vargas@gmail.com', '3123456789', 'Neiva', 'Carrera 12 #25-89', 34),
('PERSONA', 'oscar.jimenez', 'cliente396', 'Oscar Jiménez León', 'CC', '88899900', 'oscar.jimenez@outlook.com', '3134567890', 'Armenia', 'Avenida Bolívar #67-45', 38);

-- =============================================================================
-- INSERTAR DATOS DUMMY - CLIENTES EMPRESAS
-- =============================================================================

INSERT INTO clientes (tipo_cliente, usuario, clave, nit, razon_social, nombre_rep_legal, documento_rep_legal, correo, telefono_movil, ciudad, direccion, telefono_rep_legal, correo_rep_legal, contacto_alternativo) VALUES
('EMPRESA', 'empresa.abc', 'empresa123', '900123456', 'Empresa ABC S.A.S.', 'Roberto Empresario González', '11111111', 'contacto@empresaabc.com', '3005555555', 'Bogotá', 'Zona Rosa, Calle 82 #11-45', '3111111111', 'roberto.gonzalez@empresaabc.com', 'Gerente comercial: comercial@empresaabc.com'),
('EMPRESA', 'tech.solutions', 'empresa456', '800987654', 'Tech Solutions Ltda.', 'Sandra Tecnóloga Ramírez', '22222222', 'info@techsolutions.com', '3007777777', 'Medellín', 'El Poblado, Carrera 43A #5-15', '3122222222', 'sandra.ramirez@techsolutions.com', 'CTO: desarrollo@techsolutions.com'),
('EMPRESA', 'innovatech.co', 'empresa789', '900234567', 'InnovaTech Solutions S.A.S.', 'Fernando Ramírez Soto', '12345678', 'admin@innovatech.co', '3201234567', 'Bogotá', 'Centro, Carrera 7 #32-45', '3111234567', 'fernando.ramirez@innovatech.co', 'Gerente de proyectos: proyectos@innovatech.co'),
('EMPRESA', 'comercial.andina', 'empresa321', '800345678', 'Comercializadora Andina Ltda.', 'María Elena Vargas López', '23456789', 'ventas@andina.com.co', '3212345678', 'Medellín', 'Laureles, Calle 70 #52-14', '3122345678', 'maria.vargas@andina.com.co', 'Coordinador logístico: logistica@andina.com.co'),
('EMPRESA', 'logistica.caribe', 'empresa654', '900456789', 'Logística del Caribe S.A.', 'Jorge Luis Mendoza Torres', '34567890', 'operaciones@logcaribe.co', '3223456789', 'Barranquilla', 'Zona Industrial, Carrera 44 #32-76', '3133456789', 'jorge.mendoza@logcaribe.co', 'Jefe de operaciones: ops@logcaribe.co'),
('EMPRESA', 'agro.valle', 'empresa987', '800567890', 'AgroValle Productores Unidos S.A.', 'Carmen Rosa Delgado Herrera', '45678901', 'contacto@agrovalle.co', '3234567890', 'Cali', 'Valle del Cauca, Calle 5 #70-23', '3144567890', 'carmen.delgado@agrovalle.co', 'Ingeniero agrónomo: agronomia@agrovalle.co'),
('EMPRESA', 'textiles.norte', 'empresa147', '900678901', 'Textiles del Norte S.A.S.', 'Ricardo Andrés Gómez Ruiz', '56789012', 'info@textilesnorte.com', '3245678901', 'Bucaramanga', 'Zona Industrial, Carrera 15 #45-67', '3155678901', 'ricardo.gomez@textilesnorte.com', 'Diseñador textil: diseno@textilesnorte.com'),
('EMPRESA', 'minera.cordillera', 'empresa258', '800789012', 'Minera Cordillera Ltda.', 'Ana Lucía Herrera Castro', '67890123', 'gerencia@mineracordillera.co', '3256789012', 'Pereira', 'Sector Minero, Km 5 Vía Dosquebradas', '3166789012', 'ana.herrera@mineracordillera.co', 'Ingeniero de minas: ingenieria@mineracordillera.co'),
('EMPRESA', 'construcciones.pacifico', 'empresa369', '900890123', 'Construcciones del Pacífico S.A.', 'Esteban Torres Ruiz', '78901234', 'proyectos@conspacifico.co', '3267890123', 'Buenaventura', 'Puerto, Calle 2 #4-56', '3177890123', 'esteban.torres@conspacifico.co', 'Arquitecto líder: arquitectura@conspacifico.co'),
('EMPRESA', 'alimentos.tropical', 'empresa741', '800901234', 'Alimentos Tropical Ltda.', 'Claudia Patricia Rojas Morales', '89012345', 'calidad@tropical.com.co', '3278901234', 'Villavicencio', 'Zona Industrial, Carrera 35 #12-34', '3188901234', 'claudia.rojas@tropical.com.co', 'Nutricionista: nutricion@tropical.com.co'),
('EMPRESA', 'energia.renovable', 'empresa852', '900012345', 'Energía Renovable del Futuro S.A.S.', 'Mauricio Jiménez León', '90123456', 'sustentabilidad@energiarenovable.co', '3289012345', 'Manizales', 'Parque Tecnológico, Calle 65 #23-14', '3199012345', 'mauricio.jimenez@energiarenovable.co', 'Ingeniero ambiental: ambiental@energiarenovable.co'),
('EMPRESA', 'turismo.magdalena', 'empresa963', '800123456', 'Turismo Río Magdalena Ltda.', 'Gloria Esperanza Castro Silva', '01234567', 'reservas@turismomagdalena.co', '3290123456', 'Honda', 'Malecón del Río, Calle 10 #5-67', '3200123456', 'gloria.castro@turismomagdalena.co', 'Guía turístico: tours@turismomagdalena.co');

-- =============================================================================
-- INSERTAR DATOS DUMMY - BIENES ESPECÍFICOS
-- =============================================================================

-- Insertar HOGARES
INSERT INTO hogares (tipo_inmueble, ciudad_inmueble, direccion_inmueble, numero_pisos, ano_construccion, valor_inmueble_avaluo, valor_contenidos_normales_avaluo, valor_contenidos_especiales_avaluo, valor_equipo_electronico_avaluo, valor_maquinaria_equipo_avaluo) VALUES
('Casa', 'Bogotá', 'Carrera 15 #85-32', 2, 2018, 450000000.00, 35000000.00, 15000000.00, 12000000.00, 8000000.00),
('Apartamento', 'Medellín', 'Calle 70 #45-12 Apto 501', 1, 2020, 320000000.00, 28000000.00, 12000000.00, 10000000.00, 5000000.00),
('Casa', 'Bogotá', 'Avenida 19 #123-45', 3, 2015, 680000000.00, 45000000.00, 20000000.00, 15000000.00, 12000000.00),
('Apartamento', 'Medellín', 'Carrera 43A #5-67 Apto 802', 1, 2019, 280000000.00, 22000000.00, 8000000.00, 7000000.00, 3000000.00),
('Casa', 'Cali', 'Calle 5 #70-23', 2, 2016, 390000000.00, 30000000.00, 10000000.00, 8000000.00, 6000000.00),
('Apartamento', 'Barranquilla', 'Carrera 44 #32-76 Apto 304', 1, 2021, 220000000.00, 18000000.00, 6000000.00, 5000000.00, 2000000.00),
('Casa', 'Cartagena', 'Calle 30 #45-67', 2, 2017, 520000000.00, 40000000.00, 18000000.00, 14000000.00, 10000000.00),
('Apartamento', 'Bucaramanga', 'Avenida 15 #34-56 Apto 201', 1, 2022, 180000000.00, 15000000.00, 5000000.00, 4000000.00, 1500000.00),
('Casa', 'Pereira', 'Carrera 27 #65-43', 3, 2014, 350000000.00, 25000000.00, 8000000.00, 6000000.00, 4000000.00),
('Apartamento', 'Manizales', 'Calle 23 #12-34 Apto 605', 1, 2023, 240000000.00, 20000000.00, 7000000.00, 5000000.00, 3000000.00),
('Casa', 'Santa Marta', 'Avenida del Río #45-78', 2, 2019, 480000000.00, 35000000.00, 12000000.00, 9000000.00, 7000000.00),
('Apartamento', 'Ibagué', 'Carrera 5 #33-78 Apto 402', 1, 2020, 200000000.00, 16000000.00, 5000000.00, 4000000.00, 2000000.00),
('Casa', 'Cúcuta', 'Calle 10 #15-67', 2, 2018, 290000000.00, 22000000.00, 7000000.00, 5000000.00, 3000000.00),
('Apartamento', 'Neiva', 'Carrera 12 #25-89 Apto 301', 1, 2021, 170000000.00, 14000000.00, 4000000.00, 3000000.00, 1500000.00),
('Casa', 'Armenia', 'Avenida Bolívar #67-45', 2, 2016, 310000000.00, 24000000.00, 8000000.00, 6000000.00, 4000000.00);

-- Insertar VEHICULOS
INSERT INTO vehiculos (tipo_vehiculo, placa, marca, serie_referencia, ano_modelo, ano_nacimiento_conductor, codigo_fasecolda, valor_vehiculo, valor_accesorios_avaluo) VALUES
('Automóvil', 'ABC123', 'Toyota', 'Corolla Cross XLI', 2023, 1988, '81042090', 95000000.00, 4000000.00),
('Motocicleta', 'DEF456', 'Yamaha', 'MT-03', 2022, 1995, '20100190', 22000000.00, 1500000.00),
('Automóvil', 'GHI789', 'Chevrolet', 'Spark GT', 2021, 1981, '81008090', 52000000.00, 2500000.00),
('Camioneta', 'JKL012', 'Ford', 'Ranger XLT', 2022, 1990, '81080090', 140000000.00, 6000000.00),
('Automóvil', 'MNO345', 'Nissan', 'Sentra Advance', 2023, 1985, '81020090', 82000000.00, 3000000.00),
('Motocicleta', 'PQR678', 'Honda', 'CB 190R', 2021, 1996, '20110190', 18000000.00, 1200000.00),
('Automóvil', 'STU901', 'Mazda', 'Mazda 2 Sedan', 2022, 1987, '81030090', 68000000.00, 2800000.00),
('Camioneta', 'VWX234', 'Chevrolet', 'Colorado High Country', 2023, 1983, '81090090', 180000000.00, 8000000.00),
('Automóvil', 'YZA567', 'Hyundai', 'Accent Vision', 2021, 1989, '81040090', 58000000.00, 2200000.00),
('Motocicleta', 'BCD890', 'Kawasaki', 'Ninja 400', 2022, 1994, '20120190', 35000000.00, 2000000.00),
('Automóvil', 'EFG123', 'Kia', 'Rio Sedan', 2023, 1986, '81050090', 65000000.00, 2500000.00),
('Camioneta', 'HIJ456', 'Mitsubishi', 'L200 Sportero', 2021, 1982, '81100090', 125000000.00, 5500000.00),
('Automóvil', 'KLM789', 'Volkswagen', 'Virtus Comfortline', 2022, 1991, '81060090', 78000000.00, 3200000.00),
('Motocicleta', 'NOP012', 'Suzuki', 'Gixxer 155', 2021, 1993, '20130190', 16000000.00, 1000000.00),
('Automóvil', 'QRS345', 'Renault', 'Logan Life', 2023, 1988, '81070090', 48000000.00, 2000000.00);

-- Insertar COPROPIEDADES
INSERT INTO copropiedades (tipo_copropiedad, ciudad, direccion, estrato, ano_construccion, numero_torres, numero_maximo_pisos, numero_maximo_sotanos, cantidad_unidades_casa, cantidad_unidades_apartamentos, cantidad_unidades_locales, cantidad_unidades_oficinas, cantidad_unidades_otros, valor_edificio_area_comun_avaluo, valor_edificio_area_privada_avaluo, valor_maquinaria_equipo_avaluo, valor_equipo_electrico_electronico_avaluo, valor_muebles_avaluo) VALUES
('Conjunto Residencial', 'Bogotá', 'Zona Rosa, Carrera 7 #127-45', 5, 2020, 4, 18, 3, 12, 240, 8, 4, 6, 3500000000.00, 12000000000.00, 250000000.00, 300000000.00, 450000000.00),
('Edificio Comercial', 'Medellín', 'El Poblado, Calle 50 #46-78', 6, 2019, 2, 25, 4, 0, 0, 35, 60, 15, 2800000000.00, 9500000000.00, 400000000.00, 500000000.00, 350000000.00),
('Conjunto Cerrado', 'Cali', 'Norte, Avenida 5N #18-90', 4, 2018, 3, 12, 2, 36, 144, 6, 3, 4, 2200000000.00, 7200000000.00, 150000000.00, 200000000.00, 280000000.00),
('Centro Comercial', 'Barranquilla', 'Centro, Carrera 44 #75-89', 5, 2021, 1, 8, 2, 0, 0, 120, 25, 8, 4500000000.00, 8500000000.00, 600000000.00, 800000000.00, 300000000.00),
('Conjunto Residencial', 'Cartagena', 'Bocagrande, Calle 30 #12-34', 6, 2022, 2, 20, 2, 0, 80, 4, 2, 3, 2000000000.00, 6800000000.00, 120000000.00, 180000000.00, 220000000.00),
('Edificio Mixto', 'Bucaramanga', 'Cabecera, Carrera 35 #45-67', 4, 2017, 1, 15, 1, 0, 45, 18, 12, 5, 1800000000.00, 5200000000.00, 180000000.00, 250000000.00, 200000000.00),
('Parque Industrial', 'Pereira', 'Zona Industrial, Km 7 Vía Armenia', 3, 2019, 5, 8, 1, 0, 0, 25, 35, 20, 3200000000.00, 7800000000.00, 800000000.00, 400000000.00, 150000000.00),
('Torre Empresarial', 'Manizales', 'Centro, Calle 65 #23-14', 5, 2020, 1, 30, 5, 0, 0, 15, 85, 12, 1500000000.00, 8500000000.00, 350000000.00, 450000000.00, 280000000.00);

-- Insertar OTROS BIENES
INSERT INTO otros_bienes (tipo_seguro, bien_asegurado, valor_bien_asegurar, detalles_bien_asegurado) VALUES
('Seguro de Transporte', 'Mercancías Tecnológicas', 800000000.00, 'Cobertura para transporte de equipos tecnológicos entre ciudades principales'),
('Seguro de Responsabilidad Civil', 'Servicios Profesionales IT', 300000000.00, 'Cobertura para consultores y desarrolladores de software'),
('Seguro de Equipos Industriales', 'Maquinaria Textil', 1200000000.00, 'Equipos especializados para manufactura textil en Bucaramanga'),
('Seguro de Manejo y Fidelidad', 'Personal Administrativo', 150000000.00, 'Cobertura para empleados con manejo de valores y activos'),
('Seguro de Incendio', 'Bodega Productos Químicos', 600000000.00, 'Almacén de productos químicos industriales en Barranquilla'),
('Seguro de Responsabilidad Civil', 'Actividades Mineras', 500000000.00, 'Cobertura para operaciones de extracción minera en Pereira'),
('Seguro de Equipos Móviles', 'Maquinaria de Construcción', 900000000.00, 'Excavadoras, grúas y equipo pesado para construcción'),
('Seguro de Mercancías', 'Productos Alimenticios', 400000000.00, 'Cobertura para productos perecederos en cadena de frío'),
('Seguro de Equipos Electrónicos', 'Sistemas de Energía Solar', 750000000.00, 'Paneles solares y sistemas de almacenamiento energético'),
('Seguro de Responsabilidad Civil', 'Servicios Turísticos', 250000000.00, 'Cobertura para operadores turísticos y guías especializados'),
('Seguro de Transporte', 'Productos Agrícolas', 350000000.00, 'Cobertura para transporte de productos del campo a centros de distribución'),
('Seguro de Equipos', 'Sistemas de Comunicación', 180000000.00, 'Torres de comunicación y equipos de transmisión'),
('Seguro de Responsabilidad Civil', 'Servicios Médicos', 400000000.00, 'Cobertura para profesionales de la salud y clínicas'),
('Seguro de Incendio', 'Depósito de Combustibles', 1000000000.00, 'Tanques de almacenamiento de combustibles en terminal portuario'),
('Seguro de Equipos Industriales', 'Línea de Producción', 650000000.00, 'Maquinaria automatizada para producción de alimentos procesados');

-- =============================================================================
-- INSERTAR DATOS DUMMY - BIENES PRINCIPALES (POLIMORFICOS)
-- =============================================================================

INSERT INTO bienes (tipo_bien, bien_especifico_id, estado, comentarios_generales, vigencias_continuas) VALUES
-- HOGARES (15 bienes)
('HOGAR', 1, 'Activo', 'Casa principal familiar en excelente estado de conservación', TRUE),
('HOGAR', 2, 'Activo', 'Apartamento moderno con acabados premium y ubicación privilegiada', TRUE),
('HOGAR', 3, 'Activo', 'Casa amplia con jardín y zona social para reuniones familiares', TRUE),
('HOGAR', 4, 'Activo', 'Apartamento recién entregado con garantías de construcción', TRUE),
('HOGAR', 5, 'Activo', 'Casa tradicional con remodelaciones recientes y buena ubicación', TRUE),
('HOGAR', 6, 'Activo', 'Apartamento cerca del mar con vista panorámica', TRUE),
('HOGAR', 7, 'Activo', 'Casa histórica en zona colonial con valor patrimonial', TRUE),
('HOGAR', 8, 'Activo', 'Apartamento nuevo con amenidades modernas y seguridad 24/7', TRUE),
('HOGAR', 9, 'Activo', 'Casa campestre con amplios espacios verdes y tranquilidad', TRUE),
('HOGAR', 10, 'Activo', 'Apartamento ejecutivo con estudios y oficina integrada', TRUE),
('HOGAR', 11, 'Activo', 'Casa familiar con piscina y zonas de recreación', TRUE),
('HOGAR', 12, 'Activo', 'Apartamento céntrico con fácil acceso a transporte público', TRUE),
('HOGAR', 13, 'Activo', 'Casa en conjunto cerrado con vigilancia y áreas comunes', TRUE),
('HOGAR', 14, 'Activo', 'Apartamento con terraza y vista a las montañas', TRUE),
('HOGAR', 15, 'Activo', 'Casa esquinera con local comercial en primer piso', TRUE),

-- VEHICULOS (15 bienes)
('VEHICULO', 1, 'Activo', 'Vehículo familiar SUV en excelentes condiciones mecánicas', TRUE),
('VEHICULO', 2, 'Activo', 'Motocicleta urbana ideal para movilidad en la ciudad', TRUE),
('VEHICULO', 3, 'Activo', 'Automóvil económico con bajo kilometraje y mantenimiento al día', TRUE),
('VEHICULO', 4, 'Activo', 'Camioneta de trabajo con capacidad de carga y tracción 4x4', TRUE),
('VEHICULO', 5, 'Activo', 'Sedán ejecutivo con tecnología avanzada y sistema de seguridad', TRUE),
('VEHICULO', 6, 'Activo', 'Motocicleta deportiva con modificaciones estéticas aprobadas', TRUE),
('VEHICULO', 7, 'Activo', 'Automóvil compacto perfecto para ciudad con excelente rendimiento', TRUE),
('VEHICULO', 8, 'Activo', 'Camioneta premium con interior de cuero y equipamiento completo', TRUE),
('VEHICULO', 9, 'Activo', 'Hatchback práctico con amplio espacio interior y maletero', TRUE),
('VEHICULO', 10, 'Activo', 'Motocicleta deportiva de alta cilindrada con kit de seguridad', TRUE),
('VEHICULO', 11, 'Activo', 'Sedán familiar con sistemas de entretenimiento y navegación', TRUE),
('VEHICULO', 12, 'Activo', 'Pickup robusta ideal para trabajo pesado y aventuras', TRUE),
('VEHICULO', 13, 'Activo', 'Automóvil híbrido con tecnología eco-friendly y bajo consumo', TRUE),
('VEHICULO', 14, 'Activo', 'Scooter urbana económica para desplazamientos cortos', TRUE),
('VEHICULO', 15, 'Activo', 'Automóvil familiar con amplio espacio y sistemas de seguridad', TRUE),

-- COPROPIEDADES (8 bienes)
('COPROPIEDAD', 1, 'Activo', 'Conjunto residencial de lujo con amenidades completas', TRUE),
('COPROPIEDAD', 2, 'Activo', 'Edificio comercial moderno en zona financiera principal', TRUE),
('COPROPIEDAD', 3, 'Activo', 'Conjunto cerrado familiar con zonas verdes y recreación', TRUE),
('COPROPIEDAD', 4, 'Activo', 'Centro comercial con alta afluencia de público y locales premium', TRUE),
('COPROPIEDAD', 5, 'Activo', 'Torres residenciales frente al mar con vista panorámica', TRUE),
('COPROPIEDAD', 6, 'Activo', 'Edificio mixto con apartamentos y oficinas en zona central', TRUE),
('COPROPIEDAD', 7, 'Activo', 'Parque industrial con bodegas y oficinas administrativas', TRUE),
('COPROPIEDAD', 8, 'Activo', 'Torre empresarial con tecnología de punta y ubicación estratégica', TRUE),

-- OTROS BIENES (15 bienes)
('OTRO', 1, 'Activo', 'Póliza integral para transporte de mercancías de alto valor', TRUE),
('OTRO', 2, 'Activo', 'Seguro profesional para servicios tecnológicos especializados', TRUE),
('OTRO', 3, 'Activo', 'Cobertura completa para maquinaria industrial de producción', TRUE),
('OTRO', 4, 'Activo', 'Seguro de fidelidad para personal con manejo de valores', TRUE),
('OTRO', 5, 'Activo', 'Póliza especial para almacenamiento de productos peligrosos', TRUE),
('OTRO', 6, 'Activo', 'Seguro de responsabilidad civil para actividades extractivas', TRUE),
('OTRO', 7, 'Activo', 'Cobertura para equipos móviles de construcción y obra civil', TRUE),
('OTRO', 8, 'Activo', 'Seguro para productos alimenticios con cadena de frío', TRUE),
('OTRO', 9, 'Activo', 'Póliza para equipos de energía renovable y sistemas solares', TRUE),
('OTRO', 10, 'Activo', 'Seguro de responsabilidad civil para operadores turísticos', TRUE),
('OTRO', 11, 'Activo', 'Cobertura para transporte de productos agrícolas frescos', TRUE),
('OTRO', 12, 'Activo', 'Seguro para equipos de telecomunicaciones y transmisión', TRUE),
('OTRO', 13, 'Activo', 'Póliza de responsabilidad civil para profesionales médicos', TRUE),
('OTRO', 14, 'Activo', 'Seguro especializado para depósitos de combustibles', TRUE),
('OTRO', 15, 'Activo', 'Cobertura para líneas de producción automatizada', TRUE);

-- =============================================================================
-- INSERTAR DATOS DUMMY - ASIGNACIONES AGENTE-CLIENTE
-- =============================================================================

INSERT INTO agentes_clientes (agente_id, cliente_id) VALUES
-- Admin Principal (ID: 1) - Clientes empresariales estratégicos
(1, 16), (1, 17), (1, 18), (1, 19), (1, 20),

-- Carlos Rodríguez (ID: 2) - Admin con mix de clientes
(2, 1), (2, 21), (2, 22), (2, 5), (2, 6),

-- Ana Sofía Mendoza (ID: 3) - Admin con clientes premium
(3, 23), (3, 24), (3, 25), (3, 7), (3, 8),

-- Gloria Patricia Ramírez (ID: 5) - Admin con empresas medianas
(5, 26), (5, 27), (5, 9), (5, 10), (5, 11),

-- Juan Pérez (ID: 6) - agente con clientes diversos
(6, 2), (6, 3), (6, 4), (6, 16), (6, 17),

-- María García (ID: 7) - agente con enfoque en personas
(7, 12), (7, 13), (7, 14), (7, 15), (7, 18),

-- Patricia Jiménez (ID: 8) - agente con clientes corporativos
(8, 19), (8, 20), (8, 21), (8, 1), (8, 2),

-- Roberto Castillo (ID: 9) - agente con mix balanceado
(9, 22), (9, 23), (9, 3), (9, 4), (9, 5),

-- Mónica Vargas (ID: 10) - agente con clientes en crecimiento
(10, 24), (10, 25), (10, 6), (10, 7), (10, 8),

-- Daniel Herrera (ID: 11) - agente con cartera diversificada
(11, 26), (11, 27), (11, 9), (11, 10), (11, 11),

-- Alejandro Morales (ID: 13) - agente con clientes regionales
(13, 12), (13, 13), (13, 14), (13, 15), (13, 16),

-- Valentina Ospina (ID: 14) - agente con clientes especializados
(14, 17), (14, 18), (14, 19), (14, 20), (14, 21),

-- Sebastián Torres (ID: 15) - agente con nuevos clientes
(15, 22), (15, 23), (15, 1), (15, 2), (15, 3);

-- =============================================================================
-- INSERTAR DATOS DUMMY - ASIGNACIONES CLIENTE-BIEN
-- =============================================================================

INSERT INTO clientes_bienes (cliente_id, bien_id) VALUES
-- Personas Naturales con bienes variados
(1, 1), (1, 16), (1, 39), -- Carlos López: Casa + Vehículo + Seguro profesional
(2, 2), (2, 17), (2, 40), -- Ana Martínez: Apartamento + Moto + Seguro equipos
(3, 3), (3, 18), (3, 41), -- Felipe Santos: Casa + Automóvil + Seguro manejo
(4, 4), (4, 19), (4, 42), -- Laura Ramírez: Apartamento + Camioneta + Seguro incendio
(5, 5), (5, 20), (5, 43), -- Diego Moreno: Casa + Automóvil + Seguro responsabilidad civil
(6, 6), (6, 21), (6, 44), -- Camila Torres: Apartamento + Moto + Seguro equipos móviles
(7, 7), (7, 22), (7, 45), -- Andrés López: Casa + Automóvil + Seguro mercancías
(8, 8), (8, 23), (8, 46), -- Sofía Martínez: Apartamento + Camioneta + Seguro equipos electrónicos
(9, 9), (9, 24), (9, 47), -- Miguel Hernández: Casa + Automóvil + Seguro responsabilidad civil
(10, 10), (10, 25), (10, 48), -- Natalia Gómez: Apartamento + Moto + Seguro transporte
(11, 11), (11, 26), (11, 49), -- Sebastián Cruz: Casa + Automóvil + Seguro equipos
(12, 12), (12, 27), (12, 50), -- Gabriela Vega: Apartamento + Camioneta + Seguro responsabilidad civil
(13, 13), (13, 28), (13, 51), -- Ricardo Silva: Casa + Automóvil + Seguro incendio
(14, 14), (14, 29), (14, 52), -- Elena Vargas: Apartamento + Moto + Seguro equipos industriales
(15, 15), (15, 30), (15, 53), -- Oscar Jiménez: Casa + Automóvil + Seguro transporte

-- Empresas con bienes corporativos
(16, 32), (16, 39), (16, 40), (16, 41), -- Empresa ABC: Edificio comercial + Seguros múltiples
(17, 33), (17, 42), (17, 43), (17, 44), -- Tech Solutions: Conjunto cerrado + Seguros tecnológicos
(18, 34), (18, 45), (18, 46), (18, 47), -- InnovaTech: Centro comercial + Seguros innovación
(19, 35), (19, 48), (19, 49), (19, 50), -- Comercializadora Andina: Torres residenciales + Seguros comerciales
(20, 36), (20, 51), (20, 52), (20, 53), -- Logística Caribe: Edificio mixto + Seguros logísticos
(21, 37), (21, 39), (21, 41), (21, 43), -- AgroValle: Parque industrial + Seguros agrícolas
(22, 38), (22, 40), (22, 42), (22, 44), -- Textiles Norte: Torre empresarial + Seguros textiles
(23, 32), (23, 45), (23, 46), (23, 47), -- Minera Cordillera: Edificio comercial + Seguros mineros
(24, 33), (24, 48), (24, 49), (24, 50), -- Construcciones Pacífico: Conjunto cerrado + Seguros construcción
(25, 34), (25, 51), (25, 52), (25, 53), -- Alimentos Tropical: Centro comercial + Seguros alimentarios
(26, 35), (26, 39), (26, 41), (26, 43), -- Energía Renovable: Torres residenciales + Seguros energéticos
(27, 36), (27, 40), (27, 42), (27, 44); -- Turismo Magdalena: Edificio mixto + Seguros turísticos

-- =============================================================================
-- ESTADÍSTICAS FINALES
-- =============================================================================

-- Contar registros insertados
SELECT 
    'RESUMEN DE DATOS INSERTADOS' as TABLA,
    '' as CANTIDAD
UNION ALL
SELECT 'Agentes', COUNT(*) FROM agente
UNION ALL
SELECT 'Clientes', COUNT(*) FROM clientes
UNION ALL
SELECT 'Hogares', COUNT(*) FROM hogares
UNION ALL
SELECT 'Vehículos', COUNT(*) FROM vehiculos
UNION ALL
SELECT 'Copropiedades', COUNT(*) FROM copropiedades
UNION ALL
SELECT 'Otros Bienes', COUNT(*) FROM otros_bienes
UNION ALL
SELECT 'Bienes Totales', COUNT(*) FROM bienes
UNION ALL
SELECT 'Asignaciones agente-Cliente', COUNT(*) FROM agentes_clientes
UNION ALL
SELECT 'Asignaciones Cliente-Bien', COUNT(*) FROM clientes_bienes;

-- =============================================================================
-- DATOS INSERTADOS EXITOSAMENTE
-- 
-- • 15 Agentes (1 super_admin, 4 admins, 10 agentes)
-- • 27 Clientes (15 personas naturales, 12 empresas)
-- • 53 Bienes (15 hogares, 15 vehículos, 8 copropiedades, 15 otros bienes)
-- • 65 Asignaciones agente-cliente
-- • 75 Asignaciones cliente-bien
-- 
-- Base de datos lista para pruebas y desarrollo
-- ============================================================================= 