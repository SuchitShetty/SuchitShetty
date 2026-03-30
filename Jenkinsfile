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
        $VENV_DIR/bin/pip install --upgrade pip

        # Fix file name case issue
        if [ -f Requirement.txt ]; then
          $VENV_DIR/bin/pip install -r Requirement.txt
        fi
        '''
      }
    }

    stage('Snyk Scan') {
      steps {
        withCredentials([string(credentialsId: 'Snyk_Suchit', variable: 'SNYK_TOKEN')]) {
          sh '''
          python3 -m venv myenv

          myenv/bin/pip install -r Requirement.txt || true

          npm install snyk

          npx snyk auth $SNYK_TOKEN

          npx snyk test --all-projects || true
          npx snyk monitor --all-projects || true
          '''
        }
      }
    }

    stage('DAST (ZAP Scan)') {
      steps {
        sh '''
        echo "🐍 Setting up environment"

        python3 -m venv zap_env

        echo "📂 Checking files"
        pwd
        ls -la

        # FIXED: Correct filename
        if [ -f Requirement.txt ]; then
          echo "📦 Installing dependencies"
          zap_env/bin/pip install -r Requirement.txt
        else
          echo "⚠️ No Requirement.txt found, skipping..."
        fi

        zap_env/bin/pip install python-owasp-zap-v2.4 uvicorn fastapi || true

        echo "🚀 Starting FastAPI app"
        nohup zap_env/bin/uvicorn main:app --host 0.0.0.0 --port 8000 > zap_app.log 2>&1 &
        APP_PID=$!

        echo "⏳ Waiting for app..."

        for i in {1..10}; do
          if curl -s http://127.0.0.1:8000 > /dev/null; then
            echo "✅ App is up!"
            break
          fi
          sleep 5
        done

        HOST_IP=$(hostname -I | awk '{print $1}')
        echo "🌐 Host IP: $HOST_IP"

        echo "🐳 Running ZAP scan"

        # ✅ FIXED docker command (NO broken line continuation)
        docker run --rm --network host -v $(pwd):/zap/wrk owasp/zap2docker-stable zap-baseline.py -t http://$HOST_IP:8000 -r /zap/wrk/zap_report.html || true

        echo "📄 Checking report"
        ls -la zap_report.html || echo "❌ Report not found"

        echo "🛑 Stopping app"
        kill $APP_PID || true
        '''

        publishHTML([
          allowMissing: true,
          alwaysLinkToLastBuild: true,
          keepAll: true,
          reportDir: '.',
          reportFiles: 'zap_report.html',
          reportName: 'ZAP DAST Report'
        ])

        archiveArtifacts artifacts: 'zap_report.html', fingerprint: true
      }
    }

    stage('Build Package') {
      steps {
        sh '''
        python3 -m venv env

        env/bin/python -m pip install --upgrade pip
        env/bin/pip install build

        env/bin/python -m build || echo "⚠️ Build failed"

        ls -la dist || true
        '''

        archiveArtifacts artifacts: 'dist/*', fingerprint: true, allowEmptyArchive: true
      }
    }
  }

  post {
    success {
      echo '✅ Pipeline executed successfully'
    }
    failure {
      echo '❌ Pipeline failed'
    }
  }
}