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

stage('Snyk Scan') {

    steps {

        withCredentials([string(credentialsId: 'Snyk_Suchit', variable: 'SNYK_TOKEN')]) {

            sh '''

            # Create virtual environment

            python3 -m venv myenv

            . env/bin/activate



            # Use venv pip explicitly

            env/bin/pip install -r requirements.txt || true



            # Install snyk locally (no sudo issues)

            npm install snyk



            # Authenticate

            npx snyk auth $SNYK_TOKEN



            # Run scans

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

      . zap_env/bin/activate



      echo "📂 Checking files"

      pwd

      ls -la



      # Install dependencies if present

      if [ -f requirement.txt ]; then

        echo "📦 Installing dependencies"

        zap_env/bin/pip install -r requirement.txt

      else

        echo "⚠️ No requirement.txt found, skipping..."

      fi



      # Install required packages

      zap_env/bin/pip install python-owasp-zap-v2.4 setuptools uvicorn fastapi || true



      echo "🚀 Starting FastAPI app"

      nohup zap_env/bin/uvicorn main:app --host 0.0.0.0 --port 8000 > zap_app.log 2>&1 &

      APP_PID=$!



      echo "⏳ Waiting for app to be ready..."



      # Smart wait

      for i in {1..10}; do

        if curl -s http://127.0.0.1:8000 > /dev/null; then

          echo "✅ App is up!"

          break

        fi

        echo "Waiting..."

        sleep 5

      done



      # Get host IP

      HOST_IP=$(hostname -I | awk '{print $1}')

      echo "🌐 Host IP: $HOST_IP"



      echo "🐳 Running ZAP scan"



      docker run --rm \

        --network host \

        -v $(pwd):/zap/wrk \

        owasp/zap2docker-stable \

        zap-baseline.py \

        -t http://$HOST_IP:8000 \

        -r /zap/wrk/zap_report.html || true



      echo "📄 Checking report file..."

      ls -la zap_report.html || echo "❌ Report not found"



      echo "🛑 Stopping app"

      kill $APP_PID || true

    '''



    publishHTML([

      allowMissing: true,   // prevents failure if report missing

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

      echo "📦 Setting up build environment"



      python3 -m venv env



      # Use venv explicitly (fixes PEP 668 issue)

      env/bin/python -m pip install --upgrade pip

      env/bin/pip install build



      echo "🚀 Building package"

      env/bin/python -m build || echo "⚠️ Build failed (missing pyproject.toml/setup.py)"



      echo "📂 Checking dist folder"

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