# 🏠 Guía Completa: Crear Bienes Asegurables

## 🎯 **Endpoint para Crear Bienes**

```
POST /api/bienes
```

**Descripción:** Crea un nuevo bien asegurable de cualquier tipo y opcionalmente lo asigna a un cliente.

---

## 📋 **Parámetros Requeridos**

### **Campos Obligatorios:**
- `tipo_bien` (string): Tipo de bien - **HOGAR**, **VEHICULO**, **COPROPIEDAD** o **OTRO**
- `data_especifico` (object): Datos específicos según el tipo de bien

### **Campos Opcionales:**
- `data_general` (object): Datos generales del bien
- `cliente_id` (integer): ID del cliente para asignación automática

---

## 🏠 **1. HOGAR (Inmuebles Residenciales)**

### **Campos Requeridos:**
- `tipo_inmueble` (string): Casa, Apartamento, etc.

### **Campos Opcionales:**
- `ciudad_inmueble`, `direccion_inmueble`, `numero_pisos`, `ano_construccion`
- `valor_inmueble_avaluo`, `valor_contenidos_normales_avaluo`

### **Ejemplo - Casa:**
```json
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

### **Ejemplo - Apartamento:**
```json
{
  "tipo_bien": "HOGAR",
  "data_especifico": {
    "tipo_inmueble": "Apartamento",
    "ciudad_inmueble": "Medellín",
    "direccion_inmueble": "Calle 50 #20-30, Apto 501",
    "numero_pisos": 1,
    "ano_construccion": 2020,
    "valor_inmueble_avaluo": 250000000.00,
    "valor_contenidos_normales_avaluo": 15000000.00
  },
  "data_general": {
    "estado": "Activo",
    "comentarios_generales": "Apartamento moderno en zona residencial"
  }
}
```

---

## 🚗 **2. VEHICULO (Vehículos Motorizados)**

### **Campos Requeridos:**
- `placa` (string): Placa del vehículo (debe ser única)

### **Campos Opcionales:**
- `tipo_vehiculo`, `marca`, `serie_referencia`, `ano_modelo`
- `codigo_fasecolda`, `valor_vehiculo`

### **Ejemplo - Automóvil:**
```json
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
    "comentarios_generales": "Vehículo familiar principal"
  },
  "cliente_id": 1
}
```

### **Ejemplo - Motocicleta:**
```json
{
  "tipo_bien": "VEHICULO",
  "data_especifico": {
    "tipo_vehiculo": "Motocicleta",
    "placa": "MOTO123",
    "marca": "Honda",
    "serie_referencia": "CBR 600RR",
    "ano_modelo": 2022,
    "codigo_fasecolda": "12345678",
    "valor_vehiculo": 35000000.00
  },
  "data_general": {
    "estado": "Activo",
    "comentarios_generales": "Motocicleta deportiva"
  }
}
```

### **Ejemplo - Camión:**
```json
{
  "tipo_bien": "VEHICULO",
  "data_especifico": {
    "tipo_vehiculo": "Camión",
    "placa": "CAM456",
    "marca": "Chevrolet",
    "serie_referencia": "NPR 4.5 Ton",
    "ano_modelo": 2021,
    "codigo_fasecolda": "87654321",
    "valor_vehiculo": 120000000.00
  },
  "data_general": {
    "estado": "Activo",
    "comentarios_generales": "Camión para transporte de carga"
  }
}
```

---

## 🏢 **3. COPROPIEDAD (Propiedades Horizontales)**

### **Campos Requeridos:**
- `tipo_copropiedad` (string): Conjunto Residencial, Edificio, etc.

### **Campos Opcionales:**
- `ciudad`, `direccion`, `estrato`, `numero_torres`
- `numero_maximo_pisos`, `cantidad_unidades_apartamentos`
- `valor_edificio_area_comun_avaluo`

### **Ejemplo - Conjunto Residencial:**
```json
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
    "estado": "Activo",
    "comentarios_generales": "Conjunto residencial moderno con amenidades"
  }
}
```

### **Ejemplo - Edificio de Oficinas:**
```json
{
  "tipo_bien": "COPROPIEDAD",
  "data_especifico": {
    "tipo_copropiedad": "Edificio de Oficinas",
    "ciudad": "Medellín",
    "direccion": "Carrera 43A #1-50",
    "estrato": 6,
    "numero_torres": 1,
    "numero_maximo_pisos": 25,
    "cantidad_unidades_apartamentos": 200,
    "valor_edificio_area_comun_avaluo": 5000000000.00
  },
  "data_general": {
    "estado": "Activo",
    "comentarios_generales": "Torre empresarial en el centro financiero"
  }
}
```

---

## 📦 **4. OTRO (Otros Bienes Asegurables)**

### **Campos Requeridos:**
- `bien_asegurado` (string): Descripción del bien asegurado

### **Campos Opcionales:**
- `tipo_seguro`, `valor_bien_asegurar`, `detalles_bien_asegurado`

### **Ejemplo - Seguro de Transporte:**
```json
{
  "tipo_bien": "OTRO",
  "data_especifico": {
    "tipo_seguro": "Seguro de Transporte",
    "bien_asegurado": "Mercancías en Tránsito",
    "valor_bien_asegurar": 500000000.00,
    "detalles_bien_asegurado": "Cobertura para mercancías transportadas vía terrestre"
  },
  "data_general": {
    "estado": "Activo",
    "comentarios_generales": "Póliza de transporte internacional"
  }
}
```

### **Ejemplo - Seguro de Equipo:**
```json
{
  "tipo_bien": "OTRO",
  "data_especifico": {
    "tipo_seguro": "Seguro de Equipo Electrónico",
    "bien_asegurado": "Servidores y Equipos de Cómputo",
    "valor_bien_asegurar": 200000000.00,
    "detalles_bien_asegurado": "Cobertura para centro de datos empresarial"
  },
  "data_general": {
    "estado": "Activo",
    "comentarios_generales": "Equipos críticos para operación"
  }
}
```

### **Ejemplo - Seguro de Maquinaria:**
```json
{
  "tipo_bien": "OTRO",
  "data_especifico": {
    "tipo_seguro": "Seguro de Maquinaria Industrial",
    "bien_asegurado": "Equipos de Manufactura",
    "valor_bien_asegurar": 800000000.00,
    "detalles_bien_asegurado": "Línea de producción automatizada"
  },
  "data_general": {
    "estado": "Activo",
    "comentarios_generales": "Maquinaria especializada importada"
  }
}
```

---

## 🚀 **Cómo Usar el Endpoint**

### **1. Con curl:**
```bash
curl -X POST "http://localhost:5000/api/bienes" \
  -H "Content-Type: application/json" \
  -d '{
    "tipo_bien": "HOGAR",
    "data_especifico": {
      "tipo_inmueble": "Casa",
      "ciudad_inmueble": "Bogotá",
      "direccion_inmueble": "Carrera 15 #45-23",
      "valor_inmueble_avaluo": 350000000.00
    },
    "data_general": {
      "estado": "Activo",
      "comentarios_generales": "Casa principal"
    },
    "cliente_id": 1
  }'
```

### **2. En Swagger UI:**
1. Ve a `http://localhost:5000/docs/`
2. Busca la sección **"Bienes"**
3. Encuentra `POST /api/bienes`
4. Haz clic en **"Try it out"**
5. Copia uno de los ejemplos JSON
6. Haz clic en **"Execute"**

### **3. Con JavaScript:**
```javascript
const bienData = {
  tipo_bien: "VEHICULO",
  data_especifico: {
    tipo_vehiculo: "Automóvil",
    placa: "ABC123",
    marca: "Toyota",
    valor_vehiculo: 85000000.00
  },
  data_general: {
    estado: "Activo",
    comentarios_generales: "Vehículo familiar"
  },
  cliente_id: 1
};

fetch('http://localhost:5000/api/bienes', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify(bienData)
})
.then(response => response.json())
.then(data => console.log(data));
```

### **4. Con Python:**
```python
import requests

bien_data = {
    "tipo_bien": "HOGAR",
    "data_especifico": {
        "tipo_inmueble": "Casa",
        "ciudad_inmueble": "Bogotá",
        "valor_inmueble_avaluo": 350000000.00
    },
    "data_general": {
        "estado": "Activo"
    },
    "cliente_id": 1
}

response = requests.post(
    'http://localhost:5000/api/bienes',
    json=bien_data
)

print(response.json())
```

---

## ✅ **Respuesta Exitosa (201)**

```json
{
  "status": "success",
  "message": "Bien creado exitosamente",
  "data": {
    "id": 15,
    "tipo_bien": "HOGAR",
    "bien_especifico_id": 8,
    "estado": "Activo",
    "comentarios_generales": "Casa principal de familia",
    "vigencias_continuas": true,
    "fecha_creacion": "2024-01-15T10:30:00",
    "bien_especifico": {
      "id": 8,
      "tipo_inmueble": "Casa",
      "ciudad_inmueble": "Bogotá",
      "direccion_inmueble": "Carrera 15 #45-23",
      "numero_pisos": 2,
      "ano_construccion": 2015,
      "valor_inmueble_avaluo": 350000000.0,
      "valor_contenidos_normales_avaluo": 25000000.0
    }
  }
}
```

---

## ❌ **Respuestas de Error**

### **Campo requerido faltante (400):**
```json
{
  "status": "error",
  "message": "tipo_bien es requerido"
}
```

### **Tipo de bien inválido (400):**
```json
{
  "status": "error",
  "message": "tipo_bien debe ser HOGAR, VEHICULO, COPROPIEDAD o OTRO"
}
```

### **Campo específico faltante (400):**
```json
{
  "status": "error",
  "message": "placa es requerida para vehículos"
}
```

---

## 🧪 **Probar el Endpoint**

### **Script de prueba completo:**
```bash
python test_crear_bienes.py
```

Este script prueba:
- ✅ Creación de todos los tipos de bienes
- ✅ Asignación automática a cliente
- ✅ Validaciones de campos requeridos
- ✅ Validaciones específicas por tipo
- ✅ Verificación de bienes creados

---

## 🔄 **Flujo Completo de Trabajo**

### **1. Crear bien básico:**
```bash
POST /api/bienes
```

### **2. Verificar creación:**
```bash
GET /api/bienes/{bien_id}
```

### **3. Asignar a cliente (si no se hizo automáticamente):**
```bash
POST /api/bienes/{bien_id}/asignar
{
  "cliente_id": 1
}
```

### **4. Verificar asignación:**
```bash
GET /api/clientes/{cliente_id}/bienes
```

---

## 💡 **Consejos y Mejores Prácticas**

### **1. Validaciones:**
- **HOGAR:** Siempre incluir `tipo_inmueble`
- **VEHICULO:** Asegurar que la `placa` sea única
- **COPROPIEDAD:** Incluir `tipo_copropiedad`
- **OTRO:** Describir claramente el `bien_asegurado`

### **2. Asignación a Cliente:**
- Incluir `cliente_id` para asignación automática
- O usar el endpoint de asignación posterior

### **3. Datos Monetarios:**
- Usar valores en pesos colombianos (COP)
- Incluir decimales para mayor precisión

### **4. Estados:**
- Usar estados consistentes: "Activo", "Inactivo", "Suspendido"

---

## 📊 **Casos de Uso Comunes**

### **1. Casa Familiar:**
```json
{
  "tipo_bien": "HOGAR",
  "data_especifico": {
    "tipo_inmueble": "Casa",
    "ciudad_inmueble": "Bogotá",
    "direccion_inmueble": "Calle 100 #15-20",
    "numero_pisos": 2,
    "ano_construccion": 2010,
    "valor_inmueble_avaluo": 400000000.00
  },
  "cliente_id": 1
}
```

### **2. Vehículo Empresa:**
```json
{
  "tipo_bien": "VEHICULO",
  "data_especifico": {
    "tipo_vehiculo": "Camioneta",
    "placa": "EMP001",
    "marca": "Ford",
    "serie_referencia": "F-150",
    "ano_modelo": 2023,
    "valor_vehiculo": 150000000.00
  },
  "cliente_id": 5
}
```

### **3. Conjunto Residencial:**
```json
{
  "tipo_bien": "COPROPIEDAD",
  "data_especifico": {
    "tipo_copropiedad": "Conjunto Residencial",
    "ciudad": "Bogotá",
    "estrato": 5,
    "cantidad_unidades_apartamentos": 120,
    "valor_edificio_area_comun_avaluo": 3000000000.00
  }
}
```

¡El endpoint está listo y completamente documentado! 🚀

---

## 🎯 **Próximos Pasos**

Después de crear un bien, puedes:

1. **Actualizarlo:** `PUT /api/bienes/{bien_id}`
2. **Asignarlo:** `POST /api/bienes/{bien_id}/asignar`
3. **Ver sus detalles:** `GET /api/bienes/{bien_id}`
4. **Listarlo por cliente:** `GET /api/clientes/{cliente_id}/bienes` 