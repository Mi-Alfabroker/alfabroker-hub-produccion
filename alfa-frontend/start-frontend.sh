#!/bin/bash

echo "🚀 Iniciando aplicación Angular Frontend..."

# Verificar que existe el build
if [ ! -d "dist/alfa-frontend" ]; then
    echo "❌ Error: No se encontró el directorio dist/alfa-frontend"
    echo "💡 Ejecuta 'npm run build' primero para generar el build"
    exit 1
fi

# Preguntar qué tipo de servidor usar
echo "Selecciona el tipo de servidor:"
echo "1) Nginx (recomendado para producción)"
echo "2) Node.js con SSR"
read -p "Ingresa tu opción (1 o 2): " opcion

case $opcion in
    1)
        echo "🔧 Iniciando con Nginx..."
        docker-compose -f frontend.yml up -d
        echo "✅ Frontend disponible en: http://localhost:4200"
        echo "🔗 API disponible en: http://localhost:5000"
        ;;
    2)
        echo "🔧 Iniciando con Node.js SSR..."
        docker-compose -f frontend-ssr.yml up -d
        echo "✅ Frontend SSR disponible en: http://localhost:4200"
        echo "🔗 API disponible en: http://localhost:5000"
        ;;
    *)
        echo "❌ Opción inválida"
        exit 1
        ;;
esac

echo ""
echo "📋 Comandos útiles:"
echo "  - Ver logs: docker-compose -f frontend.yml logs -f"
echo "  - Detener: docker-compose -f frontend.yml down"
echo "  - Reiniciar: docker-compose -f frontend.yml restart"
