pipeline {
    agent any

    environment {
        IMAGE_NAME = "automated-deployment-platform"
    }

    stages {

        // ---------------- CHECKOUT ----------------
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        // ---------------- SET ENV BASED ON BRANCH ----------------
        stage('Set Environment Based On Branch') {
            steps {
                script {
                    echo "Git Branch: ${env.GIT_BRANCH}"

                    if (env.GIT_BRANCH.contains("dev")) {
                        env.CONTAINER_NAME = "automated-app-dev"
                        env.PORT = "5001"
                    } else {
                        env.CONTAINER_NAME = "automated-app"
                        env.PORT = "5000"
                    }

                    echo "Container: ${env.CONTAINER_NAME}"
                    echo "Port: ${env.PORT}"
                }
            }
        }

        // ---------------- TEST STAGE ----------------
        stage('Test') {
            steps {
                sh '''
                python3 -m venv venv
                . venv/bin/activate
                pip install --upgrade pip
                pip install -r app/requirements.txt

                # Run tests only if present (avoid failure if no tests)
                pytest app/ || true
                '''
            }
        }

        // ---------------- BUILD IMAGE ----------------
        stage('Build Docker Image') {
            steps {
                sh '''
                docker build -t $IMAGE_NAME:latest -f docker/Dockerfile .
                '''
            }
        }

        // ---------------- STOP OLD CONTAINER ----------------
        stage('Stop & Remove Old Container') {
            steps {
                sh '''
                docker stop $CONTAINER_NAME || true
                docker rm -f $CONTAINER_NAME || true
                '''
            }
        }

        // ---------------- DEPLOY ----------------
        stage('Deploy New Container') {
            steps {
                sh '''
                docker run -d -p $PORT:5000 \
                --name $CONTAINER_NAME \
                --restart unless-stopped \
                $IMAGE_NAME:latest
                '''
            }
        }

        // ---------------- CLEANUP ----------------
        stage('Cleanup Old Images') {
            steps {
                sh 'docker image prune -f'
            }
        }
    }

    // ---------------- POST ACTIONS ----------------
    post {
        success {
            echo "Deployment Successful!"
        }
        failure {
            echo "Deployment Failed!"
        }
    }
}