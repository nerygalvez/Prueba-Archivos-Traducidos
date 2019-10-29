/*CREATE DATABASE tareaSA;
use tareaSA;

CREATE TABLE usuarios (
  nombre VARCHAR(20),
  apellido VARCHAR(20)
);

INSERT INTO usuarios
  (nombre, apellido)
VALUES
  ('Nery', 'Galvez'),
  ('Maria Fernanda', 'Chavez'),
  ('Julio', 'Galvez'),
  ('Rodrigo', 'Galvez'),
  ('Maria Jose', 'Galvez');
*/


CREATE DATABASE  IF NOT EXISTS Traducido /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE Traducido;
-- MySQL dump 10.13  Distrib 8.0.17, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: Traducido
-- ------------------------------------------------------
-- Server version	8.0.17

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table 'Archivo'
--

DROP TABLE IF EXISTS Archivo;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE Archivo (
  Complemento varchar(100) NOT NULL,
  Localizacion varchar(100) NOT NULL,
  tipoArchivo varchar(20) DEFAULT NULL,
  Archivo blob,
  idEstado int(11) DEFAULT NULL,
  PRIMARY KEY (Complemento,Localizacion)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table 'Archivo'
--

LOCK TABLES Archivo WRITE;

UNLOCK TABLES;

--
-- Table structure for table 'ArchivoCadena'
--

DROP TABLE IF EXISTS ArchivoCadena;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE ArchivoCadena (
  idDetalleArchivo int(11) NOT NULL AUTO_INCREMENT,
  Complemento varchar(100) NOT NULL,
  Localizacion varchar(100) DEFAULT NULL,
  nombreusr varchar(100) DEFAULT NULL,
  correousr varchar(100) DEFAULT NULL,
  Cadena varchar(6000) DEFAULT NULL,
  PRIMARY KEY (idDetalleArchivo)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table 'ArchivoCadena'
--

LOCK TABLES ArchivoCadena WRITE;

INSERT INTO ArchivoCadena VALUES (1,'WordPress Menu','UA-08','Juan Carlos Maeda Juarez','jcarlosmaeda@gmail.com','Menu'),(2,'WordPress Menu','UA-08','Juan Carlos Maeda Juarez','jcarlosmaeda@gmail.com',' Login'),(3,'WordPress Menu','UA-08','Juan Carlos Maeda Juarez','jcarlosmaeda@gmail.com',' Bienvenida'),(4,'WordPress Menu','UA-08','Juan Carlos Maeda Juarez','jcarlosmaeda@gmail.com',' Acerca de');
UNLOCK TABLES;

--
-- Table structure for table 'table1'
--

DROP TABLE IF EXISTS table1;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE table1 (
  id int(11) NOT NULL AUTO_INCREMENT,
  value varchar(6000) DEFAULT NULL,
  PRIMARY KEY (id)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table 'table1'
--

LOCK TABLES table1 WRITE;
INSERT INTO table1 VALUES (1,'Menu, Login, Bienvenida, Acerca de, Cargar, Prueba');
UNLOCK TABLES;

--
-- Dumping routines for database 'Traducido'
--

/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER='root'@'%' PROCEDURE sp_traducidosubeArchivo(
_nombre varchar(100), _correo varchar(100),_nombrecomplemento varchar(100),_localizacion varchar(50),
_cadena varchar(6632)
)
BEGIN
DECLARE EXIT HANDLER FOR SQLEXCEPTION
	  BEGIN
		select 401 estado,'Error al insertar la traduccion ' mensaje;               
	  END;
truncate table table1;
insert into table1 (value) values(_cadena);
insert into ArchivoCadena (Complemento,Localizacion,nombreusr,correousr,cadena)
SELECT
  _nombrecomplemento,_localizacion,_nombre,_correo,
  SUBSTRING_INDEX(SUBSTRING_INDEX(value, ',', n.digit+1), ',', -1) Valor
FROM
  table1
  INNER JOIN
  (SELECT 0 digit UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3) n
  ON LENGTH(REPLACE(value, ',' , '')) <= LENGTH(value)-n.digit
ORDER BY
  id,
  n.digit;
  
select 200 estado, 'Archivo cargado correctamente';
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER='root'@'%' PROCEDURE sp_traducircargaArchivo(_Complemento varchar(100),_Localizacion varchar(100), _tipoArchivo varchar(20), _idEstado int,_Archivo blob)
BEGIN
	  DECLARE EXIT HANDLER FOR SQLEXCEPTION
	  BEGIN
		select 401 estado,'Error al insertar la traduccion ' mensaje;               
	  END;
      
      insert into Archivo (Complemento,Localizacion,tipoArchivo,Archivo,idEstado) values (_Complemento,_Localizacion,_tipoArchivo,_Archivo,_idEstado);
      select 200 estado, 'Archivo cargado correctamente' mensaje;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-10-27  2:12:22
