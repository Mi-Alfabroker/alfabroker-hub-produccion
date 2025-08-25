#!/bin/bash

# 🚀 Script de Configuración Automática para EC2 - Versión Corregida
# Este script resuelve problemas comunes de Amazon Linux 2023

set -e

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() { echo -e "${GREEN}[$(date +'%H:%M:%S')] $1${NC}"; }
warn() { echo -e "${YELLOW}[$(date +'%H:%M:%S')] WARNING: $1${NC}"; }
error() { echo -e "${RED}[$(date +'%H:%M:%S')] ERROR: $1${NC}"; exit 1; }
info() { echo -e "${BLUE}[$(date +'%H:%M:%S')] INFO: $1${NC}"; }

# Banner
echo -e "${BLUE}"
cat << "EOF"
╔══════════════════════════════════════════════════════════════╗
║                🚀 ALFA EC2 SETUP - FIXED 🚀                 ║
║              Configuración Automática para AWS EC2           ║
║                   Versión Corregida                          ║
╚══════════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

log "🔧 Iniciando configuración de EC2 para Alfa App..."

# Verificar que estamos en Amazon Linux
if [ ! -f /etc/amazon-linux-release ] && [ ! -f /etc/system-release ]; then
    error "Este script está diseñado para Amazon Linux 2023. Usa otra distribución bajo tu propio riesgo."
fi

# Actualizar sistema
log "📦 Actualizando sistema..."
sudo dnf update -y

# Resolver problema de curl
log "🔧 Resolviendo conflicto de curl..."
# Primero intentar remover curl-minimal
sudo dnf remove -y curl-minimal 2>/dev/null || true

# Instalar curl con --allowerasing para resolver conflictos
sudo dnf install -y curl --allowerasing --skip-broken

# Verificar que curl funciona
if ! command -v curl &> /dev/null; then
    warn "curl no se instaló correctamente, intentando método alternativo..."
    sudo dnf swap -y curl-minimal curl
fi

# Instalar herramientas básicas una por una para evitar conflictos
log "🛠️ Instalando herramientas básicas..."

packages=(
    "wget"
    "git" 
    "htop"
    "nano"
    "vim"
    "unzip"
    "tar"
    "gzip"
    "openssl"
    "firewalld"
    "cronie"
    "logrotate"
)

for package in "${packages[@]}"; do
    if ! rpm -q "$package" &>/dev/null; then
        log "Instalando $package..."
        sudo dnf install -y "$package" || warn "No se pudo instalar $package"
    else
        info "$package ya está instalado"
    fi
done

# Instalar httpd-tools (puede tener nombre diferente)
log "Instalando httpd-tools..."
sudo dnf install -y httpd-tools || sudo dnf install -y apache2-utils || warn "No se pudo instalar httpd-tools"

# Configurar firewall
log "🔥 Configurando firewall firewalld..."
sudo systemctl enable firewalld
sudo systemctl start firewalld

# Configurar puertos
sudo firewall-cmd --permanent --add-service=ssh
sudo firewall-cmd --permanent --add-service=http  
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --permanent --add-port=5000/tcp
sudo firewall-cmd --permanent --add-port=9443/tcp
sudo firewall-cmd --reload

info "✅ Firewall configurado correctamente"

# Instalar Docker
log "🐳 Instalando Docker..."
if ! command -v docker &> /dev/null; then
    # Método alternativo para Amazon Linux 2023
    sudo dnf install -y docker
    sudo systemctl enable docker
    sudo systemctl start docker
    sudo usermod -aG docker $USER
    info "✅ Docker instalado correctamente"
else
    info "✅ Docker ya está instalado"
fi

# Instalar Docker Compose
log "🐙 Instalando Docker Compose..."
if ! command -v docker-compose &> /dev/null; then
    # Usar pip para instalar docker-compose como alternativa
    sudo dnf install -y python3-pip
    sudo pip3 install docker-compose
    
    # Si falla, usar método manual
    if ! command -v docker-compose &> /dev/null; then
        DOCKER_COMPOSE_VERSION="v2.24.1"
        sudo curl -L "https://github.com/docker/compose/releases/download/${DOCKER_COMPOSE_VERSION}/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
        sudo chmod +x /usr/local/bin/docker-compose
        sudo ln -sf /usr/local/bin/docker-compose /usr/bin/docker-compose
    fi
    
    info "✅ Docker Compose instalado correctamente"
else
    info "✅ Docker Compose ya está instalado"
fi

# Instalar Node.js
log "📦 Instalando Node.js..."
if ! command -v node &> /dev/null; then
    # Usar NodeSource repository
    curl -fsSL https://rpm.nodesource.com/setup_18.x | sudo bash -
    sudo dnf install -y nodejs
    info "✅ Node.js $(node --version) instalado"
else
    info "✅ Node.js ya está instalado: $(node --version)"
fi

# Configurar fail2ban
log "🔒 Configurando fail2ban..."
sudo dnf install -y epel-release
sudo dnf install -y fail2ban

# Crear configuración
sudo tee /etc/fail2ban/jail.local > /dev/null << EOF
[DEFAULT]
bantime = 3600
findtime = 600
maxretry = 5

[sshd]
enabled = true
port = ssh
logpath = /var/log/secure
maxretry = 3
bantime = 86400
EOF

sudo systemctl enable fail2ban
sudo systemctl start fail2ban
info "✅ fail2ban configurado correctamente"

# Configurar swap
log "💾 Configurando swap..."
if [ ! -f /swapfile ]; then
    sudo fallocate -l 2G /swapfile
    sudo chmod 600 /swapfile
    sudo mkswap /swapfile
    sudo swapon /swapfile
    echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
    info "✅ Swap de 2GB configurado"
else
    info "✅ Swap ya está configurado"
fi

# Optimizaciones del sistema
log "⚡ Optimizando configuración del sistema..."

# Límites del sistema
sudo tee -a /etc/security/limits.conf > /dev/null << EOF
* soft nofile 65536
* hard nofile 65536
* soft nproc 65536
* hard nproc 65536
EOF

# Parámetros del kernel
sudo tee -a /etc/sysctl.conf > /dev/null << EOF
# Optimizaciones para aplicaciones web
net.core.somaxconn = 65536
net.core.netdev_max_backlog = 5000
net.ipv4.tcp_max_syn_backlog = 65536
net.ipv4.tcp_keepalive_time = 600
net.ipv4.tcp_keepalive_intvl = 60
net.ipv4.tcp_keepalive_probes = 10
vm.swappiness = 10
EOF

sudo sysctl -p

info "✅ Sistema optimizado correctamente"

# Configurar timezone
log "🕐 Configurando timezone..."
sudo timedatectl set-timezone America/Bogota
info "✅ Timezone configurado"

# Instalar Certbot
log "🔒 Instalando Certbot..."
sudo dnf install -y certbot
info "✅ Certbot instalado"

# Crear scripts de monitoreo y backup
log "📊 Creando scripts de utilidad..."

# Script de monitoreo
tee ~/monitor-alfa.sh > /dev/null << 'EOF'
#!/bin/bash
LOG_FILE="/var/log/alfa-monitor.log"

check_service() {
    local service=$1
    local url=$2
    
    if curl -f -s --max-time 10 "$url" > /dev/null 2>&1; then
        echo "$(date): ✅ $service OK" >> "$LOG_FILE"
    else
        echo "$(date): ❌ $service DOWN" >> "$LOG_FILE"
    fi
}

check_service "Frontend" "https://localhost/"
check_service "API" "http://localhost:5000/health"
check_service "Portainer" "https://localhost:9443/"

# Verificar recursos
DISK_USAGE=$(df / | awk 'NR==2 {print $5}' | sed 's/%//')
if [ "$DISK_USAGE" -gt 80 ]; then
    echo "$(date): ⚠️ Disk usage high: ${DISK_USAGE}%" >> "$LOG_FILE"
fi

MEM_USAGE=$(free | awk 'NR==2{printf "%.0f", $3*100/$2}')
if [ "$MEM_USAGE" -gt 85 ]; then
    echo "$(date): ⚠️ Memory usage high: ${MEM_USAGE}%" >> "$LOG_FILE"
fi
EOF

chmod +x ~/monitor-alfa.sh

# Script de backup
tee ~/backup-alfa.sh > /dev/null << 'EOF'
#!/bin/bash
BACKUP_DIR="/home/ec2-user/backups"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p "$BACKUP_DIR"

if docker ps | grep -q alfa_mysql; then
    echo "Creando backup de base de datos..."
    docker exec alfa_mysql mysqldump -u root -p${MYSQL_ROOT_PASSWORD} --all-databases > "$BACKUP_DIR/mysql_backup_$DATE.sql"
    gzip "$BACKUP_DIR/mysql_backup_$DATE.sql"
    echo "Backup creado: mysql_backup_$DATE.sql.gz"
fi

find "$BACKUP_DIR" -name "mysql_backup_*.sql.gz" -mtime +7 -delete
echo "Backup completado: $(date)"
EOF

chmod +x ~/backup-alfa.sh

# Configurar cron
(crontab -l 2>/dev/null; echo "*/5 * * * * ~/monitor-alfa.sh") | crontab -
(crontab -l 2>/dev/null; echo "0 2 * * * ~/backup-alfa.sh >> /var/log/alfa-backup.log 2>&1") | crontab -

# Crear archivo de información
tee ~/system-info.txt > /dev/null << EOF
# 🖥️ Información del Sistema Alfa App

## Configuración Completada
- Fecha: $(date)
- Usuario: $(whoami)
- Hostname: $(hostname)
- IP Pública: $(curl -s ifconfig.me 2>/dev/null || echo "No disponible")
- Sistema: $(cat /etc/system-release 2>/dev/null || echo "Amazon Linux 2023")
- Kernel: $(uname -r)

## Servicios Instalados
- Docker: $(docker --version 2>/dev/null || echo "No instalado")
- Docker Compose: $(docker-compose --version 2>/dev/null || echo "No instalado")
- Node.js: $(node --version 2>/dev/null || echo "No instalado")
- NPM: $(npm --version 2>/dev/null || echo "No instalado")

## Puertos Configurados
- 80: HTTP (Frontend)
- 443: HTTPS (Frontend)  
- 5000: API Backend
- 9443: Portainer
- 3306: MySQL (interno)

## Próximos Pasos
1. Reiniciar sesión SSH: exit && ssh -i key.pem ec2-user@IP
2. Subir código: scp -r ./Striker-dev ec2-user@IP:~/
3. Ejecutar: cd Striker-dev && ./deploy.sh
4. Configurar dominio y SSL si es necesario

## Comandos Útiles
- Ver firewall: sudo firewall-cmd --list-all
- Ver fail2ban: sudo fail2ban-client status sshd
- Ver recursos: htop
- Ver contenedores: docker ps
- Monitoreo: tail -f /var/log/alfa-monitor.log
EOF

# Mostrar resumen final
echo ""
echo -e "${GREEN}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║                    ✅ CONFIGURACIÓN COMPLETADA ✅             ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════════════════════════╝${NC}"
echo ""

log "🎉 ¡EC2 configurado exitosamente para Alfa App!"
echo ""
info "📋 Información del sistema: ~/system-info.txt"
info "📊 Monitoreo: ~/monitor-alfa.sh (cada 5 min)"
info "💾 Backup: ~/backup-alfa.sh (diario 2 AM)"
echo ""
warn "⚠️  IMPORTANTE: Reinicia la sesión SSH para aplicar cambios de Docker"
warn "⚠️  Comando: exit && ssh -i tu-key.pem ec2-user@$(curl -s ifconfig.me 2>/dev/null)"
echo ""
log "🚀 Próximos pasos:"
echo "   1. Reiniciar sesión SSH"
echo "   2. Subir código: scp -r ./Striker-dev ec2-user@IP:~/"
echo "   3. Ejecutar: cd Striker-dev && ./deploy.sh"
echo ""

# Información importante
echo -e "${BLUE}🔑 Información Importante:${NC}"
echo "   IP Pública: $(curl -s ifconfig.me 2>/dev/null || echo 'No disponible')"
echo "   Usuario SSH: ec2-user"
echo "   Puertos abiertos: 22, 80, 443, 5000, 9443"
echo "   Firewall: firewalld habilitado"
echo "   Fail2ban: Activo para SSH"
echo "   Swap: 2GB configurado"
echo "   Timezone: America/Bogota"
echo ""

log "✨ ¡Configuración completada! El servidor está listo para Alfa App."
