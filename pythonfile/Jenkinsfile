pipeline {
    agent any

    environment {
        GIT_REPO = "https://github.com/SuchitShetty/SuchitShetty.git"
        GIT_CREDENTIALS_ID = "suchit.shashi.shetty@accenture.com"
        VENV_DIR = "venv"
    }

    stages {

        stage('Checkout Code') {
            steps {
                git credentialsId: "${GIT_CREDENTIALS_ID}",
                    url: "${GIT_REPO}",
                    branch: "main"
            }
        }

        stage('Setup Python Environment') {
            steps {
                sh '''
                python3 -m venv $VENV_DIR
                . $VENV_DIR/bin/activate
                pip install --upgrade pip
                pip install -r Requirement.txt
                '''
            }
        }

        stage('Run FastAPI Validation') {
            steps {
                sh '''
                . $VENV_DIR/bin/activate
                python -m py_compile Maintest.py
                '''
            }
        }

        stage('Start FastAPI Server (Optional)') {
            steps {
                sh '''
                . $VENV_DIR/bin/activate
                nohup uvicorn main:app --host 0.0.0.0 --port 8000 &
                '''
            }
        }
    }

    post {
        success {
            echo 'Pipeline executed successfully 🚀'
        }
        failure {
            echo 'Pipeline failed ❌'
        }
    }
}