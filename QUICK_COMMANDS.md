# ⚡ Comandos Rápidos - Alfa App

Referencia rápida de comandos más utilizados para gestionar la aplicación.

## 🚀 Despliegue Inicial

```bash
# Despliegue completo local
./deploy.sh

# Despliegue en EC2 (después de setup-ec2.sh)
ssh -i key.pem ubuntu@IP
cd Striker-dev && ./deploy.sh
```

## 🔍 Monitoreo y Estado

```bash
# Ver todos los contenedores
docker ps

# Estado de servicios
docker-compose ps

# Logs en tiempo real
docker-compose logs -f

# Logs específicos
docker-compose logs -f alfa-frontend    # Nginx
docker-compose logs -f alfa-api         # Flask API
docker-compose logs -f mysql            # Base de datos
docker-compose logs -f portainer        # Portainer

# Estadísticas de recursos
docker stats

# Uso del sistema
htop
df -h
free -h
```

## 🔄 Gestión de Servicios

```bash
# Reiniciar servicio específico
docker-compose restart alfa-frontend
docker-compose restart alfa-api
docker-compose restart mysql

# Detener todos los servicios
docker-compose down

# Iniciar servicios
docker-compose up -d

# Reconstruir y reiniciar
docker-compose up -d --build

# Actualizar servicios
docker-compose pull && docker-compose up -d
```

## 🛠️ Mantenimiento

```bash
# Limpiar sistema Docker
docker system prune -f
docker image prune -f
docker volume prune -f

# Backup de base de datos
docker exec alfa_mysql mysqldump -u root -p${MYSQL_ROOT_PASSWORD} alfa_db > backup_$(date +%Y%m%d_%H%M%S).sql

# Restaurar backup
docker exec -i alfa_mysql mysql -u root -p${MYSQL_ROOT_PASSWORD} alfa_db < backup_file.sql

# Ver volúmenes
docker volume ls

# Acceso directo a contenedores
docker exec -it alfa_frontend sh       # Nginx
docker exec -it alfa_api bash          # Flask API
docker exec -it alfa_mysql mysql -u root -p  # MySQL
```

## 🔧 Configuración

```bash
# Editar configuración
nano .env                    # Variables de entorno
nano nginx.conf             # Configuración Nginx
nano docker-compose.yml     # Servicios Docker

# Regenerar certificados SSL
rm -rf ssl && ./deploy.sh   # Opción 7 -> 1

# Ver configuración actual
docker-compose config

# Variables de entorno activas
docker-compose exec alfa-api env
```

## 🌐 Conectividad

```bash
# Test de conectividad
curl -k https://localhost/
curl http://localhost:5000/health
curl -k https://localhost:9443/

# Test desde contenedor
docker exec alfa-api curl -f http://mysql:3306
docker exec alfa-frontend curl -f http://alfa-api:5000/health

# Ver puertos abiertos
netstat -tlnp | grep -E '(80|443|5000|9443|3306)'
sudo ufw status
```

## 🔒 Seguridad

```bash
# Ver intentos de acceso SSH
sudo tail -f /var/log/auth.log

# Estado de fail2ban
sudo fail2ban-client status
sudo fail2ban-client status sshd

# Verificar certificados SSL
openssl x509 -in ssl/cert.pem -text -noout
openssl s_client -connect localhost:443 -servername localhost

# Cambiar contraseñas
./deploy.sh  # Opción 7 -> 2
```

## 📊 Debugging

```bash
# Verificar health checks
docker inspect alfa_frontend | grep -A 10 Health
docker inspect alfa_api | grep -A 10 Health

# Ver eventos Docker
docker events --filter container=alfa_frontend
docker events --filter container=alfa_api

# Inspeccionar red
docker network ls
docker network inspect striker-dev_alfa_network

# Ver procesos en contenedor
docker exec alfa_api ps aux
docker exec alfa_frontend ps aux
```

## 🔄 Actualizaciones

```bash
# Actualizar código
git pull origin main

# Reconstruir frontend
cd alfa-frontend
npm run build
cd ..

# Aplicar cambios
docker-compose up -d --build

# Actualizar sistema (EC2)
sudo apt update && sudo apt upgrade -y
```

## 📱 URLs Importantes

```bash
# Local
echo "Frontend: https://localhost"
echo "API: http://localhost:5000"
echo "Portainer: https://localhost:9443"

# Producción (cambiar IP)
IP=$(curl -s ifconfig.me)
echo "Frontend: https://$IP"
echo "API: http://$IP:5000"
echo "Portainer: https://$IP:9443"
```

## 🆘 Solución Rápida de Problemas

```bash
# Frontend no carga
docker-compose logs alfa-frontend
ls -la alfa-frontend/dist/alfa-frontend/browser/
docker-compose restart alfa-frontend

# API no responde
docker-compose logs alfa-api
docker exec alfa_api curl -f http://localhost:5000/health
docker-compose restart alfa-api

# Base de datos no conecta
docker-compose logs mysql
docker exec alfa_mysql mysql -u root -p -e "SHOW DATABASES;"
docker-compose restart mysql

# Portainer no accesible
docker-compose logs portainer
netstat -tlnp | grep 9443
docker-compose restart portainer

# Certificados SSL
openssl x509 -in ssl/cert.pem -noout -dates
./deploy.sh  # Opción 7 -> 1 (regenerar)

# Espacio en disco
df -h
docker system df
docker system prune -f

# Memoria insuficiente
free -h
docker stats --no-stream
sudo swapon --show
```

## 📋 Checklist de Verificación

```bash
# ✅ Verificar que todo funciona
curl -k https://localhost/ | grep -q "html" && echo "✅ Frontend OK" || echo "❌ Frontend Error"
curl -f http://localhost:5000/health && echo "✅ API OK" || echo "❌ API Error"
curl -k https://localhost:9443/ | grep -q "Portainer" && echo "✅ Portainer OK" || echo "❌ Portainer Error"
docker exec alfa_mysql mysql -u root -p${MYSQL_ROOT_PASSWORD} -e "SELECT 1;" && echo "✅ MySQL OK" || echo "❌ MySQL Error"
```

## 🎯 Comandos de Un Solo Uso

```bash
# Despliegue completo desde cero
docker-compose down -v && docker system prune -f && ./deploy.sh

# Backup completo
tar -czf alfa_backup_$(date +%Y%m%d_%H%M%S).tar.gz \
  --exclude=node_modules \
  --exclude=.git \
  --exclude=dist \
  .

# Restaurar desde backup
tar -xzf alfa_backup_YYYYMMDD_HHMMSS.tar.gz

# Ver toda la información del sistema
echo "=== SISTEMA ===" && uname -a && \
echo "=== DOCKER ===" && docker version && \
echo "=== CONTENEDORES ===" && docker ps && \
echo "=== VOLÚMENES ===" && docker volume ls && \
echo "=== REDES ===" && docker network ls && \
echo "=== RECURSOS ===" && docker stats --no-stream
```

---

💡 **Tip**: Guarda este archivo como referencia rápida. Todos estos comandos asumen que estás en el directorio raíz del proyecto (`Striker-dev/`).
