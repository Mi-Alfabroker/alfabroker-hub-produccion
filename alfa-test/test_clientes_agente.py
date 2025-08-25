#!/usr/bin/env python3
"""
Script de prueba para el endpoint de clientes asignados a un agente
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
    print("🧪 Probando endpoint de clientes asignados a agente")
    print("=" * 60)
    
    # 1. Probar health check
    print("1. Health Check")
    test_endpoint('GET', '/health')
    
    # 2. Obtener todos los agentes
    print("2. Obtener todos los agentes")
    response = test_endpoint('GET', '/agentes')
    
    # 3. Obtener clientes del agente 1
    print("3. Obtener clientes del agente 1")
    test_endpoint('GET', '/agentes/1/clientes')
    
    # 4. Obtener clientes del agente 2
    print("4. Obtener clientes del agente 2")
    test_endpoint('GET', '/agentes/2/clientes')
    
    # 5. Probar con agente inexistente
    print("5. Probar con agente inexistente (ID 999)")
    test_endpoint('GET', '/agentes/999/clientes')
    
    # 6. Obtener todos los clientes
    print("6. Obtener todos los clientes")
    response = test_endpoint('GET', '/clientes')
    
    # 7. Obtener agentes del cliente 1
    print("7. Obtener agentes del cliente 1")
    test_endpoint('GET', '/clientes/1/agentes')
    
    # 8. Obtener todas las asignaciones
    print("8. Obtener todas las asignaciones")
    test_endpoint('GET', '/asignaciones')
    
    # 9. Probar asignación de cliente a agente
    print("9. Asignar cliente 1 a agente 1")
    test_endpoint('POST', '/agentes/1/clientes/1', expected_status=201)
    
    # 10. Verificar que se creó la asignación
    print("10. Verificar clientes del agente 1 después de asignación")
    test_endpoint('GET', '/agentes/1/clientes')
    
    # 11. Desasignar cliente de agente
    print("11. Desasignar cliente 1 del agente 1")
    test_endpoint('DELETE', '/agentes/1/clientes/1')
    
    # 12. Verificar que se eliminó la asignación
    print("12. Verificar clientes del agente 1 después de desasignación")
    test_endpoint('GET', '/agentes/1/clientes')
    
    print("\n🎉 Pruebas completadas!")
    print("Para ver la documentación interactiva, ve a: http://localhost:5000/docs/")

if __name__ == '__main__':
    main() 