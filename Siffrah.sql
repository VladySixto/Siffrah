-- -----------------------------------------------------
-- Schema Siffrah
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema Siffrah
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `Siffrah` DEFAULT CHARACTER SET utf8mb4 ;
USE `Siffrah` ;

-- -----------------------------------------------------
-- Table `Siffrah`.`clientes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Siffrah`.`clientes` (
  `idclientes` INT NOT NULL,
  `nombre_cliente` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`idclientes`),
  UNIQUE INDEX `idclientes_UNIQUE` (`idclientes` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Siffrah`.`usuario`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Siffrah`.`usuario` (
  `idusuario` INT NOT NULL,
  `nombre_usuario` VARCHAR(45) NOT NULL,
  `apellido_usuario` VARCHAR(45) NOT NULL,
  `pass_usuario` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`idusuario`),
  UNIQUE INDEX `idusuario_UNIQUE` (`idusuario` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Siffrah`.`compra`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Siffrah`.`compra` (
  `total_compra` DOUBLE NOT NULL,
  `clientes_idclientes` INT NOT NULL,
  `usuario_idusuario` INT NOT NULL,
  PRIMARY KEY (`total_compra`),
  INDEX `fk_compra_usuario1_idx` (`usuario_idusuario` ASC) VISIBLE,
  CONSTRAINT `fk_compra_usuario1`
    FOREIGN KEY (`usuario_idusuario`)
    REFERENCES `Siffrah`.`usuario` (`idusuario`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Siffrah`.`proveedores`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Siffrah`.`proveedores` (
  `id_proveedor` INT NOT NULL,
  `nombre_proveedor` VARCHAR(45) NULL,
  `apellido_proveedor` VARCHAR(45) NULL,
  `telefono_proveedor` INT NULL,
  PRIMARY KEY (`id_proveedor`),
  UNIQUE INDEX `id_proveedor_UNIQUE` (`id_proveedor` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Siffrah`.`pedido`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Siffrah`.`pedido` (
  `id_pedido` INT NOT NULL,
  `total_pedido` DOUBLE NULL,
  `estado_pedido` VARCHAR(45) NULL,
  `compra_total_compra` DOUBLE NOT NULL,
  `proveedores_id_proveedor` INT NOT NULL,
  PRIMARY KEY (`id_pedido`),
  UNIQUE INDEX `idid_pedido_UNIQUE` (`id_pedido` ASC) VISIBLE,
  INDEX `fk_id_pedido_compra1_idx` (`compra_total_compra` ASC) VISIBLE,
  INDEX `fk_id_pedido_proveedores1_idx` (`proveedores_id_proveedor` ASC) VISIBLE,
  CONSTRAINT `fk_id_pedido_compra1`
    FOREIGN KEY (`compra_total_compra`)
    REFERENCES `Siffrah`.`compra` (`total_compra`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_id_pedido_proveedores1`
    FOREIGN KEY (`proveedores_id_proveedor`)
    REFERENCES `Siffrah`.`proveedores` (`id_proveedor`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Siffrah`.`detalle_productos`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Siffrah`.`detalle_productos` (
  `id_detalle_productos` INT NOT NULL,
  `pedido_id_pedido` INT NOT NULL,
  PRIMARY KEY (`id_detalle_productos`),
  INDEX `fk_detalle_productos_pedido1_idx` (`pedido_id_pedido` ASC) VISIBLE,
  CONSTRAINT `fk_detalle_productos_pedido1`
    FOREIGN KEY (`pedido_id_pedido`)
    REFERENCES `Siffrah`.`pedido` (`id_pedido`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Siffrah`.`productos`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Siffrah`.`productos` (
  `idproductos` INT NOT NULL,
  `nombre_producto` VARCHAR(45) NULL,
  `precio_venta_producto` DECIMAL NULL,
  `precio_compra_producto` DECIMAL NULL,
  `stock_producto` INT NULL,
  `compra_total_compra` DOUBLE NOT NULL,
  `detalle_productos_id_detalle_productos` INT NOT NULL,
  PRIMARY KEY (`idproductos`),
  INDEX `fk_productos_detalle_productos1_idx` (`detalle_productos_id_detalle_productos` ASC) VISIBLE,
  CONSTRAINT `fk_productos_detalle_productos1`
    FOREIGN KEY (`detalle_productos_id_detalle_productos`)
    REFERENCES `Siffrah`.`detalle_productos` (`id_detalle_productos`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Siffrah`.`detalle_compra`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Siffrah`.`detalle_compra` (
  `iddetalle_compra` INT NOT NULL,
  `cantidad_detalle` INT NULL,
  `subtotal_detalle` DOUBLE NULL,
  `compra_total_compra` DOUBLE NOT NULL,
  `productos_idproductos` INT NOT NULL,
  PRIMARY KEY (`iddetalle_compra`),
  INDEX `fk_detalle_compra_compra1_idx` (`compra_total_compra` ASC) VISIBLE,
  INDEX `fk_detalle_compra_productos1_idx` (`productos_idproductos` ASC) VISIBLE,
  CONSTRAINT `fk_detalle_compra_compra1`
    FOREIGN KEY (`compra_total_compra`)
    REFERENCES `Siffrah`.`compra` (`total_compra`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_detalle_compra_productos1`
    FOREIGN KEY (`productos_idproductos`)
    REFERENCES `Siffrah`.`productos` (`idproductos`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


