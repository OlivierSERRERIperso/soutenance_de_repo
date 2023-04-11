pipeline {
agent any
    stages{
        stage("scrapping avec selenium "){

            steps {
                script {
                    sh'''
                    python3 scraping/PART2_scraping_trustpilot_company_soutenance.py
                    sleep 90
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
                     #  chmod +x SQL/install.sh
                     #  LOAD DATA INFILE '~/SQL/info_company.csv’ IGNORE INTO TABLE info_company FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS;

                    '''
                }
            }

        }

    stage("Analyse de sentiment "){

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
                       docker-compose up -d
                       
                    '''
                }
            }
        }

    stage("Dashboard avec FastAPI"){

   steps {
                script {
                    sh'''
                       uvicorn main:api --host 0.0.0.0 --port 80
                       
                    '''
                }
            }

        }

    }


}
