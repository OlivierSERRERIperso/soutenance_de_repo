CREATE DATABASE  IF NOT EXISTS `satisfaction_client`; 
USE `satisfaction_client`;
 
SET FOREIGN_KEY_CHECKS=0 ;
 
DROP TABLE IF EXISTS `MyTable` CASCADE;
/* Some more table dropping */
/* Recreate tables */
/* Set constraints */

CREATE TABLE `info_company` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name_company` varchar(50) DEFAULT NULL,
  `note_trustpilot` float DEFAULT NULL,
  `nombre_avis` int DEFAULT NULL,
  `localisation_company` varchar(50) DEFAULT NULL,
  `domaine_activite` varchar(150) DEFAULT NULL,
  `nombre_avis_excellent` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=360 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

LOAD DATA INFILE '/home/ubuntu/soutenance/SQL/info_company.csv’ IGNORE INTO TABLE info_company FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS";
