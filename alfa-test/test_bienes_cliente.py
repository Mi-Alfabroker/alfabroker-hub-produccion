#!/usr/bin/env python3
"""
Script de prueba para el endpoint de bienes asignados a un cliente
"""

import requests
import json
import sys

BASE_URL = "http://localhost:5000/api"

def test_endpoint(method, endpoint, data=None, expected_status=200):
    """Función auxiliar para probar endpoints"""
    url = f"{BASE_URL}{endpoint}"
    
    try:
        if method == 'GET':
            response = requests.get(url)
        elif method == 'POST':
            response = requests.post(url, json=data)
        elif method == 'PUT':
            response = requests.put(url, json=data)
        elif method == 'DELETE':
            response = requests.delete(url)
        
        print(f"{method} {endpoint}")
        print(f"Status: {response.status_code}")
        
        if response.status_code == expected_status:
            print("✅ OK")
        else:
            print(f"❌ Error - Expected {expected_status}, got {response.status_code}")
        
        try:
            result = response.json()
            if response.status_code < 400:
                if 'data' in result:
                    if isinstance(result['data'], list):
                        print(f"Returned {len(result['data'])} items")
                        if len(result['data']) > 0:
                            print(f"First item: {result['data'][0]}")
                    else:
                        print("Returned data object")
                    
                    # Mostrar total si existe
                    if 'total' in result:
                        print(f"Total: {result['total']} bienes")
                else:
                    print("Response:", result.get('message', 'No message'))
            else:
                print("Error:", result.get('message', 'Unknown error'))
        except:
            print("Response not JSON")
        
        print("-" * 50)
        return response
        
    except requests.exceptions.ConnectionError:
        print(f"❌ Error: No se pudo conectar a {url}")
        print("Asegúrate de que la API esté corriendo con: python run_api.py")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def main():
    print("🧪 Probando endpoint de bienes asignados a cliente")
    print("=" * 60)
    
    # 1. Probar health check
    print("1. Health Check")
    test_endpoint('GET', '/health')
    
    # 2. Obtener todos los clientes
    print("2. Obtener todos los clientes")
    response = test_endpoint('GET', '/clientes')
    
    # 3. Obtener bienes del cliente 1
    print("3. Obtener bienes del cliente 1")
    test_endpoint('GET', '/clientes/1/bienes')
    
    # 4. Obtener bienes del cliente 2
    print("4. Obtener bienes del cliente 2")
    test_endpoint('GET', '/clientes/2/bienes')
    
    # 5. Probar con cliente inexistente
    print("5. Probar con cliente inexistente (ID 999)")
    test_endpoint('GET', '/clientes/999/bienes')
    
    # 6. Obtener todos los bienes
    print("6. Obtener todos los bienes")
    test_endpoint('GET', '/bienes')
    
    # 7. Obtener bienes filtrados por cliente (usando query param)
    print("7. Obtener bienes filtrados por cliente 1 (usando query param)")
    test_endpoint('GET', '/bienes?cliente_id=1')
    
    # 8. Obtener tipos de bienes disponibles
    print("8. Obtener tipos de bienes disponibles")
    test_endpoint('GET', '/bienes/tipos')
    
    # 9. Crear un nuevo bien para el cliente 1
    print("9. Crear nuevo bien (HOGAR) para cliente 1")
    bien_data = {
        "tipo_bien": "HOGAR",
        "data_especifico": {
            "tipo_inmueble": "Apartamento",
            "ciudad_inmueble": "Bogotá",
            "direccion_inmueble": "Calle Test #456",
            "numero_pisos": 1,
            "ano_construccion": 2020,
            "valor_inmueble_avaluo": 250000000.00
        },
        "data_general": {
            "estado": "Activo",
            "comentarios_generales": "Apartamento creado para testing",
            "vigencias_continuas": True
        },
        "cliente_id": 1
    }
    response = test_endpoint('POST', '/bienes', bien_data, 201)
    
    # 10. Verificar que se agregó el bien al cliente
    print("10. Verificar bienes del cliente 1 después de agregar nuevo bien")
    test_endpoint('GET', '/clientes/1/bienes')
    
    # 11. Crear un vehículo para cliente 2
    print("11. Crear nuevo bien (VEHICULO) para cliente 2")
    vehiculo_data = {
        "tipo_bien": "VEHICULO",
        "data_especifico": {
            "tipo_vehiculo": "Motocicleta",
            "placa": "TEST123",
            "marca": "Honda",
            "serie_referencia": "CBR 600RR",
            "ano_modelo": 2022,
            "codigo_fasecolda": "12345678",
            "valor_vehiculo": 35000000.00
        },
        "data_general": {
            "estado": "Activo",
            "comentarios_generales": "Motocicleta de prueba"
        },
        "cliente_id": 2
    }
    test_endpoint('POST', '/bienes', vehiculo_data, 201)
    
    # 12. Verificar bienes del cliente 2
    print("12. Verificar bienes del cliente 2 después de agregar vehículo")
    test_endpoint('GET', '/clientes/2/bienes')
    
    # 13. Obtener bien específico
    print("13. Obtener bien específico (ID 1)")
    test_endpoint('GET', '/bienes/1')
    
    print("\n🎉 Pruebas completadas!")
    print("📊 Resumen de endpoints probados:")
    print("   - GET /api/clientes/{id}/bienes (principal)")
    print("   - GET /api/bienes?cliente_id={id} (alternativo)")
    print("   - POST /api/bienes (crear con cliente_id)")
    print("   - GET /api/bienes/tipos")
    print("   - GET /api/bienes/{id}")
    print("\n📖 Para ver la documentación interactiva:")
    print("   http://localhost:5000/docs/")

if __name__ == '__main__':
    main() 