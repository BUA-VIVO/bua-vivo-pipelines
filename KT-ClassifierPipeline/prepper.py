from pathlib import Path
from functions.edocLoader import loadInfo
from functions.pdfLoader import loadPdfs
from functions.classifier import classify
from functions.apiClassifier import apiClassifier
from functions.documentUploader import load_envs, wait_for_job

# Pathes
cwd = Path.cwd()
filesPath = cwd / 'files'
pdfPath = cwd / 'pdfs'
fp_edocRI = Path(filesPath, 'pdfUrlList.json')
fp_b2find = Path(filesPath, 'B2Find_corrected.json')
fp_dewey = Path(filesPath, 'dewey.json')

# Load Info from Edoc-Server
#  --> There is a 1sec Wait-Periode between reconnects, can be changed via sleep var
# loadInfo(riPath=fp_edocRI,
#          skip=True)
#
# # Load PDFs from HU Server
# # --> Will always download additional PDFs!
# loadPdfs(riPath=fp_edocRI,
#          pdfPath = pdfPath,
#          numberOfDownloads=20000,
#          skip=False)

# Classify PDFs
# classify(filepathRI=fp_edocRI,
#          filepathB2Find=fp_b2find,
#          filepathDewey=fp_dewey,
#          pdfPath=pdfPath)


# Upload pdf JSON files to Sherpa over SHERPA API

#localpath = str(filesPath) + '/api_inputs/'
#files = Path(localpath).glob('*')
#load_envs()
#index = 1

#for file in files:
#    if not wait_for_job():
#        print(str(index) + "_" + str(file) + " IN PROJECT " + os.getenv("PROJECT_NAME"))
#        res = upload_document(os.getenv("PROJECT_NAME"), file, {"ignoreLabelling": "false", "segmentationPolicy": "no_segmentation", "splitCorpus": "false", "cleanText": "true", "generateCategoriesFromSourceFolder": "false"}, os.getenv("ADMIN_USER"), os.getenv("ADMIN_PASS"), str(index))
#        index = index + 1

	
# Classify PDFs over Sherpa-API
# load_envs()
# if not wait_for_job():
#    api_Classifier = apiClassifier(fp_edocRI, fp_b2find, fp_dewey, pdfPath)
#    api_Classifier.call_api()







