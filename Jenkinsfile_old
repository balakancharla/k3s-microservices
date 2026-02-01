pipeline {
    agent any

    environment {
        FRONTEND_IMAGE_TAG = "latest"
        BACKEND_IMAGE_TAG = "latest"
    }

    stages {
        stage('Build Frontend') {
            steps {
                sh 'npm run build'
                archiveArtifacts artifacts: 'dist/**/*', onlyIfSuccessful: true
            }
        }
        stage('Build Backend') {
            steps {
                sh 'mvn package'
                archiveArtifacts artifacts: 'target/*.jar', onlyIfSuccessful: true
            }
        }
        stage('Build Docker Images') {
            steps {
                sh 'docker build -t frontend:${FRONTEND_IMAGE_TAG} .'
                sh 'docker build -t backend:${BACKEND_IMAGE_TAG} .'
            }
        }
        stage('Push Docker Images') {
            steps {
                sh 'docker tag frontend:${FRONTEND_IMAGE_TAG} ${IMAGE_REGISTRY}/frontend:${FRONTEND_IMAGE_TAG}'
                sh 'docker push ${IMAGE_REGISTRY}/frontend:${FRONTEND_IMAGE_TAG}'
                sh 'docker tag backend:${BACKEND_IMAGE_TAG} ${IMAGE_REGISTRY}/backend:${BACKEND_IMAGE_TAG}'
                sh 'docker push ${IMAGE_REGISTRY}/backend:${BACKEND_IMAGE_TAG}'
            }
        }
        stage('Deploy to k3s') {
            steps {
                sh 'kubectl apply -f deployment.yaml'
            }
        }
    }
}
---