import time, requests, json, xmltodict
from tqdm import tqdm
from functions.tools import dataCleaner,jsonHandler

def loadInfo(riPath,skip=False,sleep=1):
    # Check if List of URLs already exists - creates it if not
    files = jsonHandler(path=riPath,defaultContent=[])
    if len(files) > 0:
        titleList = [x['title'] for x in files]
    else:
        titleList = []
    
    # You want to scrape again? - Takes a couple of Minutes 
    if not skip: 
        # Request fot the HU OAI-PMH
        apiRequest= 'https://edoc.hu-berlin.de/oai/request/?verb=ListRecords&metadataPrefix=xMetaDissPlus'

        # Grabbing the first batch of entries (The ones without Token)
        counter = 1
        print(f'No of Connections: {counter}')
        initialRequest = requests.get(apiRequest)
        initialJson = xmltodict.parse(initialRequest.content)
        initialRecords = initialJson['OAI-PMH']['ListRecords']['record']
        print(f'{len(initialRecords)=} <- if everything went according to plan it should say 100')
        for rec in tqdm(initialRecords):
            title, recDict = dataCleaner(rec)
            if title not in titleList and title != '':
                titleList.append(title)
                files.append(recDict)
            with open(riPath,'w+') as fp:
                json.dump(files,fp)
        time.sleep(1)

        # Setting Var jsonCont to Lookup the ResumptionTtoken
        jsonCont = initialJson

        # Looping through all other entries (now with Token): 
        counter += 1
        while 'resumptionToken' in jsonCont['OAI-PMH']['ListRecords']:
            if '#text' in jsonCont['OAI-PMH']['ListRecords']['resumptionToken']:
                token = jsonCont['OAI-PMH']['ListRecords']['resumptionToken']['#text']
                req = 'https://edoc.hu-berlin.de/oai/request/?verb=ListRecords&resumptionToken='+token
                resp = requests.get(req)
                jsonCont = xmltodict.parse(resp.content)
                records = jsonCont['OAI-PMH']['ListRecords']['record']
                print(f'No of Connections: {counter} - No of Records:{len(records)=}')
                for rec in tqdm(records):
                    title, recDict = dataCleaner(rec)
                    if title not in titleList and title != '':
                        titleList.append(title)
                        files.append(recDict)
                with open(riPath,'w+') as fp:
                    json.dump(files,fp)
                counter += 1
                time.sleep(sleep)
            else:
                print('URL-Download Complete')
                break

        print(f'We got {len(files)} files')
    else:
        print('JSON Download skipped')
