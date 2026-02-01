pipeline {
    agent {
        kubernetes {
            label 'microservices'
            defaultContainer 'jnlp'
            yaml """
apiVersion: v1
kind: Pod
spec:
  containers:
    - name: python
      image: python:3.11
      command:
        - cat
      tty: true
      volumeMounts:
        - name: workspace-volume
          mountPath: /home/jenkins/agent
    - name: docker
      image: docker:24
      command:
        - cat
      tty: true
      volumeMounts:
        - name: workspace-volume
          mountPath: /home/jenkins/agent
  volumes:
    - name: workspace-volume
      emptyDir: {}
"""
        }
    }

    parameters {
        choice(name: 'ENV', choices: ['dev', 'prod'], description: 'Choose your environment')
    }

    environment {
        FRONTEND_IMAGE_TAG = "latest"
        BACKEND_IMAGE_TAG = "latest"
        IMAGE_REGISTRY = ""  // leave blank if not pushing
        K8S_NAMESPACE = "billpay"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/balakancharla/k3s-microservices.git'
            }
        }

        stage('Build Backend') {
            steps {
                container('python') {
                    dir('backend') {
                        sh 'pip install -r requirements.txt'
                        archiveArtifacts artifacts: '*.py', onlyIfSuccessful: true
                    }
                }
            }
        }

        stage('Build Docker Images') {
            steps {
                container('docker') {
                    // Build frontend static site image
                    sh 'docker build -t frontend:${FRONTEND_IMAGE_TAG} frontend/'
                    // Build backend image
                    sh 'docker build -t backend:${BACKEND_IMAGE_TAG} backend/'
                }
            }
        }

        stage('Push Docker Images') {
            when {
                expression { env.IMAGE_REGISTRY?.trim() }
            }
            steps {
                container('docker') {
                    sh 'docker tag frontend:${FRONTEND_IMAGE_TAG} ${IMAGE_REGISTRY}/frontend:${FRONTEND_IMAGE_TAG}'
                    sh 'docker push ${IMAGE_REGISTRY}/frontend:${FRONTEND_IMAGE_TAG}'
                    sh 'docker tag backend:${BACKEND_IMAGE_TAG} ${IMAGE_REGISTRY}/backend:${BACKEND_IMAGE_TAG}'
                    sh 'docker push ${IMAGE_REGISTRY}/backend:${BACKEND_IMAGE_TAG}'
                }
            }
        }

        stage('Deploy to k3s') {
            steps {
                container('python') {
                    sh 'kubectl apply -f k8s/namespace.yaml'
                    sh 'kubectl apply -f k8s/backend.yaml'
                    sh 'kubectl apply -f k8s/frontend.yaml'
                }
            }
        }

        stage('Verify Deployment') {
            steps {
                container('python') {
                    sh 'kubectl get pods -n $K8S_NAMESPACE'
                    sh 'kubectl get svc -n $K8S_NAMESPACE'
                }
            }
        }
    }
}
