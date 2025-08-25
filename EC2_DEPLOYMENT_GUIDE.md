# 🚀 Guía de Despliegue en AWS EC2

Esta guía te ayudará a desplegar la aplicación Alfa completa en una instancia EC2 de AWS.

## 📋 Prerrequisitos

- Cuenta de AWS activa
- Conocimientos básicos de AWS EC2
- Dominio propio (opcional, para SSL real)

## 🖥️ Configuración de la Instancia EC2

### 1. Crear Instancia EC2

**Especificaciones Recomendadas:**
- **AMI**: Ubuntu Server 22.04 LTS
- **Tipo de Instancia**: 
  - Desarrollo: `t3.medium` (2 vCPU, 4 GB RAM)
  - Producción: `t3.large` (2 vCPU, 8 GB RAM) o superior
- **Almacenamiento**: 20-30 GB SSD (gp3)
- **VPC**: Default o personalizada

### 2. Configurar Security Groups

Crear un Security Group con las siguientes reglas:

#### Reglas de Entrada (Inbound Rules)

| Tipo | Protocolo | Puerto | Origen | Descripción |
|------|-----------|--------|--------|-------------|
| SSH | TCP | 22 | Tu IP pública | Acceso SSH |
| HTTP | TCP | 80 | 0.0.0.0/0 | Tráfico web HTTP |
| HTTPS | TCP | 443 | 0.0.0.0/0 | Tráfico web HTTPS |
| Custom TCP | TCP | 5000 | 0.0.0.0/0 | API Backend (opcional) |
| Custom TCP | TCP | 9443 | Tu IP pública | Portainer HTTPS |
| Custom TCP | TCP | 3306 | Security Group ID | MySQL (solo interno) |

#### Reglas de Salida (Outbound Rules)
- **Todas**: 0.0.0.0/0 (permitir todo el tráfico saliente)

### 3. Configurar Key Pair

```bash
# En tu máquina local, generar par de llaves si no tienes
ssh-keygen -t rsa -b 4096 -f ~/.ssh/alfa-ec2-key

# Importar la llave pública a AWS EC2
# O descargar la llave .pem generada por AWS
```

## 🔧 Configuración del Servidor

### 1. Conectar a la Instancia

```bash
# Cambiar permisos de la llave
chmod 400 ~/.ssh/alfa-ec2-key.pem

# Conectar via SSH
ssh -i ~/.ssh/alfa-ec2-key.pem ubuntu@YOUR_EC2_PUBLIC_IP
```

### 2. Actualizar el Sistema

```bash
# Actualizar paquetes
sudo apt update && sudo apt upgrade -y

# Instalar herramientas básicas
sudo apt install -y curl wget git htop nano ufw
```

### 3. Configurar Firewall (UFW)

```bash
# Habilitar UFW
sudo ufw enable

# Configurar reglas básicas
sudo ufw default deny incoming
sudo ufw default allow outgoing

# Permitir conexiones necesarias
sudo ufw allow ssh
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 5000/tcp
sudo ufw allow 9443/tcp

# Verificar estado
sudo ufw status
```

### 4. Instalar Docker y Docker Compose

```bash
# Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Agregar usuario al grupo docker
sudo usermod -aG docker $USER

# Instalar Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Verificar instalación
docker --version
docker-compose --version

# Reiniciar sesión para aplicar cambios de grupo
exit
# Volver a conectar via SSH
```

## 📦 Despliegue de la Aplicación

### 1. Clonar el Repositorio

```bash
# Clonar el proyecto
git clone https://github.com/tu-usuario/Striker-dev.git
cd Striker-dev

# O subir archivos via SCP
scp -i ~/.ssh/alfa-ec2-key.pem -r ./Striker-dev ubuntu@YOUR_EC2_PUBLIC_IP:~/
```

### 2. Configurar Variables de Entorno

```bash
# Copiar y editar archivo de configuración
cp .env.example .env
nano .env
```

**Configuración recomendada para producción:**

```bash
# Configuración de Base de Datos
MYSQL_ROOT_PASSWORD=TuPasswordSegura123!
MYSQL_DATABASE=alfa_db
MYSQL_USER=alfa_user
MYSQL_PASSWORD=TuPasswordUsuario123!

# Configuración de la Aplicación
FLASK_ENV=production
APP_SECRET_KEY=tu-clave-secreta-muy-larga-y-segura

# Configuración de Dominio
DOMAIN_NAME=tu-dominio.com
EMAIL=admin@tu-dominio.com
```

### 3. Configurar SSL (Certificados Reales)

#### Opción A: Let's Encrypt (Recomendado)

```bash
# Instalar Certbot
sudo apt install -y certbot

# Obtener certificados (requiere dominio apuntando a la IP)
sudo certbot certonly --standalone -d tu-dominio.com -d www.tu-dominio.com

# Copiar certificados
sudo mkdir -p ssl
sudo cp /etc/letsencrypt/live/tu-dominio.com/fullchain.pem ssl/cert.pem
sudo cp /etc/letsencrypt/live/tu-dominio.com/privkey.pem ssl/key.pem
sudo chown $USER:$USER ssl/*
```

#### Opción B: Certificados Autofirmados (Desarrollo)

```bash
# Los certificados se generan automáticamente con el script deploy.sh
```

### 4. Ejecutar Despliegue

```bash
# Hacer ejecutable el script
chmod +x deploy.sh

# Ejecutar despliegue
./deploy.sh
```

Selecciona la opción **1) Despliegue completo** en el menú.

## 🌐 Configuración de DNS (Opcional)

Si tienes un dominio, configura los registros DNS:

```
Tipo: A
Nombre: @
Valor: TU_IP_PUBLICA_EC2
TTL: 300

Tipo: A  
Nombre: www
Valor: TU_IP_PUBLICA_EC2
TTL: 300
```

## 🔍 Verificación del Despliegue

### 1. Verificar Servicios

```bash
# Ver estado de contenedores
docker ps

# Ver logs
docker-compose logs -f

# Verificar conectividad
curl -k https://localhost/health
curl http://localhost:5000/health
```

### 2. URLs de Acceso

- **Frontend**: `https://TU_IP_PUBLICA` o `https://tu-dominio.com`
- **API**: `http://TU_IP_PUBLICA:5000`
- **Portainer**: `https://TU_IP_PUBLICA:9443`

### 3. Credenciales por Defecto

- **Portainer**: 
  - Usuario: `admin`
  - Contraseña: Se genera automáticamente (ver logs del script)

## 🔧 Mantenimiento y Monitoreo

### 1. Comandos Útiles

```bash
# Ver uso de recursos
htop
docker stats

# Backup de base de datos
docker exec alfa_mysql mysqldump -u root -pTU_PASSWORD alfa_db > backup_$(date +%Y%m%d).sql

# Actualizar aplicación
git pull origin main
./deploy.sh  # Opción 2: Actualizar servicios
```

### 2. Logs Importantes

```bash
# Logs de Nginx
docker-compose logs alfa-frontend

# Logs de API
docker-compose logs alfa-api

# Logs de Base de Datos
docker-compose logs mysql

# Logs del sistema
sudo journalctl -u docker
```

### 3. Renovación de Certificados SSL

```bash
# Renovar certificados Let's Encrypt (automático)
sudo certbot renew --dry-run

# Configurar renovación automática
sudo crontab -e
# Agregar: 0 12 * * * /usr/bin/certbot renew --quiet
```

## 🚨 Solución de Problemas

### Problema: No se puede acceder al sitio

```bash
# Verificar firewall
sudo ufw status

# Verificar servicios
docker ps
docker-compose ps

# Verificar logs
docker-compose logs
```

### Problema: Error de SSL

```bash
# Verificar certificados
openssl x509 -in ssl/cert.pem -text -noout

# Regenerar certificados
rm -rf ssl
./deploy.sh  # Opción 7: Configuración avanzada -> 1
```

### Problema: Base de datos no conecta

```bash
# Verificar MySQL
docker exec -it alfa_mysql mysql -u root -p

# Verificar variables de entorno
docker-compose config
```

## 📊 Monitoreo con CloudWatch (Opcional)

### 1. Instalar CloudWatch Agent

```bash
# Descargar e instalar
wget https://s3.amazonaws.com/amazoncloudwatch-agent/ubuntu/amd64/latest/amazon-cloudwatch-agent.deb
sudo dpkg -i amazon-cloudwatch-agent.deb
```

### 2. Configurar Métricas

```bash
# Configurar agent
sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-config-wizard
```

## 🔒 Mejores Prácticas de Seguridad

1. **Cambiar contraseñas por defecto**
2. **Configurar backup automático**
3. **Actualizar regularmente el sistema**
4. **Monitorear logs de acceso**
5. **Usar certificados SSL válidos**
6. **Configurar fail2ban para SSH**

```bash
# Instalar fail2ban
sudo apt install -y fail2ban

# Configurar
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

## 📈 Escalabilidad

Para mayor tráfico, considera:

- **Load Balancer**: AWS Application Load Balancer
- **Base de datos**: Amazon RDS MySQL
- **CDN**: Amazon CloudFront
- **Auto Scaling**: Auto Scaling Groups
- **Contenedores**: Amazon ECS o EKS

## 💰 Estimación de Costos (USD/mes)

| Recurso | Tipo | Costo Aprox. |
|---------|------|--------------|
| EC2 t3.medium | 24/7 | $30-35 |
| EBS 30GB | gp3 | $3-4 |
| Elastic IP | Fija | $3.65 |
| Data Transfer | 1GB out | $0.09 |
| **Total** | | **~$37-43/mes** |

*Precios pueden variar según región y uso real.*
