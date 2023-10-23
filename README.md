# Berlin University Alliance VIVO  Pipelines

This repository contains artefacts produced for the [Berlin University Alliance](https://www.berlin-university-alliance.de/) [VIVO project](https://www.berlin-university-alliance.de/commitments/sharing-resources/vivo/index.html).

The applications make up the pipelines needed to import and format research data from sources ranging from Excel sheets to harvested data over REST API calls.

The data is then formatted into RDF triples in a JSON format for ingestion in MongoDB

THe MongoDB data serves as a federation point for the possibility of import of RDF triples into multiple VIVO instances

In addition, the repository contains an application for registering user consent for the  publication of research artefacts linked to the User over Open Linked Data in the VIVO platform

## Configuration

There are 4 configuration files that need to be in place for the application to work:

1. copy static/config_template.yaml to static/config.yaml, and set the correct information for the MongodDB host to be used
2. copy static/token_template.yaml to static/token.yaml, and generate a list of unique strings for tokens for each project needing data consent to be registered
3. copy data/projectname_token.yaml to data/yourproject_token.yaml for each project needing data consent to be registered, and create a list of and generate a list of uniqute string tokens
4. open .streamlit/config.toml and configure the browser.serverAdress to your domain hosting the application

