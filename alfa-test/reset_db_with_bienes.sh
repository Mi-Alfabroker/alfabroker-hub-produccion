#!/bin/bash

echo "🔄 Reseteando base de datos con nuevas tablas de bienes..."

# Parar contenedores si están corriendo
docker-compose down

# Eliminar volumen de datos para empezar limpio
docker volume rm alfa-test_mysql_data 2>/dev/null || true

# Iniciar MySQL
docker-compose up -d mysql

# Esperar a que MySQL esté listo
echo "⏳ Esperando a que MySQL esté disponible..."
sleep 10

# Verificar conexión a MySQL
echo "🔍 Verificando conexión a MySQL..."
max_attempts=30
attempt=1

while [ $attempt -le $max_attempts ]; do
    if docker exec alfa-test-mysql-1 mysql -u root -prootpassword -e "SELECT 1;" >/dev/null 2>&1; then
        echo "✅ MySQL está disponible!"
        break
    else
        echo "⏳ Intento $attempt/$max_attempts - Esperando MySQL..."
        sleep 2
        ((attempt++))
    fi
done

if [ $attempt -gt $max_attempts ]; then
    echo "❌ Error: MySQL no está disponible después de $max_attempts intentos"
    exit 1
fi

# Crear base de datos y aplicar esquema
echo "📊 Creando base de datos y aplicando esquema..."
docker exec -i alfa-test-mysql-1 mysql -u root -prootpassword << 'EOF'
DROP DATABASE IF EXISTS davivienda_seguros;
CREATE DATABASE davivienda_seguros;
USE davivienda_seguros;
EOF

# Aplicar esquema base
echo "🏗️ Aplicando esquema de base de datos..."
docker exec -i alfa-test-mysql-1 mysql -u root -prootpassword davivienda_seguros < database/init.sql

# Cargar datos de ejemplo para bienes
echo "📋 Cargando datos de ejemplo para bienes..."
docker exec -i alfa-test-mysql-1 mysql -u root -prootpassword davivienda_seguros < database/datos_bienes_ejemplo.sql

echo "✅ Base de datos reseteada exitosamente con nuevas tablas de bienes!"
echo ""
echo "📈 Resumen de datos:"
echo "   • Agentes: 13 (1 super_admin, 4 admins, 8 agentes)"
echo "   • Clientes: 24 (12 personas, 12 empresas)" 
echo "   • Asignaciones agente-cliente: 35+"
echo "   • Bienes totales: 18 (5 hogares, 5 vehículos, 3 copropiedades, 5 otros)"
echo "   • Asignaciones cliente-bien: 16+"
echo ""
echo "🚀 La API está lista para probar con bienes asegurables!"
echo "   Ejecuta: python run_api.py" 