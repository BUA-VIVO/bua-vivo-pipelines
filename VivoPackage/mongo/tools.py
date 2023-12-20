from mongoengine import *

def clusterNameFormatter(nameraw):
    if nameraw.lower() == 'neurocure':
        return 'NeuroCure'
    elif nameraw in ['nc','NC','neuro cure','Neuro cure', 'neuro Cure','Neuro Cure']:
        return 'NeuroCure'
    elif nameraw.lower() == 'matters of activity':
        return 'Matters of Activity'
    elif nameraw in ['moa','MoA','MOA','mattersofactivity','mattersOfActivity','MattersOfActivity','Mattersofactivity']:
        return 'Matters of Activity'
    elif nameraw.lower() == 'science of intelligence':
        return 'Science of Intelligence'
    elif nameraw in ['scioi','SCIoI','SCIOI', 'ScienceofIntelligence','ScienceOfIntelligence','scienceofintelligence','Scienceofintelligence']:
        return 'Science of Intelligence'
    else:
        return nameraw

def updateOwnership(db,cluster):
    obj = db[0]
    owner = obj.flag_owner
    if cluster.__name__() not in owner: 
        owner.append(cluster.__name__())
        obj.flag_owner = owner
        obj.save()

def typeAdd(collection,collInsertString, subject):
    tripleStart = "INSERT DATA { GRAPH <http://vitro.mannlib.cornell.edu/default/vitro-kb-2> {"
    tripleEnd = ".} } "
    predicate = "<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>"

    if collection == Cluster: 
        return collInsertString
    elif collection == Year:
        return collInsertString
    elif collection == Publication:
        return collInsertString
    elif collection == ClusterVCard:
        object = "<http://www.w3.org/2006/vcard/ns#Organizational>"
        tripString = tripleStart+subject+predicate+object+tripleEnd 
        collInsertString = collInsertString+tripString
        return collInsertString
    elif collection == Person:
        object = "<http://xmlns.com/foaf/0.1/Person>"
        tripString = tripleStart+subject+predicate+object+tripleEnd 
        collInsertString = collInsertString+tripString
        return collInsertString
    elif collection == VCard:
        object = "<http://www.w3.org/2006/vcard/ns#Individual>"
        tripString = tripleStart+subject+predicate+object+tripleEnd 
        collInsertString = collInsertString+tripString
        return collInsertString
    elif collection == VCardName:
        object = "<http://www.w3.org/2006/vcard/ns#Name>"
        tripString = tripleStart+subject+predicate+object+tripleEnd 
        collInsertString = collInsertString+tripString
        return collInsertString
    elif collection == Position:
        object = "<http://vivoweb.org/ontology/core#Position>"
        tripString = tripleStart+subject+predicate+object+tripleEnd 
        collInsertString = collInsertString+tripString
        return collInsertString
    elif collection == MembershipRole:
        object = "<http://vivoweb.org/ontology/core#MemberRole>"
        tripString = tripleStart+subject+predicate+object+tripleEnd 
        collInsertString = collInsertString+tripString
        return collInsertString
    elif collection == Authorship:
        object = "<http://vivoweb.org/ontology/core#Authorship>"
        tripString = tripleStart+subject+predicate+object+tripleEnd 
        collInsertString = collInsertString+tripString
        return collInsertString
    elif collection == Project:
        object = "<http://vivoweb.org/ontology/core#Project>"
        tripString = tripleStart+subject+predicate+object+tripleEnd 
        collInsertString = collInsertString+tripString
        return collInsertString
    elif collection == Journal:
        object = "<http://purl.org/ontology/bibo/Journal>"
        tripString = tripleStart+subject+predicate+object+tripleEnd 
        collInsertString = collInsertString+tripString
        return collInsertString



    
