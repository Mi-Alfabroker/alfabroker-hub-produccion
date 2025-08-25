# API de Bienes Asegurables - Guía de Uso

## 📖 Descripción

El sistema de bienes asegurables implementa un **patrón polimórfico** que permite manejar diferentes tipos de bienes (hogares, vehículos, copropiedades, otros) de manera unificada, manteniendo la flexibilidad para datos específicos de cada tipo.

## 🏗️ Arquitectura

### Patrón Polimórfico
- **Tabla principal:** `bienes` - Contiene datos comunes y referencia al bien específico
- **Tablas específicas:** `hogares`, `vehiculos`, `copropiedades`, `otros_bienes`
- **Relación:** `clientes_bienes` - Conecta clientes con sus bienes

### Tipos de Bienes Soportados
1. **HOGAR** - Inmuebles residenciales
2. **VEHICULO** - Vehículos motorizados  
3. **COPROPIEDAD** - Propiedades horizontales/edificios
4. **OTRO** - Otros tipos de bienes asegurables

## 🚀 Configuración Inicial

### 1. Resetear Base de Datos con Bienes
```bash
# Opción 1: Script automático
./reset_db_with_bienes.sh

# Opción 2: Manual
docker-compose down
docker volume rm alfa-test_mysql_data
docker-compose up -d mysql
# Esperar MySQL...
docker exec -i alfa-test-mysql-1 mysql -u root -prootpassword davivienda_seguros < database/init.sql
docker exec -i alfa-test-mysql-1 mysql -u root -prootpassword davivienda_seguros < database/datos_bienes_ejemplo.sql
```

### 2. Iniciar API
```bash
python run_api.py
```

### 3. Probar Endpoints
```bash
python test_bienes_api.py
```

## 📡 Endpoints Disponibles

### Endpoints Principales

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/bienes` | Obtener todos los bienes |
| GET | `/api/bienes?tipo=HOGAR` | Filtrar por tipo |
| GET | `/api/bienes?cliente_id=1` | Filtrar por cliente |
| GET | `/api/bienes/{id}` | Obtener bien específico |
| POST | `/api/bienes` | Crear nuevo bien |
| PUT | `/api/bienes/{id}` | Actualizar bien |
| DELETE | `/api/bienes/{id}` | Eliminar bien |

### Endpoints de Asignación

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/bienes/{id}/asignar` | Asignar bien a cliente |
| POST | `/api/bienes/{id}/desasignar` | Desasignar bien de cliente |
| GET | `/api/clientes/{id}/bienes` | Obtener bienes de un cliente |

### Endpoints de Información

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/bienes/tipos` | Obtener tipos disponibles |

## 💾 Ejemplos de Uso

### 1. Crear un Hogar
```json
POST /api/bienes
{
  "tipo_bien": "HOGAR",
  "data_especifico": {
    "tipo_inmueble": "Casa",
    "ciudad_inmueble": "Bogotá",
    "direccion_inmueble": "Carrera 15 #45-23",
    "numero_pisos": 2,
    "ano_construccion": 2015,
    "valor_inmueble_avaluo": 350000000.00,
    "valor_contenidos_normales_avaluo": 25000000.00
  },
  "data_general": {
    "estado": "Activo",
    "comentarios_generales": "Casa principal de familia",
    "vigencias_continuas": true
  },
  "cliente_id": 1
}
```

### 2. Crear un Vehículo
```json
POST /api/bienes
{
  "tipo_bien": "VEHICULO",
  "data_especifico": {
    "tipo_vehiculo": "Automóvil",
    "placa": "ABC123",
    "marca": "Toyota",
    "serie_referencia": "Corolla Cross XLI",
    "ano_modelo": 2023,
    "codigo_fasecolda": "81042090",
    "valor_vehiculo": 85000000.00
  },
  "data_general": {
    "estado": "Activo",
    "comentarios_generales": "Vehículo familiar"
  }
}
```

### 3. Crear una Copropiedad
```json
POST /api/bienes
{
  "tipo_bien": "COPROPIEDAD",
  "data_especifico": {
    "tipo_copropiedad": "Conjunto Residencial",
    "ciudad": "Bogotá",
    "direccion": "Carrera 7 #127-45",
    "estrato": 4,
    "numero_torres": 3,
    "numero_maximo_pisos": 15,
    "cantidad_unidades_apartamentos": 180,
    "valor_edificio_area_comun_avaluo": 2500000000.00
  },
  "data_general": {
    "estado": "Activo"
  }
}
```

### 4. Crear Otro Bien
```json
POST /api/bienes
{
  "tipo_bien": "OTRO",
  "data_especifico": {
    "tipo_seguro": "Seguro de Transporte",
    "bien_asegurado": "Mercancías en Tránsito",
    "valor_bien_asegurar": 500000000.00,
    "detalles_bien_asegurado": "Cobertura para mercancías transportadas"
  },
  "data_general": {
    "estado": "Activo"
  }
}
```

### 5. Actualizar un Bien
```json
PUT /api/bienes/1
{
  "data_general": {
    "estado": "Inactivo",
    "comentarios_generales": "Bien suspendido temporalmente"
  },
  "data_especifico": {
    "valor_inmueble_avaluo": 380000000.00
  }
}
```

### 6. Asignar Bien a Cliente
```json
POST /api/bienes/1/asignar
{
  "cliente_id": 2
}
```

## 📊 Estructura de Respuesta

### Respuesta de Bien con Detalles
```json
{
  "status": "success",
  "data": {
    "id": 1,
    "tipo_bien": "HOGAR",
    "bien_especifico_id": 1,
    "estado": "Activo",
    "comentarios_generales": "Casa principal de familia",
    "vigencias_continuas": true,
    "fecha_creacion": "2024-01-15T10:30:00",
    "bien_especifico": {
      "id": 1,
      "tipo_inmueble": "Casa",
      "ciudad_inmueble": "Bogotá",
      "direccion_inmueble": "Carrera 15 #45-23",
      "numero_pisos": 2,
      "ano_construccion": 2015,
      "valor_inmueble_avaluo": 350000000.0
    }
  }
}
```

## 🔧 Validaciones

### Campos Requeridos por Tipo

**HOGAR:**
- `tipo_inmueble` (requerido)

**VEHICULO:**
- `placa` (requerido, único)

**COPROPIEDAD:**
- `tipo_copropiedad` (requerido)

**OTRO:**
- `bien_asegurado` (requerido)

## 🗃️ Datos de Prueba Incluidos

El sistema incluye datos de ejemplo:
- **5 Hogares** en diferentes ciudades
- **5 Vehículos** de diferentes tipos
- **3 Copropiedades** con características variadas
- **5 Otros Bienes** con diferentes coberturas
- **16+ Asignaciones** cliente-bien

## 🚨 Manejo de Errores

### Errores Comunes
- **400** - Datos de validación incorrectos
- **404** - Bien o cliente no encontrado
- **500** - Error interno del servidor

### Ejemplo de Error
```json
{
  "status": "error",
  "message": "tipo_bien debe ser HOGAR, VEHICULO, COPROPIEDAD o OTRO"
}
```

## 🔄 Flujo de Trabajo Típico

1. **Crear cliente** (si no existe)
2. **Crear bien** específico con `POST /api/bienes`
3. **Asignar bien** al cliente (automático si se incluye `cliente_id`)
4. **Consultar bienes** del cliente con `/api/clientes/{id}/bienes`
5. **Actualizar bien** según necesidades
6. **Gestionar asignaciones** según cambios de propiedad

¡El sistema está listo para gestionar bienes asegurables de forma completa y escalable! 🎉 