#!/bin/bash

# 🚀 Script de Despliegue Automatizado - Alfa App
# Autor: Sistema de Despliegue Alfa
# Versión: 1.0

set -e  # Salir si hay algún error

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para logging
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

warn() {
    echo -e "${YELLOW}[$(date +'%Y-%m-%d %H:%M:%S')] WARNING: $1${NC}"
}

error() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ERROR: $1${NC}"
    exit 1
}

info() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')] INFO: $1${NC}"
}

# Banner
echo -e "${BLUE}"
cat << "EOF"
 █████╗ ██╗     ███████╗ █████╗     ██████╗ ███████╗██████╗ ██╗      ██████╗ ██╗   ██╗
██╔══██╗██║     ██╔════╝██╔══██╗    ██╔══██╗██╔════╝██╔══██╗██║     ██╔═══██╗╚██╗ ██╔╝
███████║██║     █████╗  ███████║    ██║  ██║█████╗  ██████╔╝██║     ██║   ██║ ╚████╔╝ 
██╔══██║██║     ██╔══╝  ██╔══██║    ██║  ██║██╔══╝  ██╔═══╝ ██║     ██║   ██║  ╚██╔╝  
██║  ██║███████╗██║     ██║  ██║    ██████╔╝███████╗██║     ███████╗╚██████╔╝   ██║   
╚═╝  ╚═╝╚══════╝╚═╝     ╚═╝  ╚═╝    ╚═════╝ ╚══════╝╚═╝     ╚══════╝ ╚═════╝    ╚═╝   
EOF
echo -e "${NC}"

log "🚀 Iniciando despliegue de Alfa App..."

# Verificar que estamos en el directorio correcto
if [ ! -f "docker-compose.yml" ]; then
    error "No se encontró docker-compose.yml. Ejecuta este script desde el directorio raíz del proyecto."
fi

# Verificar dependencias
log "🔍 Verificando dependencias..."

# Verificar Docker
if ! command -v docker &> /dev/null; then
    error "Docker no está instalado. Por favor instala Docker primero."
fi

# Verificar Docker Compose
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    error "Docker Compose no está instalado. Por favor instala Docker Compose primero."
fi

# Usar docker compose o docker-compose según disponibilidad
DOCKER_COMPOSE_CMD="docker-compose"
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
fi

log "✅ Docker y Docker Compose están disponibles"

# Verificar archivo .env
if [ ! -f ".env" ]; then
    warn "No se encontró archivo .env, creando uno por defecto..."
    cp .env.example .env 2>/dev/null || {
        error "No se pudo crear .env. Crea el archivo manualmente."
    }
fi

# Función para generar contraseña segura
generate_password() {
    openssl rand -base64 32 | tr -d "=+/" | cut -c1-25
}

# Configurar contraseñas si no existen
log "🔐 Configurando credenciales de seguridad..."

# Generar contraseña para Portainer si no existe
if [ ! -f "portainer_password.txt" ]; then
    PORTAINER_PASS=$(generate_password)
    echo -n "$PORTAINER_PASS" | htpasswd -niB admin | cut -d ":" -f 2 > portainer_password.txt
    log "✅ Contraseña de Portainer generada: $PORTAINER_PASS"
    log "📝 Guarda esta contraseña en un lugar seguro"
fi

# Crear directorio SSL si no existe
if [ ! -d "ssl" ]; then
    log "🔒 Creando certificados SSL autofirmados..."
    mkdir -p ssl
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
        -keyout ssl/key.pem \
        -out ssl/cert.pem \
        -subj "/C=CO/ST=State/L=City/O=Organization/CN=localhost"
    log "✅ Certificados SSL creados (autofirmados para desarrollo)"
fi

# Verificar build del frontend
log "🏗️ Verificando build del frontend..."
if [ ! -d "alfa-frontend/dist/alfa-frontend/browser" ]; then
    warn "No se encontró el build del frontend. Construyendo..."
    cd alfa-frontend
    if [ ! -d "node_modules" ]; then
        log "📦 Instalando dependencias de Node.js..."
        npm install
    fi
    log "🔨 Construyendo aplicación Angular..."
    npm run build
    cd ..
    log "✅ Build del frontend completado"
else
    log "✅ Build del frontend encontrado"
fi

# Función para mostrar menú de opciones
show_menu() {
    echo ""
    echo -e "${BLUE}Selecciona una opción:${NC}"
    echo "1) 🚀 Despliegue completo (recomendado)"
    echo "2) 🔄 Actualizar servicios existentes"
    echo "3) 🛑 Detener todos los servicios"
    echo "4) 🗑️  Limpiar y reiniciar (elimina datos)"
    echo "5) 📊 Ver estado de servicios"
    echo "6) 📋 Ver logs"
    echo "7) 🔧 Configuración avanzada"
    echo "8) ❌ Salir"
    echo ""
}

# Función de despliegue completo
deploy_full() {
    log "🚀 Iniciando despliegue completo..."
    
    # Detener servicios existentes
    log "🛑 Deteniendo servicios existentes..."
    $DOCKER_COMPOSE_CMD down --remove-orphans
    
    # Limpiar imágenes huérfanas
    log "🧹 Limpiando imágenes no utilizadas..."
    docker image prune -f
    
    # Construir y levantar servicios
    log "🏗️ Construyendo y levantando servicios..."
    $DOCKER_COMPOSE_CMD up -d --build
    
    # Esperar a que los servicios estén listos
    log "⏳ Esperando a que los servicios estén listos..."
    sleep 30
    
    # Verificar estado de servicios
    check_services
}

# Función para verificar servicios
check_services() {
    log "🔍 Verificando estado de servicios..."
    
    services=("mysql" "alfa-api" "alfa-frontend" "portainer")
    
    for service in "${services[@]}"; do
        if $DOCKER_COMPOSE_CMD ps | grep -q "$service.*Up"; then
            log "✅ $service está ejecutándose"
        else
            warn "❌ $service no está ejecutándose correctamente"
        fi
    done
    
    echo ""
    log "🌐 URLs de acceso:"
    log "   Frontend: https://localhost (HTTP redirige a HTTPS)"
    log "   API: http://localhost:5000"
    log "   Portainer: https://localhost:9443"
    log "   Base de datos: localhost:3306"
    echo ""
}

# Función para actualizar servicios
update_services() {
    log "🔄 Actualizando servicios..."
    $DOCKER_COMPOSE_CMD pull
    $DOCKER_COMPOSE_CMD up -d --build
    log "✅ Servicios actualizados"
}

# Función para limpiar y reiniciar
clean_restart() {
    warn "⚠️  Esta acción eliminará todos los datos. ¿Continuar? (y/N)"
    read -r response
    if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        log "🗑️ Eliminando todos los contenedores y volúmenes..."
        $DOCKER_COMPOSE_CMD down -v --remove-orphans
        docker system prune -f
        deploy_full
    else
        log "❌ Operación cancelada"
    fi
}

# Función para ver logs
view_logs() {
    echo "Selecciona el servicio para ver logs:"
    echo "1) Todos los servicios"
    echo "2) Frontend (nginx)"
    echo "3) API (backend)"
    echo "4) Base de datos"
    echo "5) Portainer"
    read -r log_choice
    
    case $log_choice in
        1) $DOCKER_COMPOSE_CMD logs -f ;;
        2) $DOCKER_COMPOSE_CMD logs -f alfa-frontend ;;
        3) $DOCKER_COMPOSE_CMD logs -f alfa-api ;;
        4) $DOCKER_COMPOSE_CMD logs -f mysql ;;
        5) $DOCKER_COMPOSE_CMD logs -f portainer ;;
        *) error "Opción inválida" ;;
    esac
}

# Función de configuración avanzada
advanced_config() {
    echo "🔧 Configuración Avanzada:"
    echo "1) Regenerar certificados SSL"
    echo "2) Cambiar contraseñas"
    echo "3) Backup de base de datos"
    echo "4) Restaurar backup"
    echo "5) Volver al menú principal"
    read -r config_choice
    
    case $config_choice in
        1)
            log "🔒 Regenerando certificados SSL..."
            rm -rf ssl
            mkdir -p ssl
            openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
                -keyout ssl/key.pem \
                -out ssl/cert.pem \
                -subj "/C=CO/ST=State/L=City/O=Organization/CN=localhost"
            log "✅ Certificados SSL regenerados"
            ;;
        2)
            log "🔐 Regenerando contraseñas..."
            rm -f portainer_password.txt
            PORTAINER_PASS=$(generate_password)
            echo -n "$PORTAINER_PASS" | htpasswd -niB admin | cut -d ":" -f 2 > portainer_password.txt
            log "✅ Nueva contraseña de Portainer: $PORTAINER_PASS"
            ;;
        3)
            log "💾 Creando backup de base de datos..."
            docker exec alfa_mysql mysqldump -u root -p${MYSQL_ROOT_PASSWORD} alfa_db > backup_$(date +%Y%m%d_%H%M%S).sql
            log "✅ Backup creado"
            ;;
        4)
            echo "Ingresa el nombre del archivo de backup:"
            read -r backup_file
            if [ -f "$backup_file" ]; then
                log "📥 Restaurando backup..."
                docker exec -i alfa_mysql mysql -u root -p${MYSQL_ROOT_PASSWORD} alfa_db < "$backup_file"
                log "✅ Backup restaurado"
            else
                error "Archivo de backup no encontrado"
            fi
            ;;
        5) return ;;
        *) error "Opción inválida" ;;
    esac
}

# Menú principal
while true; do
    show_menu
    read -r choice
    
    case $choice in
        1) deploy_full ;;
        2) update_services ;;
        3) 
            log "🛑 Deteniendo servicios..."
            $DOCKER_COMPOSE_CMD down
            log "✅ Servicios detenidos"
            ;;
        4) clean_restart ;;
        5) 
            $DOCKER_COMPOSE_CMD ps
            check_services
            ;;
        6) view_logs ;;
        7) advanced_config ;;
        8) 
            log "👋 ¡Hasta luego!"
            exit 0
            ;;
        *) 
            error "Opción inválida. Por favor selecciona 1-8."
            ;;
    esac
    
    echo ""
    echo "Presiona Enter para continuar..."
    read -r
done
