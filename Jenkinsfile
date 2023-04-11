pipeline {
agent any
    stages{
        stage("scrapping avec selenium "){

            steps {
                script {
                    sh'''
                    python3 scraping/PART2_scraping_trustpilot_company_soutenance.py
                    sleep 10
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
                   
                     echo "hello"
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
                    echo "bonjour"
                       
                    '''
                }
            }
        }

    stage("Dashboard avec FastAPI"){

   steps {
                script {
                    sh'''
                       uvicorn fastapi/app/main:api --host 0.0.0.0 --port 80
                       
                    '''
                }
            }

        }

    }


}
