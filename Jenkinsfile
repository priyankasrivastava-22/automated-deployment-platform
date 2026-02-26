// pipeline {
//     agent any

//     environment {
//         IMAGE_NAME = "automated-deployment-platform"
//         CONTAINER_NAME = "automated-app"
//     }

//     stages {

//         stage('Checkout') {
//             steps {
//                 checkout scm
//             }
//         }

//         stage('Build Docker Image') {
//             steps {
//                 sh '''
//                 docker build -t $IMAGE_NAME:latest -f docker/Dockerfile .
//                 '''
//             }
//         }

//         stage('Stop & Remove Old Container') {
//             steps {
//                 sh '''
//                 docker stop $CONTAINER_NAME || true
//                 docker rm $CONTAINER_NAME || true
//                 '''
//             }
//         }

//         stage('Deploy New Container') {
//             steps {
//                 sh '''
//                 docker run -d -p 5000:5000 --name $CONTAINER_NAME $IMAGE_NAME:latest
//                 '''
//             }
//         }

//         stage('Cleanup Old Images') {
//             steps {
//                 sh 'docker image prune -f'
//             }
//         }
//     }
// }

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
                    if (env.BRANCH_NAME == 'dev') {
                        env.CONTAINER_NAME = "automated-app-dev"
                        env.PORT = "5001"
                    } else {
                        env.CONTAINER_NAME = "automated-app"
                        env.PORT = "5000"
                    }
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                docker build -t $IMAGE_NAME:latest -f docker/Dockerfile .
                '''
            }
        }

        stage('Stop & Remove Old Container') {
            steps {
                sh '''
                docker stop $CONTAINER_NAME || true
                docker rm $CONTAINER_NAME || true
                '''
            }
        }

        stage('Deploy New Container') {
            steps {
                sh '''
                docker run -d -p $PORT:5000 --name $CONTAINER_NAME $IMAGE_NAME:latest
                '''
            }
        }

        stage('Cleanup Old Images') {
            steps {
                sh 'docker image prune -f'
            }
        }
    }
}