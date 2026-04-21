pipeline {
    agent any

    environment {
        DOCKER_HUB = "raj122"
        IMAGE_TAG = "latest"
    }

    stages {

        stage('Clone Code') {
            steps {
                git 'https://github.com/rajkushwaha01/three-tier-app.git'
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('sonar-server') {
                    sh '''
                    sonar-scanner \
                    -Dsonar.projectKey=three-tier-app \
                    -Dsonar.sources=. \
                    -Dsonar.login=<SONAR_TOKEN>
                    '''
                }
            }
        }

        stage('Build Backend Image') {
            steps {
                dir('backend') {
                    sh 'docker build -t raj122/backend:latest .'
                }
            }
        }

        stage('Build Frontend Image') {
            steps {
                dir('frontend') {
                    sh 'docker build -t raj122/frontend:latest .'
                }
            }
        }

        stage('Push Images') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-creds', usernameVariable: 'USER', passwordVariable: 'PASS')]) {
                    sh '''
                    echo $PASS | docker login -u $USER --password-stdin
                    docker push raj122/backend:latest
                    docker push raj122/frontend:latest
                    '''
                }
            }
        }

        stage('Upload to Nexus') {
            steps {
                sh '''
                curl -u admin:admin123 --upload-file backend/app.py \
                http://<NEXUS-IP>:8081/repository/maven-releases/app.py
                '''
            }
        }

        stage('Deploy Backend') {
            steps {
                sh 'kubectl apply -f k8s/backend.yaml'
            }
        }

        stage('Deploy Frontend') {
            steps {
                sh 'kubectl apply -f backend.yaml'
		sh 'kubectl apply -f frontend.yaml'
          }
        }

    }
}
