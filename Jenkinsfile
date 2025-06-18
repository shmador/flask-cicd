pipeline {
  agent {
    kubernetes {
      cloud 'imtech-eks'
      defaultContainer 'kaniko'
      yaml """
apiVersion: v1
kind: Pod
spec:
  serviceAccountName: default
  containers:
    - name: kaniko
      image: gcr.io/kaniko-project/executor:latest
      command:
        - cat
      tty: true

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

    - name: jnlp
      image: jenkins/inbound-agent:latest
      resources:
        requests:
          cpu: "100m"
          memory: "256Mi"
"""
    }
  }

  environment {
    REGISTRY   = 'your.registry.io'          // ← e.g. index.docker.io or my-registry.com
    REPO       = 'myorg/myapp'               // ← e.g. shmador/flask-cicd
    IMAGE_TAG  = "${env.BUILD_NUMBER}"
  }

  stages {
    stage('Checkout') {
      steps { checkout scm }
    }

    stage('Build & Push with Kaniko') {
      steps {
        container('kaniko') {
          withCredentials([usernamePassword(
            credentialsId: 'docker',
            usernameVariable: 'DOCKER_USER',
            passwordVariable: 'DOCKER_PASS'
          )]) {
            sh '''
# write a minimal docker config for Kaniko auth
mkdir -p /kaniko/.docker
cat > /kaniko/.docker/config.json <<EOF
{
  "auths": {
    "${REGISTRY}": {
      "username": "${DOCKER_USER}",
      "password": "${DOCKER_PASS}"
    }
  }
}
EOF

# now build & push
/kaniko/executor \
  --context "${WORKSPACE}" \
  --dockerfile "${WORKSPACE}/Dockerfile" \
  --destination "${REGISTRY}/${REPO}:${IMAGE_TAG}" \
  --cleanup
'''
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

    stage('Deploy with Helm') {
      steps {
        container('helm') {
          sh './deploy'
        }
      }
    }
  }
}

