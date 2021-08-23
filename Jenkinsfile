pipeline {
    agent {
        kubernetes {
            yamlFile 'podTemplates/ps-create-doc.yaml'
        }
    }
    environment {
        CLIENT_DIR='1AW4XjI4HIeFAB5dWI5S1cipfyOfxJD9m'
    }
    parameters {
        string(name: 'CUSTOMER_NAME', defaultValue: 'Customer Name, Inc', description: 'What is the legal name of the customer?')
        string(name: 'CUSTOMER_ABBR', defaultValue: 'Customer Name', description: 'What is the abbreviation of the name of the customer?')
        string(name: 'CUSTOMER_NOSPACE', defaultValue: 'CustomerName', description: 'What is the name of the customer with no spaces?')
        choice(name: 'APPLICATION', choices: ['ci', 'cd'], description: 'Which application?')
        choice(name: 'INSTALL_TYPE', choices: ['modern', 'traditional'], description: 'Which installation type?')
        choice(name: 'ENGAGEMENT_TYPE', choices: ['general', 'prescription', 'quickstart', 'pipeline'], description: '')
        choice(name: 'K8S_PLATFORM', choices: ['AKS', 'GKE', 'EKS', 'Kubernetes', 'PKS', 'N/A'], description: 'When applicable, which k8s platform is used?')
        choice(name: 'IS_ON_PREMISE', choices: ['yes', 'no'], description: 'When applicable, will k8s be installed on premise?')
        booleanParam(name: 'INCLUDE_DETAILED_RECOMMENDATIONS', defaultValue: true, description: '')
        string(name: 'CONSULTANT_NAME', defaultValue: 'My Name', description: '')
        string(name: 'DOC_DATE', defaultValue: '2021-01-01', description: '')
        string(name: 'ENGAGEMENT_END_DATE', defaultValue: '2021-01-01', description: 'When was the last day of the engagement?')
        string(name: 'SOW_ID', defaultValue: '0061O00001OvF41QAF', description: 'What is the SOW ID?')
        string(name: 'SOW_DATE', defaultValue: '2021-01-01', description: 'When was the SOW executed?')
        string(name: 'SOW_OWNER', defaultValue: 'Daniel Martin', description: 'Who owns the SOW for this customer?')
        string(name: 'PREPAID_DAYS_REMAINING', defaultValue: '0', description: 'How many prepaid days are left?')
        /*
        Need to add parameters for traditional prescription
        :HA_MODE: yes
        :SR_PROD_CJOC_QTY: 2
        :SR_PROD_CJM_QTY: 2
        :SR_PROD_ES_QTY: 3
        :SR_PROD_AGENT_QTY: 2
        :INCLUDE_PROXY: no
        :INCLUDE_ES: yes
        :SELF_SIGNED_CERT: no
        :SSL_REQUIRED: yes
        */

    }
    stages {
        stage ("Create asciidoc from template") {
            steps {
                container("alpine") {
                    sh """
                    cat > "templates/${params.APPLICATION}-${params.INSTALL_TYPE}-${params.ENGAGEMENT_TYPE}/${params.APPLICATION}-${params.INSTALL_TYPE}-${params.ENGAGEMENT_TYPE}.adoc" <<EOF
:imagesdir: ../images
:CUSTOMER_NAME: ${params.CUSTOMER_NAME}
:CUSTOMER_ABBR: ${params.CUSTOMER_ABBR}
:CONSULTANT_NAME: ${params.CONSULTANT_NAME}
:DOC_DATE: ${params.DOC_DATE}
:HA_MODE: ${params.HA_MODE}
:ENGAGEMENT_END_DATE: ${params.ENGAGEMENT_END_DATE}
:SOW_ID: ${params.SOW_ID}
:SOW_DATE: ${params.SOW_DATE}
:SOW_OWNER: ${params.SOW_OWNER}
:PREPAID_DAYS_REMAINING: ${params.PREPAID_DAYS_REMAINING}
:K8S_PLATFORM: ${params.K8S_PLATFORM}
:IS_ON_PREMISE: ${params.IS_ON_PREMISE}
EOF
                    """
                    sh """
                    cat templates/${params.APPLICATION}-${params.INSTALL_TYPE}-${params.ENGAGEMENT_TYPE}/00-${params.APPLICATION}-${params.INSTALL_TYPE}-${params.ENGAGEMENT_TYPE}.adoc >> \
                    templates/${params.APPLICATION}-${params.INSTALL_TYPE}-${params.ENGAGEMENT_TYPE}/${params.APPLICATION}-${params.INSTALL_TYPE}-${params.ENGAGEMENT_TYPE}.adoc
                    """
                }
            }
        }

        stage ("Convert adoc to xml") {
            steps {
                container("asciidoctor") {
                    sh """
                    asciidoctor -b docbook -a allow-uri-read \
                    templates/${params.APPLICATION}-${params.INSTALL_TYPE}-${params.ENGAGEMENT_TYPE}/${params.APPLICATION}-${params.INSTALL_TYPE}-${params.ENGAGEMENT_TYPE}.adoc
                    """
                }
            }
        }

        stage ("Convert xml to docx") {
            steps {
                container("pandoc") {
                    sh """
                    /usr/local/bin/pandoc \
                    --from docbook --to docx \
                    --output ${params.CUSTOMER_NOSPACE}-${params.APPLICATION}-${params.INSTALL_TYPE}-${params.ENGAGEMENT_TYPE}.docx \
                    --reference-doc=templates/pandoc/my-custom-style-00.docx \
                    templates/${params.APPLICATION}-${params.INSTALL_TYPE}-${params.ENGAGEMENT_TYPE}/${params.APPLICATION}-${params.INSTALL_TYPE}-${params.ENGAGEMENT_TYPE}.xml
                    """
                }
            }
        }

        stage ("Upload to Google Docs") {
            steps {
                container("gdocs") {
                    withCredentials([file(credentialsId: 'token.json', variable: 'token')]) {
                        writeFile file: './gdocs/token.json', text: readFile(token)
                    }
                    script {
                        DOC_ID = sh (
                            script: "./gdocs/uploadDoc.py ${env.CLIENT_DIR} ${params.CUSTOMER_NOSPACE}-${params.APPLICATION}-${params.INSTALL_TYPE}-${params.ENGAGEMENT_TYPE}.docx",
                            returnStdout: true
                            ).trim()
                    }
                    sh "echo ${DOC_ID}"
                    sh """
                        ./gdocs/addCoverPage.py ${DOC_ID}
                        """
                }
            }
        }
    }
}