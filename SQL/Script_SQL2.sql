show databases;
use customer_satisfaction;
show tables;
SHOW columns FROM info_company;
SELECT domaine_activite, COUNT(domaine_activite) FROM info_company GROUP BY domaine_activite limit 10;
SELECT name_company ,nombre_avis,  nombre_avis_excellent FROM info_company LIMIT 10;
SELECT name_company, nombre_avis_excellent, note_trustpilot FROM info_company WHERE CAST(nombre_avis_excellent AS UNSIGNED)=100 LIMIT 5;
SELECT * FROM info_company WHERE localisation_company="Paris, France" and note_trustpilot BETWEEN '0.0' AND '3.0' LIMIT 10;
SELECT name_company, nombre_avis_excellent, note_trustpilot FROM info_company WHERE CAST(nombre_avis_excellent AS UNSIGNED) BETWEEN 50 AND 100;
 SELECT name_company, nombre_avis FROM info_company WHERE nombre_avis >=1000;
 SELECT COUNT(nombre_avis) FROM info_company WHERE nombre_avis >=1000;
 SELECT * FROM showroom_comment WHERE Nombre_etoile BETWEEN 1 AND 2 LIMIT 10;
 
 -- Quelques sur la deuxième table --
 SHOW columns FROM showroom_comment;
 ALTER TABLE showroom_comment MODIFY Reponse_ou_non VARCHAR(225);
 UPDATE showroom_comment SET Reponse_ou_non = 'True' WHERE Reponse_ou_non = '0';
 SELECT * FROM showroom_comment WHERE Nombre_etoile BETWEEN 1 AND 2 LIMIT 10;
 