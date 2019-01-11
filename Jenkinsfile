pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                sh 'virtualenv .venv'
                sh '. .venv/bin/activate'
                sh 'pip install -r requirements.txt -i https://pypi.douban.com/simple'
                sh 'python manage.py migrate'
                sh 'python manage.py runserver &'
            }
        }
        stage('Test') {
            steps {
                sh 'python manage.py test'
            }
        }
    }
    post {
        always {
            archiveArtifacts '**/*'
        }
    }
}
