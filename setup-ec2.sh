#!/bin/bash

# 🚀 Script de Configuración Automática para EC2
# Este script configura automáticamente una instancia EC2 para Alfa App

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
║                    🚀 ALFA EC2 SETUP 🚀                     ║
║              Configuración Automática para AWS EC2           ║
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

# Instalar herramientas básicas
log "🛠️ Instalando herramientas básicas..."
sudo dnf install -y \
    curl \
    wget \
    git \
    htop \
    nano \
    vim \
    unzip \
    tar \
    gzip \
    openssl \
    httpd-tools \
    firewalld \
    cronie \
    logrotate

# Configurar firewall (firewalld en Amazon Linux)
log "🔥 Configurando firewall firewalld..."
sudo systemctl enable firewalld
sudo systemctl start firewalld

# Configurar zonas y puertos
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
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker $USER
    rm get-docker.sh
    info "✅ Docker instalado correctamente"
else
    info "✅ Docker ya está instalado"
fi

# Instalar Docker Compose
log "🐙 Instalando Docker Compose..."
if ! command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_VERSION=$(curl -s https://api.github.com/repos/docker/compose/releases/latest | grep 'tag_name' | cut -d\" -f4)
    sudo curl -L "https://github.com/docker/compose/releases/download/${DOCKER_COMPOSE_VERSION}/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
    info "✅ Docker Compose instalado correctamente"
else
    info "✅ Docker Compose ya está instalado"
fi

# Instalar Node.js (para builds futuros)
log "📦 Instalando Node.js..."
if ! command -v node &> /dev/null; then
    curl -fsSL https://rpm.nodesource.com/setup_18.x | sudo bash -
    sudo dnf install -y nodejs
    info "✅ Node.js $(node --version) instalado"
else
    info "✅ Node.js ya está instalado: $(node --version)"
fi

# Configurar fail2ban para seguridad SSH
log "🔒 Configurando fail2ban..."
sudo dnf install -y epel-release
sudo dnf install -y fail2ban
sudo systemctl enable fail2ban
sudo systemctl start fail2ban

# Crear configuración básica de fail2ban
sudo tee /etc/fail2ban/jail.local > /dev/null << EOF
[DEFAULT]
bantime = 3600
findtime = 600
maxretry = 5

[sshd]
enabled = true
port = ssh
logpath = /var/log/auth.log
maxretry = 3
bantime = 86400
EOF

sudo systemctl restart fail2ban
info "✅ fail2ban configurado correctamente"

# Configurar swapfile si no existe
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

# Optimizar configuración del sistema
log "⚡ Optimizando configuración del sistema..."

# Configurar límites del sistema
sudo tee -a /etc/security/limits.conf > /dev/null << EOF
* soft nofile 65536
* hard nofile 65536
* soft nproc 65536
* hard nproc 65536
EOF

# Configurar parámetros del kernel
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

# Configurar logrotate para Docker
sudo tee /etc/logrotate.d/docker > /dev/null << EOF
/var/lib/docker/containers/*/*.log {
    rotate 7
    daily
    compress
    size=1M
    missingok
    delaycompress
    copytruncate
}
EOF

info "✅ Sistema optimizado correctamente"

# Crear directorio para la aplicación
log "📁 Preparando directorio de aplicación..."
mkdir -p ~/alfa-app
cd ~/alfa-app

# Crear script de monitoreo básico
log "📊 Creando script de monitoreo..."
tee ~/monitor-alfa.sh > /dev/null << 'EOF'
#!/bin/bash
# Script básico de monitoreo para Alfa App

LOG_FILE="/var/log/alfa-monitor.log"

check_service() {
    local service=$1
    local url=$2
    
    if curl -f -s --max-time 10 "$url" > /dev/null 2>&1; then
        echo "$(date): ✅ $service OK" >> "$LOG_FILE"
        return 0
    else
        echo "$(date): ❌ $service DOWN" >> "$LOG_FILE"
        return 1
    fi
}

# Verificar servicios
check_service "Frontend" "https://localhost/"
check_service "API" "http://localhost:5000/health"
check_service "Portainer" "https://localhost:9443/"

# Verificar uso de disco
DISK_USAGE=$(df / | awk 'NR==2 {print $5}' | sed 's/%//')
if [ "$DISK_USAGE" -gt 80 ]; then
    echo "$(date): ⚠️ Disk usage high: ${DISK_USAGE}%" >> "$LOG_FILE"
fi

# Verificar memoria
MEM_USAGE=$(free | awk 'NR==2{printf "%.0f", $3*100/$2}')
if [ "$MEM_USAGE" -gt 85 ]; then
    echo "$(date): ⚠️ Memory usage high: ${MEM_USAGE}%" >> "$LOG_FILE"
fi
EOF

chmod +x ~/monitor-alfa.sh

# Configurar cron para monitoreo
(crontab -l 2>/dev/null; echo "*/5 * * * * ~/monitor-alfa.sh") | crontab -

info "✅ Monitoreo configurado (cada 5 minutos)"

# Configurar actualizaciones automáticas de seguridad
log "🔄 Configurando actualizaciones automáticas..."
sudo dnf install -y dnf-automatic
sudo systemctl enable dnf-automatic.timer
sudo systemctl start dnf-automatic.timer

# Configurar dnf-automatic para solo actualizaciones de seguridad
sudo sed -i 's/upgrade_type = default/upgrade_type = security/' /etc/dnf/automatic.conf
sudo sed -i 's/apply_updates = no/apply_updates = yes/' /etc/dnf/automatic.conf

# Crear script de backup
log "💾 Creando script de backup..."
tee ~/backup-alfa.sh > /dev/null << 'EOF'
#!/bin/bash
# Script de backup para Alfa App

BACKUP_DIR="/home/ec2-user/backups"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p "$BACKUP_DIR"

# Backup de base de datos
if docker ps | grep -q alfa_mysql; then
    echo "Creando backup de base de datos..."
    docker exec alfa_mysql mysqldump -u root -p${MYSQL_ROOT_PASSWORD} --all-databases > "$BACKUP_DIR/mysql_backup_$DATE.sql"
    
    # Comprimir backup
    gzip "$BACKUP_DIR/mysql_backup_$DATE.sql"
    
    echo "Backup creado: mysql_backup_$DATE.sql.gz"
fi

# Limpiar backups antiguos (mantener últimos 7 días)
find "$BACKUP_DIR" -name "mysql_backup_*.sql.gz" -mtime +7 -delete

echo "Backup completado: $(date)"
EOF

chmod +x ~/backup-alfa.sh

# Configurar backup automático diario
(crontab -l 2>/dev/null; echo "0 2 * * * ~/backup-alfa.sh >> /var/log/alfa-backup.log 2>&1") | crontab -

info "✅ Backup automático configurado (diario a las 2 AM)"

# Instalar Certbot para SSL
log "🔒 Instalando Certbot para SSL..."
sudo dnf install -y certbot
info "✅ Certbot instalado (usar después con tu dominio)"

# Configurar timezone
log "🕐 Configurando timezone..."
sudo timedatectl set-timezone America/Bogota
info "✅ Timezone configurado a America/Bogota"

# Crear archivo de información del sistema
log "📋 Creando información del sistema..."
tee ~/system-info.txt > /dev/null << EOF
# 🖥️ Información del Sistema Alfa App

## Configuración Completada
- Fecha: $(date)
- Usuario: $(whoami)
- Hostname: $(hostname)
- IP Pública: $(curl -s ifconfig.me)
- Sistema: $(cat /etc/system-release)
- Kernel: $(uname -r)

## Servicios Instalados
- Docker: $(docker --version)
- Docker Compose: $(docker-compose --version)
- Node.js: $(node --version)
- NPM: $(npm --version)

## Puertos Configurados
- 80: HTTP (Frontend)
- 443: HTTPS (Frontend)
- 5000: API Backend
- 9443: Portainer
- 3306: MySQL (interno)

## Archivos Importantes
- ~/monitor-alfa.sh: Script de monitoreo
- ~/backup-alfa.sh: Script de backup
- /var/log/alfa-monitor.log: Logs de monitoreo
- /var/log/alfa-backup.log: Logs de backup

## Próximos Pasos
1. Subir código de la aplicación
2. Configurar dominio y SSL
3. Ejecutar deploy.sh
4. Configurar Portainer

## Comandos Útiles
- Ver estado firewall: sudo firewall-cmd --list-all
- Ver logs fail2ban: sudo fail2ban-client status sshd
- Ver uso de recursos: htop
- Ver contenedores: docker ps
- Monitoreo en tiempo real: tail -f /var/log/alfa-monitor.log
- Ver actualizaciones automáticas: sudo systemctl status dnf-automatic.timer
EOF

# Mostrar resumen final
echo ""
echo -e "${GREEN}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║                    ✅ CONFIGURACIÓN COMPLETADA ✅             ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════════════════════════╝${NC}"
echo ""

log "🎉 ¡EC2 configurado exitosamente para Alfa App!"
echo ""
info "📋 Información del sistema guardada en: ~/system-info.txt"
info "📊 Monitoreo configurado: ~/monitor-alfa.sh"
info "💾 Backup configurado: ~/backup-alfa.sh"
echo ""
warn "⚠️  IMPORTANTE: Reinicia la sesión SSH para aplicar cambios de grupo Docker"
warn "⚠️  Comando: exit && ssh -i tu-key.pem ec2-user@$(curl -s ifconfig.me)"
echo ""
log "🚀 Próximos pasos:"
echo "   1. Reiniciar sesión SSH"
echo "   2. Subir código: scp -r ./Striker-dev ec2-user@IP:~/"
echo "   3. Ejecutar: cd Striker-dev && ./deploy.sh"
echo "   4. Configurar dominio y SSL si es necesario"
echo ""
log "📖 Consulta EC2_DEPLOYMENT_GUIDE.md para más detalles"
echo ""

# Mostrar información importante
echo -e "${BLUE}🔑 Información Importante:${NC}"
echo "   IP Pública: $(curl -s ifconfig.me)"
echo "   Usuario SSH: ec2-user"
echo "   Puertos abiertos: 22, 80, 443, 5000, 9443"
echo "   Firewall: firewalld habilitado"
echo "   Fail2ban: Activo para SSH"
echo "   Swap: 2GB configurado"
echo "   Timezone: America/Bogota"
echo ""

log "✨ ¡Configuración completada! El servidor está listo para Alfa App."
