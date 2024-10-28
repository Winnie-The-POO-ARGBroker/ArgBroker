# Diseñar el modelo relacional de base de datos que soporte las entidades principales
# del sistema. Pueden utilizar los modelos entregados en la primera parte haciendo las
# mejoras que crean correspondiente luego de las devoluciones. El diseño debe
# contemplar lo siguiente:

CREATE DATABASE ArgBrokerDEMO;

USE ArgBrokerDEMO;

-- Creamos la tabla tipos_documentos
CREATE TABLE tipos_documentos(
    id_tipo_documento INT AUTO_INCREMENT PRIMARY KEY,
    tipo_documento VARCHAR(20)
);

-- Creamos la tabla usuarios
CREATE TABLE usuarios(
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    contrasena VARCHAR(60) NOT NULL,
    documento VARCHAR(20) UNIQUE,
    email VARCHAR(50) UNIQUE,
    nombre_usuario VARCHAR(50),
    id_tipo_documento INT,
    FOREIGN KEY (id_tipo_documento) REFERENCES tipos_documentos(id_tipo_documento)
);

-- Creamos la tabla cuentas 
CREATE TABLE cuentas (
    id_cuenta INT AUTO_INCREMENT PRIMARY KEY,
    numero_cuenta VARCHAR(20) UNIQUE NOT NULL,
    saldo DECIMAL(10, 2) NOT NULL,
    id_usuario INT,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
);

-- Creamos la tabla acciones
CREATE TABLE acciones(
    id_accion INT AUTO_INCREMENT PRIMARY KEY,
    simbolo VARCHAR(50) UNIQUE,
    nombre_empresa VARCHAR(50),
    precio_compra DECIMAL(10, 2),
    precio_venta DECIMAL(10, 2)
);

-- Creamos la tabla portafolio
CREATE TABLE portafolio(
    id_usuario INT,
    id_accion INT,
    cantidad_acciones INT,
    precio_compra DECIMAL(10, 2),
    precio_venta DECIMAL(10, 2),
    PRIMARY KEY (id_usuario, id_accion),
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario),
    FOREIGN KEY (id_accion) REFERENCES acciones(id_accion)
);

-- Creamos la tabla tipos_transacciones
CREATE TABLE tipos_transacciones (
    id_tipo_transaccion INT AUTO_INCREMENT PRIMARY KEY,
    nombre_transaccion VARCHAR(50)
);

-- Creamos la tabla transacciones
CREATE TABLE transacciones(
    id_transaccion INT AUTO_INCREMENT PRIMARY KEY,
    cantidad_acciones INT,
    monto_total DECIMAL(10, 2),
    comision DECIMAL(10,2),
    fecha_hora DATETIME,
    numero_cuenta VARCHAR(20),
    id_tipo_transaccion INT,
    id_accion INT,
    FOREIGN KEY (numero_cuenta) REFERENCES cuentas(numero_cuenta),
    FOREIGN KEY (id_tipo_transaccion) REFERENCES tipos_transacciones(id_tipo_transaccion),
    FOREIGN KEY (id_accion) REFERENCES acciones (id_accion)
);

-- 3. Escribe un conjunto de sentencias DML de tipo INSERT que inserten datos iniciales
-- en la base de datos.

INSERT INTO tipos_documentos 
VALUES (1, "CUIL"), (2, "CUIT"), (3, "PASAPORTE");

INSERT INTO acciones (simbolo, nombre_empresa, precio_compra, precio_venta) 
VALUES 
('AAPL', 'Apple Inc.', 150.00, 155.00),
('EA', 'Electronic Arts Inc.', 130.00, 135.00),
('AMZN', 'Amazon.com Inc.', 3400.00, 3450.00),
('MSFT', 'Microsoft Corp.', 295.00, 300.00),
('TSLA', 'Tesla Inc.', 720.00, 730.00),
('META', 'Meta Platforms Inc.', 330.00, 335.00),
('NFLX', 'Netflix Inc.', 550.00, 560.00),
('NVDA', 'NVIDIA Corp.', 600.00, 610.00),
('PYPL', 'PayPal Holdings Inc.', 270.00, 275.00),
('ADBE', 'Adobe Inc.', 630.00, 640.00);

INSERT INTO tipos_transacciones (id_tipo_transaccion, nombre_transaccion) 
VALUES 
(1, 'Compra'), (2,'Venta');

INSERT INTO usuarios (contrasena, documento, email, nombre_usuario, id_tipo_documento) 
VALUES 
('Eliana09*', '20207777772', 'elianad@gmail.com', 'Eliana', 1),
('Franco07*', '20222222222', 'francoa@gmail.com', 'Franco', 1);

INSERT INTO cuentas 
VALUES 
(1, 'RCPCGNH1BYQGNUMNR54Z', 927221.25, 1),
(2, 'VI0FWANKSQK7XARBFKGZ', 996038.50, 2);

INSERT INTO transacciones (cantidad_acciones, monto_total, comision, fecha_hora, numero_cuenta, id_tipo_transaccion, id_accion) 
VALUES 
(10, 1500.00, 15.00, '2024-01-01 10:00:00', 'RCPCGNH1BYQGNUMNR54Z', 1, 1);

INSERT INTO portafolio (id_usuario, id_accion, cantidad_acciones, precio_compra, precio_venta) 
VALUES
(1, 1, 10, 150.00, 155.00),   -- Usuario 1 compró 10 acciones de Apple
(1, 3, 5, 3400.00, 3450.00),  -- Usuario 1 compró 5 acciones de Amazon
(2, 2, 8, 130.00, 135.00);    -- Usuario 2 compró 8 acciones de Electronic Arts

-- Selects
select * from usuarios;
select * from cuentas;
select * from tipos_documentos;
select * from tipos_transacciones;
select * from transacciones;
select * from acciones;
select * from portafolio;

-- Consultas utiles
