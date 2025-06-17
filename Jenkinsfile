pipeline {
    agent any;
    stages {
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
