# KT Sherpa Classifier Pipeline
These scripts perform pre-classifications, API-transactions for training and classification of Documents using the https://kairntech.com/ Sherpa engine

The prepper.py file does calls to the Classes and funcitons in /functions perfroming different tasks:


1. Downloads academic articles and books from https://edoc.hu-berlin.de

	```
		# Load Info from Edoc-Server
		#  --> There is a 1sec Wait-Periode between reconnects, can be changed via sleep var
			loadInfo(riPath=fp_edocRI, skip=True)
		
		# Load PDFs from HU Server
		# # --> Will always download additional PDFs!
		loadPdfs(riPath=fp_edocRI,
		pdfPath = pdfPath,
		numberOfDownloads=20000,
		skip=False)
	```

2. Performs pre-classification of the documents based on the [b2find displinary research classification vocabulary](https://github.com/EUDAT-B2FIND/md-ingestion/blob/master/etc/b2find_disciplines.json) mapped onto a  topics within the semantic space of each category, retrived through [ChatGPT](https://chat.openai.com)

	```
		# Classify PDFs
		classify(filepathRI=fp_edocRI,
		        filepathB2Find=fp_b2find,
		        filepathDewey=fp_dewey,
		        pdfPath=pdfPath)
	
	```

3. Uploads text extracted from the downloaded PDFs, then pre-classified to LLM ML training projects in the Sherpa application over its REST API

	```
		# Upload pdf JSON files to Sherpa over SHERPA API
		localpath = str(filesPath) + '/api_inputs/'
		files = Path(localpath).glob('*')
		load_envs() # Load environment variables from .env
		index = 1
		
		for file in files:
			if not wait_for_job():
				res = upload_document(os.getenv("PROJECT_NAME"), file, {"ignoreLabelling": "false", "segmentationPolicy": "no_segmentation", "splitCorpus": "false", "cleanText": "true", "generateCategoriesFromSourceFolder": "false"}, os.getenv("ADMIN_USER"), os.getenv("ADMIN_PASS"), str(index))
	
	```

4. Classifies documents over Sherpa's REST APIs classifications endpoints, using the resulting train models and produces resulting JSON files containing the classifications and pre-classifications for proof

	```
		#  Classify PDFs over Sherpa-API
		load_envs() # Load environment variables from .env
		if not wait_for_job():
			api_Classifier = apiClassifier(fp_edocRI, fp_b2find, fp_dewey, pdfPath)
			api_Classifier.call_api()
		
	```



## Configuration of Uploader and api-classifier
The .env file at the root of the project informs the scripts in 3 and 4, and has to be updated with the relevant metadata in order to connect to- and be able to perform the tasks in Sherpa

## The Jupiter Notebook files @todo

* /splits/full
* /splits/less50



