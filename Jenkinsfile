pipeline {
  agent {
    kubernetes {
      cloud 'imtech-eks'
      defaultContainer 'docker'
      yaml """
apiVersion: v1
kind: Pod
spec:
  serviceAccountName: jenkins-admin
  volumes:
    - name: docker-graph
      emptyDir: {}
  containers:
    - name: docker
      image: docker:20.10.7-dind
      securityContext:
        privileged: true
      command:
        - dockerd-entrypoint.sh
        - --host=tcp://0.0.0.0:2375
        - --storage-driver=overlay2
      env:
        - name: DOCKER_HOST
          value: tcp://127.0.0.1:2375
        - name: DOCKER_TLS_CERTDIR
          value: ""
      volumeMounts:
        - name: docker-graph
          mountPath: /var/lib/docker
    - name: python
      image: python:3.9
      command:
        - cat
      tty: true
    - name: helm
      image: alpine/helm:3.10.0
      command:
        - cat
      tty: true
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

    stage('Run Python Tests') {
      steps {
        container('python') {
          sh 'pip install pytest flask && python3 test-app.py'
        }
      }
    }

    stage('Build & Push Docker Image') {
      steps {
        container('docker') {
          sh 'until docker info >/dev/null 2>&1; do sleep 1; done && ./build'
        }
      }
    }

    stage('Deploy with Helm') {
      steps {
        container('helm') {
          sh 'cd "$WORKSPACE" && sh deploy'
        }
      }
    }
  }

  post {
    always {
      slackSend channel: '#imtech',
                message: "Find Status of Pipeline:- ${currentBuild.currentResult} ${env.JOB_NAME} ${env.BUILD_NUMBER} ${BUILD_URL}"
    }
  }
}

