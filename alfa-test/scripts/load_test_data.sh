#!/bin/bash

echo "📊 Cargando datos de prueba extendidos en MySQL..."

# Verificar si MySQL está corriendo
if ! docker exec alfa_mysql mysqladmin ping -h"localhost" --silent; then
    echo "❌ Error: MySQL no está corriendo. Ejecuta primero:"
    echo "   bash scripts/start_mysql.sh"
    exit 1
fi

echo "📋 Ejecutando archivo de datos de prueba..."
docker exec -i alfa_mysql mysql -u alfa_user -palfa_password alfa_db < database/test_data.sql

if [ $? -eq 0 ]; then
    echo "✅ Datos de prueba cargados exitosamente!"
    echo ""
    echo "📈 Estadísticas de la base de datos:"
    
    # Mostrar estadísticas
    docker exec alfa_mysql mysql -u alfa_user -palfa_password alfa_db -e "
    SELECT 'Agentes' as Tabla, COUNT(*) as Total FROM Agente
    UNION ALL
    SELECT 'Clientes', COUNT(*) FROM clientes
    UNION ALL
    SELECT 'Asignaciones', COUNT(*) FROM agentes_clientes;
    "
    
    echo ""
    echo "🎯 Distribución por roles:"
    docker exec alfa_mysql mysql -u alfa_user -palfa_password alfa_db -e "
    SELECT rol as Rol, COUNT(*) as Cantidad, 
           SUM(CASE WHEN activo = 1 THEN 1 ELSE 0 END) as Activos
    FROM Agente 
    GROUP BY rol;
    "
    
    echo ""
    echo "👥 Distribución de clientes:"
    docker exec alfa_mysql mysql -u alfa_user -palfa_password alfa_db -e "
    SELECT tipo_cliente as Tipo, COUNT(*) as Cantidad
    FROM clientes 
    GROUP BY tipo_cliente;
    "
    
else
    echo "❌ Error al cargar los datos de prueba"
    exit 1
fi 