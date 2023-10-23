# Berlin University Alliance VIVO  Pipelines

This repository contains artefacts produced for the [Berlin University Alliance](https://www.berlin-university-alliance.de/) [VIVO project](https://www.berlin-university-alliance.de/commitments/sharing-resources/vivo/index.html).

The applications make up the pipelines needed to import and format research data from sources ranging from Excel sheets to h[arvested data over REST API](https://github.com/BUA-VIVO/bua-vivo-pipelines/tree/main/orcidfetcher) calls.

The data is then formatted into RDF triples in a JSON format for ingestion in MongoDB

The MongoDB data serves as a federation point for the possibility of import of RDF triples into multiple VIVO instances

In addition, the repository contains an [application for registering user consent](https://github.com/BUA-VIVO/bua-vivo-pipelines/tree/main/Consent-Website) for the  publication of research artefacts linked to the User over Open Linked Data in the VIVO platform
