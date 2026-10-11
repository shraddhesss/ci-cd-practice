pipeline {
    agent any
    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/shraddhesss/ci-cd-practice.git'
            }
        }
        stage('Clean Environment') {
            steps {
                // Safely find all containers and remove them (Jenkins-proof)
                sh 'docker ps -aq | xargs -r docker rm -f || true'
                // Clear out any lingering Docker networks
                sh 'docker network prune -f || true'
            }
        }
        stage('Deploy Application') {
            steps {
                // Build and launch the new multi-container app
                sh 'docker compose up -d --build'
            }
        }
    }
}