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
                     mysql -u root -proot -e "
                     USE satisfaction_client; 
                     LOAD DATA INFILE '/var/lib/mysql/info_company.csv' 
                     IGNORE INTO TABLE info_company 
                     FIELDS TERMINATED BY ',' 
                     LINES TERMINATED BY '\n'
                     IGNORE 1 ROWS;
                     "
                    '''
                }
            }

        }

    stage("Analyse de Sentiments  "){

   steps {
                script {
                    sh'''
                       
                       python3 machine_learning/ml.py

                    '''
                }
            }

        }


    stage("ElasticSearch "){

   steps {
                script {
                    sh'''
                    cd elasticsearch/
                    sudo docker compose up -d
                       
                    '''
                }
            }
        }

    stage("Dashboard avec FastAPI"){

   steps {
                script {
                    sh'''
                       cd fastapi/app
                       sudo uvicorn main:api --host 0.0.0.0 --port 81
                       
                    '''
                }
            }

        }

    }


}
