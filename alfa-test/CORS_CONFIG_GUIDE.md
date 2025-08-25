# 🌐 Guía de Configuración CORS - API Alfa Broker

## 📋 **Resumen de Implementación**

Se ha implementado una configuración completa de CORS (Cross-Origin Resource Sharing) que permite controlar qué dominios pueden consumir la API.

---

## 🔧 **Componentes Implementados**

### **1. Flask-CORS** (`requirements.txt`)
```txt
Flask-CORS==4.0.0
```

### **2. Configuración CORS** (`app/config.py`)
- **Orígenes permitidos**: Lista de dominios autorizados
- **Headers permitidos**: Cabeceras HTTP autorizadas
- **Métodos HTTP**: GET, POST, PUT, DELETE, OPTIONS
- **Credenciales**: Soporte para cookies y autenticación

### **3. Aplicación de CORS** (`app/__init__.py`)
- Configuración automática en el factory de la aplicación
- Endpoint de verificación de estado y CORS

---

## 🌍 **Configuración por Ambiente**

### **🔨 Desarrollo (DevelopmentConfig)**
```python
CORS_ORIGINS = [
    "http://localhost:4200",     # Angular dev server  
    "http://127.0.0.1:4200",    # Angular dev server (alternativo)
    "http://localhost:3000",     # React/Vue dev servers
    "http://127.0.0.1:3000",    # React/Vue dev servers (alternativo)
    "http://localhost:8080",     # Vue CLI dev server
    "http://127.0.0.1:8080",    # Vue CLI dev server (alternativo)
    "http://localhost:5173",     # Vite dev server
    "http://127.0.0.1:5173",    # Vite dev server (alternativo)
]
```

### **🚀 Producción (ProductionConfig)**
```python
CORS_ORIGINS = [
    # Agregar aquí los dominios de producción cuando estén disponibles
    # "https://alfabroker.com",
    # "https://www.alfabroker.com", 
    # "https://app.alfabroker.com",
]
```

---

## 📱 **Endpoints de Verificación**

### **🔍 Health Check con CORS Info**
```
GET /api/health
```

**Response:**
```json
{
  "status": "success",
  "message": "API de Seguros funcionando correctamente",
  "cors_enabled": true,
  "allowed_origins": [
    "http://localhost:4200",
    "http://127.0.0.1:4200"
  ],
  "timestamp": "2024-01-01T00:00:00Z"
}
```

---

## 🚀 **Cómo Usar**

### **1. Instalar Dependencias:**
```bash
cd alfa-test
pip install -r requirements.txt
```

### **2. Ejecutar API:**
```bash
python run_api.py
```

### **3. Verificar CORS:**
```bash
# Desde el navegador o con curl
curl -H "Origin: http://localhost:4200" \
     -H "Access-Control-Request-Method: POST" \
     -H "Access-Control-Request-Headers: Content-Type" \
     -X OPTIONS \
     http://localhost:5000/api/health
```

---

## 🔐 **Headers Permitidos**

```python
CORS_ALLOW_HEADERS = [
    'Content-Type',              # Para JSON requests
    'Authorization',             # Para JWT tokens
    'Access-Control-Allow-Credentials',
    'Access-Control-Allow-Headers',
    'Access-Control-Allow-Methods',
    'Access-Control-Allow-Origin',
    'X-Requested-With'          # Para AJAX requests
]
```

---

## 🎯 **Métodos HTTP Permitidos**

```python
CORS_METHODS = ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS']
```

---

## 🍪 **Soporte de Credenciales**

```python
CORS_SUPPORTS_CREDENTIALS = True
```

Esto permite:
- ✅ Envío de cookies entre dominios
- ✅ Headers de autenticación (JWT)
- ✅ Credentials en fetch requests

---

## 📝 **Configuración en el Frontend Angular**

En tu servicio HTTP de Angular, puedes usar:

```typescript
// En auth.service.ts
const cabeceras = new HttpHeaders({
  'Content-Type': 'application/json'
});

this.http.post<RespuestaLogin>(
  `${this.urlApi}/auth/agente/login`,
  datosLogin,
  { 
    headers: cabeceras,
    withCredentials: true  // Para enviar cookies si es necesario
  }
)
```

---

## 🛡️ **Seguridad**

### **Desarrollo vs Producción**
- **Desarrollo**: CORS permisivo para múltiples puertos locales
- **Producción**: CORS restrictivo solo para dominios específicos

### **Variables de Entorno**
Puedes sobrescribir la configuración usando variables de entorno:

```bash
# .env
CORS_ORIGINS=https://app.alfabroker.com,https://www.alfabroker.com
```

---

## 📊 **Testing CORS**

### **Verificar desde el Navegador:**
```javascript
// Abre la consola del navegador en http://localhost:4200
fetch('http://localhost:5000/api/health')
  .then(response => response.json())
  .then(data => console.log(data));
```

### **Verificar Preflight Requests:**
```bash
curl -H "Origin: http://localhost:4200" \
     -H "Access-Control-Request-Method: POST" \
     -H "Access-Control-Request-Headers: Content-Type,Authorization" \
     -X OPTIONS \
     http://localhost:5000/api/auth/agente/login
```

---

## 🐛 **Troubleshooting**

### **Error: "CORS policy blocked"**
1. Verifica que el origen esté en `CORS_ORIGINS`
2. Confirma que el método HTTP esté permitido
3. Revisa que los headers requeridos estén en `CORS_ALLOW_HEADERS`

### **Error: "Preflight request failed"**
1. Asegúrate de que `OPTIONS` esté permitido
2. Verifica la configuración de headers
3. Confirma que el servidor esté enviando las cabeceras CORS correctas

---

## 📈 **Próximos Pasos**

1. **✅ CORS configurado** para desarrollo local
2. **🔄 Pendiente**: Configurar dominios de producción
3. **🔄 Pendiente**: Implementar rate limiting por origen
4. **🔄 Pendiente**: Logging de requests CORS para monitoring

---

## 🎉 **¡Listo!**

La API ahora puede ser consumida desde tu frontend Angular sin problemas de CORS. El frontend en `http://localhost:4200` tiene acceso completo a todos los endpoints de autenticación y datos.
