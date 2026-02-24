pipeline {
    agent any

    parameters {
        booleanParam(name: 'DEPLOY', defaultValue: false, description: 'Trigger Deployment Stage')
    }

    stages {

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t cicd-app -f docker/Dockerfile .'
            }
        }

        stage('Test') {
            steps {
                sh 'echo Running tests...'
            }
        }

        stage('Deploy') {
            when {
                expression { params.DEPLOY == true }
            }
            steps {
                sh 'docker run -d -p 5000:5000 cicd-app'
            }
        }
    }
}w