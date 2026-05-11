pipepline{
    agent any
    environment{
        KUBECONFIG: 'C:\\Users\\Admin\\.kube\\config'
    }
    stages{
        stage('Clone Source'){
            steps{
                git url: 'https://github.com/Adhyantha/python-flask-crud-app.git',
                branch: 'main'
            }
        }
        stage('Build Docker Image'){
            steps{
                dir('app'){
                    bat 'docker build -t pythonflaskcrudapp:v1 .'
                }
            }
        }
        stage('Verify Docker Image'){
            steps{
                bat 'docker images'
            }
        }
        stage('Deploy MySQL'){
            steps{
                dir('kubernetes'){
                    bat 'kubectl apply -f mysql-deployment.yaml'
                    bat 'kubectl apply -f mysql-service.yaml'
                }
            }
        }
        stage('Deploy Flask App'){
            steps{
                dir('kubernetes'){
                    bat 'kubectl apply -f app-deployment.yaml'
                    bat 'kubectl apply -f app-service.yaml'
                }
            }
        }
        stage('Check Kubernetes Resources'){
            steps{
                bat 'kubectl get pods'
                bat 'kubectl get svc'
                bat 'kubectl get deployments'
            }
        }
        stage('Deploy Helm Chart'){
            steps{
                bat 'helm upgrade --install python-flask-app ./python-flask-crud-chart'
            }
        }
    }
}