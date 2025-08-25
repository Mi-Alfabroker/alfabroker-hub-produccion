# 🗄️ Inicialización de Base de Datos con Datos Dummy

Este directorio contiene archivos para inicializar completamente la base de datos del sistema de seguros ALFA con datos dummy realistas para pruebas y desarrollo.

## 📁 Archivos Disponibles

### `init_with_dummy_data.sql`
Archivo SQL completo que contiene:
- **Estructura completa de la base de datos** (todas las tablas y relaciones)
- **Datos dummy realistas** para pruebas y desarrollo
- **Limpieza automática** de datos existentes antes de la inserción
- **Estadísticas finales** de los datos insertados

### `init_dummy_database.sh`
Script bash interactivo que:
- Verifica la conectividad con MySQL
- Ejecuta el archivo SQL de inicialización
- Muestra estadísticas de los datos insertados
- Proporciona ejemplos de consultas útiles

## 🎯 Datos Incluidos

| Tipo de Dato | Cantidad | Descripción |
|--------------|----------|-------------|
| **Agentes** | 15 | 1 super_admin, 4 admins, 10 agentes |
| **Clientes** | 27 | 15 personas naturales, 12 empresas |
| **Hogares** | 15 | Casas y apartamentos con avalúos |
| **Vehículos** | 15 | Automóviles, motos, camionetas |
| **Copropiedades** | 8 | Conjuntos, edificios, centros comerciales |
| **Otros Bienes** | 15 | Seguros especializados variados |
| **Bienes Totales** | 53 | Todos los tipos de bienes asegurables |
| **Asignaciones Agente-Cliente** | 65 | Relaciones realistas |
| **Asignaciones Cliente-Bien** | 75 | Clientes con múltiples bienes |

## 🚀 Métodos de Ejecución

### Método 1: Usando el Script Bash (Recomendado)

```bash
# Navegar al directorio database
cd database

# Dar permisos de ejecución (si es necesario)
chmod +x init_dummy_database.sh

# Ejecutar con configuración por defecto
./init_dummy_database.sh

# Ejecutar con configuración personalizada
./init_dummy_database.sh -u mi_usuario -p mi_password -h localhost
```

### Método 2: Ejecución Manual con MySQL

```bash
# Opción 1: Desde línea de comandos
mysql -u root -p < init_with_dummy_data.sql

# Opción 2: Desde cliente MySQL
mysql -u root -p
mysql> source init_with_dummy_data.sql;
```

### Método 3: Usando Docker (si aplica)

```bash
# Si tienes MySQL en Docker
docker exec -i mysql_container mysql -u root -p < init_with_dummy_data.sql
```

## ⚙️ Configuración

### Requisitos Previos
- MySQL 5.7+ o MariaDB 10.3+
- Usuario con permisos para crear/eliminar bases de datos
- Acceso a la línea de comandos

### Configuración por Defecto
```bash
DB_NAME="alfa_db"
DB_USER="root"
DB_PASSWORD="root"
DB_HOST="localhost"
DB_PORT="3306"
```

### Personalización
Puedes modificar la configuración usando argumentos:

```bash
./init_dummy_database.sh --help
```

## 🔍 Ejemplos de Consultas

Una vez ejecutado el script, puedes probar estas consultas:

### Consultar Agentes
```sql
SELECT id, nombre, rol, activo FROM Agente;
```

### Ver Clientes con sus Agentes
```sql
SELECT c.nombre, c.tipo_cliente, a.nombre as agente
FROM clientes c
JOIN agentes_clientes ac ON c.id = ac.cliente_id
JOIN Agente a ON ac.agente_id = a.id;
```

### Estadísticas de Bienes
```sql
SELECT tipo_bien, COUNT(*) as cantidad 
FROM bienes 
GROUP BY tipo_bien;
```

### Clientes con sus Bienes
```sql
SELECT c.nombre, b.tipo_bien, b.comentarios_generales
FROM clientes c
JOIN clientes_bienes cb ON c.id = cb.cliente_id
JOIN bienes b ON cb.bien_id = b.id
LIMIT 10;
```

### Hogares con Avalúos
```sql
SELECT h.tipo_inmueble, h.ciudad_inmueble, h.valor_inmueble_avaluo
FROM hogares h
ORDER BY h.valor_inmueble_avaluo DESC;
```

### Vehículos por Marca
```sql
SELECT v.marca, COUNT(*) as cantidad, AVG(v.valor_vehiculo) as valor_promedio
FROM vehiculos v
GROUP BY v.marca;
```

## 📊 Casos de Uso

### Para Desarrollo
- Pruebas de endpoints de la API
- Desarrollo de funcionalidades
- Validación de relaciones entre entidades

### Para Testing
- Pruebas unitarias e integración
- Verificación de consultas complejas
- Validación de reglas de negocio

### Para Demos
- Presentaciones del sistema
- Capacitaciones
- Documentación de funcionalidades

## 🔧 Personalización

### Modificar Datos
1. Edita el archivo `init_with_dummy_data.sql`
2. Agrega o modifica los INSERT statements
3. Ejecuta el script nuevamente

### Agregar Nuevos Datos
```sql
-- Ejemplo: Agregar más agentes
INSERT INTO Agente (nombre, correo, usuario, clave, rol, activo) VALUES
('Nuevo Agente', 'nuevo@empresa.com', 'nuevo.agente', 'password123', 'agente', TRUE);
```

## ⚠️ Importante

- **Este script ELIMINA todos los datos existentes** antes de insertar los nuevos
- **Úsalo solo en entornos de desarrollo/testing**
- **NO ejecutes en producción** sin un respaldo completo
- **Verifica las credenciales** antes de ejecutar

## 🆘 Solución de Problemas

### Error de Conexión
```bash
# Verificar que MySQL esté corriendo
systemctl status mysql

# Verificar credenciales
mysql -u root -p -e "SELECT 1;"
```

### Error de Permisos
```bash
# Dar permisos al script
chmod +x init_dummy_database.sh

# Verificar permisos de usuario MySQL
GRANT ALL PRIVILEGES ON *.* TO 'root'@'localhost';
FLUSH PRIVILEGES;
```

### Error de Archivo No Encontrado
```bash
# Verificar que estás en el directorio correcto
ls -la init_with_dummy_data.sql

# Navegar al directorio database
cd database
```

## 📝 Logs y Depuración

El script bash proporciona output colorido para facilitar la depuración:
- 🔵 **INFO**: Mensajes informativos
- 🟢 **SUCCESS**: Operaciones exitosas
- 🟡 **WARNING**: Advertencias importantes
- 🔴 **ERROR**: Errores que requieren atención

## 🤝 Contribuir

Para agregar más datos dummy o mejorar el script:

1. Modifica los archivos correspondientes
2. Prueba los cambios en un entorno local
3. Documenta los cambios realizados
4. Actualiza este README si es necesario

---

## 📞 Soporte

Si tienes problemas con la inicialización:
1. Verifica los requisitos previos
2. Revisa la configuración de MySQL
3. Consulta la sección de solución de problemas
4. Revisa los logs del script bash

¡La base de datos está lista para ser inicializada! 🎉 