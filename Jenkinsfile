// pipeline {
//     agent any

//     stages {
//         stage('Test Stage') {
//             steps {
//                 echo 'Pipeline is working!'
//             }
//         }
//     }
// }


pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t automated-deployment-platform -f docker/Dockerfile .'
            }
        }

        stage('Run Container') {
            steps {
                sh '''
                docker stop automated-app || true
                docker rm automated-app || true
                docker run -d -p 5000:5000 --name automated-app automated-deployment-platform
                '''
            }
        }
    }
}