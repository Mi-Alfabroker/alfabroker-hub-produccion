# API Flask con SQLAlchemy y MySQL

Esta es una API RESTful desarrollada con Flask y SQLAlchemy que gestiona agentes, clientes y sus asignaciones, conectada a una base de datos MySQL 8.0 en Docker.

## Estructura del Proyecto

```
alfa-test/
├── app/
│   ├── __init__.py              # Inicializa la app y las extensiones
│   ├── config.py                # Configuraciones MySQL
│   ├── routes/                  # Controladores - Define los endpoints de la API
│   │   ├── __init__.py
│   │   ├── agente_routes.py     # CRUD agentes + health check
│   │   ├── cliente_routes.py    # CRUD clientes
│   │   └── asignacion_routes.py # Gestión asignaciones
│   ├── models/                  # Define las tablas de la base de datos (SQLAlchemy)
│   │   ├── __init__.py
│   │   ├── agente_model.py      # Modelo adaptado a MySQL
│   │   ├── cliente_model.py     # Modelo adaptado a MySQL
│   │   └── agente_cliente_model.py # Relación muchos-a-muchos
│   ├── services/                # Lógica de Negocio
│   │   ├── __init__.py
│   │   ├── agente_service.py
│   │   ├── cliente_service.py
│   │   └── agente_cliente_service.py
│   └── utils/                   # Utilidades
│       └── __init__.py
├── database/
│   └── init.sql                 # Script de inicialización de MySQL
├── scripts/
│   ├── start_mysql.sh           # Script para iniciar MySQL
│   ├── stop_mysql.sh            # Script para detener MySQL
│   └── reset_db.sh              # Script para resetear BD
├── docker-compose.yml           # Configuración de MySQL en Docker
├── run.py                       # Punto de entrada original
├── run_api.py                   # Punto de entrada con verificación MySQL
├── requirements.txt             # Dependencias (incluye PyMySQL)
└── README.md                    # Este archivo
```

## 🚀 Instalación y Configuración

### Prerequisitos
- Docker y Docker Compose instalados
- Python 3.8+ instalado

### 1. Instalar dependencias de Python
```bash
cd alfa-test
pip install -r requirements.txt
```

### 2. Iniciar MySQL en Docker
```bash
# Hacer script ejecutable (solo la primera vez)
chmod +x scripts/*.sh

# Iniciar MySQL 8.0 en Docker
bash scripts/start_mysql.sh
```

### 3. Ejecutar la API
```bash
# Opción 1: Con verificación automática de MySQL
python run_api.py

# Opción 2: Forma tradicional
python run.py
```

La API estará disponible en `http://localhost:5000`

## 🐳 Gestión de MySQL en Docker

### Iniciar MySQL
```bash
bash scripts/start_mysql.sh
```

### Detener MySQL
```bash
bash scripts/stop_mysql.sh
```

### Resetear base de datos (elimina todos los datos)
```bash
bash scripts/reset_db.sh
```

### Conectarse directamente a MySQL
```bash
# Desde línea de comandos
mysql -h localhost -P 3306 -u alfa_user -p alfa_db

# Password: alfa_password
```

### Ver logs de MySQL
```bash
docker logs alfa_mysql
```

## 🔧 Configuración de Base de Datos

**Credenciales de MySQL:**
- **Host:** localhost
- **Puerto:** 3306
- **Base de datos:** alfa_db
- **Usuario:** alfa_user
- **Contraseña:** alfa_password
- **Usuario root:** root (contraseña: root_password)

**Datos de prueba incluidos:**
- 3 agentes (1 super_admin, 2 agentes)
- 4 clientes (2 personas, 2 empresas)
- Varias asignaciones de prueba

## 📍 Endpoints Principales

### Health Check
- **GET** `/api/health` - Verificar si la API está en línea

### Agentes
- **GET** `/api/agentes` - Obtener todos los agentes
- **GET** `/api/agentes?rol=admin` - Filtrar agentes por rol (super_admin, admin, agente)
- **GET** `/api/agentes?activo=true` - Obtener solo agentes activos
- **GET** `/api/agentes/{id}` - Obtener un agente específico
- **POST** `/api/agentes` - Crear un nuevo agente
- **PUT** `/api/agentes/{id}` - Actualizar un agente
- **DELETE** `/api/agentes/{id}` - Eliminar un agente

### Clientes
- **GET** `/api/clientes` - Obtener todos los clientes
- **GET** `/api/clientes?tipo=PERSONA` - Filtrar clientes por tipo (PERSONA, EMPRESA)
- **GET** `/api/clientes/{id}` - Obtener un cliente específico
- **POST** `/api/clientes` - Crear un nuevo cliente
- **PUT** `/api/clientes/{id}` - Actualizar un cliente
- **DELETE** `/api/clientes/{id}` - Eliminar un cliente

### Asignaciones Agente-Cliente
- **GET** `/api/asignaciones` - Obtener todas las asignaciones
- **GET** `/api/agentes/{agente_id}/clientes` - Obtener clientes de un agente
- **GET** `/api/clientes/{cliente_id}/agentes` - Obtener agentes de un cliente
- **POST** `/api/asignaciones` - Crear una nueva asignación
- **DELETE** `/api/asignaciones/{agente_id}/{cliente_id}` - Eliminar asignación

## 🧪 Ejemplos de Uso

### Verificar que la API esté en línea
```bash
curl -X GET http://localhost:5000/api/health
```

### Obtener todos los agentes
```bash
curl -X GET http://localhost:5000/api/agentes
```

### Crear un agente
```bash
curl -X POST http://localhost:5000/api/agentes \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Juan Pérez",
    "correo": "juan@ejemplo.com",
    "usuario": "juan.perez",
    "clave": "mi_clave_segura",
    "rol": "agente",
    "activo": true
  }'
```

### Crear un cliente persona natural
```bash
curl -X POST http://localhost:5000/api/clientes \
  -H "Content-Type: application/json" \
  -d '{
    "tipo_cliente": "PERSONA",
    "usuario": "maria.gonzalez",
    "clave": "clave_segura",
    "nombre": "María González",
    "tipo_documento": "CC",
    "numero_documento": "12345678",
    "correo": "maria@ejemplo.com",
    "telefono_movil": "3001234567",
    "ciudad": "Bogotá",
    "direccion": "Calle 123 #45-67"
  }'
```

### Crear una asignación agente-cliente
```bash
curl -X POST http://localhost:5000/api/asignaciones \
  -H "Content-Type: application/json" \
  -d '{
    "agente_id": 1,
    "cliente_id": 1
  }'
```

## 🏗️ Arquitectura y Modelos

### Agente
- id (Integer, PK)
- nombre (String, 150)
- correo (String, 100, unique)
- usuario (String, 50, unique)
- clave (String, 255)
- rol (Enum: super_admin, admin, agente)
- activo (Boolean, default=True)
- fecha_creacion (DateTime)

### Cliente
- id (Integer, PK)
- tipo_cliente (String: PERSONA o EMPRESA)
- **Campos comunes:**
  - ciudad, direccion, telefono_movil, correo, usuario, clave
- **Para PERSONA:**
  - tipo_documento, numero_documento, nombre, edad
- **Para EMPRESA:**
  - nit, razon_social, nombre_rep_legal, documento_rep_legal, telefono_rep_legal, correo_rep_legal, contacto_alternativo

### Relación Agente-Cliente
- agente_id (Integer, FK)
- cliente_id (Integer, FK)
- fecha_asignacion (DateTime)

## 🛠️ Solución de Problemas

### Error: No se puede conectar a MySQL
```bash
# 1. Verificar que Docker esté corriendo
docker ps

# 2. Verificar estado del contenedor MySQL
docker logs alfa_mysql

# 3. Reiniciar MySQL
bash scripts/reset_db.sh
```

### Error: Puerto 3306 ya está en uso
```bash
# Detener otros servicios MySQL
sudo service mysql stop

# O cambiar el puerto en docker-compose.yml
# ports:
#   - "3307:3306"  # Cambiar puerto externo
```

### Error: Permisos en scripts
```bash
# Hacer scripts ejecutables
chmod +x scripts/*.sh
```

## 🌟 Estado de la API

Para verificar que todo esté funcionando:

1. **MySQL:** `bash scripts/start_mysql.sh`
2. **API:** `python run_api.py`
3. **Health Check:** `curl http://localhost:5000/api/health`

**Respuesta esperada del health check:**
```json
{
  "status": "online",
  "message": "API está funcionando correctamente",
  "timestamp": "2024-01-01T12:00:00.000000",
  "version": "1.0.0"
}
``` 