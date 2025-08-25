#!/bin/bash

echo "🚀 Iniciando MySQL 8.0 en Docker..."

# Verificar si Docker está corriendo
if ! docker info > /dev/null 2>&1; then
    echo "❌ Error: Docker no está corriendo. Por favor, inicia Docker Desktop."
    exit 1
fi

# Crear el directorio database si no existe
mkdir -p database

# Detener y remover contenedor anterior si existe
echo "🧹 Limpiando contenedores previos..."
docker-compose down

# Iniciar MySQL
echo "📦 Iniciando contenedor MySQL..."
docker-compose up -d mysql

echo "⏳ Esperando a que MySQL esté listo..."
sleep 15

# Verificar conexión
echo "🔍 Verificando conexión a MySQL..."
until docker exec alfa_mysql mysqladmin ping -h"localhost" --silent; do
    echo "⏳ Esperando a MySQL..."
    sleep 2
done

echo "✅ MySQL está listo y funcionando!"
echo "📊 Base de datos: alfa_db"
echo "👤 Usuario: alfa_user"
echo "🔐 Contraseña: alfa_password"
echo "🔌 Puerto: 3306"
echo ""
echo "🔧 Para conectarse desde un cliente MySQL:"
echo "   mysql -h localhost -P 3306 -u alfa_user -p alfa_db"
echo ""
echo "📝 Para ver los logs del contenedor:"
echo "   docker logs alfa_mysql" 