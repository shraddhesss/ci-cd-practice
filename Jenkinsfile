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
                // Wipe out the old containers started by GitHub Actions
                sh 'docker rm -f $(docker ps -aq) || true'
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
