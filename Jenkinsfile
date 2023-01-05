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
        stage('Build variables'){
            when {
                anyOf {
                    changeset "infra-SOT/tenants_mapping.yaml"
                    changeset "dummy"
                }
            }
            steps {
                dir('builder'){
                     sh 'ansible-playbook playbook/tenant_delete_generator.yaml -i deleteinventory -v'
                     sh 'ansible-playbook playbook/tenant_update_generator.yaml -i inventory -v'
                }
            }
        }
	stage('Check generated variables files'){
           when {
                anyOf {
                    changeset "infra-SOT/tenants_mapping.yaml"
                    changeset "dummy"
                }
            }
            steps {
                sh 'yamllint builder/host_vars/*'
            }
        }


    }
}
