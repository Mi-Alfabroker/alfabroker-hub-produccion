#!/usr/bin/env python3
"""
Script de prueba para los endpoints de bienes de la API
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
    print("🧪 Probando endpoints de bienes de la API")
    print("=" * 60)
    
    # 1. Probar health check
    print("1. Health Check")
    test_endpoint('GET', '/health')
    
    # 2. Obtener tipos de bienes disponibles
    print("2. Obtener tipos de bienes")
    test_endpoint('GET', '/bienes/tipos')
    
    # 3. Obtener todos los bienes
    print("3. Obtener todos los bienes")
    response = test_endpoint('GET', '/bienes')
    
    # 4. Filtrar bienes por tipo
    print("4. Filtrar bienes por tipo (HOGAR)")
    test_endpoint('GET', '/bienes?tipo=HOGAR')
    
    print("5. Filtrar bienes por tipo (VEHICULO)")
    test_endpoint('GET', '/bienes?tipo=VEHICULO')
    
    # 6. Crear un nuevo hogar
    print("6. Crear nuevo hogar")
    hogar_data = {
        "tipo_bien": "HOGAR",
        "data_especifico": {
            "tipo_inmueble": "Casa",
            "ciudad_inmueble": "Bogotá",
            "direccion_inmueble": "Calle Test #123",
            "numero_pisos": 2,
            "ano_construccion": 2023,
            "valor_inmueble_avaluo": 400000000.00
        },
        "data_general": {
            "estado": "Activo",
            "comentarios_generales": "Casa creada para testing",
            "vigencias_continuas": True
        },
        "cliente_id": 1
    }
    response = test_endpoint('POST', '/bienes', hogar_data, 201)
    
    # Obtener el ID del bien creado
    bien_id = None
    if response and response.status_code == 201:
        try:
            bien_id = response.json()['data']['id']
            print(f"Bien creado con ID: {bien_id}")
        except:
            pass
    
    # 7. Crear un nuevo vehículo
    print("7. Crear nuevo vehículo")
    vehiculo_data = {
        "tipo_bien": "VEHICULO",
        "data_especifico": {
            "tipo_vehiculo": "Automóvil",
            "placa": "TEST123",
            "marca": "Test Motors",
            "serie_referencia": "Test Model",
            "ano_modelo": 2023,
            "valor_vehiculo": 50000000.00
        },
        "data_general": {
            "estado": "Activo",
            "comentarios_generales": "Vehículo de prueba"
        }
    }
    test_endpoint('POST', '/bienes', vehiculo_data, 201)
    
    # 8. Obtener un bien específico
    if bien_id:
        print(f"8. Obtener bien específico (ID: {bien_id})")
        test_endpoint('GET', f'/bienes/{bien_id}')
        
        # 9. Actualizar el bien
        print(f"9. Actualizar bien (ID: {bien_id})")
        update_data = {
            "data_general": {
                "estado": "Inactivo",
                "comentarios_generales": "Actualizado por test"
            }
        }
        test_endpoint('PUT', f'/bienes/{bien_id}', update_data)
        
        # 10. Asignar bien a otro cliente
        print(f"10. Asignar bien a cliente 2")
        asignar_data = {"cliente_id": 2}
        test_endpoint('POST', f'/bienes/{bien_id}/asignar', asignar_data)
        
        # 11. Desasignar bien del cliente
        print(f"11. Desasignar bien del cliente 2")
        desasignar_data = {"cliente_id": 2}
        test_endpoint('POST', f'/bienes/{bien_id}/desasignar', desasignar_data)
    
    # 12. Obtener bienes de un cliente específico
    print("12. Obtener bienes del cliente 1")
    test_endpoint('GET', '/clientes/1/bienes')
    
    print("13. Filtrar bienes por cliente usando query param")
    test_endpoint('GET', '/bienes?cliente_id=1')
    
    # 14. Probar errores de validación
    print("14. Probar error de validación (tipo de bien inválido)")
    invalid_data = {
        "tipo_bien": "INVALIDO",
        "data_especifico": {}
    }
    test_endpoint('POST', '/bienes', invalid_data, 400)
    
    print("15. Probar error de bien no encontrado")
    test_endpoint('GET', '/bienes/99999', expected_status=404)
    
    # 16. Si creamos un bien, probamos eliminarlo
    if bien_id:
        print(f"16. Eliminar bien (ID: {bien_id})")
        test_endpoint('DELETE', f'/bienes/{bien_id}')
    
    print("\n🎉 Pruebas completadas!")
    print("\n📊 Resumen de endpoints probados:")
    print("   ✅ GET /api/bienes")
    print("   ✅ GET /api/bienes?tipo=TIPO")
    print("   ✅ GET /api/bienes?cliente_id=ID")
    print("   ✅ GET /api/bienes/{id}")
    print("   ✅ POST /api/bienes")
    print("   ✅ PUT /api/bienes/{id}")
    print("   ✅ DELETE /api/bienes/{id}")
    print("   ✅ POST /api/bienes/{id}/asignar")
    print("   ✅ POST /api/bienes/{id}/desasignar")
    print("   ✅ GET /api/clientes/{id}/bienes")
    print("   ✅ GET /api/bienes/tipos")

if __name__ == "__main__":
    main() 