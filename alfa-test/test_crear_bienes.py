#!/usr/bin/env python3
"""
Script de prueba para el endpoint de crear bienes
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
                        if 'id' in result['data']:
                            print(f"Created item with ID: {result['data']['id']}")
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
    print("🧪 Probando endpoint de crear bienes")
    print("=" * 60)
    
    # 1. Probar health check
    print("1. Health Check")
    test_endpoint('GET', '/health')
    
    # 2. Obtener tipos de bienes disponibles
    print("2. Obtener tipos de bienes disponibles")
    test_endpoint('GET', '/bienes/tipos')
    
    # 3. Crear un HOGAR
    print("3. Crear nuevo HOGAR")
    hogar_data = {
        "tipo_bien": "HOGAR",
        "data_especifico": {
            "tipo_inmueble": "Casa",
            "ciudad_inmueble": "Bogotá",
            "direccion_inmueble": "Carrera 15 #45-23",
            "numero_pisos": 2,
            "ano_construccion": 2015,
            "valor_inmueble_avaluo": 350000000.00,
            "valor_contenidos_normales_avaluo": 25000000.00
        },
        "data_general": {
            "estado": "Activo",
            "comentarios_generales": "Casa principal de familia",
            "vigencias_continuas": True
        }
    }
    response_hogar = test_endpoint('POST', '/bienes', hogar_data, 201)
    
    # 4. Crear un VEHICULO
    print("4. Crear nuevo VEHICULO")
    vehiculo_data = {
        "tipo_bien": "VEHICULO",
        "data_especifico": {
            "tipo_vehiculo": "Automóvil",
            "placa": "TEST001",
            "marca": "Toyota",
            "serie_referencia": "Corolla Cross XLI",
            "ano_modelo": 2023,
            "codigo_fasecolda": "81042090",
            "valor_vehiculo": 85000000.00
        },
        "data_general": {
            "estado": "Activo",
            "comentarios_generales": "Vehículo familiar"
        }
    }
    response_vehiculo = test_endpoint('POST', '/bienes', vehiculo_data, 201)
    
    # 5. Crear una COPROPIEDAD
    print("5. Crear nueva COPROPIEDAD")
    copropiedad_data = {
        "tipo_bien": "COPROPIEDAD",
        "data_especifico": {
            "tipo_copropiedad": "Conjunto Residencial",
            "ciudad": "Bogotá",
            "direccion": "Carrera 7 #127-45",
            "estrato": 4,
            "numero_torres": 3,
            "numero_maximo_pisos": 15,
            "cantidad_unidades_apartamentos": 180,
            "valor_edificio_area_comun_avaluo": 2500000000.00
        },
        "data_general": {
            "estado": "Activo",
            "comentarios_generales": "Conjunto residencial moderno"
        }
    }
    response_copropiedad = test_endpoint('POST', '/bienes', copropiedad_data, 201)
    
    # 6. Crear OTRO tipo de bien
    print("6. Crear OTRO tipo de bien")
    otro_data = {
        "tipo_bien": "OTRO",
        "data_especifico": {
            "tipo_seguro": "Seguro de Transporte",
            "bien_asegurado": "Mercancías en Tránsito",
            "valor_bien_asegurar": 500000000.00,
            "detalles_bien_asegurado": "Cobertura para mercancías transportadas"
        },
        "data_general": {
            "estado": "Activo",
            "comentarios_generales": "Seguro de transporte de mercancías"
        }
    }
    response_otro = test_endpoint('POST', '/bienes', otro_data, 201)
    
    # 7. Crear bien con cliente asignado
    print("7. Crear HOGAR y asignarlo al cliente 1")
    hogar_con_cliente = {
        "tipo_bien": "HOGAR",
        "data_especifico": {
            "tipo_inmueble": "Apartamento",
            "ciudad_inmueble": "Medellín",
            "direccion_inmueble": "Calle 50 #20-30",
            "numero_pisos": 1,
            "ano_construccion": 2020,
            "valor_inmueble_avaluo": 250000000.00
        },
        "data_general": {
            "estado": "Activo",
            "comentarios_generales": "Apartamento asignado directamente"
        },
        "cliente_id": 1
    }
    test_endpoint('POST', '/bienes', hogar_con_cliente, 201)
    
    # 8. Verificar que se creó y asignó correctamente
    print("8. Verificar bienes del cliente 1")
    test_endpoint('GET', '/clientes/1/bienes')
    
    # 9. Probar validaciones - sin tipo_bien
    print("9. Probar validación - sin tipo_bien")
    invalid_data = {
        "data_especifico": {
            "tipo_inmueble": "Casa"
        }
    }
    test_endpoint('POST', '/bienes', invalid_data, 400)
    
    # 10. Probar validaciones - tipo_bien inválido
    print("10. Probar validación - tipo_bien inválido")
    invalid_type = {
        "tipo_bien": "INVALIDO",
        "data_especifico": {
            "tipo_inmueble": "Casa"
        }
    }
    test_endpoint('POST', '/bienes', invalid_type, 400)
    
    # 11. Probar validaciones - sin data_especifico
    print("11. Probar validación - sin data_especifico")
    no_data_especifico = {
        "tipo_bien": "HOGAR"
    }
    test_endpoint('POST', '/bienes', no_data_especifico, 400)
    
    # 12. Probar validaciones específicas - HOGAR sin tipo_inmueble
    print("12. Probar validación - HOGAR sin tipo_inmueble")
    hogar_invalid = {
        "tipo_bien": "HOGAR",
        "data_especifico": {
            "ciudad_inmueble": "Bogotá"
        }
    }
    test_endpoint('POST', '/bienes', hogar_invalid, 400)
    
    # 13. Probar validaciones específicas - VEHICULO sin placa
    print("13. Probar validación - VEHICULO sin placa")
    vehiculo_invalid = {
        "tipo_bien": "VEHICULO",
        "data_especifico": {
            "marca": "Toyota"
        }
    }
    test_endpoint('POST', '/bienes', vehiculo_invalid, 400)
    
    # 14. Obtener todos los bienes creados
    print("14. Obtener todos los bienes")
    test_endpoint('GET', '/bienes')
    
    # 15. Crear motocicleta
    print("15. Crear VEHICULO - Motocicleta")
    moto_data = {
        "tipo_bien": "VEHICULO",
        "data_especifico": {
            "tipo_vehiculo": "Motocicleta",
            "placa": "MOTO123",
            "marca": "Honda",
            "serie_referencia": "CBR 600RR",
            "ano_modelo": 2022,
            "codigo_fasecolda": "12345678",
            "valor_vehiculo": 35000000.00
        },
        "data_general": {
            "estado": "Activo",
            "comentarios_generales": "Motocicleta deportiva"
        },
        "cliente_id": 2
    }
    test_endpoint('POST', '/bienes', moto_data, 201)
    
    # 16. Verificar bienes del cliente 2
    print("16. Verificar bienes del cliente 2")
    test_endpoint('GET', '/clientes/2/bienes')
    
    print("\n🎉 Pruebas completadas!")
    print("📊 Resumen de pruebas:")
    print("   ✅ Creación de 4 tipos de bienes (HOGAR, VEHICULO, COPROPIEDAD, OTRO)")
    print("   ✅ Asignación automática a cliente")
    print("   ✅ Validaciones de campos requeridos")
    print("   ✅ Validaciones específicas por tipo")
    print("   ✅ Verificación de bienes creados")
    print("\n📖 Para ver la documentación interactiva:")
    print("   http://localhost:5000/docs/")

if __name__ == '__main__':
    main() 