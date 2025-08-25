# Esquema de Base de Datos - BIEN ASEGURADO

Este documento describe la arquitectura de la base de datos para el sistema de gestión de clientes, agentes y bienes asegurables. El diseño utiliza una relación polimórfica para manejar distintos tipos de bienes de forma escalable y organizada.

***

## Diagrama de Entidad-Relación (Simplificado) 🗺️

El siguiente diagrama ilustra cómo se conectan las tablas principales del sistema.

```mermaid
erDiagram
    agente ||--o{ agentes_clientes : "asigna"
    clientes ||--o{ agentes_clientes : "es asignado a"
    clientes ||--o{ clientes_bienes : "posee"
    bienes ||--o{ clientes_bienes : "es poseído por"

    bienes {
        INT id PK
        ENUM tipo_bien
        INT bien_especifico_id
        VARCHAR estado
    }

    clientes_bienes {
        INT cliente_id FK
        INT bien_id FK
    }

    agentes_clientes {
        INT agente_id FK
        INT cliente_id FK
    }

    subgraph "Bienes Específicos"
        bienes --> hogares : "apunta a"
        bienes --> vehiculos : "apunta a"
        bienes --> copropiedades : "apunta a"
        bienes --> otros_bienes : "apunta a"
    end
```
*Este es un diagrama conceptual. La relación polimórfica de `bienes` a las tablas específicas se maneja a nivel de aplicación.*

***

## Descripción de las Tablas 📁

### Tablas Principales

#### `clientes`
Almacena la información de los clientes, ya sean personas naturales o empresas.

```sql
CREATE TABLE clientes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    tipo_cliente VARCHAR(10) NOT NULL, -- 'PERSONA' o 'EMPRESA'
    ciudad VARCHAR(100),
    direccion VARCHAR(255),
    telefono_movil VARCHAR(20),
    correo VARCHAR(100) UNIQUE,
    usuario VARCHAR(50) UNIQUE NOT NULL,
    clave VARCHAR(255) NOT NULL,
    -- Campos para Persona Natural
    tipo_documento VARCHAR(10),
    numero_documento VARCHAR(20),
    nombre VARCHAR(150),
    edad INT,
    -- Campos para Empresa
    nit VARCHAR(20),
    razon_social VARCHAR(255),
    nombre_rep_legal VARCHAR(150),
    documento_rep_legal VARCHAR(20),
    telefono_rep_legal VARCHAR(20),
    correo_rep_legal VARCHAR(100),
    contacto_alternativo VARCHAR(255)
);
```

#### `agente`
Contiene los usuarios administradores del software con sus respectivos roles.

```sql
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
```

***

### Tablas de Unión (Relaciones) 🔗

#### `agentes_clientes`
Tabla de rompimiento que asigna un agente a un cliente (relación N:N).

```sql
CREATE TABLE agentes_clientes (
    agente_id INT NOT NULL,
    cliente_id INT NOT NULL,
    fecha_asignacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (agente_id, cliente_id),
    FOREIGN KEY (agente_id) REFERENCES agente(id) ON DELETE CASCADE,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE CASCADE
);
```

#### `clientes_bienes`
Tabla de rompimiento que asigna un bien a un cliente (relación N:N).

```sql
CREATE TABLE clientes_bienes (
    cliente_id INT NOT NULL,
    bien_id INT NOT NULL,
    PRIMARY KEY (cliente_id, bien_id),
    FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE CASCADE,
    FOREIGN KEY (bien_id) REFERENCES bienes(id) ON DELETE CASCADE
);
```

***

### Módulo de Bienes (Núcleo Polimórfico) 🏛️

#### `bienes`
Tabla central que unifica todos los bienes. Actúa como ancla para la relación polimórfica.

```sql
CREATE TABLE bienes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    tipo_bien ENUM('HOGAR', 'VEHICULO', 'COPROPIEDAD', 'OTRO') NOT NULL,
    bien_especifico_id INT NOT NULL,
    estado VARCHAR(50),
    comentarios_generales TEXT,
    vigencias_continuas BOOLEAN DEFAULT FALSE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

***

### Tablas Específicas de Bienes 🏠🚗🏢

#### `hogares`
```sql
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
```

#### `vehiculos`
```sql
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
```

#### `copropiedades`
```sql
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
```

#### `otros_bienes`
```sql
CREATE TABLE otros_bienes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    tipo_seguro VARCHAR(255),
    bien_asegurado VARCHAR(255),
    valor_bien_asegurar DECIMAL(15, 2),
    detalles_bien_asegurado TEXT
);
