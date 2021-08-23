#!/usr/bin/env bash

THIS_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo "Capturing variables"
# Basic Info, also captured from CI job
CUSTOMER_NAME="Sample Customer"
CUSTOMER_ABBR="Sample Customer"
APPLICATION="ci"        			# [ci,cd]
INSTALL_TYPE="traditional"   	# [modern,traditional]
ENGAGEMENT_TYPE="general"			# [general,prescription,quickstart,pipeline]
K8S_PLATFORM="AKS"            # [AKS,GKE,EKS,Kubernetes,PKS,N/A]
IS_ON_PREMISE="yes"           # [yes,no]
INCLUDE_DETAILED_RECOMMENDATIONS="true"
CONSULTANT_NAME="My Name"
DOC_DATE=$(date +"%Y-%m-%d")
ENGAGEMENT_END_DATE="2021-07-01"
SOW_ID="PS-0061O00001OvF41QAF"
SOW_DATE="2021-04-05"
SOW_OWNER="Daniel Martin"
PREPAID_DAYS_REMAINING="0"

# HA_MODE="yes"

# Create Client name var with no spaces
CLIENT_NOSPACE=$(echo -e "${CUSTOMER_ABBR}" | tr -d '[:space:]')

echo "Create asciidoc from template"
cat > "templates/${APPLICATION}-${INSTALL_TYPE}-${ENGAGEMENT_TYPE}/${APPLICATION}-${INSTALL_TYPE}-${ENGAGEMENT_TYPE}.adoc" <<EOF
:imagesdir: ../images
:CUSTOMER_NAME: ${CUSTOMER_NAME}
:CUSTOMER_ABBR: ${CUSTOMER_ABBR}
:CONSULTANT_NAME: ${CONSULTANT_NAME}
:DOC_DATE: ${DOC_DATE}
:ENGAGEMENT_END_DATE: ${ENGAGEMENT_END_DATE}
:SOW_ID: ${SOW_ID}
:SOW_DATE: ${SOW_DATE}
:SOW_OWNER: ${SOW_OWNER}
:PREPAID_DAYS_REMAINING: ${PREPAID_DAYS_REMAINING}
:K8S_PLATFORM: ${K8S_PLATFORM}
:IS_ON_PREMISE: ${IS_ON_PREMISE}
EOF

cat "templates/${APPLICATION}-${INSTALL_TYPE}-${ENGAGEMENT_TYPE}/00-${APPLICATION}-${INSTALL_TYPE}-${ENGAGEMENT_TYPE}.adoc" >> \
"templates/${APPLICATION}-${INSTALL_TYPE}-${ENGAGEMENT_TYPE}/${APPLICATION}-${INSTALL_TYPE}-${ENGAGEMENT_TYPE}.adoc"

echo "Convert asciidoc to XML"
 docker run -it -v "${THIS_DIR}:/opt/docs" -w /opt/docs asciidoctor/docker-asciidoctor \
   asciidoctor \
   -b docbook \
   -a allow-uri-read \
   -a pdf-stylesdir=resources/themes \
   -a pdf-style=cloudbees \
   -a pdf-fontsdir=resources/fonts/ttf \
   templates/${APPLICATION}-${INSTALL_TYPE}-${ENGAGEMENT_TYPE}/${APPLICATION}-${INSTALL_TYPE}-${ENGAGEMENT_TYPE}.adoc

echo "Convert XML to DOCX"
docker run -it -v "${THIS_DIR}:/opt/docs" -w /opt/docs pandoc/core \
  --from docbook \
  --to docx \
  --output "${CLIENT_NOSPACE}-${APPLICATION}-${INSTALL_TYPE}-${ENGAGEMENT_TYPE}.docx" \
  --reference-doc=templates/pandoc/my-custom-style-00.docx \
  templates/${APPLICATION}-${INSTALL_TYPE}-${ENGAGEMENT_TYPE}/${APPLICATION}-${INSTALL_TYPE}-${ENGAGEMENT_TYPE}.xml

# echo "Locate the client's PS directory"
#./gdocs/findClient.py ${CUSTOMER_ABBR}
CLIENT_DIR="1AW4XjI4HIeFAB5dWI5S1cipfyOfxJD9m"

echo "Upload the DOCX to Google Docs"
DOC_ID=$(./gdocs/uploadDoc.py ${CLIENT_DIR} ${CLIENT_NOSPACE}-${APPLICATION}-${INSTALL_TYPE}-${ENGAGEMENT_TYPE}.docx)

echo "Add the cover page to the doc"
./gdocs/addCoverPage.py ${DOC_ID}

echo "Clean up"
rm -f "templates/${APPLICATION}-${INSTALL_TYPE}-${ENGAGEMENT_TYPE}/${APPLICATION}-${INSTALL_TYPE}-${ENGAGEMENT_TYPE}.adoc"
rm -f "templates/${APPLICATION}-${INSTALL_TYPE}-${ENGAGEMENT_TYPE}/${APPLICATION}-${INSTALL_TYPE}-${ENGAGEMENT_TYPE}.xml"
rm -f "${CLIENT_NOSPACE}-${APPLICATION}-${INSTALL_TYPE}-${ENGAGEMENT_TYPE}.docx"

echo "done"