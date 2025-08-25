-- Archivo de datos de prueba extendidos para alfa_db
-- Ejecutar después de init.sql para tener más datos de prueba

USE alfa_db;

-- Insertar más agentes con diferentes roles
INSERT INTO Agente (nombre, correo, usuario, clave, rol, activo) VALUES
-- Administradores
('Carlos Rodríguez', 'carlos.rodriguez@alfa.com', 'carlos.rodriguez', 'admin456', 'admin', TRUE),
('Ana Sofia Mendoza', 'ana.mendoza@alfa.com', 'ana.mendoza', 'admin789', 'admin', TRUE),
('Luis Fernando Torres', 'luis.torres@alfa.com', 'luis.torres', 'admin321', 'admin', FALSE), -- Inactivo

-- Agentes regulares
('Patricia Jiménez', 'patricia.jimenez@alfa.com', 'patricia.jimenez', 'agente456', 'agente', TRUE),
('Roberto Castillo', 'roberto.castillo@alfa.com', 'roberto.castillo', 'agente789', 'agente', TRUE),
('Mónica Vargas', 'monica.vargas@alfa.com', 'monica.vargas', 'agente321', 'agente', TRUE),
('Daniel Herrera', 'daniel.herrera@alfa.com', 'daniel.herrera', 'agente654', 'agente', TRUE),
('Isabella Cruz', 'isabella.cruz@alfa.com', 'isabella.cruz', 'agente987', 'agente', FALSE), -- Inactiva
('Alejandro Morales', 'alejandro.morales@alfa.com', 'alejandro.morales', 'agente147', 'agente', TRUE),
('Valentina Ospina', 'valentina.ospina@alfa.com', 'valentina.ospina', 'agente258', 'agente', TRUE);

-- Insertar más clientes - Personas Naturales
INSERT INTO clientes (tipo_cliente, usuario, clave, nombre, tipo_documento, numero_documento, correo, telefono_movil, ciudad, direccion, edad) VALUES
('PERSONA', 'felipe.santos', 'cliente456', 'Felipe Santos Restrepo', 'CC', '98765432', 'felipe.santos@gmail.com', '3012345678', 'Bogotá', 'Carrera 15 #85-32', 28),
('PERSONA', 'laura.ramirez', 'cliente789', 'Laura Ramírez Vélez', 'CC', '11223344', 'laura.ramirez@hotmail.com', '3023456789', 'Medellín', 'Calle 70 #45-12', 35),
('PERSONA', 'diego.moreno', 'cliente321', 'Diego Moreno Castro', 'CC', '55667788', 'diego.moreno@yahoo.com', '3034567890', 'Cali', 'Avenida 5N #23-45', 42),
('PERSONA', 'camila.torres', 'cliente654', 'Camila Torres Giraldo', 'CC', '99887766', 'camila.torres@gmail.com', '3045678901', 'Barranquilla', 'Calle 84 #52-18', 26),
('PERSONA', 'andres.lopez', 'cliente987', 'Andrés López Fernández', 'CE', '123456789', 'andres.lopez@outlook.com', '3056789012', 'Cartagena', 'Barrio Getsemaní #12-34', 31),
('PERSONA', 'sofia.martinez', 'cliente147', 'Sofía Martínez Ruiz', 'CC', '77788899', 'sofia.martinez@gmail.com', '3067890123', 'Bucaramanga', 'Carrera 27 #34-56', 29),
('PERSONA', 'miguel.hernan', 'cliente258', 'Miguel Hernández Silva', 'CC', '44455566', 'miguel.hernan@hotmail.com', '3078901234', 'Pereira', 'Calle 14 #7-89', 38),
('PERSONA', 'natalia.gomez', 'cliente369', 'Natalia Gómez Aguilar', 'CC', '66677788', 'natalia.gomez@gmail.com', '3089012345', 'Manizales', 'Carrera 23 #65-12', 24),
('PERSONA', 'sebastian.cruz', 'cliente741', 'Sebastián Cruz Delgado', 'TI', '1234567890', 'sebastian.cruz@yahoo.com', '3090123456', 'Santa Marta', 'Calle 22 #3-45', 19),
('PERSONA', 'gabriela.vega', 'cliente852', 'Gabriela Vega Montoya', 'CC', '33344455', 'gabriela.vega@outlook.com', '3101234567', 'Ibagué', 'Carrera 5 #33-78', 33);

-- Insertar más clientes - Empresas
INSERT INTO clientes (tipo_cliente, usuario, clave, nit, razon_social, nombre_rep_legal, documento_rep_legal, correo, telefono_movil, ciudad, direccion, telefono_rep_legal, correo_rep_legal, contacto_alternativo) VALUES
('EMPRESA', 'innovatech.sas', 'empresa456', '900234567', 'InnovaTech Solutions S.A.S.', 'Fernando Ramírez Soto', '12345678', 'info@innovatech.co', '3201234567', 'Bogotá', 'Zona Rosa, Calle 82 #11-45', '3111234567', 'fernando.ramirez@innovatech.co', 'Contacto comercial: comercial@innovatech.co'),
('EMPRESA', 'comercial.andina', 'empresa789', '800345678', 'Comercializadora Andina Ltda.', 'María Elena Vargas', '23456789', 'contacto@andina.com.co', '3212345678', 'Medellín', 'El Poblado, Carrera 43A #5-15', '3122345678', 'maria.vargas@andina.com.co', 'Gerente comercial: ventas@andina.com.co'),
('EMPRESA', 'logistica.caribe', 'empresa321', '900456789', 'Logística del Caribe S.A.', 'Jorge Luis Mendoza', '34567890', 'admin@logcaribe.co', '3223456789', 'Barranquilla', 'Centro, Carrera 44 #32-76', '3133456789', 'jorge.mendoza@logcaribe.co', 'Coordinador operativo: operaciones@logcaribe.co'),
('EMPRESA', 'agro.valle', 'empresa654', '800567890', 'AgroValle Productores Unidos', 'Carmen Rosa Delgado', '45678901', 'gerencia@agrovalle.co', '3234567890', 'Cali', 'Sur de Cali, Calle 5 #70-23', '3144567890', 'carmen.delgado@agrovalle.co', 'Jefe de producción: produccion@agrovalle.co'),
('EMPRESA', 'textiles.norte', 'empresa987', '900678901', 'Textiles del Norte S.A.S.', 'Ricardo Andrés Gómez', '56789012', 'info@textilesnorte.com', '3245678901', 'Bucaramanga', 'Zona Industrial, Carrera 15 #45-67', '3155678901', 'ricardo.gomez@textilesnorte.com', 'Supervisor de calidad: calidad@textilesnorte.com'),
('EMPRESA', 'minera.cordillera', 'empresa147', '800789012', 'Minera Cordillera Ltda.', 'Ana Lucía Herrera', '67890123', 'contacto@mineracordillera.co', '3256789012', 'Pereira', 'Sector La Virginia, Km 5 Vía Dosquebradas', '3166789012', 'ana.herrera@mineracordillera.co', 'Jefe de operaciones: ops@mineracordillera.co'),
('EMPRESA', 'construcciones.pacifico', 'empresa258', '900890123', 'Construcciones del Pacífico S.A.', 'Esteban Torres Ruiz', '78901234', 'ventas@conspacifico.co', '3267890123', 'Buenaventura', 'Centro, Calle 2 #4-56', '3177890123', 'esteban.torres@conspacifico.co', 'Arquitecto principal: proyectos@conspacifico.co'),
('EMPRESA', 'alimentos.tropical', 'empresa369', '800901234', 'Alimentos Tropical Ltda.', 'Claudia Patricia Rojas', '89012345', 'admin@tropical.com.co', '3278901234', 'Villavicencio', 'Zona Industrial, Carrera 35 #12-34', '3188901234', 'claudia.rojas@tropical.com.co', 'Control de calidad: calidad@tropical.com.co'),
('EMPRESA', 'energia.renovable', 'empresa741', '900012345', 'Energía Renovable del Futuro S.A.S.', 'Mauricio Jiménez León', '90123456', 'info@energiarenovable.co', '3289012345', 'Manizales', 'Sector Universitario, Calle 65 #23-14', '3199012345', 'mauricio.jimenez@energiarenovable.co', 'Ingeniero jefe: ingenieria@energiarenovable.co'),
('EMPRESA', 'turismo.magdalena', 'empresa852', '800123456', 'Turismo Río Magdalena Ltda.', 'Gloria Esperanza Castro', '01234567', 'reservas@turismomagdalena.co', '3290123456', 'Honda', 'Malecón del Río, Calle 10 #5-67', '3200123456', 'gloria.castro@turismomagdalena.co', 'Coordinador turístico: tours@turismomagdalena.co');

-- Crear asignaciones más complejas entre agentes y clientes
INSERT INTO agentes_clientes (agente_id, cliente_id) VALUES
-- Admin Principal (ID: 1) - Clientes empresariales importantes
(1, 6), -- Admin a Empresa ABC S.A.S.
(1, 7), -- Admin a Tech Solutions Ltda.
(1, 11), -- Admin a InnovaTech Solutions S.A.S.

-- Juan Pérez (ID: 2) - Ya tiene asignaciones, agregar más
(2, 8), -- Juan a Felipe Santos Restrepo
(2, 12), -- Juan a Comercializadora Andina Ltda.

-- María García (ID: 3) - Ya tiene asignaciones, agregar más  
(3, 9), -- María a Laura Ramírez Vélez
(3, 13), -- María a Logística del Caribe S.A.

-- Carlos Rodríguez (ID: 4) - Admin
(4, 10), -- Carlos a Diego Moreno Castro
(4, 14), -- Carlos a AgroValle Productores Unidos
(4, 15), -- Carlos a Textiles del Norte S.A.S.

-- Ana Sofia Mendoza (ID: 5) - Admin
(5, 11), -- Ana a Camila Torres Giraldo
(5, 16), -- Ana a Minera Cordillera Ltda.
(5, 17), -- Ana a Construcciones del Pacífico S.A.

-- Patricia Jiménez (ID: 7) - Agente
(7, 12), -- Patricia a Andrés López Fernández
(7, 13), -- Patricia a Sofía Martínez Ruiz
(7, 18), -- Patricia a Alimentos Tropical Ltda.

-- Roberto Castillo (ID: 8) - Agente
(8, 14), -- Roberto a Miguel Hernández Silva
(8, 15), -- Roberto a Natalia Gómez Aguilar
(8, 19), -- Roberto a Energía Renovable del Futuro S.A.S.

-- Mónica Vargas (ID: 9) - Agente
(9, 16), -- Mónica a Sebastián Cruz Delgado
(9, 17), -- Mónica a Gabriela Vega Montoya
(9, 20), -- Mónica a Turismo Río Magdalena Ltda.

-- Daniel Herrera (ID: 10) - Agente
(10, 5), -- Daniel a Carlos López (persona existente)
(10, 8), -- Daniel a Felipe Santos Restrepo

-- Alejandro Morales (ID: 12) - Agente
(12, 18), -- Alejandro a Alimentos Tropical (compartido)
(12, 6), -- Alejandro a Empresa ABC (compartido)

-- Valentina Ospina (ID: 13) - Agente
(13, 19), -- Valentina a Energía Renovable (compartido)
(13, 4); -- Valentina a Ana Martínez (persona existente)

-- Estadísticas finales tras insertar esta data:
-- Total Agentes: 13 (3 originales + 10 nuevos)
-- Total Clientes: 24 (4 originales + 20 nuevos)
-- Total Asignaciones: Aproximadamente 35+ asignaciones
-- Distribución: ~14 personas naturales, ~10 empresas
-- Roles: 1 super_admin, 4 admins, 8 agentes activos, 2 inactivos 