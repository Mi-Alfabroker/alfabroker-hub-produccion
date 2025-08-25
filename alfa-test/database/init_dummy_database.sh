#!/bin/bash

# =============================================================================
# SCRIPT DE INICIALIZACIÓN DE BASE DE DATOS CON DATOS DUMMY
# Sistema de Gestión de Seguros - Davivienda
# =============================================================================

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuración de base de datos
DB_NAME="alfa_db"
DB_USER="root"
DB_PASSWORD="root"
DB_HOST="localhost"
DB_PORT="3306"

# Función para mostrar mensajes
print_message() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Función para verificar si MySQL está corriendo
check_mysql() {
    print_message "Verificando si MySQL está corriendo..."
    
    if command -v mysql &> /dev/null; then
        mysql -h$DB_HOST -P$DB_PORT -u$DB_USER -p$DB_PASSWORD -e "SELECT 1;" &> /dev/null
        if [ $? -eq 0 ]; then
            print_success "MySQL está corriendo y accesible"
            return 0
        else
            print_error "MySQL está instalado pero no se puede conectar"
            print_error "Verifique las credenciales: usuario=$DB_USER, host=$DB_HOST, puerto=$DB_PORT"
            return 1
        fi
    else
        print_error "MySQL no está instalado o no está en el PATH"
        return 1
    fi
}

# Función para ejecutar el script SQL
execute_sql() {
    print_message "Ejecutando script de inicialización..."
    
    # Verificar si el archivo SQL existe
    if [ ! -f "init_with_dummy_data.sql" ]; then
        print_error "El archivo init_with_dummy_data.sql no existe en el directorio actual"
        return 1
    fi
    
    # Ejecutar el script SQL
    mysql -h$DB_HOST -P$DB_PORT -u$DB_USER -p$DB_PASSWORD < init_with_dummy_data.sql
    
    if [ $? -eq 0 ]; then
        print_success "Script ejecutado exitosamente"
        return 0
    else
        print_error "Error al ejecutar el script SQL"
        return 1
    fi
}

# Función para mostrar estadísticas
show_stats() {
    print_message "Consultando estadísticas de la base de datos..."
    
    mysql -h$DB_HOST -P$DB_PORT -u$DB_USER -p$DB_PASSWORD -D$DB_NAME -e "
    SELECT 
        'RESUMEN DE DATOS INSERTADOS' as TABLA,
        '' as CANTIDAD
    UNION ALL
    SELECT 'Agentes', COUNT(*) FROM Agente
    UNION ALL
    SELECT 'Clientes', COUNT(*) FROM clientes
    UNION ALL
    SELECT 'Hogares', COUNT(*) FROM hogares
    UNION ALL
    SELECT 'Vehículos', COUNT(*) FROM vehiculos
    UNION ALL
    SELECT 'Copropiedades', COUNT(*) FROM copropiedades
    UNION ALL
    SELECT 'Otros Bienes', COUNT(*) FROM otros_bienes
    UNION ALL
    SELECT 'Bienes Totales', COUNT(*) FROM bienes
    UNION ALL
    SELECT 'Asignaciones Agente-Cliente', COUNT(*) FROM agentes_clientes
    UNION ALL
    SELECT 'Asignaciones Cliente-Bien', COUNT(*) FROM clientes_bienes;
    "
}

# Función para mostrar ejemplos de consultas
show_examples() {
    print_message "Algunos ejemplos de consultas que puedes ejecutar:"
    echo
    echo "# Ver todos los agentes:"
    echo "SELECT id, nombre, rol, activo FROM Agente;"
    echo
    echo "# Ver clientes con sus agentes asignados:"
    echo "SELECT c.nombre, c.tipo_cliente, a.nombre as agente"
    echo "FROM clientes c"
    echo "JOIN agentes_clientes ac ON c.id = ac.cliente_id"
    echo "JOIN Agente a ON ac.agente_id = a.id;"
    echo
    echo "# Ver bienes por tipo:"
    echo "SELECT tipo_bien, COUNT(*) as cantidad FROM bienes GROUP BY tipo_bien;"
    echo
    echo "# Ver clientes con sus bienes:"
    echo "SELECT c.nombre, b.tipo_bien, b.comentarios_generales"
    echo "FROM clientes c"
    echo "JOIN clientes_bienes cb ON c.id = cb.cliente_id"
    echo "JOIN bienes b ON cb.bien_id = b.id"
    echo "LIMIT 10;"
}

# Función principal
main() {
    echo "======================================================================="
    echo "       INICIALIZADOR DE BASE DE DATOS CON DATOS DUMMY - ALFA"
    echo "======================================================================="
    echo
    
    # Verificar MySQL
    if ! check_mysql; then
        exit 1
    fi
    
    # Confirmar ejecución
    echo
    print_warning "Este script eliminará todos los datos existentes en la base de datos $DB_NAME"
    print_warning "¿Estás seguro de que deseas continuar? (y/n)"
    read -r response
    
    if [[ ! "$response" =~ ^[Yy]$ ]]; then
        print_message "Operación cancelada por el usuario"
        exit 0
    fi
    
    # Ejecutar script SQL
    if execute_sql; then
        print_success "Base de datos inicializada exitosamente"
        echo
        show_stats
        echo
        show_examples
    else
        print_error "Falló la inicialización de la base de datos"
        exit 1
    fi
    
    echo
    print_success "¡Proceso completado! La base de datos está lista para usar."
}

# Verificar si se están pasando argumentos para configuración personalizada
while [[ $# -gt 0 ]]; do
    case $1 in
        -u|--user)
            DB_USER="$2"
            shift 2
            ;;
        -p|--password)
            DB_PASSWORD="$2"
            shift 2
            ;;
        -h|--host)
            DB_HOST="$2"
            shift 2
            ;;
        -P|--port)
            DB_PORT="$2"
            shift 2
            ;;
        -d|--database)
            DB_NAME="$2"
            shift 2
            ;;
        --help)
            echo "Uso: $0 [opciones]"
            echo
            echo "Opciones:"
            echo "  -u, --user      Usuario de MySQL (default: root)"
            echo "  -p, --password  Contraseña de MySQL (default: root)"
            echo "  -h, --host      Host de MySQL (default: localhost)"
            echo "  -P, --port      Puerto de MySQL (default: 3306)"
            echo "  -d, --database  Nombre de la base de datos (default: alfa_db)"
            echo "  --help          Mostrar esta ayuda"
            echo
            echo "Ejemplo:"
            echo "  $0 -u mi_usuario -p mi_password -h 192.168.1.100"
            exit 0
            ;;
        *)
            print_error "Opción desconocida: $1"
            echo "Use --help para ver las opciones disponibles"
            exit 1
            ;;
    esac
done

# Ejecutar función principal
main 