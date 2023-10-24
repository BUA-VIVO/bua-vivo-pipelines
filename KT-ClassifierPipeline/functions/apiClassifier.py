# -*- coding: utf-8 -*-
import json
from functions.tools import jsonHandler
import fitz
from tqdm import tqdm
import requests
import pathlib
import os



class apiClassifier:

    def __init__(self, filepathRI, filepathB2Find, filepathDewey, pdfPath):
        self.filepathRI = filepathRI
        self.filepathB2Find = filepathB2Find
        self.filepathDewey = filepathDewey
        self.pdfPath = pdfPath



    def call_api(self):
        print('lets Preclassify')
        KToutput = []
        b2find = jsonHandler(path=self.filepathB2Find,defaultContent=[])
        edocRI = jsonHandler(path=self.filepathRI,defaultContent=[])
        dewey = jsonHandler(path=self.filepathDewey,defaultContent=[])

        glob = self.pdfPath.glob('**/*')
        pdfs = [f for f in glob if f.is_file()]
        outer_counter = 1
        counter = 1
        for pdf in tqdm(pdfs):
            print(str(outer_counter) + " : " + str(counter))
            ktDict = {}
            researchInfo = [x for x in edocRI if x['filename'] == pdf.stem][0]
            print(pdf.stem)
            try:
                doc = fitz.open(pdf)
            except:
                pass
            else:


                pages=[page.get_text("text") for page in doc]
                doctext = " ".join(pages)

                if doctext.strip() == '':
                    ## PDF has no OCR - Text will be skipped
                    print(f" {pdf.stem} skipped - No Text in PDF")
                else:

                    ktDict['identifier'] = pdf.stem+'.'+pdf.suffix
                    ktDict['title'] = pdf.stem
                    print("TITLE")
                    print(pdf.stem)
                    ktDict['categories'] = []
                    probs = {}
                    for catID,catInfo in b2find.items():
                        probs[catID] = 0
                        if catInfo['keywords_de'] == "-- error --":
                            keywords = catInfo['keywords_en']
                        elif catInfo['keywords_en'] == "-- error --":
                            keywords = catInfo['keywords_de']
                        else:
                            keywords = catInfo['keywords_de']+catInfo['keywords_en']
                        for kwDict in keywords:
                            kw = kwDict['Keyword']
                            prob = kwDict['Wahrscheinlichkeit']
                            # perfect match FullText
                            pageCount = int(doc.page_count)
                            if ' '+kw+' ' in doctext:
                                no = str(doctext).count(kw)
                                probs[catID] += (float(no)*float(prob) / pageCount)
                            # Perfect Author Keyword matches
                            if kw in researchInfo['subjects']:
                                probs[catID] += 10
                            # perfect Dewey matches
                            ddc = [x for x in researchInfo['ddc'] if x[0].isnumeric()]
                            deweyCats = [dewey[x[0]] for x in ddc]
                            if kw in deweyCats:
                                probs[catID] += 2.5


                    probsOut = {x:y for x,y in probs.items() if float(y) >= 1}
                    if probsOut == {}:
                        ktDict = {}
                        print(f" {pdf.stem} skipped - No Categories found")
                    else:
                        maxProb = max(probsOut.values())
                        probsFinal = {x:y for x,y in probs.items() if float(y) >= maxProb*0.3}
                        for label,score in probsFinal.items():
                            ktDict['categories'].append({'label':label,'score':score/maxProb})

                    result_data = self.annotate_document(doctext)
                    ktDict['api_classified'] = result_data
                    KToutput.append(ktDict)


                    if counter == 200:
                        with open("files/api_outputs/16Kall_classified_"+str(outer_counter)+".json", 'w') as file_object:
                            file_object.write(json.dumps(KToutput))
                            KToutput = []
                            counter = 1

                outer_counter += 1
                counter += 1

    def annotate_document(self, document):
        resultdata = []
        endpoint = os.getenv("HOST_URL")+"/"+os.getenv("ANNOTATION_PATH")
        headers = {'Content-Type': 'text/plain'}
        post_response = requests.post(
            url=endpoint,
            data=document.encode('utf-8'),
            auth=(os.getenv("NORMAL_USER"), os.getenv("NORMAL_PASS")),
            headers=headers)

        if post_response.status_code == 200:
            result = post_response.json()
            for cat in result['categories']:
                resultdata.append({"label": cat['label'], 'score': cat['score']})

        else:
            print(str(post_response.status_code) + " : We have an error ")

        print("ANNOTATION DONE")

        return resultdata

