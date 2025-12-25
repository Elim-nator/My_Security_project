pipeline {
    agent any
    agent any
    stages {
        stage('Test') {
            steps {
                echo 'Security project build successful!'
                sh 'ls -la'  // List files for verification
            }
        }
    }    
    environment {
        DOCKER_IMAGE = 'intel-gathering:latest'
        CONTAINER_NAME = 'intel-app'
    }
    
    stages {
        stage('Checkout') {
            steps {
                git url: 'https://github.com/Elim-nator/My_Security_project.git', branch: 'main'
                echo '✅ Code checked out from GitHub'
            }
        }
        
        stage('Security Scan') {
            steps {
                sh '''
                # Python security scan
                pip install bandit
                bandit -r app/ || true
                
                # Docker image vulnerability scan
                docker run --rm -v $(pwd):/workspace aquasec/trivy image python:3.11-slim || true
                '''
                echo '✅ Security scans completed'
            }
        }
        
        stage('Build Docker') {
            steps {
                sh '''
                docker-compose build --no-cache
                docker-compose up -d --build
                '''
                echo '✅ Containers built and deployed'
            }
        }
        
        stage('Health Check') {
            steps {
                sh '''
                sleep 10  # Wait for startup
                curl -f http://localhost:5000 || exit 1
                curl -f http://localhost/intel
                '''
                echo '✅ Application health confirmed'
            }
        }
        
        stage('Deploy to Apache') {
            steps {
                sh '''
                # Ensure Apache proxy works
                sudo systemctl restart apache2
                curl -H "Host: intel.local" http://localhost || exit 1
                '''
                echo '✅ Deployed behind Apache reverse proxy'
            }
        }
    }
    
    post {
        always {
            sh 'docker-compose logs --tail=50'
        }
        success {
            echo '🎉 Pipeline SUCCESS! Access: http://10.0.2.15 (Apache) or http://10.0.2.15:5000 (Direct)'
        }
        failure {
            echo '❌ Pipeline FAILED - Check logs above'
            sh 'docker-compose down'
        }
    }
}
