
pipeline {
    agent any

    environment {
        PATH+DOCKER = 'C:\\Users\\Dimas Ramadhan\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin'
        IMAGE_NAME = 'dimasramadhan/simple-app'
        REGISTRY_CREDENTIALS = 'dockerhub-credentials'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build') {
            steps {
                bat 'echo "Build di Windows"'
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t %IMAGE_NAME%:%BUILD_NUMBER% .'
            }
        }

        stage('Push Docker Image') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-credentials',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    bat '''
                        @echo off
                        echo %DOCKER_PASS%| docker login -u %DOCKER_USER% --password-stdin
                    '''
                    bat 'docker push %IMAGE_NAME%:%BUILD_NUMBER%'
                    bat 'docker tag %IMAGE_NAME%:%BUILD_NUMBER% %IMAGE_NAME%:latest'
                    bat 'docker push %IMAGE_NAME%:latest'
                }
            }
        }
    }

    post {
        always {
            echo 'Selesai build'
        }
    }
}
