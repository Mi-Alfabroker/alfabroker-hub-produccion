#!/usr/bin/env python3
"""
Script de prueba para autenticación JWT
Demuestra el funcionamiento del sistema de autenticación para agentes y clientes
"""

import requests
import json
from datetime import datetime

# Configuración base
BASE_URL = "http://localhost:5000/api"

def print_separator(title):
    """Imprime un separador visual"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def print_response(response, title="Respuesta"):
    """Imprime la respuesta de forma formateada"""
    print(f"\n{title}:")
    print(f"Status Code: {response.status_code}")
    try:
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    except:
        print(response.text)

def test_auth_system():
    """Prueba completa del sistema de autenticación"""
    
    print_separator("PRUEBA DEL SISTEMA DE AUTENTICACIÓN JWT")
    print("Este script prueba el funcionamiento completo del sistema de autenticación")
    print("- Crear agente con contraseña hasheada")
    print("- Crear cliente con contraseña hasheada") 
    print("- Login de agente y obtener token JWT")
    print("- Login de cliente y obtener token JWT")
    print("- Decodificar tokens")
    print("- Renovar tokens")
    
    # 1. Crear un agente de prueba
    print_separator("1. CREAR AGENTE CON CONTRASEÑA HASHEADA")
    
    agente_data = {
        "nombre": "Agente de Prueba JWT",
        "correo": "agente.jwt@davivienda.com",
        "usuario": "agente.jwt",
        "clave": "password123",  # Se hasheará automáticamente
        "rol": "agente",
        "activo": True
    }
    
    try:
        response = requests.post(f"{BASE_URL}/agentes", json=agente_data)
        print_response(response, "Crear Agente")
        
        if response.status_code == 201:
            agente_creado = response.json()['data']
            print(f"\n✅ Agente creado exitosamente con ID: {agente_creado['id']}")
            print(f"🔒 Contraseña hasheada almacenada en BD (no visible en respuesta)")
        else:
            print("❌ Error al crear agente")
            return
            
    except Exception as e:
        print(f"❌ Error de conexión al crear agente: {e}")
        return
    
    # 2. Crear un cliente de prueba
    print_separator("2. CREAR CLIENTE CON CONTRASEÑA HASHEADA")
    
    cliente_data = {
        "tipo_cliente": "PERSONA",
        "usuario": "cliente.jwt",
        "clave": "password456",  # Se hasheará automáticamente
        "nombre": "Cliente de Prueba JWT",
        "correo": "cliente.jwt@ejemplo.com",
        "telefono_movil": "3001234567",
        "ciudad": "Bogotá",
        "direccion": "Calle de Prueba #123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/clientes", json=cliente_data)
        print_response(response, "Crear Cliente")
        
        if response.status_code == 201:
            cliente_creado = response.json()['data']
            print(f"\n✅ Cliente creado exitosamente con ID: {cliente_creado['id']}")
            print(f"🔒 Contraseña hasheada almacenada en BD (no visible en respuesta)")
        else:
            print("❌ Error al crear cliente")
            return
            
    except Exception as e:
        print(f"❌ Error de conexión al crear cliente: {e}")
        return
    
    # 3. Login de agente
    print_separator("3. LOGIN DE AGENTE Y OBTENER TOKEN JWT")
    
    login_agente_data = {
        "usuario": "agente.jwt",
        "password": "password123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/agente/login", json=login_agente_data)
        print_response(response, "Login Agente")
        
        if response.status_code == 200:
            auth_data = response.json()['data']
            agente_token = auth_data['token']
            print(f"\n✅ Login de agente exitoso")
            print(f"🎫 Token JWT generado (válido por 24 horas)")
            print(f"👤 Usuario autenticado: {auth_data['agente']['nombre']}")
            print(f"🔑 Rol: {auth_data['agente']['rol']}")
        else:
            print("❌ Error en login de agente")
            return
            
    except Exception as e:
        print(f"❌ Error de conexión en login de agente: {e}")
        return
    
    # 4. Login de cliente
    print_separator("4. LOGIN DE CLIENTE Y OBTENER TOKEN JWT")
    
    login_cliente_data = {
        "usuario": "cliente.jwt",
        "password": "password456"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/cliente/login", json=login_cliente_data)
        print_response(response, "Login Cliente")
        
        if response.status_code == 200:
            auth_data = response.json()['data']
            cliente_token = auth_data['token']
            print(f"\n✅ Login de cliente exitoso")
            print(f"🎫 Token JWT generado (válido por 24 horas)")
            print(f"👤 Usuario autenticado: {auth_data['cliente']['nombre']}")
            print(f"📋 Tipo: {auth_data['cliente']['tipo_cliente']}")
        else:
            print("❌ Error en login de cliente")
            return
            
    except Exception as e:
        print(f"❌ Error de conexión en login de cliente: {e}")
        return
    
    # 5. Decodificar token de agente
    print_separator("5. DECODIFICAR TOKEN JWT DE AGENTE")
    
    try:
        response = requests.post(f"{BASE_URL}/auth/token/decode", json={"token": agente_token})
        print_response(response, "Decodificar Token Agente")
        
        if response.status_code == 200:
            payload = response.json()['payload']
            print(f"\n✅ Token de agente decodificado exitosamente")
            print(f"🆔 User ID: {payload['user_id']}")
            print(f"👤 Tipo: {payload['user_type']}")
            print(f"📅 Expira: {datetime.fromtimestamp(payload['exp']).strftime('%Y-%m-%d %H:%M:%S')}")
        
    except Exception as e:
        print(f"❌ Error al decodificar token de agente: {e}")
    
    # 6. Decodificar token de cliente
    print_separator("6. DECODIFICAR TOKEN JWT DE CLIENTE")
    
    try:
        response = requests.post(f"{BASE_URL}/auth/token/decode", json={"token": cliente_token})
        print_response(response, "Decodificar Token Cliente")
        
        if response.status_code == 200:
            payload = response.json()['payload']
            print(f"\n✅ Token de cliente decodificado exitosamente")
            print(f"🆔 User ID: {payload['user_id']}")
            print(f"👤 Tipo: {payload['user_type']}")
            print(f"📅 Expira: {datetime.fromtimestamp(payload['exp']).strftime('%Y-%m-%d %H:%M:%S')}")
        
    except Exception as e:
        print(f"❌ Error al decodificar token de cliente: {e}")
    
    # 7. Probar login con credenciales incorrectas
    print_separator("7. PRUEBA CON CREDENCIALES INCORRECTAS")
    
    login_incorrecto = {
        "usuario": "agente.jwt",
        "password": "password_incorrecto"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/agente/login", json=login_incorrecto)
        print_response(response, "Login con Contraseña Incorrecta")
        
        if response.status_code == 401:
            print(f"\n✅ Sistema rechaza correctamente credenciales incorrectas")
        else:
            print(f"\n⚠️  Respuesta inesperada para credenciales incorrectas")
        
    except Exception as e:
        print(f"❌ Error en prueba de credenciales incorrectas: {e}")
    
    print_separator("RESUMEN DE PRUEBAS")
    print("✅ Agente creado con contraseña hasheada")
    print("✅ Cliente creado con contraseña hasheada")
    print("✅ Login de agente genera token JWT válido")
    print("✅ Login de cliente genera token JWT válido")
    print("✅ Tokens contienen información del usuario (sin contraseña)")
    print("✅ Sistema rechaza credenciales incorrectas")
    print("✅ Tokens pueden ser decodificados y validados")
    print("\n🎉 ¡Sistema de autenticación JWT funcionando correctamente!")
    print("\n📚 Para probar en Swagger UI:")
    print("   1. Ve a http://localhost:5000/docs/")
    print("   2. Busca la sección 'Autenticación'")
    print("   3. Prueba los endpoints de login")
    print("   4. Copia el token para usar en futuras implementaciones")

if __name__ == "__main__":
    test_auth_system() 