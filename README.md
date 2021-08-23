# Professional Services Document Generation

This repo contains the next iteration of the `cloudbees/ps-autogen-docs` repo and is created to do the same thing, but updated to include new features. The primary new feature is the ability to generate an editable document that is uploaded to Google Docs automatically.

As of 2021-07-26, this tool is in the beta stage. It is ready for use, however, each line of the generated document should be reviewed closely to ensure the content is up to standard.

**NOTE: This tool is not designed to create a completed document. The consultant is responsible for reviewing and adding context to the doc before it is delivered to the customer. Do not run the tool and send the output directly to the customer.**

## Known Issues / To Dos
* CD is not include at this time
* Searching Google Drive for the appropriate customer folder is not trivial. To work around this, the tool has coded the folder ID to a `PS_AUTOMATION` directory in the root of the Customers and Prospects folder in Drive. All created docs will be created there.
* Google Docs Authentication for the the CLI tool is not ready. A secret is required to make it work, and I am unsure on where it needs to be stored.
* Prescription documents are generating, but the checklist tables are being destroyed

## How to Create a Doc
A CloudBees controller is installed at [https://ps.core-devops.com] which contains the parameterized job that will create the document. Please create an account at the URL and let Scott Batchelder know. He will add you to the user group that will allow you to run the job. Before starting the job, you will need to know the following parameters:
* CUSTOMER_NAME - the full legal name of the customer, Cool Customer, Inc.
* CUSTOMER_ABBR - the abbreviation of the full name, Cool Customer
* CUSTOMER_NOSPACE - the abbreviation of the full name, but with no spaces, CoolCustomer
* APPLICATION - either "ci" or "cd"
* INSTALL_TYPE - either "modern" or "traditional"
* ENGAGEMENT_TYPE - either "general", "prescription", "quickstart", or "pipeline"
* K8S_PLATFORM - name of kubernetes platform used. If traditional, select "N/A"
* IS_ON_PREMISE - is the kubernetes installation on premise
* INCLUDE_DETAILED_RECOMMENDATIONS - should the detailed recommendations be appended to the doc
* CONSULTANT_NAME - name of person(s) on the engagement
* DOC_DATE - date the document is created
* ENGAGEMENT_END_DATE - final day of the engagement
* SOW_ID - the ID of the SOW for the engagement
* SOW_DATE - the date the SOW was signed
* SOW_OWNER - owner of the SOW
* PREPAID_DAYS_REMAINING - the number of prepaid days left for the engagement

## Feedback
If you have questions or comments about this tool, please ping Scott Batchelder in Slack or email him at sbatchelder@cloudbees.com.

