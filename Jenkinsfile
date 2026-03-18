pipeline {
    agent any

    environment {
        IMAGE_NAME = "automated-deployment-platform"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Set Environment Based On Branch') {
            steps {
                script {
                    echo "Git Branch: ${env.GIT_BRANCH}"

                    if (env.GIT_BRANCH.contains("dev")) {
                        env.ENVIRONMENT = "dev"
                    } else {
                        env.ENVIRONMENT = "prod"
                    }
                }
            }
        }

        stage('Test') {
            steps {
                sh '''
                python3 -m venv venv
                . venv/bin/activate
                pip install --upgrade pip
                pip install -r app/requirements.txt
                pytest app/ || true
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                docker build -t $IMAGE_NAME:latest -f docker/Dockerfile .
                '''
            }
        }

        stage('Auto Deploy via API') {
            steps {
                sh """
                curl -X POST http://localhost:5001/deploy \
                -H "Content-Type: application/json" \
                -d '{\\"environment\\":\\"${ENVIRONMENT}\\",\\"version\\":\\"latest\\"}'
                """
            }
        }
    }
}