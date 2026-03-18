pipeline {
    agent any

    environment {
        IMAGE_NAME = "automated-app"
        CONTAINER_NAME = "automated-app-dev"
        PORT = "5001"
    }

    stages {

        stage('Checkout Code') {
            steps {
                git branch: 'dev', url: 'https://github.com/priyankasrivastava-22/automated-deployment-platform.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                docker build -t $IMAGE_NAME:latest .
                '''
            }
        }

        stage('Stop & Remove Old Container') {
            steps {
                sh '''
                docker stop $CONTAINER_NAME || true
                docker rm -f $CONTAINER_NAME || true
                '''
            }
        }

        stage('Deploy New Container') {
            steps {
                sh '''
                docker run -d -p $PORT:5000 --name $CONTAINER_NAME --restart unless-stopped $IMAGE_NAME:latest
                '''
            }
        }

        stage('Cleanup Old Images') {
            steps {
                sh '''
                docker image prune -f
                '''
            }
        }
    }

    post {
        success {
            echo "Deployment Successful!"
        }
        failure {
            echo "Deployment Failed!"
        }
    }
}