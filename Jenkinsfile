pipeline {
    agent {label 'services'}
    stages {
	stage('Test command') {
            steps {
		    sh 'python3 --version'
                    sh 'yamllint -v'
            }
        }
    }
}
