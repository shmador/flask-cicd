pipeline {
  agent {
    kubernetes {
      cloud 'kubernetes'
      defaultContainer 'docker'
      yaml """
apiVersion: v1
kind: Pod
spec:
  serviceAccountName: default
  securityContext:
    fsGroup: 1000
  volumes:
    - name: docker-graph-storage
      emptyDir: {}
  containers:
    - name: docker
      image: docker:20.10.7
      command: ['cat']; tty: true
      volumeMounts:
        - name: docker-graph-storage
          mountPath: /var/lib/docker
      securityContext:
        privileged: true

    - name: dind
      image: docker:20.10.7-dind
      command: ['dockerd-entrypoint.sh']; tty: true
      securityContext:
        privileged: true
      volumeMounts:
        - name: docker-graph-storage
          mountPath: /var/lib/docker

    - name: python
      image: python:3.9
      command: ['cat']; tty: true

    - name: helm
      image: helm/helm:v3.7.1
      imagePullPolicy: IfNotPresent
      command: ['cat']; tty: true
"""
    }
  }

  stages {
    stage('Login to Docker Registry') {
      steps {
        container('docker') {
          withCredentials([usernamePassword(
            credentialsId: 'docker',
            usernameVariable: 'DOCKER_USER',
            passwordVariable: 'DOCKER_PASS'
          )]) {
            sh 'echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin'
          }
        }
      }
    }

    stage('Run python tests') {
      steps {
        container('python') {
          sh 'python3 test-app.py'
        }
      }
    }

    stage('Build and push docker image') {
      steps {
        container('docker') {
          sh './build'
        }
      }
    }

    stage('Deploy on local cluster with helm') {
      steps {
        container('helm') {
          sh './deploy'
        }
      }
    }
  }
}

