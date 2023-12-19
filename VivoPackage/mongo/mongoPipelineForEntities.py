from mongoengine import *
from tqdm import tqdm
from tools import updateOwnership
from dbSchema import Cluster, Person,Project,Publication,Journal, Year

def importEntities(importlist):
    # mongo Connect
    MONGOURI: "mongodb://USERNAME:PASSWORD@ServerIP:PORT/"
    disconnect()
    connect(host=MONGOURI)

    # load Cluster
    clusterList = importlist
    methodList = ['Person','Cluster','Project','Publication','Journal']

    # write Entities
    print('writing Entities')
    for cluster in clusterList:
        for method in methodList:
            print(f'writing: {cluster.__name__()} --> {method}')
            try:
                meth = getattr(cluster,method)
            except: 
                print(cluster.__name__(),method,'not found')
            else:
                entityList = meth()
                for entity in tqdm(entityList):
        ## --> Person
                    if method == 'Person': 
                        firstName = entity['firstName']
                        middleName = entity['middleName']
                        lastName = entity['lastName']
                        db = Person.objects(__raw__={'$and':[
                                {"firstName":{"$in":[firstName]}},
                                {"lastName":{"$in":[lastName]}}
                                    ]})
                        if db:
                            updateOwnership(db,cluster)
                        else:
                            if middleName == '':
                                name = firstName+' '+lastName
                            else:
                                name = firstName+' '+middleName+' '+lastName
                            Person(name= name,firstName = firstName, middleName=middleName,lastName=lastName,flag_owner=[cluster.__name__()]).save()
        ## --> Cluster
                    elif method == 'Cluster':
                        name = entity['name']
                        if name not in ['','None']:
                            db = Cluster.objects(name=name)
                            if db:
                                updateOwnership(db,cluster)
                            else:
                                db = Cluster(name=name,flag_owner=[cluster.__name__()]).save() 
        ## --> Project
                    elif method == 'Project': 
                        name = entity['name']
                        if name not in ['','None']:
                            db = Project.objects(name=name)
                            if db:
                                updateOwnership(db,cluster)
                            else:
                                db = Project(name=name,flag_owner=[cluster.__name__()]).save() 
        ## --> Journal
                    elif method == 'Journal': 
                        name = entity['name']
                        if name not in ['','None']:
                            db = Journal.objects(name=name)
                            if db:
                                updateOwnership(db,cluster)
                            else:
                                db = Journal(name=name,flag_owner=[cluster.__name__()]).save() 
        ## --> Publication
                    elif method == 'Publication': 
                        name = entity['name']
                        if name not in ['','None']:
                            year = str(entity['year'])
                            db = Publication.objects(__raw__={'$and':[
                                    {"name":{"$in":[name]}},
                                    {"year":{"$in":[year]}}
                                        ]})
                            if db:
                                updateOwnership(db,cluster)
                            else:
                                db = Publication(name=name, year=year,flag_owner=[cluster.__name__()]).save() 

    # Writing static objects
    ## Years 
    print('writing Years')
    yearList = Year.objects()
    if not all(item in [x.name for x in yearList] for item in list(range(1500,2200))):
        for year in tqdm(range(1500,2200)):
            yearObject = Year(name = str(year))
            yearObject['@type'] = 'http://vivoweb.org/ontology/core#DateTimeValue'
            yearObject['dateTime'] = str(year)+'-01-01T12:00:00'
            yearObject['dateTimePrecision'] = 'http://vivoweb.org/ontology/core#yearPrecision'
            yearObject.save()

    print('Entities: done')
    disconnect()



