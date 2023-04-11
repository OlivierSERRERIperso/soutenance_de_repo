#!/bin/bash
 
mysql -uroot -ppassword  < database.sql > outputCreate.log

mysql -uroot -ppassword  < /var/lib/jenkins/workspace/soutenance/SQL/info_company.csv.sql > outputCreate.log
#mysql -uroot -ppassword  < database_drop.sql > outputCreate.log
