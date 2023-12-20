# -*- coding: utf-8 -*-
import os
from subprocess import DEVNULL, STDOUT, check_call
from tqdm import tqdm
from mongoengine import *
from mongoengine.base.datastructures import BaseList
from bson.dbref import DBRef
from mongo.tools import typeAdd
from functions.context import builder
from mongo.dbSchema import Cluster,ClusterVCard,Year,Person,VCard,VCardName,Position,MembershipRole,Authorship,Project,Publication,Journal

# mongo Connect
MONGOURI: "mongodb://USERNAME:PASSWORD@ServerIP:PORT/"
disconnect()
connect(host=MONGOURI)

# curlstring
email = 'Email'
password = 'PASSWORD'
url = 'http://XXX.XXX.XXX.XXX:PORT'
curlCommand = f"curl -i -d 'email={email}' -d 'password={password}' -d '@insert.sparql' '{url}/vivo/api/sparqlUpdate'"
tripleStart = "GRAPH <http://vitro.mannlib.cornell.edu/a/graph/sparqlUpdate> {"
tripleEnd = " . } "

# Transfer

domain = 'http://vivo.berlin-university-alliance.de/individual/'
context = builder()

def escapeStr(s):
    escList = ["~",".","-","!","$","'","(",")","*","+",",",";","=","/","?","#","@","%","_","{","}","<",">",":"]
    for x in escList:
        s = s.replace(x,'\\'+x)
    return s


collections = [Cluster,ClusterVCard,Year,Person,VCard,VCardName,Position,MembershipRole,Authorship,Project,Publication,Journal]
for coll in collections:
    print(f'building String for {coll=}')
    collectionList = coll.objects()
    collInsertString = ""
    for obj in tqdm(collectionList):
        mongoID = str(obj.id) 
        if coll == Cluster:
            clusterdict = {'Matters of Activity':"http://vivo.berlin-university-alliance.de/ontology/core/v1/bua/matters-activity",
                           'NeuroCure':'http://vivo.berlin-university-alliance.de/ontology/core/v1/bua/neurocure',
                           'Science of Intelligence': 'http://vivo.berlin-university-alliance.de/ontology/core/v1/bua/SCIoI'}
            subjString = clusterdict[obj.name]
        else: 
            subjString = domain+mongoID
        s = " <"+subjString+">"
        typeAdd(coll,collInsertString,s)

        objFields = list(obj._fields_ordered)
        _ = objFields.pop(objFields.index('id'))
        _ = objFields.pop(objFields.index('name'))

        if 'label' not in objFields:
            p = " <"+context['label']+"> "
            o = "\""+escapeStr(str(obj.name)).replace('\n','').replace('\t','').replace('&',r'\u0026').replace('"','\\"').strip()+"\""
            tripString = tripleStart+s+p+o+tripleEnd
            collInsertString = collInsertString+tripString

        if '@type' not in objFields:
            if coll not in [Cluster,Publication]:
                p = " <"+context['@type']+"> "
                typeDict = {Year: ' <http://vivoweb.org/ontology/core#DateTimeValue> ',
                            Person: ' <http://xmlns.com/foaf/0.1/Person> ',
                            VCard: ' <http://www.w3.org/2006/vcard/ns#Individual> ',
                            VCardName: ' <http://www.w3.org/2006/vcard/ns#Name> ',
                            Position: ' <http://vivoweb.org/ontology/core#Position> ',
                            MembershipRole: ' <http://vivoweb.org/ontology/core#MemberRole> ',
                            Authorship: ' <http://vivoweb.org/ontology/core#Authorship> ',
                            Project: ' <http://vivoweb.org/ontology/core#Project> ',
                            Journal: ' <http://purl.org/ontology/bibo/Journal> '}
                o = typeDict[coll]
                tripString = tripleStart+s+p+o+tripleEnd
                collInsertString = collInsertString+tripString

        for field in objFields:
            if field not in context:
                pass
            else: 
                p = " <"+context[field]+"> "

                dbobj = getattr(obj, field)
                if type(dbobj) == str:
                    if dbobj[:4] == "http":
                        o = "<"+escapeStr(str(dbobj)).replace('\n','').replace('\t','').strip()+">"
                        tripString = tripleStart+s+p+o+tripleEnd
                        collInsertString = collInsertString+tripString
                    else:
                        trip = escapeStr(str(dbobj)).replace('\n','').replace('\t','').replace('"','\\"').replace('&',r'\u0026').strip()#
                        o = "\""+trip+"\" "
                        tripString = tripleStart+s+p+o+tripleEnd
                        collInsertString = collInsertString+tripString
                elif type(dbobj) == DBRef:
                    o = " <"+domain+str(dbobj.id)+"> "  
                    tripString = tripleStart+s+p+o+tripleEnd 
                    collInsertString = collInsertString+tripString
                elif type(dbobj) == BaseList:
                    for listobj in dbobj:
                        if type(listobj) == str:
                            if dbobj[:4] == "http":
                                o = "<"+listobj.replace('\n','').replace('\n','').replace('\t','').strip()+">"
                                tripString = tripleStart+s+p+o+tripleEnd
                                collInsertString = collInsertString+tripString
                            else:
                                trip = escapeStr(str(listobj)).replace('\n','').replace('\t','').replace('&',r'\u0026').replace('"','\\"').strip()
                                o = "\""+trip+"\" "
                                tripString = tripleStart+s+p+o+tripleEnd
                                collInsertString = collInsertString+tripString
                        elif type(listobj) == DBRef:
                            o = " <"+domain+str(listobj.id)+"> " 
                            tripString = tripleStart+s+p+o+tripleEnd
                            collInsertString = collInsertString+tripString

    name = coll.__name__
    exportString = 'update=INSERT DATA { '+collInsertString+' }'

    print('savingCurlstr')
    # insert.sparql
    with open('insert.sparql','w',encoding='UTF-8') as fp:
        fp.write(exportString)
    
    # log
    # with open(name+'_insert.sparql','w',encoding='UTF-8') as fp:
    #     fp.write(exportString)

    print('executing Curl Command')
    try:
        os.system(curlCommand)
    except:
        print('Error: Curl broke')
    print(f'{coll=} done')


disconnect()
print('done')