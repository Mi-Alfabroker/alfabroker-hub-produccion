#!/bin/bash

echo "🔄 Reset completo de la base de datos con datos extendidos..."

# Verificar si Docker está corriendo
if ! docker info > /dev/null 2>&1; then
    echo "❌ Error: Docker no está corriendo. Por favor, inicia Docker Desktop."
    exit 1
fi

# Detener contenedor
echo "🛑 Deteniendo contenedor MySQL..."
docker-compose down

# Eliminar volúmenes (esto borra todos los datos)
echo "🗑️ Eliminando datos anteriores..."
docker-compose down -v

# Backup del archivo init.sql original
if [ -f "database/init.sql" ] && [ ! -f "database/init.sql.backup" ]; then
    echo "💾 Creando backup del init.sql original..."
    cp database/init.sql database/init.sql.backup
fi

# Usar el archivo de reset completo
echo "📝 Configurando datos extendidos..."
cp database/reset_with_extended_data.sql database/init.sql

# Volver a iniciar
echo "🚀 Reiniciando MySQL con datos extendidos..."
docker-compose up -d mysql

echo "⏳ Esperando a que MySQL esté listo..."
sleep 25

# Verificar conexión
echo "🔍 Verificando conexión a MySQL..."
until docker exec alfa_mysql mysqladmin ping -h"localhost" --silent; do
    echo "⏳ Esperando a MySQL..."
    sleep 2
done

# Mostrar estadísticas finales
echo "✅ Base de datos reseteada con datos extendidos!"
echo ""
echo "📈 Estadísticas finales:"

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
echo "💡 Para restaurar los datos originales:"
echo "   cp database/init.sql.backup database/init.sql"
echo "   bash scripts/reset_db.sh" 