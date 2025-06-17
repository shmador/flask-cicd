pipeline {
    agent any;
    stages {
        stage('Login to Docker Registry') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'docker',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh '''echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin'''
                }
            }
        }
        stage ('Run python tests') {
            steps {
                sh "python3 test-app.py"                   
            }
        }
        stage ('Build and push docker image') {
            steps {
                sh "./build"
            }
        }
        stage ('Deploy on local cluster with helm') {
            steps {
                sh "./helm upgrade --install app"
            }
        }
    }
}
