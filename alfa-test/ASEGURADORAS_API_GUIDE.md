# Guía del Módulo de Aseguradoras - API Davivienda

## Introducción

Este módulo implementa un sistema completo de gestión de seguros que conecta las aseguradoras con los bienes asegurables existentes en el sistema. Sigue una arquitectura de tres etapas:

1. **Etapa 1: Catálogo de Aseguradoras** - Plantillas de productos y servicios
2. **Etapa 2: Opciones de Seguro** - Cotizaciones personalizadas
3. **Etapa 3: Pólizas** - Contratos formales con planes de pago

## Configuración Inicial

### 1. Ejecutar Migraciones

```bash
# Configurar el módulo de aseguradoras
bash scripts/setup_aseguradoras.sh
```

### 2. Iniciar la API

```bash
# Iniciar la API
python run_api.py
```

La documentación Swagger estará disponible en: `http://localhost:5000/docs/`

## Flujo de Trabajo

### Flujo Típico de Creación de Seguros

```
1. Crear Aseguradora → 2. Configurar Productos → 3. Crear Cotización → 4. Generar Póliza
```

## Endpoints Principales

### 1. Aseguradoras (`/api/aseguradoras`)

#### Crear Aseguradora
```http
POST /api/aseguradoras
Content-Type: application/json

{
  "nombre": "Seguros Alfa",
  "codigo": "SALFA",
  "descripcion": "Aseguradora líder en el mercado",
  "porcentaje_comision": 10.0,
  "activa": true
}
```

#### Obtener Aseguradoras
```http
GET /api/aseguradoras
```

#### Configurar Deducibles
```http
POST /api/aseguradoras/1/deducibles

{
  "tipo_bien": "HOGAR",
  "porcentaje_deducible": 5.0,
  "descripcion": "Deducible para hogares"
}
```

#### Configurar Coberturas
```http
POST /api/aseguradoras/1/coberturas

{
  "tipo_bien": "HOGAR",
  "nombre_cobertura": "Incendio",
  "descripcion": "Cobertura contra incendios",
  "porcentaje_cobertura": 100.0
}
```

#### Configurar Financiación
```http
POST /api/aseguradoras/1/financiacion

{
  "tipo_bien": "VEHICULO",
  "cuotas_minimas": 1,
  "cuotas_maximas": 12,
  "tasa_interes": 0.0
}
```

### 2. Opciones de Seguro (`/api/opciones-seguro`)

#### Crear Cotización
```http
POST /api/opciones-seguro
Content-Type: application/json

{
  "bien_id": 1,
  "aseguradora_id": 1,
  "agente_id": 1,
  "valor_asegurado": 100000000,
  "deducibles_ids": [1, 2],
  "coberturas_ids": [1, 2, 3],
  "financiacion_id": 1,
  "observaciones": "Cotización para hogar familiar"
}
```

#### Simular Prima
```http
POST /api/opciones-seguro/simular-prima

{
  "bien_id": 1,
  "aseguradora_id": 1,
  "valor_asegurado": 100000000,
  "deducibles_ids": [1],
  "coberturas_ids": [1, 2]
}
```

### 3. Pólizas (`/api/polizas`)

#### Crear Póliza
```http
POST /api/polizas
Content-Type: application/json

{
  "opcion_seguro_id": 1,
  "tomador_id": 1,
  "beneficiario_id": 1,
  "asegurado_id": 1,
  "fecha_inicio": "2024-01-15",
  "fecha_fin": "2025-01-15",
  "forma_pago": "MENSUAL",
  "observaciones": "Póliza con descuento por buen conductor"
}
```

#### Obtener Plan de Pagos
```http
GET /api/polizas/1/plan-pagos
```

#### Registrar Pago
```http
POST /api/polizas/1/pagos/1

{
  "valor_pagado": 100000.00,
  "fecha_pago": "2024-02-15",
  "observaciones": "Pago realizado en efectivo"
}
```

## Modelos de Datos

### Aseguradora
- `id`: Identificador único
- `nombre`: Nombre de la aseguradora
- `codigo`: Código único
- `descripcion`: Descripción
- `porcentaje_comision`: Porcentaje de comisión
- `activa`: Estado activo/inactivo

### Opción de Seguro
- `id`: Identificador único
- `bien_id`: Referencia al bien asegurado
- `aseguradora_id`: Referencia a la aseguradora
- `agente_id`: Referencia al agente
- `valor_asegurado`: Valor asegurado
- `valor_prima`: Prima calculada
- `valor_comision`: Comisión calculada
- `estado`: Estado de la cotización

### Póliza
- `id`: Identificador único
- `numero_poliza`: Número único generado
- `opcion_seguro_id`: Referencia a la opción de seguro
- `tomador_id`: Cliente tomador
- `beneficiario_id`: Cliente beneficiario
- `asegurado_id`: Cliente asegurado
- `fecha_inicio`: Fecha de inicio
- `fecha_fin`: Fecha de fin
- `forma_pago`: Forma de pago
- `estado`: Estado de la póliza

## Validaciones Importantes

### Validaciones de Negocio

1. **Valor Asegurado**: No puede exceder el avalúo del bien
2. **Fechas**: La fecha de fin debe ser posterior a la fecha de inicio
3. **Estados**: Solo se pueden crear pólizas de opciones aceptadas
4. **Pagos**: Solo se pueden registrar pagos en cuotas pendientes

### Códigos de Estado

- **Opciones de Seguro**: `BORRADOR`, `ACTIVA`, `ACEPTADA`, `RECHAZADA`
- **Pólizas**: `ACTIVA`, `VENCIDA`, `CANCELADA`, `SUSPENDIDA`
- **Pagos**: `PENDIENTE`, `PAGADA`, `VENCIDA`

## Ejemplos de Uso

### Ejemplo Completo: Crear Seguro para un Hogar

```bash
# 1. Crear aseguradora
curl -X POST http://localhost:5000/api/aseguradoras \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Seguros Premium",
    "codigo": "SPREM",
    "descripcion": "Seguros de alta calidad",
    "porcentaje_comision": 12.0,
    "activa": true
  }'

# 2. Configurar deducible para hogares
curl -X POST http://localhost:5000/api/aseguradoras/1/deducibles \
  -H "Content-Type: application/json" \
  -d '{
    "tipo_bien": "HOGAR",
    "porcentaje_deducible": 5.0,
    "descripcion": "Deducible estándar hogares"
  }'

# 3. Configurar cobertura
curl -X POST http://localhost:5000/api/aseguradoras/1/coberturas \
  -H "Content-Type: application/json" \
  -d '{
    "tipo_bien": "HOGAR",
    "nombre_cobertura": "Todo Riesgo",
    "descripcion": "Cobertura completa",
    "porcentaje_cobertura": 100.0
  }'

# 4. Crear cotización
curl -X POST http://localhost:5000/api/opciones-seguro \
  -H "Content-Type: application/json" \
  -d '{
    "bien_id": 1,
    "aseguradora_id": 1,
    "agente_id": 1,
    "valor_asegurado": 100000000,
    "deducibles_ids": [1],
    "coberturas_ids": [1]
  }'

# 5. Crear póliza
curl -X POST http://localhost:5000/api/polizas \
  -H "Content-Type: application/json" \
  -d '{
    "opcion_seguro_id": 1,
    "tomador_id": 1,
    "beneficiario_id": 1,
    "asegurado_id": 1,
    "fecha_inicio": "2024-01-15",
    "fecha_fin": "2025-01-15",
    "forma_pago": "MENSUAL"
  }'
```

## Reportes y Estadísticas

### Estadísticas de Pólizas
```http
GET /api/polizas/estadisticas?fecha_inicio=2024-01-01&fecha_fin=2024-12-31
```

### Pólizas Vencidas
```http
GET /api/polizas/vencidas?dias_vencimiento=30
```

## Integración con Módulos Existentes

### Conexión con Bienes
- Las opciones de seguro se vinculan directamente con los bienes existentes
- Se valida que el valor asegurado no exceda el avalúo del bien
- Se consideran las características específicas de cada tipo de bien

### Conexión con Clientes
- Los roles de tomador, beneficiario y asegurado pueden ser diferentes clientes
- Se mantiene la trazabilidad completa de la relación cliente-póliza

### Conexión con Agentes
- Cada opción de seguro está vinculada a un agente específico
- Se calculan automáticamente las comisiones según la configuración de la aseguradora

## Notas Técnicas

### Arquitectura
- **Modelos**: Definición de estructuras de datos con SQLAlchemy
- **Servicios**: Lógica de negocio y validaciones
- **Rutas**: Endpoints REST con documentación Swagger
- **Validaciones**: Validaciones de negocio y integridad referencial

### Consideraciones de Rendimiento
- Paginación en endpoints de listado
- Índices en campos de búsqueda frecuente
- Carga diferida de relaciones complejas

### Seguridad
- Validación de entrada en todos los endpoints
- Manejo de errores consistente
- Logging de operaciones críticas

## Solución de Problemas

### Problemas Comunes

1. **Error de conexión MySQL**: Verificar que MySQL esté corriendo
2. **Tablas no encontradas**: Ejecutar migraciones con `setup_aseguradoras.sh`
3. **Validaciones de negocio**: Revisar que los valores cumplan las restricciones

### Logs y Debugging

Los logs de la aplicación incluyen información detallada sobre:
- Validaciones de negocio
- Cálculos de primas y comisiones
- Operaciones de base de datos
- Errores de validación

## Próximos Pasos

1. Implementar notificaciones automáticas para pólizas próximas a vencer
2. Agregar reportes avanzados y dashboards
3. Implementar workflow de aprobación para pólizas de alto valor
4. Integrar con sistemas de pago externos
5. Agregar funcionalidad de renovación automática de pólizas 