# 🏠 Endpoint: Bienes de un Cliente

## 🎯 **Endpoint Principal**

```
GET /api/clientes/{cliente_id}/bienes
```

**Descripción:** Obtiene todos los bienes asignados a un cliente específico con detalles completos.

---

## 📋 **Parámetros**

### **Path Parameters:**
- `cliente_id` (integer, requerido): ID del cliente

### **Query Parameters:**
Ninguno

---

## 🚀 **Ejemplos de Uso**

### **1. Obtener bienes del cliente 1:**
```bash
curl -X GET "http://localhost:5000/api/clientes/1/bienes"
```

### **2. Con JavaScript/Fetch:**
```javascript
fetch('http://localhost:5000/api/clientes/1/bienes')
  .then(response => response.json())
  .then(data => console.log(data));
```

### **3. Con Python requests:**
```python
import requests

response = requests.get('http://localhost:5000/api/clientes/1/bienes')
bienes = response.json()
print(f"Cliente tiene {bienes['total']} bienes")
```

---

## 📊 **Respuesta Exitosa (200)**

```json
{
  "status": "success",
  "data": [
    {
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
        "valor_inmueble_avaluo": 350000000.0,
        "valor_contenidos_normales_avaluo": 25000000.0
      }
    },
    {
      "id": 2,
      "tipo_bien": "VEHICULO",
      "bien_especifico_id": 2,
      "estado": "Activo",
      "comentarios_generales": "Vehículo familiar",
      "vigencias_continuas": false,
      "fecha_creacion": "2024-01-12T09:15:00",
      "bien_especifico": {
        "id": 2,
        "tipo_vehiculo": "Automóvil",
        "placa": "ABC123",
        "marca": "Toyota",
        "serie_referencia": "Corolla Cross XLI",
        "ano_modelo": 2023,
        "codigo_fasecolda": "81042090",
        "valor_vehiculo": 85000000.0
      }
    },
    {
      "id": 3,
      "tipo_bien": "COPROPIEDAD",
      "bien_especifico_id": 3,
      "estado": "Activo",
      "comentarios_generales": "Apartamento en conjunto residencial",
      "vigencias_continuas": true,
      "fecha_creacion": "2024-01-10T16:45:00",
      "bien_especifico": {
        "id": 3,
        "tipo_copropiedad": "Conjunto Residencial",
        "ciudad": "Bogotá",
        "direccion": "Carrera 7 #127-45",
        "estrato": 4,
        "numero_torres": 3,
        "numero_maximo_pisos": 15,
        "cantidad_unidades_apartamentos": 180,
        "valor_edificio_area_comun_avaluo": 2500000000.0
      }
    }
  ],
  "total": 3
}
```

---

## ❌ **Respuestas de Error**

### **Cliente no encontrado (404):**
```json
{
  "status": "error",
  "message": "Cliente no encontrado"
}
```

### **Error interno (500):**
```json
{
  "status": "error",
  "message": "Error interno del servidor"
}
```

---

## 🔍 **Tipos de Bienes Incluidos**

### **1. HOGAR (Inmuebles residenciales):**
- `tipo_inmueble`: Casa, Apartamento, etc.
- `ciudad_inmueble`: Ciudad donde se ubica
- `direccion_inmueble`: Dirección completa
- `numero_pisos`: Cantidad de pisos
- `ano_construccion`: Año de construcción
- `valor_inmueble_avaluo`: Valor del inmueble
- `valor_contenidos_normales_avaluo`: Valor de contenidos

### **2. VEHICULO (Vehículos motorizados):**
- `tipo_vehiculo`: Automóvil, Motocicleta, etc.
- `placa`: Placa del vehículo
- `marca`: Marca del vehículo
- `serie_referencia`: Modelo/referencia
- `ano_modelo`: Año del modelo
- `codigo_fasecolda`: Código FASECOLDA
- `valor_vehiculo`: Valor comercial

### **3. COPROPIEDAD (Propiedades horizontales):**
- `tipo_copropiedad`: Conjunto Residencial, Edificio, etc.
- `ciudad`: Ciudad
- `direccion`: Dirección
- `estrato`: Estrato socioeconómico
- `numero_torres`: Cantidad de torres
- `numero_maximo_pisos`: Pisos máximos
- `cantidad_unidades_apartamentos`: Número de unidades
- `valor_edificio_area_comun_avaluo`: Valor áreas comunes

### **4. OTRO (Otros bienes asegurables):**
- `tipo_seguro`: Tipo de seguro
- `bien_asegurado`: Descripción del bien
- `valor_bien_asegurar`: Valor a asegurar
- `detalles_bien_asegurado`: Detalles adicionales

---

## 🔄 **Endpoints Relacionados**

### **Filtrar bienes por cliente (alternativo):**
```
GET /api/bienes?cliente_id={cliente_id}
```

### **Asignar bien existente a cliente:**
```
POST /api/bienes/{bien_id}/asignar
{
  "cliente_id": 1
}
```

### **Crear bien y asignarlo a cliente:**
```
POST /api/bienes
{
  "tipo_bien": "HOGAR",
  "data_especifico": {...},
  "data_general": {...},
  "cliente_id": 1
}
```

### **Desasignar bien de cliente:**
```
POST /api/bienes/{bien_id}/desasignar
{
  "cliente_id": 1
}
```

---

## 🧪 **Probar el Endpoint**

### **1. En Swagger UI:**
1. Ve a `http://localhost:5000/docs/`
2. Busca la sección **"Bienes"**
3. Encuentra `GET /api/clientes/{cliente_id}/bienes`
4. Haz clic en **"Try it out"**
5. Ingresa el `cliente_id` (ej: `1`)
6. Haz clic en **"Execute"**

### **2. Con script de prueba:**
```bash
python test_bienes_cliente.py
```

### **3. Con curl:**
```bash
# Bienes del cliente 1
curl -X GET "http://localhost:5000/api/clientes/1/bienes"

# Bienes del cliente 2
curl -X GET "http://localhost:5000/api/clientes/2/bienes"
```

---

## 📈 **Casos de Uso Comunes**

### **1. Dashboard de Cliente:**
Mostrar todos los bienes asegurados de un cliente en su dashboard personal.

### **2. Reporte de Portafolio:**
Generar reportes completos del portafolio de bienes de un cliente.

### **3. Cálculo de Primas:**
Obtener todos los bienes para calcular primas totales de seguros.

### **4. Renovación de Pólizas:**
Listar todos los bienes para procesos de renovación masiva.

### **5. Auditoría de Bienes:**
Revisar el inventario completo de bienes asegurados por cliente.

---

## 💡 **Notas Importantes**

- **Detalles completos:** El endpoint incluye tanto datos generales como específicos de cada bien
- **Campo `total`:** Indica la cantidad total de bienes del cliente
- **Datos específicos:** Cada tipo de bien incluye campos específicos según su naturaleza
- **Fechas:** Todas las fechas están en formato ISO 8601
- **Valores:** Los valores monetarios están en pesos colombianos (COP)

---

## 🎯 **Próximos Pasos**

Después de obtener los bienes de un cliente, puedes:

1. **Ver detalles específicos:** `GET /api/bienes/{bien_id}`
2. **Actualizar un bien:** `PUT /api/bienes/{bien_id}`
3. **Crear nuevo bien:** `POST /api/bienes`
4. **Gestionar asignaciones:** Usar endpoints de asignación

¡El endpoint está listo y completamente documentado! 🚀 