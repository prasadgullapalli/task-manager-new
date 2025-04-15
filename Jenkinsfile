pipeline {
    agent any

    tools {
        python 'Python 3.13' // Or whichever version you've configured in Jenkins
    }

    environment {
        VENV_DIR = 'venv'
    }

    stages {
        stage('Clone Repository') {
            steps {
                git 'https://github.com/prasadgullapalli/task-manager-new.git'
            }
        }

        stage('Set Up Virtual Environment') {
            steps {
                bat "python -m venv %VENV_DIR%"
                bat "call %VENV_DIR%\\Scripts\\activate && pip install --upgrade pip"
            }
        }

        stage('Install Dependencies') {
            steps {
                bat "call %VENV_DIR%\\Scripts\\activate && pip install -r requirements.txt"
            }
        }

        stage('Run Flask App') {
            steps {
                bat "call %VENV_DIR%\\Scripts\\activate && python app.py"
            }
        }
    }
}
