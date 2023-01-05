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
		    changeset "dummy"
                }
            }
            steps {
                sh 'yamllint infra-SOT/*'
            }
        }
        stage('Build delete variables'){
            when {
                anyOf {
                    changeset "infra-SOT/tenants_mapping.yaml"
                    changeset "dummy"
                }
            }
            steps {
                dir('builder'){
                     sh 'ansible-playbook playbook/tenant_delete_generator.yaml -v'
		     sh 'yamllint builder/host_vars/*'
                }
            }
        }
	stage('Deploy delete vars'){
           when {
                anyOf {
                    changeset "infra-SOT/tenants_mapping.yaml"
                    changeset "dummy"
                }
            }
            steps {
                dir('builder'){
                     sh 'ansible-playbook playbook/tenant-delete.yaml -v'
                }
            }
        }


    }
}
