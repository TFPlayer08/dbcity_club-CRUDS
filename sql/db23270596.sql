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
  `codigo` CHAR(13) NOT NULL,
  `idempleados` INT NOT NULL,
  `idmetodo_pago` INT NOT NULL,
  PRIMARY KEY (`idventas`),
  INDEX `fk_ventas_Cliente1_idx` (`idCliente` ASC, `codigo` ASC) VISIBLE,
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
  `cantidad` INT NOT NULL,
  `total` FLOAT NOT NULL,
  `idventas` INT NOT NULL,
  `codigo_articulo` CHAR(13) NOT NULL,
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
