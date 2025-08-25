-- Datos de ejemplo para bienes

-- Insertar hogares de ejemplo
INSERT INTO hogares (tipo_inmueble, ciudad_inmueble, direccion_inmueble, numero_pisos, ano_construccion, valor_inmueble_avaluo, valor_contenidos_normales_avaluo, valor_contenidos_especiales_avaluo, valor_equipo_electronico_avaluo, valor_maquinaria_equipo_avaluo) VALUES
('Casa', 'Bogotá', 'Carrera 15 #45-23', 2, 2015, 350000000.00, 25000000.00, 10000000.00, 8000000.00, 5000000.00),
('Apartamento', 'Medellín', 'Calle 70 #52-14 Apt 502', 1, 2018, 280000000.00, 20000000.00, 8000000.00, 6000000.00, 3000000.00),
('Casa', 'Cali', 'Avenida 6N #23-45', 1, 2010, 220000000.00, 15000000.00, 5000000.00, 4000000.00, 2000000.00),
('Apartamento', 'Barranquilla', 'Carrera 53 #75-89 Apt 301', 1, 2020, 180000000.00, 18000000.00, 7000000.00, 5000000.00, 2500000.00),
('Casa', 'Bucaramanga', 'Calle 42 #18-67', 2, 2012, 290000000.00, 22000000.00, 9000000.00, 7000000.00, 4000000.00);

-- Insertar vehículos de ejemplo
INSERT INTO vehiculos (tipo_vehiculo, placa, marca, serie_referencia, ano_modelo, ano_nacimiento_conductor, codigo_fasecolda, valor_vehiculo, valor_accesorios_avaluo) VALUES
('Automóvil', 'ABC123', 'Toyota', 'Corolla Cross XLI', 2023, 1985, '81042090', 85000000.00, 3000000.00),
('Motocicleta', 'DEF456', 'Yamaha', 'MT-03', 2022, 1990, '20100190', 18000000.00, 1000000.00),
('Automóvil', 'GHI789', 'Chevrolet', 'Spark GT', 2021, 1988, '81008090', 45000000.00, 2000000.00),
('Camioneta', 'JKL012', 'Ford', 'Ranger XLT', 2022, 1982, '81080090', 120000000.00, 5000000.00),
('Automóvil', 'MNO345', 'Nissan', 'Sentra Advance', 2023, 1987, '81020090', 75000000.00, 2500000.00);

-- Insertar copropiedades de ejemplo
INSERT INTO copropiedades (tipo_copropiedad, ciudad, direccion, estrato, ano_construccion, numero_torres, numero_maximo_pisos, numero_maximo_sotanos, cantidad_unidades_casa, cantidad_unidades_apartamentos, cantidad_unidades_locales, cantidad_unidades_oficinas, cantidad_unidades_otros, valor_edificio_area_comun_avaluo, valor_edificio_area_privada_avaluo, valor_maquinaria_equipo_avaluo, valor_equipo_electrico_electronico_avaluo, valor_muebles_avaluo) VALUES
('Conjunto Residencial', 'Bogotá', 'Carrera 7 #127-45', 4, 2019, 3, 15, 2, 0, 180, 8, 2, 4, 2500000000.00, 8500000000.00, 150000000.00, 200000000.00, 300000000.00),
('Edificio Comercial', 'Medellín', 'Calle 50 #46-78', 5, 2020, 1, 20, 3, 0, 0, 25, 45, 10, 1800000000.00, 6200000000.00, 300000000.00, 400000000.00, 250000000.00),
('Conjunto Cerrado', 'Cali', 'Avenida 5N #18-90', 3, 2017, 2, 8, 1, 24, 96, 4, 1, 2, 1200000000.00, 4800000000.00, 80000000.00, 120000000.00, 180000000.00);

-- Insertar otros bienes de ejemplo
INSERT INTO otros_bienes (tipo_seguro, bien_asegurado, valor_bien_asegurar, detalles_bien_asegurado) VALUES
('Seguro de Transporte', 'Mercancías en Tránsito', 500000000.00, 'Cobertura para mercancías transportadas por carretera entre Bogotá y Medellín'),
('Seguro de Responsabilidad Civil', 'Actividades Profesionales', 200000000.00, 'Cobertura para consultores en tecnología y desarrollo de software'),
('Seguro de Equipos', 'Maquinaria Industrial', 800000000.00, 'Equipos de manufactura textil ubicados en planta de Pereira'),
('Seguro de Manejo', 'Fidelidad y Manejo', 100000000.00, 'Cobertura para empleados que manejan dinero en efectivo'),
('Seguro de Incendio', 'Bodega de Almacenamiento', 300000000.00, 'Bodega con productos químicos en zona industrial de Barranquilla');

-- Crear bienes principales (polimórficos)
INSERT INTO bienes (tipo_bien, bien_especifico_id, estado, comentarios_generales, vigencias_continuas) VALUES
-- Hogares
('HOGAR', 1, 'Activo', 'Casa principal de familia en excelente estado', TRUE),
('HOGAR', 2, 'Activo', 'Apartamento moderno con acabados de lujo', TRUE),
('HOGAR', 3, 'Activo', 'Casa familiar tradicional', TRUE),
('HOGAR', 4, 'Activo', 'Apartamento nuevo con garantía de construcción', TRUE),
('HOGAR', 5, 'Activo', 'Casa con amplio jardín y zona social', TRUE),

-- Vehículos
('VEHICULO', 1, 'Activo', 'Vehículo familiar en excelentes condiciones', TRUE),
('VEHICULO', 2, 'Activo', 'Motocicleta para uso urbano', TRUE),
('VEHICULO', 3, 'Activo', 'Vehículo económico ideal para ciudad', TRUE),
('VEHICULO', 4, 'Activo', 'Camioneta de trabajo y uso familiar', TRUE),
('VEHICULO', 5, 'Activo', 'Sedán ejecutivo con tecnología avanzada', TRUE),

-- Copropiedades
('COPROPIEDAD', 1, 'Activo', 'Conjunto residencial de alto nivel', TRUE),
('COPROPIEDAD', 2, 'Activo', 'Edificio comercial en zona céntrica', TRUE),
('COPROPIEDAD', 3, 'Activo', 'Conjunto familiar con zonas comunes', TRUE),

-- Otros bienes
('OTRO', 1, 'Activo', 'Póliza para transporte de mercancías', TRUE),
('OTRO', 2, 'Activo', 'Cobertura profesional para consultores', TRUE),
('OTRO', 3, 'Activo', 'Seguro para maquinaria especializada', TRUE),
('OTRO', 4, 'Activo', 'Póliza de fidelidad para empleados', TRUE),
('OTRO', 5, 'Activo', 'Seguro específico para bodega industrial', TRUE);

-- Asignar bienes a clientes (ejemplos)
INSERT INTO clientes_bienes (cliente_id, bien_id) VALUES
-- Cliente 1 (Juan Pérez) tiene casa y carro
(1, 1), (1, 6),
-- Cliente 2 (María García) tiene apartamento y moto
(2, 2), (2, 7),
-- Cliente 3 (Carlos López) tiene casa y camioneta
(3, 3), (3, 9),
-- Cliente 4 (Ana Martínez) tiene apartamento y sedán
(4, 4), (4, 10),
-- Cliente 5 (Luis Rodríguez) tiene casa
(5, 5),
-- Cliente 6 (Empresa ABC) tiene edificio comercial y seguros
(6, 12), (6, 15), (6, 16),
-- Cliente 7 (Transportes XYZ) tiene vehículo comercial y seguro de transporte
(7, 9), (7, 14),
-- Cliente 8 (Constructora DEF) tiene conjunto residencial
(8, 11),
-- Cliente 9 (Tech Solutions) tiene seguros profesionales
(9, 15), (9, 17),
-- Cliente 10 (Manufacturas GHI) tiene maquinaria y seguro industrial
(10, 16), (10, 18); 