pipeline {
    agent any
    stages {
	stage('Test command') {
            steps {
		    sh 'python3 --version'
                    sh 'yamllint -v'
            }
        }
    }
}
