from pathlib import Path
import fitz, json
from functions.tools import jsonHandler
from tqdm import tqdm

def classify(filepathRI,filepathB2Find,filepathDewey,pdfPath):
    print('lets Classify')

    counter = 1

    b2find = jsonHandler(path=filepathB2Find,defaultContent=[])
    dewey = jsonHandler(path=filepathDewey,defaultContent=[])
    edocRI = jsonHandler(path=filepathRI,defaultContent=[])
    KToutput = []

    glob = pdfPath.glob('**/*')
    pdfs = [f for f in glob if f.is_file()]
    for pdf in tqdm(pdfs): 
        ktDict = {}
        researchInfo = [x for x in edocRI if x['filename'] == pdf.stem][0]
        try:
            doc = fitz.open(pdf)  
            pages=[page.get_text("text") for page in doc]
            doctext = " ".join(pages)
            if doctext.strip() == '':
                ## PDF has no OCR - Text will be skipped
                print(f" {pdf.stem} skipped - No Text in PDF")
            else:
                ktDict['identifier'] = pdf.stem+pdf.suffix
                ktDict['title'] = pdf.stem
                ktDict['text'] = doctext
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
        except:
            ktDict = {}
            print(f" {pdf.stem} skipped - Categorization Error (Fitz?)")

        if ktDict != {}:
            if len(KToutput) >= 100: 
                KToutput = []
                counter += 1
                KToutput.append(ktDict)
                with open(f'splits/Kairntech{str(counter)}.json','w+') as fp:
                    json.dump(KToutput,fp)
            else:
                KToutput.append(ktDict)
                with open(f'splits/Kairntech{str(counter)}.json','w+') as fp:
                    json.dump(KToutput,fp)

