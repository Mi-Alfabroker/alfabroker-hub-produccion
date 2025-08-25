#!/bin/bash

echo "🛑 Deteniendo MySQL en Docker..."

# Detener el contenedor
docker-compose down

echo "✅ MySQL detenido correctamente"
echo ""
echo "💡 Para eliminar también los datos (CUIDADO - se perderán todos los datos):"
echo "   docker-compose down -v" 