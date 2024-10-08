-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema tarea2
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema tarea2
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `tarea2` DEFAULT CHARACTER SET utf8 ;
USE `tarea2` ;

-- -----------------------------------------------------
-- Table `tarea2`.`region`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `tarea2`.`region` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(200) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `tarea2`.`comuna`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `tarea2`.`comuna` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(200) NOT NULL,
  `region_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_comuna_region1_idx` (`region_id` ASC),
  CONSTRAINT `fk_comuna_region1`
    FOREIGN KEY (`region_id`)
    REFERENCES `tarea2`.`region` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `tarea2`.`contacto`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `tarea2`.`contacto` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(80) NOT NULL,
  `email` VARCHAR(30) NOT NULL,
  `celular` VARCHAR(15) NULL,
  `comuna_id` INT NOT NULL,
  `fecha_creacion` TIMESTAMP NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_contacto_comuna1_idx` (`comuna_id` ASC),
  CONSTRAINT `fk_contacto_comuna1`
    FOREIGN KEY (`comuna_id`)
    REFERENCES `tarea2`.`comuna` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `tarea2`.`dispositivo`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `tarea2`.`dispositivo` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `contacto_id` INT NOT NULL,
  `nombre` VARCHAR(80) NOT NULL,
  `descripcion` VARCHAR(300) NULL,
  `tipo` ENUM("pantalla", "notebook", "tablet", "celular", "consola", "mouse", "teclado", "impresora", "parlante", "audífonos", "otro") NOT NULL,
  `anos_uso` INT NOT NULL,
  `estado` ENUM("funciona perfecto", "funciona a medias", "no funciona") NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `fk_dispositivo_contacto1`
    FOREIGN KEY (`contacto_id`)
    REFERENCES `tarea2`.`contacto` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `tarea2`.`archivo`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `tarea2`.`archivo` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `ruta_archivo` VARCHAR(300) NOT NULL,
  `nombre_archivo` VARCHAR(300) NOT NULL,
  `dispositivo_id` INT NOT NULL,
  PRIMARY KEY (`id`, `dispositivo_id`),
  INDEX `fk_archivo_dispositivo1_idx` (`dispositivo_id` ASC),
  CONSTRAINT `fk_archivo_dispositivo1`
    FOREIGN KEY (`dispositivo_id`)
    REFERENCES `tarea2`.`dispositivo` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `tarea2`.`comentario`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `tarea2`.`comentario` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(80) NOT NULL,
  `texto` VARCHAR(300) NOT NULL,
  `fecha` TIMESTAMP NOT NULL,
  `dispositivo_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_comentario_dispositivo1_idx` (`dispositivo_id` ASC),
  CONSTRAINT `fk_comentario_dispositivo1`
    FOREIGN KEY (`dispositivo_id`)
    REFERENCES `tarea2`.`dispositivo` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

COMMIT;

