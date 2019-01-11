pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                sh '. $VIRTUAL_ENV/bin/activate'
                sh 'pip install -r requirements.txt -i https://pypi.douban.com/simple'
                sh 'python manage.py migrate'
                sh 'python manage.py runserver'
            }
        }
        stage('Test') {
            steps {
                sh 'python manage.py test'
            }
        }
        stage('Deliver') {
            steps {
                sh 'pyinstaller --onefile sources/add2vals.py'
                sh 'dist/add2vals 1 2'
            }
        post {
            unstable {
                archiveArtifacts 'dist/add2vals'
            }
        }
    }
}
