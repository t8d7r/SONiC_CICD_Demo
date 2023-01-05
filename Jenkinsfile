pipeline {
    agent {label 'services'}
    stages {
	stage('Test command') {
            steps {
		    sh 'python3 --version'
                    sh 'yamllint -v'
            }
        }
        stage('Check syntax'){
	    when {
                anyOf {
                    changeset "infra-SOT/tenants_mapping.yaml"
		    changeset "infra-SOT/dummy"
                }
            }
            steps {
                sh 'yamllint infra-SOT/tenants_mapping.yaml'
            }
        }
    }
}
