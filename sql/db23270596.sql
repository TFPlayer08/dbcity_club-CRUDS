-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema dbcity_club
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `dbcity_club` ;

-- -----------------------------------------------------
-- Schema dbcity_club
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `dbcity_club` DEFAULT CHARACTER SET utf8 ;
USE `dbcity_club` ;

-- -----------------------------------------------------
-- Table `dbcity_club`.`Cliente`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `dbcity_club`.`Cliente` ;

CREATE TABLE IF NOT EXISTS `dbcity_club`.`Cliente` (
  `idCliente` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(45) NOT NULL,
  `telefono` CHAR(10) NOT NULL,
  PRIMARY KEY (`idCliente`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `dbcity_club`.`Categoria`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `dbcity_club`.`Categoria` ;

CREATE TABLE IF NOT EXISTS `dbcity_club`.`Categoria` (
  `idCategoria` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`idCategoria`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `dbcity_club`.`proveedor`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `dbcity_club`.`proveedor` ;

CREATE TABLE IF NOT EXISTS `dbcity_club`.`proveedor` (
  `idproveedor` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(45) NOT NULL,
  `telefono` CHAR(10) NOT NULL,
  PRIMARY KEY (`idproveedor`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `dbcity_club`.`Unidad`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `dbcity_club`.`Unidad` ;

CREATE TABLE IF NOT EXISTS `dbcity_club`.`Unidad` (
  `idUnidad` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(25) NOT NULL,
  PRIMARY KEY (`idUnidad`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `dbcity_club`.`Articulo`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `dbcity_club`.`Articulo` ;

CREATE TABLE IF NOT EXISTS `dbcity_club`.`Articulo` (
  `codigo_articulo` CHAR(13) NOT NULL,
  `nombre` VARCHAR(45) NOT NULL,
  `precio` FLOAT NOT NULL,
  `costo` FLOAT NOT NULL,
  `existencia` INT NOT NULL,
  `idCategoria` INT NOT NULL,
  `idproveedor` INT NOT NULL,
  `idUnidad` INT NOT NULL,
  PRIMARY KEY (`codigo_articulo`),
  INDEX `fk_Articulo_Categoria1_idx` (`idCategoria` ASC) VISIBLE,
  INDEX `fk_Articulo_proveedor1_idx` (`idproveedor` ASC) VISIBLE,
  INDEX `fk_Articulo_Unidad1_idx` (`idUnidad` ASC) VISIBLE,
  CONSTRAINT `fk_Articulo_Categoria1`
    FOREIGN KEY (`idCategoria`)
    REFERENCES `dbcity_club`.`Categoria` (`idCategoria`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Articulo_proveedor1`
    FOREIGN KEY (`idproveedor`)
    REFERENCES `dbcity_club`.`proveedor` (`idproveedor`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Articulo_Unidad1`
    FOREIGN KEY (`idUnidad`)
    REFERENCES `dbcity_club`.`Unidad` (`idUnidad`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `dbcity_club`.`Membresia`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `dbcity_club`.`Membresia` ;

CREATE TABLE IF NOT EXISTS `dbcity_club`.`Membresia` (
  `codigo` CHAR(13) NOT NULL,
  `nombre_Credencial` VARCHAR(45) NOT NULL,
  `fecha_activacion` DATE NOT NULL,
  `fecha_vigencia` DATE NOT NULL,
  `tipo_membresia` ENUM('Clasica', 'Premia') NOT NULL,
  `idCliente` INT NOT NULL,
  PRIMARY KEY (`codigo`),
  INDEX `fk_Membresia_Cliente1_idx` (`idCliente` ASC) VISIBLE,
  CONSTRAINT `fk_Membresia_Cliente1`
    FOREIGN KEY (`idCliente`)
    REFERENCES `dbcity_club`.`Cliente` (`idCliente`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `dbcity_club`.`empleados`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `dbcity_club`.`empleados` ;

CREATE TABLE IF NOT EXISTS `dbcity_club`.`empleados` (
  `idempleados` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(45) NOT NULL,
  `apellido` VARCHAR(45) NOT NULL,
  `puesto` VARCHAR(45) NOT NULL,
  `sueldo` FLOAT NOT NULL,
  `edad` INT NOT NULL,
  `telefono` CHAR(10) NOT NULL,
  PRIMARY KEY (`idempleados`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `dbcity_club`.`metodo_pago`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `dbcity_club`.`metodo_pago` ;

CREATE TABLE IF NOT EXISTS `dbcity_club`.`metodo_pago` (
  `idmetodo_pago` INT NOT NULL AUTO_INCREMENT,
  `nombre_del_pago` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`idmetodo_pago`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `dbcity_club`.`ventas`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `dbcity_club`.`ventas` ;

CREATE TABLE IF NOT EXISTS `dbcity_club`.`ventas` (
  `idventas` INT NOT NULL AUTO_INCREMENT,
  `fecha` DATE NOT NULL,
  `importe` FLOAT NOT NULL,
  `idCliente` INT NOT NULL,
  `idempleados` INT NOT NULL,
  `idmetodo_pago` INT NOT NULL,
  PRIMARY KEY (`idventas`),
  INDEX `fk_ventas_Cliente1_idx` (`idCliente` ASC) VISIBLE,
  INDEX `fk_ventas_empleados1_idx` (`idempleados` ASC) VISIBLE,
  INDEX `fk_ventas_metodo_pago1_idx` (`idmetodo_pago` ASC) VISIBLE,
  CONSTRAINT `fk_ventas_Cliente1`
    FOREIGN KEY (`idCliente`)
    REFERENCES `dbcity_club`.`Cliente` (`idCliente`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_ventas_empleados1`
    FOREIGN KEY (`idempleados`)
    REFERENCES `dbcity_club`.`empleados` (`idempleados`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_ventas_metodo_pago1`
    FOREIGN KEY (`idmetodo_pago`)
    REFERENCES `dbcity_club`.`metodo_pago` (`idmetodo_pago`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `dbcity_club`.`descventa`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `dbcity_club`.`descventa` ;

CREATE TABLE IF NOT EXISTS `dbcity_club`.`descventa` (
  `idventas` INT NOT NULL,
  `codigo_articulo` CHAR(13) NOT NULL,
  `cantidad` INT NOT NULL,
  `precio` FLOAT NOT NULL,
  `total` FLOAT NOT NULL,
  PRIMARY KEY (`idventas`, `codigo_articulo`),
  INDEX `fk_descventa_Articulo1_idx` (`codigo_articulo` ASC) VISIBLE,
  CONSTRAINT `fk_descventa_ventas1`
    FOREIGN KEY (`idventas`)
    REFERENCES `dbcity_club`.`ventas` (`idventas`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_descventa_Articulo1`
    FOREIGN KEY (`codigo_articulo`)
    REFERENCES `dbcity_club`.`Articulo` (`codigo_articulo`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;


INSERT INTO proveedor (idproveedor, nombre, telefono) VALUES
(1, 'Distribuidora Central', '5512345678'),
(2, 'Alimentos del Norte', '5598765432'),
(3, 'Tecnologia MX', '5544332211'),
(4, 'Servicios Integrales', '5588997766'),
(5, 'Proveedor del Sur', '5522113344'),
(6, 'Global Trade SA', '5577889900'),
(7, 'EcoClean', '5511998877'),
(8, 'Super Suministros', '5533221100'),
(9, 'Multimarca', '5566778899'),
(10, 'Bebidas Premium', '5544556677');


INSERT INTO unidad (idUnidad, nombre) VALUES
(1, 'Pieza'),
(2, 'Caja'),
(3, 'Litro'),
(4, 'Kilogramo'),
(5, 'Paquete'),
(6, 'Metro'),
(7, 'Bolsa'),
(8, 'Galón'),
(9, 'Unidad'),
(10, 'Par');

INSERT INTO categoria (idCategoria, nombre) VALUES
(1, 'Alimentos'),
(2, 'Bebidas'),
(3, 'Limpieza'),
(4, 'Tecnologia'),
(5, 'Hogar'),
(6, 'Lacteos'),
(7, 'Aseo personal');

INSERT INTO empleados (idempleados, nombre, apellido, puesto, sueldo, edad, telefono) VALUES
(1, 'Carlos', 'Lopez', 'Cajero', 8500.00, 25, '9612345432'),
(2, 'Marta', 'Fernandez', 'Vendedora', 9000.00, 28, '5552223344'),
(3, 'Roberto', 'Garcia', 'Gerente', 15000.00, 40, '5553334455'),
(4, 'Elena', 'Mendoza', 'Auxiliar', 7800.00, 22, '5554445566'),
(5, 'Ricardo', 'Ramirez', 'Supervisor', 12000.00, 35, '5555556677'),
(6, 'Diana', 'Torres', 'Inventario', 8800.00, 27, '5556667788'),
(7, 'Hugo', 'Santos', 'Limpieza', 7000.00, 30, '5557778899'),
(8, 'Paola', 'Vega', 'Recepcionista', 8000.00, 24, '5558889900'),
(9, 'Andres', 'Cruz', 'Cajero', 8500.00, 26, '5559990011'),
(10, 'Lucia', 'Flores', 'Vendedora', 9000.00, 29, '5550001122');

INSERT INTO metodo_pago (idmetodo_pago, nombre_del_pago) VALUES
(1, 'Credito'),
(2, 'Debito'),
(3, 'Efectivo'),
(4, 'Cupones');


INSERT INTO cliente (idCliente, nombre, telefono) VALUES
(1, 'Juan Perez', '5551234567'),
(2, 'Maria Gomez', '5559876543'),
(3, 'Luis Hernandez', '5552468101'),
(4, 'Ana Torres', '5551122334'),
(5, 'Jose Martinez', '5553344556'),
(6, 'Laura Jimenez', '5557788990'),
(7, 'Pedro Sanchez', '5556655443'),
(8, 'Claudia Rios', '5557788221'),
(9, 'Miguel Diaz', '5553322110'),
(10, 'Sofia Vega', '5554433221');

INSERT INTO membresia (codigo, nombre_Credencial, fecha_activacion, fecha_vigencia, tipo_membresia, idCliente) VALUES
('5211029384756', 'Sofia Vega', '2024-10-30', '2025-10-30', 'Clasica', 10),
('5211928374650', 'Ana Torres', '2024-04-05', '2025-04-05', 'Premia', 4),
('5212309485721', 'Claudia Rios', '2024-08-10', '2025-08-10', 'Clasica', 8),
('5213849201872', 'Juan Perez', '2024-01-01', '2025-01-01', 'Clasica', 1),
('5214810293746', 'Pedro Sanchez', '2024-07-15', '2025-07-15', 'Clasica', 7),
('5215647382910', 'Jose Martinez', '2024-05-20', '2025-05-20', 'Clasica', 5),
('5217192038475', 'Laura Jimenez', '2024-06-01', '2025-06-01', 'Premia', 6),
('5218372019456', 'Maria Gomez', '2024-02-15', '2025-02-15', 'Premia', 2),
('5219384751029', 'Luis Hernandez', '2024-03-10', '2025-03-10', 'Clasica', 3),
('5219482710394', 'Miguel Diaz', '2024-09-25', '2025-09-25', 'Premia', 9);


INSERT INTO articulo (codigo_articulo, nombre, precio, costo, existencia, idCategoria, idproveedor, idUnidad) VALUES
('7501234567850', 'Flan Napolitano', 120, 30, 120, 1, 1, 1),
('7501234567893', 'Television 40 pulgadas', 12000, 5600, 10, 4, 3, 1),
('7503256332178', 'Laptop Victus HP', 25000, 19785, 30, 4, 3, 1),
('7503321212121', 'Caja de Chocolates 50pzas', 300, 130, 30, 1, 2, 2),
('7503452267891', 'Agua 1L', 13, 8, 96, 2, 10, 3),
('7503456677832', 'Toalla de Bano', 150, 120, 25, 5, 5, 1),
('7504445578902', 'Leche Deslactosada Six Pack', 140, 99, 2, 6, 2, 2),
('7505522885532', 'Quesillo Oaxaca 300g', 70, 30, 100, 6, 2, 3),
('7506782341299', 'Paquete de 20 sabritas', 340, 230, 30, 1, 1, 5),
('7506783222111', 'Agua de Jamaica 1L premium', 40, 16, 50, 2, 10, 3),
('7507653321678', 'Lampara para Sala', 200, 98, 20, 5, 4, 1),
('7507733562678', 'Pasta de Dientes', 30, 21, 10, 7, 5, 1),
('7507733562998', '3 pzas Cepillo Dental', 40, 25, 20, 7, 5, 2),
('7508755443200', 'Silla Ergonomica', 1100, 870, 0, 5, 4, 1),
('7508883335631', 'Escoba', 35, 20, 8, 3, 7, 1),
('7509612041589', 'Limpiador de sarro para banos', 120, 78, 20, 3, 1, 1),
('7509804321665', 'Samsung S24 plus 512GB', 18999, 13999, 28, 4, 3, 1),
('7509911120421', 'Jamon', 120, 80, 30, 1, 2, 3),
('7509944335678', 'Jugo de Naranja', 18, 12, 5, 2, 10, 3),
('7509994562313', 'Laptop Msi', 20000, 14000, 10, 4, 3, 1);


INSERT INTO ventas (idventas, fecha, importe, idCliente, idempleados, idmetodo_pago) VALUES
(1, '2025-05-29', 120, 5, 4, 3),
(2, '2025-05-29', 140, 8, 3, 2),
(3, '2025-05-29', 180, 8, 6, 3);


INSERT INTO descventa (idventas, codigo_articulo, cantidad, precio, total) VALUES
(1, 7501234567850, 1, 120, 120),
(2, 7503456677832, 1, 140, 140),
(3, 7503456677832, 1, 180, 180);
