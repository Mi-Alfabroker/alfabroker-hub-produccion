# 🚀 Guía de Swagger para API de Davivienda

## 📋 **Resumen de Cambios**

Se ha implementado **Swagger/OpenAPI** para documentar todos los endpoints de la API de forma interactiva y completa.

### ✅ **Endpoint Solicitado Agregado:**
- `GET /api/agentes/{agente_id}/clientes` - **Obtener todos los clientes asignados a un agente**

### ✅ **Documentación Swagger Completa:**
- **15+ endpoints** documentados con esquemas detallados
- **Ejemplos de request/response** para cada endpoint
- **Validación automática** de parámetros
- **Interfaz interactiva** para probar endpoints

---

## 🛠️ **Instalación y Configuración**

### 1. **Instalar Dependencias:**
```bash
cd alfa-test
pip install -r requirements.txt
```

### 2. **Iniciar MySQL:**
```bash
bash scripts/start_mysql.sh
```

### 3. **Iniciar API:**
```bash
python run_api.py
```

### 4. **Acceder a Swagger:**
Abre en tu navegador:
```
http://localhost:5000/docs/
```

---

## 🔍 **Endpoint Principal: Clientes de un Agente**

### **URL:**
```
GET /api/agentes/{agente_id}/clientes
```

### **Descripción:**
Obtiene todos los clientes asignados a un agente específico.

### **Parámetros:**
- `agente_id` (requerido): ID del agente

### **Ejemplo de uso:**
```bash
curl -X GET "http://localhost:5000/api/agentes/1/clientes"
```

### **Respuesta exitosa:**
```json
{
  "status": "success",
  "data": [
    {
      "id": 1,
      "tipo_cliente": "PERSONA",
      "usuario": "maria.gonzalez",
      "nombre": "María González",
      "correo": "maria@ejemplo.com",
      "telefono_movil": "3001234567",
      "ciudad": "Bogotá",
      "direccion": "Calle 123 #45-67",
      "fecha_creacion": "2024-01-15T10:30:00"
    },
    {
      "id": 2,
      "tipo_cliente": "EMPRESA",
      "usuario": "empresa.abc",
      "razon_social": "Empresa ABC S.A.S.",
      "correo": "contacto@empresa.com",
      "telefono_movil": "3009876543",
      "ciudad": "Medellín",
      "direccion": "Carrera 50 #20-30",
      "fecha_creacion": "2024-01-10T14:20:00"
    }
  ]
}
```

---

## 📊 **Todos los Endpoints Documentados**

### **🔧 Health Check:**
- `GET /api/health` - Verificar estado de la API

### **👥 Agentes:**
- `GET /api/agentes` - Lista con filtros por rol/estado
- `GET /api/agentes/{id}` - Agente específico
- `POST /api/agentes` - Crear nuevo agente
- `PUT /api/agentes/{id}` - Actualizar agente
- `DELETE /api/agentes/{id}` - Eliminar agente
- `GET /api/agentes/{id}/clientes` - **Clientes del agente**
- `POST /api/agentes/{id}/clientes/{cliente_id}` - Asignar cliente
- `DELETE /api/agentes/{id}/clientes/{cliente_id}` - Desasignar cliente

### **👤 Clientes:**
- `GET /api/clientes` - Lista con filtros por tipo
- `GET /api/clientes/{id}` - Cliente específico
- `POST /api/clientes` - Crear nuevo cliente
- `PUT /api/clientes/{id}` - Actualizar cliente
- `DELETE /api/clientes/{id}` - Eliminar cliente

### **🏠 Bienes:**
- `GET /api/bienes` - Lista con filtros por tipo/cliente
- `GET /api/bienes/{id}` - Bien específico
- `POST /api/bienes` - Crear nuevo bien
- `PUT /api/bienes/{id}` - Actualizar bien
- `DELETE /api/bienes/{id}` - Eliminar bien
- `GET /api/bienes/tipos` - Tipos de bienes disponibles
- `GET /api/clientes/{id}/bienes` - Bienes del cliente
- `POST /api/bienes/{id}/asignar` - Asignar bien a cliente
- `POST /api/bienes/{id}/desasignar` - Desasignar bien de cliente

### **🔗 Asignaciones:**
- `GET /api/asignaciones` - Todas las asignaciones
- `POST /api/asignaciones` - Crear asignación
- `GET /api/clientes/{id}/agentes` - Agentes del cliente
- `DELETE /api/asignaciones/{agente_id}/{cliente_id}` - Eliminar asignación

---

## 🧪 **Probar la API**

### **Opción 1: Usar Swagger UI**
1. Ve a `http://localhost:5000/docs/`
2. Encuentra el endpoint que quieres probar
3. Haz clic en **"Try it out"**
4. Completa los parámetros
5. Haz clic en **"Execute"**

### **Opción 2: Usar curl**
```bash
# Obtener clientes del agente 1
curl -X GET "http://localhost:5000/api/agentes/1/clientes"

# Asignar cliente 2 al agente 1
curl -X POST "http://localhost:5000/api/agentes/1/clientes/2"

# Obtener agentes del cliente 1
curl -X GET "http://localhost:5000/api/clientes/1/agentes"
```

### **Opción 3: Usar el script de prueba**
```bash
python test_clientes_agente.py
```

---

## 🎯 **Casos de Uso Comunes**

### **1. Consultar cartera completa de un agente:**
```bash
GET /api/agentes/1/clientes
```

### **2. Asignar nuevo cliente a un agente:**
```bash
POST /api/agentes/1/clientes/3
```

### **3. Ver todos los bienes de un cliente:**
```bash
GET /api/clientes/1/bienes
```

### **4. Verificar qué agentes atienden a un cliente:**
```bash
GET /api/clientes/1/agentes
```

### **5. Crear una asignación directa:**
```bash
POST /api/asignaciones
{
  "agente_id": 1,
  "cliente_id": 2
}
```

---

## 🔧 **Funcionalidades de Swagger**

### **📋 Documentación Automática:**
- **Parámetros requeridos** claramente marcados
- **Tipos de datos** con validación
- **Ejemplos de respuesta** para cada código de estado
- **Descripciones detalladas** de cada endpoint

### **🚀 Pruebas Interactivas:**
- **Botón "Try it out"** para ejecutar endpoints
- **Formularios automáticos** para parámetros
- **Respuestas en tiempo real** con formato JSON
- **Códigos de estado** y mensajes de error

### **📊 Organización por Módulos:**
- **Health** - Verificación de estado
- **Agentes** - Gestión de agentes
- **Clientes** - Gestión de clientes  
- **Bienes** - Gestión de bienes asegurables
- **Asignaciones** - Relaciones agente-cliente

---

## 🔍 **Estructura de Respuestas**

Todos los endpoints siguen el formato estándar:

```json
{
  "status": "success|error",
  "data": [...],        // Solo en respuestas exitosas
  "message": "...",     // Solo en errores
  "total": 0           // En algunos endpoints de listado
}
```

---

## 🚨 **Códigos de Respuesta**

| Código | Descripción |
|--------|-------------|
| **200** | Operación exitosa |
| **201** | Recurso creado exitosamente |
| **400** | Datos inválidos o campos faltantes |
| **404** | Recurso no encontrado |
| **500** | Error interno del servidor |

---

## 📝 **Archivos Creados/Modificados**

### **Archivos modificados:**
- `requirements.txt` - Agregada dependencia `flasgger`
- `app/__init__.py` - Configuración de Swagger
- `app/routes/agente_routes.py` - Documentación endpoints agentes
- `app/routes/cliente_routes.py` - Documentación endpoints clientes
- `app/routes/bien_routes.py` - Documentación endpoints bienes
- `app/routes/asignacion_routes.py` - Documentación endpoints asignaciones

### **Archivos creados:**
- `SWAGGER_ENDPOINTS.md` - Documentación de endpoints
- `GUIA_SWAGGER.md` - Esta guía de uso
- `test_clientes_agente.py` - Script de pruebas

---

## 🎉 **¡Listo para usar!**

El endpoint `GET /api/agentes/{agente_id}/clientes` ya está disponible y documentado. Puedes:

1. **Verlo en Swagger:** `http://localhost:5000/docs/`
2. **Probarlo directamente:** `curl -X GET http://localhost:5000/api/agentes/1/clientes`
3. **Usar el script de prueba:** `python test_clientes_agente.py`

La API ahora tiene documentación completa e interactiva con Swagger UI. ¡Disfruta explorando todos los endpoints! 🚀 