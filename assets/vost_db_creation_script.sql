-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema vost_db
-- -----------------------------------------------------
-- Local database for vost
-- 
DROP SCHEMA IF EXISTS `vost_db` ;

-- -----------------------------------------------------
-- Schema vost_db
--
-- Local database for vost
-- 
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `vost_db` DEFAULT CHARACTER SET utf8 COLLATE utf8_bin ;
USE `vost_db` ;

-- -----------------------------------------------------
-- Table `vost_db`.`country`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `vost_db`.`country` ;

CREATE TABLE IF NOT EXISTS `vost_db`.`country` (
  `country_name` VARCHAR(100) NOT NULL,
  `code` VARCHAR(20) NULL,
  `region` VARCHAR(100) NULL,
  `subregion` VARCHAR(100) NULL,
  PRIMARY KEY (`country_name`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `vost_db`.`entity`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `vost_db`.`entity` ;

CREATE TABLE IF NOT EXISTS `vost_db`.`entity` (
  `entity_name` VARCHAR(100) NOT NULL,
  `website` VARCHAR(100) NULL,
  `signatory_of_code_of_practice_on_disinformation` VARCHAR(10) NOT NULL,
  `country_name` VARCHAR(100) NULL,
  PRIMARY KEY (`entity_name`),
  INDEX `affiliation_country_pk_idx` (`country_name` ASC) VISIBLE,
  CONSTRAINT `affiliation_country_pk`
    FOREIGN KEY (`country_name`)
    REFERENCES `vost_db`.`country` (`country_name`)
    ON DELETE NO ACTION
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `vost_db`.`vetted_user`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `vost_db`.`vetted_user` ;

CREATE TABLE IF NOT EXISTS `vost_db`.`vetted_user` (
  `work_email` VARCHAR(50) NOT NULL,
  `hashed_password` CHAR(60) NOT NULL,
  `first_name` VARCHAR(50) NOT NULL,
  `last_name` VARCHAR(50) NOT NULL,
  `is_admin` BIT(2) NOT NULL DEFAULT 0,
  `affiliation_name` VARCHAR(100) NOT NULL,
  `application_date` TIMESTAMP(6) NOT NULL,
  `approval_date` TIMESTAMP(6) NULL,
  PRIMARY KEY (`work_email`),
  INDEX `user_affiliation_pk_idx` (`affiliation_name` ASC) VISIBLE,
  CONSTRAINT `user_affiliation_pk`
    FOREIGN KEY (`affiliation_name`)
    REFERENCES `vost_db`.`entity` (`entity_name`)
    ON DELETE NO ACTION
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `vost_db`.`platform`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `vost_db`.`platform` ;

CREATE TABLE IF NOT EXISTS `vost_db`.`platform` (
  `platform_name` VARCHAR(100) NOT NULL,
  `country_name` VARCHAR(100) NULL,
  PRIMARY KEY (`platform_name`),
  INDEX `platform_country_fk_idx` (`country_name` ASC) VISIBLE,
  CONSTRAINT `platform_country_fk`
    FOREIGN KEY (`country_name`)
    REFERENCES `vost_db`.`country` (`country_name`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `vost_db`.`report_classification`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `vost_db`.`report_classification` ;

CREATE TABLE IF NOT EXISTS `vost_db`.`report_classification` (
  `report_type` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`report_type`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `vost_db`.`report`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `vost_db`.`report` ;

CREATE TABLE IF NOT EXISTS `vost_db`.`report` (
  `timestamp` TIMESTAMP(6) NOT NULL,
  `reporting_user` VARCHAR(100) NOT NULL,
  `platform_name` VARCHAR(100) NOT NULL,
  `url` VARCHAR(200) NOT NULL,
  `report_type` VARCHAR(50) NOT NULL,
  `screenshot_url` VARCHAR(200) NULL,
  `answer_date` TIMESTAMP(6) NULL,
  `platform_decision` VARCHAR(50) NULL,
  `policy` VARCHAR(100) NULL,
  `appeal` VARCHAR(10) NULL,
  UNIQUE INDEX `url_UNIQUE` (`url` ASC) VISIBLE,
  UNIQUE INDEX `screenshot_url_UNIQUE` (`screenshot_url` ASC) VISIBLE,
  PRIMARY KEY (`url`),
  INDEX `report_user_fk_idx` (`reporting_user` ASC) VISIBLE,
  INDEX `report_platform_fk_idx` (`platform_name` ASC) VISIBLE,
  INDEX `report_classification_fk_idx` (`report_type` ASC) VISIBLE,
  CONSTRAINT `report_user_fk`
    FOREIGN KEY (`reporting_user`)
    REFERENCES `vost_db`.`vetted_user` (`work_email`)
    ON DELETE NO ACTION
    ON UPDATE CASCADE,
  CONSTRAINT `report_platform_fk`
    FOREIGN KEY (`platform_name`)
    REFERENCES `vost_db`.`platform` (`platform_name`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `report_classification_fk`
    FOREIGN KEY (`report_type`)
    REFERENCES `vost_db`.`report_classification` (`report_type`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
