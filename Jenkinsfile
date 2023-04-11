pipeline {
agent any
    stages{
        stage("scrapping avec selenium "){

            steps {
                script {
                    sh'''
                    python3 scraping/PART2_scraping_trustpilot_company_soutenance.py
                    sleep 3
                    '''
                }
            }

        }
  stage("CLEAN DATA"){

        steps {
                script {
                    sh'''
                       python3 SQL/Data_Cleaning_info_Company.py
                    '''
                }
            }

        }
    stage("MYSQL"){

   steps {
                script {
                    sh'''
                   
                     sudo chmod +x SQL/install.sh
                     cd SQL/
                     sudo mv info_company.csv ../../../../mysql
                     
                     sudo mysql -u root "
                     USE satisfaction_client;
                     LOAD DATA INFILE '/var/lib/mysql/info_company.csv' IGNORE INTO TABLE info_company FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS;"
                    '''
                }
            }

        }

    stage("Analyse de Sentiments  "){

   steps {
                script {
                    sh'''
                       
                       echo "bonjour"

                    '''
                }
            }

        }


    stage("ElasticSearch "){

   steps {
                script {
                    sh'''
                    echo "bonjour"
                       
                    '''
                }
            }
        }

    stage("Dashboard avec FastAPI"){

   steps {
                script {
                    sh'''
                       echo "bonjour"
                       
                    '''
                }
            }

        }

    }


}
