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
    # Docker daemon (DinD)
    - name: docker
      image: docker:24-dind
      securityContext:
        privileged: true
      env:
        - name: DOCKER_TLS_CERTDIR
          value: ""
      command:
        - dockerd
        - --host=unix:///var/run/docker.sock
      volumeMounts:
        - name: docker-sock
          mountPath: /var/run

    # Python + kubectl container
    - name: python
      image: python:3.11
      command: ["cat"]
      tty: true
      volumeMounts:
        - name: docker-sock
          mountPath: /var/run
        - name: workspace-volume
          mountPath: /home/jenkins/agent

    # Jenkins agent
    - name: jnlp
      image: jenkins/inbound-agent:latest
      volumeMounts:
        - name: workspace-volume
          mountPath: /home/jenkins/agent

  volumes:
    - name: docker-sock
      emptyDir: {}
    - name: workspace-volume
      emptyDir: {}
"""
        }
    }

    parameters {
        choice(name: 'ENV', choices: ['dev', 'prod'], description: 'Choose environment')
    }

    environment {
        FRONTEND_IMAGE_TAG = "latest"
        BACKEND_IMAGE_TAG  = "latest"
        IMAGE_REGISTRY     = ""     // e.g. docker.io/yourname
        K8S_NAMESPACE      = "billpay"
    }

    stages {

        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/balakancharla/k3s-microservices.git'
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
                container('python') {
                    sh 'docker version'
                    sh 'docker build -t frontend:${FRONTEND_IMAGE_TAG} frontend/'
                    sh 'docker build -t backend:${BACKEND_IMAGE_TAG} backend/'
                }
            }
        }

        stage('Push Docker Images') {
            when {
                expression { env.IMAGE_REGISTRY?.trim() }
            }
            steps {
                container('python') {
                    sh '''
                      docker tag frontend:${FRONTEND_IMAGE_TAG} ${IMAGE_REGISTRY}/frontend:${FRONTEND_IMAGE_TAG}
                      docker push ${IMAGE_REGISTRY}/frontend:${FRONTEND_IMAGE_TAG}

                      docker tag backend:${BACKEND_IMAGE_TAG} ${IMAGE_REGISTRY}/backend:${BACKEND_IMAGE_TAG}
                      docker push ${IMAGE_REGISTRY}/backend:${BACKEND_IMAGE_TAG}
                    '''
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
                    sh 'kubectl get pods -n ${K8S_NAMESPACE}'
                    sh 'kubectl get svc -n ${K8S_NAMESPACE}'
                }
            }
        }
    }
}
