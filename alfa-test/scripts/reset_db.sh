#!/bin/bash

echo "🔄 Reseteando base de datos MySQL..."

# Detener contenedor
echo "🛑 Deteniendo contenedor MySQL..."
docker-compose down

# Eliminar volúmenes (esto borra todos los datos)
echo "🗑️ Eliminando datos anteriores..."
docker-compose down -v

# Volver a iniciar
echo "🚀 Reiniciando MySQL con datos frescos..."
docker-compose up -d mysql

echo "⏳ Esperando a que MySQL esté listo..."
sleep 20

# Verificar conexión
echo "🔍 Verificando conexión a MySQL..."
until docker exec alfa_mysql mysqladmin ping -h"localhost" --silent; do
    echo "⏳ Esperando a MySQL..."
    sleep 2
done

echo "✅ Base de datos reseteada y lista!"
echo "📊 La base de datos se ha inicializado con datos de prueba" 