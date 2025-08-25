#!/bin/bash

# Script para probar la configuración de Nginx

echo "🔍 Verificando configuración de Nginx..."

# Probar configuración con contenedor temporal
docker run --rm -v "$(pwd)/nginx.conf:/etc/nginx/nginx.conf:ro" nginx:alpine nginx -t

if [ $? -eq 0 ]; then
    echo "✅ Configuración de Nginx válida"
    echo "🔄 Reiniciando contenedor frontend..."
    docker-compose restart alfa-frontend
    echo "✅ Frontend reiniciado"
else
    echo "❌ Error en configuración de Nginx"
    exit 1
fi
