from pathlib import Path
from slugify import slugify
import json

def jsonHandler(path: str,defaultContent = []):
    outfilePath = Path(path)
    if outfilePath.is_file():
        with open(outfilePath,'r') as fp:
            content = json.load(fp)
    else:
        with open(outfilePath,'w+') as fp:
            content = defaultContent
            json.dump(content,fp)
    return content

def dataCleaner(entry:  dict):
    if 'metadata' in entry:
        if 'xMetaDiss:xMetaDiss' in entry['metadata']:
            meta = entry['metadata']['xMetaDiss:xMetaDiss']
            title = meta['dc:title']['#text']
            try:
                url = meta['ddb:transfer']['#text']
            except:
                print(f'Error: no URL found for {title=}')
                return ['',{}]
            else:
                url = meta['ddb:transfer']['#text']
                if Path(url).suffix != '.pdf':
                    print(f'Skipped: no PDF-File in {title=}')
                    return ['',{}]
                subjects = []
                ddc = []
                if 'dc:subject' in meta:
                    if type(meta['dc:subject']) == list:
                        for subjDict in  meta['dc:subject']:
                            if subjDict['@xsi:type'] == 'xMetaDiss:noScheme':
                                subjects.append(subjDict['#text'])
                            if subjDict['@xsi:type'] == 'xMetaDiss:DDC-SG':
                                ddc.append(subjDict['#text'])
                return [title, {'title':title,'filename':slugify(title),'url':url,'subjects':subjects,'ddc':ddc}]
        else:
            print(f'Error: xMetaDiss:xMetaDiss not found in {entry=}')
            return ['',{}]
    else:
        if 'header' in entry:
            if '@status' in entry['header']:
                if entry['header']['@status'] == 'deleted':
                    print(f'File Deleted')
                else:
                    print(f'Error: metadata not found in {entry=}')
            else:
                print(f'Error: metadata not found in {entry=}')
        else:
            print(f'Error: metadata not found in {entry=}')
        return ['',{}]



