# 🔗 Nuevos Endpoints Documentados con Swagger

## 📋 **Endpoints Añadidos/Documentados**

### 🔍 **Endpoint Principal: Clientes de un Agente**
Este es el endpoint que solicitaste:

```
GET /api/agentes/{agente_id}/clientes
```

**Descripción:** Obtiene todos los clientes asignados a un agente específico

**Ejemplo de uso:**
```bash
curl -X GET http://localhost:5000/api/agentes/1/clientes
```

**Respuesta:**
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
    }
  ]
}
```

### 📊 **Endpoints Relacionados Documentados**

#### **Agentes:**
- `GET /api/agentes/{id}` - Obtener agente específico
- `GET /api/agentes/{agente_id}/clientes` - **Clientes de un agente**
- `POST /api/agentes/{agente_id}/clientes/{cliente_id}` - Asignar cliente a agente
- `DELETE /api/agentes/{agente_id}/clientes/{cliente_id}` - Desasignar cliente de agente

#### **Asignaciones:**
- `GET /api/clientes/{cliente_id}/agentes` - Agentes asignados a un cliente
- `DELETE /api/asignaciones/{agente_id}/{cliente_id}` - Eliminar asignación específica

#### **Bienes:**
- `GET /api/clientes/{cliente_id}/bienes` - Bienes de un cliente específico

## 🚀 **Cómo Usar con Swagger**

### 1. **Iniciar la API:**
```bash
pip install -r requirements.txt
python run_api.py
```

### 2. **Acceder a Swagger UI:**
```
http://localhost:5000/docs/
```

### 3. **Probar el Endpoint:**
1. Ve a la sección **"Agentes"** en Swagger
2. Busca `GET /api/agentes/{agente_id}/clientes`
3. Haz clic en **"Try it out"**
4. Introduce el ID del agente (ej: `1`)
5. Haz clic en **"Execute"**

## 📝 **Ejemplos de Uso**

### **Obtener clientes de un agente:**
```bash
curl -X GET "http://localhost:5000/api/agentes/1/clientes"
```

### **Asignar un cliente a un agente:**
```bash
curl -X POST "http://localhost:5000/api/agentes/1/clientes/2"
```

### **Obtener agentes de un cliente:**
```bash
curl -X GET "http://localhost:5000/api/clientes/1/agentes"
```

### **Obtener bienes de un cliente:**
```bash
curl -X GET "http://localhost:5000/api/clientes/1/bienes"
```

## 🔧 **Funcionalidades de Swagger**

### **Documentación Interactiva:**
- **Parámetros requeridos** claramente marcados
- **Ejemplos de respuesta** para cada endpoint
- **Códigos de error** con descripciones
- **Esquemas JSON** con tipos de datos

### **Pruebas Directas:**
- **Botón "Try it out"** para probar endpoints
- **Formularios automáticos** para parámetros
- **Respuestas en tiempo real** con código de estado

### **Filtros y Búsqueda:**
- **Tags organizados** por módulo (Agentes, Clientes, Bienes, etc.)
- **Búsqueda rápida** de endpoints
- **Navegación intuitiva**

## 📊 **Estructura de Respuestas**

Todos los endpoints siguen la estructura estándar:

```json
{
  "status": "success|error",
  "data": [...],        // Solo en success
  "message": "...",     // Solo en error
  "total": 0           // Solo en algunos endpoints
}
```

## 🔍 **Endpoints Disponibles por Módulo**

### **Health Check:**
- `GET /api/health` - Verificar estado de la API

### **Agentes:**
- `GET /api/agentes` - Lista con filtros
- `GET /api/agentes/{id}` - Agente específico
- `POST /api/agentes` - Crear agente
- `GET /api/agentes/{id}/clientes` - **Clientes del agente**
- `POST /api/agentes/{id}/clientes/{cliente_id}` - Asignar cliente
- `DELETE /api/agentes/{id}/clientes/{cliente_id}` - Desasignar cliente

### **Clientes:**
- `GET /api/clientes` - Lista con filtros
- `POST /api/clientes` - Crear cliente

### **Bienes:**
- `GET /api/bienes` - Lista con filtros
- `GET /api/bienes/tipos` - Tipos disponibles
- `GET /api/clientes/{id}/bienes` - Bienes del cliente

### **Asignaciones:**
- `GET /api/asignaciones` - Todas las asignaciones
- `POST /api/asignaciones` - Crear asignación
- `GET /api/clientes/{id}/agentes` - Agentes del cliente
- `DELETE /api/asignaciones/{agente_id}/{cliente_id}` - Eliminar asignación

## 🎯 **Casos de Uso Comunes**

### **1. Consultar cartera de un agente:**
```bash
GET /api/agentes/1/clientes
```

### **2. Ver todos los bienes de un cliente:**
```bash
GET /api/clientes/1/bienes
```

### **3. Asignar nuevo cliente a agente:**
```bash
POST /api/agentes/1/clientes/3
```

### **4. Ver qué agentes atienden a un cliente:**
```bash
GET /api/clientes/1/agentes
```

¡La API ahora tiene documentación completa e interactiva con Swagger! 🎉 