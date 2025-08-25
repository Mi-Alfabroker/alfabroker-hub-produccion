# 🚀 Despliegue del Frontend Angular

Este directorio contiene los archivos necesarios para desplegar la aplicación Angular usando Docker.

## 📁 Archivos Creados

- `frontend.yml` - Configuración Docker Compose con Nginx
- `frontend-ssr.yml` - Configuración Docker Compose con Node.js SSR
- `nginx.conf` - Configuración del servidor Nginx
- `start-frontend.sh` - Script de inicio automatizado

## 🛠️ Prerrequisitos

1. **Build de Angular generado:**
   ```bash
   cd alfa-frontend
   npm run build
   ```

2. **Docker y Docker Compose instalados**

## 🚀 Opciones de Despliegue

### Opción 1: Nginx (Recomendado para Producción)
```bash
# Desde el directorio alfa-frontend
docker-compose -f frontend.yml up -d
```

**Características:**
- ✅ Mejor rendimiento para archivos estáticos
- ✅ Configuración de cache optimizada
- ✅ Proxy automático para API calls
- ✅ Headers de seguridad incluidos

### Opción 2: Node.js con SSR
```bash
# Desde el directorio alfa-frontend
docker-compose -f frontend-ssr.yml up -d
```

**Características:**
- ✅ Server-Side Rendering
- ✅ Mejor SEO
- ✅ Carga inicial más rápida

### Opción 3: Script Automatizado
```bash
# Desde el directorio alfa-frontend
./start-frontend.sh
```

## 🌐 URLs de Acceso

- **Frontend:** http://localhost:4200
- **API Backend:** http://localhost:5000

## 📋 Comandos Útiles

```bash
# Ver logs del frontend
docker-compose -f frontend.yml logs -f alfa-frontend

# Ver logs del API
docker-compose -f frontend.yml logs -f alfa-api

# Detener servicios
docker-compose -f frontend.yml down

# Reiniciar servicios
docker-compose -f frontend.yml restart

# Ver estado de contenedores
docker-compose -f frontend.yml ps
```

## 🔧 Configuración de Nginx

El archivo `nginx.conf` incluye:

- **Soporte para Angular Router:** Redirección automática a `index.html`
- **Proxy API:** Las llamadas a `/api/*` se redirigen al backend
- **Cache de archivos estáticos:** Optimización para JS, CSS, imágenes
- **Compresión Gzip:** Reducción del tamaño de archivos
- **Headers de seguridad:** Protección básica contra ataques

## 🔗 Integración con Backend

El frontend está configurado para comunicarse automáticamente con el API backend:

- Las llamadas HTTP a `/api/*` se proxy al contenedor `alfa-api:5000`
- Ambos servicios están en la misma red Docker (`alfa-network`)
- El frontend espera a que el API esté disponible antes de iniciar

## 🐛 Solución de Problemas

### Error: "No se encontró el directorio dist"
```bash
cd alfa-frontend
npm run build
```

### Error: "Puerto 4200 ya está en uso"
Cambiar el puerto en el archivo `frontend.yml`:
```yaml
ports:
  - "8080:80"  # Cambiar 4200 por 8080
```

### Error de conexión con API
Verificar que el backend esté ejecutándose:
```bash
curl http://localhost:5000/health
```

## 📦 Estructura de Archivos

```
alfa-frontend/
├── dist/                    # Build de Angular
├── frontend.yml            # Docker Compose (Nginx)
├── frontend-ssr.yml        # Docker Compose (Node.js SSR)
├── nginx.conf              # Configuración Nginx
├── start-frontend.sh       # Script de inicio
└── DEPLOYMENT.md          # Esta documentación
```
