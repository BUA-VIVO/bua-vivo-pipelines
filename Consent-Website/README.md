# Berlin University Alliance - GDPR (DSGVO) - Consent Application 


{DESCRIPTION}


## Configuration

There are 4 configuration files that need to be in place for the application to work:

1. copy static/config_template.yaml to static/config.yaml, and set the correct information for the MongodDB host to be used
2. copy static/token_template.yaml to static/token.yaml, and generate a list of unique strings for tokens for each project needing data consent to be registered
3. copy data/projectname_token.yaml to data/yourproject_token.yaml for each project needing data consent to be registered, and create a list of and generate a list of unique string tokens
4. open .streamlit/config.toml and configure the browser.serverAdress to your domain hosting the application
