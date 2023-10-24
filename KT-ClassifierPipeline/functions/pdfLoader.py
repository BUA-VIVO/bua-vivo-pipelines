import requests
from pathlib import Path
from functions.tools import jsonHandler

def loadPdfs(riPath, pdfPath, numberOfDownloads= 10,skip= False):
    print('starting to Download PDFs')
    if not skip:
        # Download PDFs 
        dlcounter = 1
        files = jsonHandler(path=riPath,defaultContent=[])
        glob = pdfPath.glob('**/*')
        downloadedFiles = [f.stem for f in glob if f.is_file()]

        while numberOfDownloads > 0:
            if files != []:
                file = files.pop(0)
            else:
                break

            filename = file['filename']
            if filename not in downloadedFiles: 
                print(f' Downloading PDF No {dlcounter}')
                url = file['url']
                try:
                    dl = requests.get(url)
                except:
                    print(f'Request Error: skipped {url}')
                else:
                    try:
                        with open(Path(pdfPath,filename+'.pdf'), 'wb') as fp:
                            fp.write(dl.content)
                        numberOfDownloads -= 1
                        dlcounter += 1
                    except:
                        print(f'Writing Error: skipped {url}')
        print('PDF Download complete')
    else:
        print('PDF download skipped')