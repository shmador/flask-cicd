pipeline {
    agent any;
    stages {
        stage ('Run python tests') {
            steps {
                python3 test-app                   
            }
        }
        stage ('Build and push docker image') {
            steps {
                ./build
            }
        }
        stage ('Deploy on local cluster with helm') {
            helm upgrade --install app
        }
    }
}
