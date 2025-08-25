-- Usar la base de datos alfa_db
USE alfa_db;

-- Crear tabla de clientes
CREATE TABLE clientes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    tipo_cliente VARCHAR(10) NOT NULL, -- 'PERSONA' o 'EMPRESA'

    -- CAMPOS COMUNES Y DE LOGIN
    ciudad VARCHAR(100),
    direccion VARCHAR(255),
    telefono_movil VARCHAR(20),
    correo VARCHAR(100) UNIQUE,
    usuario VARCHAR(50) UNIQUE NOT NULL,
    clave VARCHAR(255) NOT NULL, -- Se recomienda guardar la clave encriptada

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

-- crear tabla agentes
CREATE TABLE Agente (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(150) NOT NULL,
    correo VARCHAR(100) UNIQUE NOT NULL,
    usuario VARCHAR(50) UNIQUE NOT NULL,
    clave VARCHAR(255) NOT NULL,
    rol ENUM('super_admin', 'admin', 'agente') NOT NULL,
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- crear tabla de rompimiento agente cliente
CREATE TABLE agentes_clientes (
    agente_id INT NOT NULL,
    cliente_id INT NOT NULL,
    fecha_asignacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- Se define una clave primaria compuesta para evitar duplicados
    PRIMARY KEY (agente_id, cliente_id),

    -- Se establecen las relaciones con las otras tablas (llaves foráneas)
    FOREIGN KEY (agente_id) REFERENCES Agente(id) ON DELETE CASCADE,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE CASCADE
);

-- tabla bienes (principal)
CREATE TABLE bienes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    tipo_bien ENUM('HOGAR', 'VEHICULO', 'COPROPIEDAD', 'OTRO') NOT NULL,
    bien_especifico_id INT NOT NULL,
    estado VARCHAR(50),
    comentarios_generales TEXT,
    vigencias_continuas BOOLEAN DEFAULT FALSE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- tabla de relación cliente-bien
CREATE TABLE clientes_bienes (
    cliente_id INT NOT NULL,
    bien_id INT NOT NULL,

    -- Clave primaria compuesta para la relación única
    PRIMARY KEY (cliente_id, bien_id),

    -- Llaves foráneas que garantizan la integridad
    FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE CASCADE,
    FOREIGN KEY (bien_id) REFERENCES bienes(id) ON DELETE CASCADE
);

-- tablas de bienes específicos
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

-- Insertar datos de prueba

-- Insertar agentes de prueba
INSERT INTO Agente (nombre, correo, usuario, clave, rol, activo) VALUES
('Admin Principal', 'admin@alfa.com', 'admin', 'admin123', 'super_admin', TRUE),
('Juan Pérez', 'juan@alfa.com', 'juan.perez', 'agente123', 'agente', TRUE),
('María García', 'maria@alfa.com', 'maria.garcia', 'agente123', 'agente', TRUE);

-- Insertar clientes de prueba (personas naturales)
INSERT INTO clientes (tipo_cliente, usuario, clave, nombre, tipo_documento, numero_documento, correo, telefono_movil, ciudad, direccion, edad) VALUES
('PERSONA', 'carlos.lopez', 'cliente123', 'Carlos López', 'CC', '12345678', 'carlos@email.com', '3001234567', 'Bogotá', 'Calle 123 #45-67', 30),
('PERSONA', 'ana.martinez', 'cliente123', 'Ana Martínez', 'CC', '87654321', 'ana@email.com', '3009876543', 'Medellín', 'Carrera 45 #67-89', 25);

-- Insertar clientes de prueba (empresas)
INSERT INTO clientes (tipo_cliente, usuario, clave, nit, razon_social, nombre_rep_legal, documento_rep_legal, correo, telefono_movil, ciudad, direccion) VALUES
('EMPRESA', 'empresa.abc', 'empresa123', '900123456', 'Empresa ABC S.A.S.', 'Roberto Empresario', '11111111', 'contacto@empresaabc.com', '3005555555', 'Cali', 'Avenida 6 #12-34'),
('EMPRESA', 'tech.solutions', 'empresa123', '800987654', 'Tech Solutions Ltda.', 'Sandra Tecnóloga', '22222222', 'info@techsolutions.com', '3007777777', 'Barranquilla', 'Calle 72 #43-21');

-- Crear algunas asignaciones de prueba
INSERT INTO agentes_clientes (agente_id, cliente_id) VALUES
(2, 1), -- Juan Pérez asignado a Carlos López
(2, 3), -- Juan Pérez asignado a Empresa ABC
(3, 2), -- María García asignada a Ana Martínez
(3, 4); -- María García asignada a Tech Solutions 