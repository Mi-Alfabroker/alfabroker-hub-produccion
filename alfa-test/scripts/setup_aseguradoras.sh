#!/bin/bash

# Script para configurar el módulo de aseguradoras

echo "=====> Configurando módulo de aseguradoras..."

# Verificar que MySQL esté corriendo
if ! mysql -u alfa_user -palfa_password -e "SELECT 1" > /dev/null 2>&1; then
    echo "=====> Error: MySQL no está corriendo o no se puede conectar"
    echo "=====> Iniciando MySQL..."
    bash scripts/start_mysql.sh
    sleep 3
fi

# Verificar conexión nuevamente
if ! mysql -u alfa_user -palfa_password -e "SELECT 1" > /dev/null 2>&1; then
    echo "=====> Error: No se pudo conectar a MySQL"
    echo "=====> Asegúrate de que MySQL esté corriendo correctamente"
    exit 1
fi

echo "=====> Conexión a MySQL exitosa"

# Ejecutar migraciones del módulo de aseguradoras
echo "=====> Ejecutando migraciones del módulo de aseguradoras..."
mysql -u alfa_user -palfa_password alfa_db < database/aseguradoras_module.sql

if [ $? -eq 0 ]; then
    echo "=====> Migraciones ejecutadas exitosamente"
else
    echo "=====> Error al ejecutar las migraciones"
    exit 1
fi

echo "=====> Verificando tablas creadas..."
mysql -u alfa_user -palfa_password alfa_db -e "
SELECT TABLE_NAME 
FROM information_schema.TABLES 
WHERE TABLE_SCHEMA = 'alfa_db' 
AND TABLE_NAME LIKE '%aseguradora%' 
OR TABLE_NAME LIKE '%opcion%' 
OR TABLE_NAME LIKE '%poliza%';
"

echo "=====> Módulo de aseguradoras configurado exitosamente"
echo "=====> Tablas disponibles para el módulo de seguros:"
echo "   - Aseguradoras y sus configuraciones"
echo "   - Opciones de seguro (cotizaciones)"
echo "   - Pólizas y planes de pago"
echo ""
echo "=====> Para probar la API, ejecuta:"
echo "   python run_api.py"
echo ""
echo "=====> Documentación disponible en:"
echo "   http://localhost:5000/docs/" 