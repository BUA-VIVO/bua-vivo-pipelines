# KT Sherpa Classifier Pipeline
These scripts perform pre-classifications, API-transactions for training and classification of Documents using the https://kairntech.com/ Sherpa engine

The prepper.py file does calls to the Classes and funcitons in /functions perfroming different tasks:

1. Downloads academic articles and books from https://edoc.hu-berlin.de
2. Performs pre-classification of the documents based on the [b2find displinary research classification vocabulary](https://github.com/EUDAT-B2FIND/md-ingestion/blob/master/etc/b2find_disciplines.json) mapped onto a  topics within the semantic space of each category, retrived through [ChatGPT](https://chat.openai.com)
3. Uploads text extracted from the downloaded PDFs, then pre-classified to LLM ML training projects in the Sherpa application over its REST API
4. Classifies documents over Sherpa's REST APIs classifications endpoints, using the resulting train models and produces resulting JSON files containing the classifications and pre-classifications for proof


## Configuration of Uploader and api-classifier
The .env file at the root of the project informs the scripts in 3 and 4, and has to be updated with the relevant metadata in order to connect to- and be able to perform the tasks in Sherpa

## The Jupiter Notebook files @todo

* /splits/full
* /splits/less50



