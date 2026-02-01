pipeline {
    agent {
        kubernetes {
            defaultContainer 'jnlp'
            yaml """
apiVersion: v1
kind: Pod
spec:
  containers:
    - name: docker
      image: docker:24.0.2-dind
      securityContext:
        privileged: true
      command:
        - dockerd-entrypoint.sh
      args:
        - --host=tcp://0.0.0.0:2375
        - --host=unix:///var/run/docker.sock
      env:
        - name: DOCKER_TLS_CERTDIR
          value: ""
      tty: true
      volumeMounts:
        - name: docker-graph-storage
          mountPath: /var/lib/docker
        - name: workspace-volume
          mountPath: /home/jenkins/agent

    - name: python
      image: python:3.11
      command: ["cat"]
      tty: true
      volumeMounts:
        - name: workspace-volume
          mountPath: /home/jenkins/agent

    - name: kubectl
      image: lachlanevenson/k8s-kubectl:latest
      command: ["cat"]
      tty: true
      volumeMounts:
        - name: workspace-volume
          mountPath: /home/jenkins/agent

  volumes:
    - name: docker-graph-storage
      emptyDir: {}
    - name: workspace-volume
      emptyDir: {}
"""
        }
    }

    environment {
        DOCKER_HOST = "tcp://127.0.0.1:2375"
        FRONTEND_IMAGE_TAG = "latest"
        BACKEND_IMAGE_TAG  = "latest"
        K8S_NAMESPACE      = "billpay"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Backend') {
            steps {
                container('python') {
                    dir('backend') {
                        sh 'pip install -r requirements.txt'
                    }
                }
            }
        }

        stage('Build Docker Images') {
            steps {
                container('docker') {
                    sh '''
                    echo "Waiting for Docker daemon..."
                    i=0
                    while ! docker info >/dev/null 2>&1; do
                      i=$((i+1))
                      if [ "$i" -gt 15 ]; then
                        echo "Docker not ready"
                        exit 1
                      fi
                      sleep 2
                    done
                    docker version
                    docker build -t frontend:${FRONTEND_IMAGE_TAG} frontend/
                    docker build -t backend:${BACKEND_IMAGE_TAG} backend/
                    '''
                }
            }
        }

        stage('Deploy to k3s') {
            steps {
                container('kubectl') {
                    sh '''
                    kubectl apply -f k8s/namespace.yaml
                    kubectl apply -f k8s/backend-deployment.yaml
                    kubectl apply -f k8s/backend-service.yaml
                    kubectl apply -f k8s/frontend-deployment.yaml
                    kubectl apply -f k8s/frontend-service.yaml
                    '''
                }
            }
        }

        stage('Verify Deployment') {
            steps {
                container('kubectl') {
                    sh '''
                    kubectl get pods -n billpay
                    kubectl get svc -n billpay
                    '''
                }
            }
        }
    }
}
