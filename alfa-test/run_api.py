#!/usr/bin/env python3

import sys
import time
import pymysql
from app import create_app

def check_mysql_connection():
    """Verificar si MySQL está disponible antes de iniciar la API"""
    max_retries = 30
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            # Intentar conectar a MySQL
            connection = pymysql.connect(
                host='localhost',
                port=3306,
                user='alfa_user',
                password='alfa_password',
                database='alfa_db'
            )
            connection.close()
            print("-----> Conexión a MySQL exitosa!")
            return True
        except Exception as e:
            retry_count += 1
            print(f"-----> Intento {retry_count}/{max_retries} - Esperando MySQL...")
            if retry_count >= max_retries:
                print(f"-----> Error: No se pudo conectar a MySQL después de {max_retries} intentos")
                print("-----> Asegúrate de que MySQL esté corriendo:")
                print("   cd alfa-test && bash scripts/start_mysql.sh")
                return False
            time.sleep(2)
    
    return False

def main():
    print("-----> Iniciando API Flask...")
    
    # Verificar conexión a MySQL
    if not check_mysql_connection():
        sys.exit(1)
    
    # Crear e iniciar la aplicación
    app = create_app()
    
    print("-----> API iniciada exitosamente!")
    print("-----> Endpoints disponibles:")
    print("   - Health Check: http://localhost:5000/api/health")
    print("   - 🔐 Autenticación: http://localhost:5000/api/auth/[agente|cliente]/login")
    print("   - Agentes: http://localhost:5000/api/agentes")
    print("   - Clientes: http://localhost:5000/api/clientes")
    print("   - Bienes: http://localhost:5000/api/bienes")
    print("   - Asignaciones: http://localhost:5000/api/asignaciones")
    print("   - Aseguradoras: http://localhost:5000/api/aseguradoras")
    print("   - Opciones de Seguro: http://localhost:5000/api/opciones-seguro")
    print("   - Pólizas: http://localhost:5000/api/polizas")
    print("   - Documentación Swagger: http://localhost:5000/docs/")
    print("")
    print("-----> Sistema de autenticación JWT habilitado:")
    print("   - Login agentes: POST /api/auth/agente/login")
    print("   - Login clientes: POST /api/auth/cliente/login")
    print("   - Renovar token: POST /api/auth/token/refresh")
    print("   - Decodificar token: POST /api/auth/token/decode")
    print("")
    print("-----> Presiona Ctrl+C para detener la API")
    
    app.run(debug=True, host='0.0.0.0', port=5000)

if __name__ == '__main__':
    main() 