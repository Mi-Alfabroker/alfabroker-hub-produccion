# 🔐 Guía de Autenticación JWT - API Davivienda

## 📋 **Resumen de Implementación**

Se ha implementado un sistema completo de autenticación JWT que incluye:

✅ **Hash de contraseñas** con bcrypt  
✅ **Tokens JWT** para agentes y clientes  
✅ **Endpoints de login** documentados con Swagger  
✅ **Validación y decodificación** de tokens  
✅ **Renovación de tokens** próximos a expirar  

---

## 🛠️ **Dependencias Agregadas**

```txt
PyJWT==2.8.0        # Para manejo de tokens JWT
bcrypt==4.1.2       # Para hash seguro de contraseñas
```

---

## 🔧 **Componentes Implementados**

### **1. AuthService** (`app/services/auth_service.py`)
Servicio central que maneja:
- Hash y verificación de contraseñas
- Generación y decodificación de tokens JWT
- Autenticación de agentes y clientes
- Renovación de tokens

### **2. Rutas de Autenticación** (`app/routes/auth_routes.py`)
Endpoints documentados con Swagger:
- `POST /api/auth/agente/login` - Login de agente
- `POST /api/auth/cliente/login` - Login de cliente
- `POST /api/auth/token/refresh` - Renovar token
- `POST /api/auth/token/decode` - Decodificar token

### **3. Servicios Modificados**
- **AgenteService**: Hash automático de contraseñas al crear/actualizar
- **ClienteService**: Hash automático de contraseñas al crear/actualizar

---

## 🚀 **Cómo Usar**

### **1. Instalar Dependencias:**
```bash
cd alfa-test
pip install -r requirements.txt
```

### **2. Iniciar la API:**
```bash
python run_api.py
```

### **3. Acceder a Swagger:**
```
http://localhost:5000/docs/
```

---

## 📱 **Endpoints de Autenticación**

### **🔐 Login de Agente**
```
POST /api/auth/agente/login
```

**Request:**
```json
{
  "usuario": "juan.perez",
  "password": "mi_password_seguro"
}
```

**Response (200):**
```json
{
  "success": true,
  "message": "Login exitoso",
  "data": {
    "agente": {
      "id": 1,
      "nombre": "Juan Pérez",
      "correo": "juan.perez@davivienda.com",
      "usuario": "juan.perez",
      "rol": "agente",
      "activo": true,
      "fecha_creacion": "2024-01-15T10:30:00"
    },
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "expires_in": 86400
  }
}
```

### **👤 Login de Cliente**
```
POST /api/auth/cliente/login
```

**Request:**
```json
{
  "usuario": "maria.gonzalez",
  "password": "mi_password_seguro"
}
```

**Response (200):**
```json
{
  "success": true,
  "message": "Login exitoso",
  "data": {
    "cliente": {
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
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "expires_in": 86400
  }
}
```

### **🔄 Renovar Token**
```
POST /api/auth/token/refresh
```

**Request:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### **🔍 Decodificar Token**
```
POST /api/auth/token/decode
```

**Request:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response (200):**
```json
{
  "success": true,
  "message": "Token válido",
  "payload": {
    "user_id": 1,
    "user_type": "agente",
    "usuario": "juan.perez",
    "nombre": "Juan Pérez",
    "correo": "juan.perez@davivienda.com",
    "rol": "agente",
    "activo": true,
    "iat": 1642248000,
    "exp": 1642334400
  }
}
```

---

## 🎫 **Estructura del Token JWT**

### **Para Agentes:**
```json
{
  "user_id": 1,
  "user_type": "agente",
  "usuario": "juan.perez",
  "nombre": "Juan Pérez",
  "correo": "juan.perez@davivienda.com",
  "rol": "agente",
  "activo": true,
  "iat": 1642248000,
  "exp": 1642334400
}
```

### **Para Clientes:**
```json
{
  "user_id": 1,
  "user_type": "cliente",
  "usuario": "maria.gonzalez",
  "nombre": "María González",
  "correo": "maria@ejemplo.com",
  "tipo_cliente": "PERSONA",
  "razon_social": null,
  "ciudad": "Bogotá",
  "iat": 1642248000,
  "exp": 1642334400
}
```

---

## 🔒 **Seguridad Implementada**

### **Hash de Contraseñas:**
- **Algoritmo**: bcrypt con salt automático
- **Aplicación**: Automática al crear/actualizar usuarios
- **Verificación**: Comparación segura al hacer login

### **Tokens JWT:**
- **Algoritmo**: HS256
- **Expiración**: 24 horas
- **Contenido**: Info del usuario (sin contraseña)
- **Validación**: Firma digital verificable

### **Validaciones:**
- ✅ Usuario existe
- ✅ Contraseña correcta
- ✅ Agente activo (solo para agentes)
- ✅ Token válido y no expirado

---

## 🧪 **Probar el Sistema**

### **Opción 1: Script de Prueba**
```bash
python test_auth.py
```

### **Opción 2: Swagger UI**
1. Ve a `http://localhost:5000/docs/`
2. Busca la sección **"Autenticación"**
3. Prueba los endpoints de login
4. Copia el token generado

### **Opción 3: cURL**
```bash
# Login de agente
curl -X POST "http://localhost:5000/api/auth/agente/login" \
     -H "Content-Type: application/json" \
     -d '{"usuario": "agente.test", "password": "password123"}'

# Login de cliente
curl -X POST "http://localhost:5000/api/auth/cliente/login" \
     -H "Content-Type: application/json" \
     -d '{"usuario": "cliente.test", "password": "password456"}'
```

---

## 📊 **Estados de Respuesta**

| Código | Descripción |
|--------|-------------|
| **200** | Login exitoso |
| **400** | Datos faltantes/inválidos |
| **401** | Credenciales incorrectas |
| **500** | Error interno del servidor |

---

## 🔄 **Flujo de Autenticación**

```mermaid
sequenceDiagram
    participant C as Cliente/App
    participant API as API Server
    participant DB as Base de Datos
    
    C->>API: POST /auth/[agente|cliente]/login
    API->>DB: Buscar usuario
    DB-->>API: Datos del usuario
    API->>API: Verificar contraseña (bcrypt)
    API->>API: Generar token JWT
    API-->>C: Token + datos usuario (sin password)
    
    Note over C,API: Para futuras requests:
    C->>API: Request con header Authorization: Bearer <token>
    API->>API: Validar token JWT
    API-->>C: Respuesta autorizada
```

---

## 🚀 **Próximos Pasos (Futuras Implementaciones)**

### **Protección de Rutas:**
```python
# Ejemplo de decorador para proteger endpoints
@require_auth(['agente', 'admin'])
def protected_endpoint():
    # Solo agentes y admins pueden acceder
    pass
```

### **Middleware de Autenticación:**
```python
# Verificación automática de tokens en headers
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### **Refresh Tokens:**
- Tokens de corta duración (1-2 horas)
- Refresh tokens de larga duración (30 días)
- Renovación automática

---

## 🎯 **Casos de Uso**

### **1. Autenticación de Agente:**
```python
# El agente hace login
response = login_agente("juan.perez", "password123")
token = response['data']['token']

# Usar token en futuras requests
headers = {"Authorization": f"Bearer {token}"}
```

### **2. Validación de Token:**
```python
# Decodificar token para obtener info del usuario
payload = decode_token(token)
user_id = payload['user_id']
user_type = payload['user_type']  # 'agente' o 'cliente'
```

### **3. Verificación de Permisos:**
```python
# Verificar rol del usuario
if payload['user_type'] == 'agente' and payload['rol'] == 'admin':
    # Usuario tiene permisos de administrador
    pass
```

---

## ✅ **Características Implementadas**

- [x] Hash seguro de contraseñas con bcrypt
- [x] Generación de tokens JWT con información del usuario
- [x] Login separado para agentes y clientes
- [x] Validación de credenciales
- [x] Decodificación y validación de tokens
- [x] Renovación de tokens próximos a expirar
- [x] Documentación completa en Swagger
- [x] Manejo de errores y validaciones
- [x] Script de pruebas completo
- [x] Exclusión de contraseñas en respuestas
- [x] Tokens con expiración configurable (24 horas)

---

## 🎉 **¡Sistema Listo!**

El sistema de autenticación JWT está completamente implementado y listo para usar. Todos los endpoints están documentados en Swagger y pueden ser probados inmediatamente.

**Para empezar a usar:**
1. **Inicia la API:** `python run_api.py`
2. **Ve a Swagger:** `http://localhost:5000/docs/`
3. **Crea usuarios** con los endpoints existentes
4. **Haz login** con los nuevos endpoints de autenticación
5. **Obtén tokens JWT** para futuras implementaciones

¡El token contiene toda la información del usuario excepto la contraseña, tal como solicitaste! 🚀 