from mongoengine import *
from tqdm import tqdm
from tools import clusterNameFormatter
from dbSchema import Cluster, Person,Project,Publication,Journal,VCard, VCardName, MembershipRole, Authorship, Year


def importRelations(importlist):
    # mongo Connect
    MONGOURI: "mongodb://USERNAME:PASSWORD@ServerIP:PORT/"
    disconnect()
    connect(host=MONGOURI)

    # load Cluster
    clusterList = importlist
    methodList = ['Person','Cluster','Project','Publication','Journal']

    # ClusterURIs
    clusterURIs = {
        'Matters of Activity': 'http://vivo.berlin-university-alliance.de/ontology/core/v1/bua/matters-activity',
        'NeuroCure': 'http://vivo.berlin-university-alliance.de/ontology/core/v1/bua/neurocure',
        'Science of Intelligence': 'http://vivo.berlin-university-alliance.de/ontology/core/v1/bua/SCIoI'
    }


    # write Relations
    print('writing Relations')
    for cluster in clusterList:
        for method in methodList:
            print('writing:',cluster.__name__(),'-->',method)
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
                        lastName = entity['lastName']
                        db = Person.objects(__raw__={'$and':[
                                {"firstName":{"$in":[firstName]}},
                                {"lastName":{"$in":[lastName]}}]})
                        if db:
                            personObject = db[0]
                            personObject.reload(max_depth=5)
                            ignoredKeys = ['firstName','middleName','lastName','givenName']
                            newKeys =  [x for x in entity.keys() if x not in ignoredKeys]

                            # writing VCard:name
                            vcardNameID= str(personObject.id)+str('-vcardname')
                            vcardname = VCardName.objects(name = vcardNameID)
                            if vcardname:
                                vcardname = vcardname[0]
                            else:
                                vcardname = VCardName(name = vcardNameID)
                            vcardname.givenName = entity.get('givenName','')
                            vcardname.familyName = entity.get('lastName','')
                            vcardname.flag_owner = [cluster.__name__()]
                            vcardname.save()

                            # writing VCard
                            vcardID = str(personObject.id)+str('-vcard')
                            vcard = VCard.objects(name = vcardID)
                            if vcard:
                                vcard = vcard[0]
                            else:
                                vcard = VCard(name = vcardID)
                            vcard.ARG_2000029 = personObject.to_dbref()
                            vcard.hasName = vcardname.to_dbref()
                            vcard.flag_owner = [cluster.__name__()]
                            vcard.save()

                            # Connecting VCard to Person
                            personObject.reload(max_depth=5)
                            personObject.ARG_2000028 = vcard.to_dbref()

                            # Copy all other Key-Value Pairs
                            for k in newKeys:
                                setattr(personObject,k,entity[k])
                            
                            # adding Empty Lists
                            personObject.bearerof = []

                            # Saving Object
                            personObject.save()
                
                ## --> Project
                    elif method == 'Project':
                        name = entity['name']
                        db = Project.objects(name = name)
                        if db:
                            projectObject = db[0]
                            ignoredKeys = ['name','organization','members']
                            newKeys =  [x for x in entity.keys() if x not in ignoredKeys]
                            projectObject.label = name
                            organizationraw = entity.get('organization','')
                            organization = clusterNameFormatter(organizationraw)
                            if organization != '':
                                org = Cluster.objects(name=organization)[0]
                                projectObject.hasGoverningAuthority = clusterURIs[org.name]
                            projectObject.contributingRole = []
                            if 'members' in newKeys:
                                for memberDict in entity['members']:
                                    memberFirstName = memberDict.get('firstname','')
                                    memberLastName = memberDict.get('lastName','')
                                    memberRole = memberDict.get('role','')
                                    if memberRole != '':
                                        memberObjectList  = Person.objects(__raw__={'$and':[
                                                            {"firstName":{"$in":[memberFirstName]}},
                                                            {"lastName":{"$in":[memberLastName]}}]})
                                        memberObj = memberObjectList[0]

                                        # Writing MembershipRole
                                        memRoleUri = str(memberObj.id)+'-'+str(projectObject.id)
                                        memRoleObj = MembershipRole.objects(name = memRoleUri)
                                        if memRoleObj:
                                            memRoleObj = memRoleObj.get(name = memRoleUri)
                                        else:
                                            memRoleObj = MembershipRole(name = memRoleUri)
                                        memRoleObj.label = memberRole.to_dbref()
                                        memRoleObj.roleContributesTo = projectObject.to_dbref()
                                        memRoleObj.inhersin = memberObj.to_dbref()
                                        memRoleObj.save()
                                        ## Linking MembershipRole back to Person
                                        memberObjectList  = Person.objects(__raw__={'$and':[
                                                            {"firstName":{"$in":[memberFirstName]}},
                                                            {"lastName":{"$in":[memberLastName]}}]})
                                        memberObj = memberObjectList[0]

                                        membershipList = memberObj.bearerof
                                        membershipList.append(memRoleObj.to_dbref())
                                        memberObj.bearerof = membershipList
                                        memberObj.save()

                                        ## adding MembershipRole to Project
                                        db = Project.objects(name = name)
                                        projectObject = db[0]
                                        projectObject.contributingRole.append(memRoleObj.to_dbref())
                            
                            # Copy all other Key-Value Pairs
                            for k in newKeys:
                                setattr(projectObject,k,entity[k])

                            # Saving Object
                            projectObject.save()
                    
                ## --> Publications
                    elif method == 'Publication':
                        name = entity['name']
                        year = str(entity['year'])
                        db = Publication.objects(__raw__={'$and':[
                                            {"name":{"$in":[name]}},
                                            {"year":{"$in":[year]}}]})
                        pubObject = db[0]
                        # Connecting to DateTime-Object
                        if year != '':
                            yearObj = Year.objects(name = year)[0]
                            pubObject['dateTimeValue'] = yearObj.to_dbref()

                        ignoredKeys = ['name','year','hasPublicationVenue','authors']
                        newKeys =  [x for x in entity.keys() if x not in ignoredKeys]
                        if 'hasPublicationVenue' in entity and entity['hasPublicationVenue'] != 'None':
                            journalTitle = entity['hasPublicationVenue']
                            journalObject = Journal.objects(name = journalTitle)[0]
                            pubObject.hasPublicationVenue = journalObject.to_dbref()

                            # Connecting Journal to Publication
                            try: 
                                journalObject.publicationVenueFor.append(pubObject.to_dbref())
                            except:
                                journalObject.publicationVenueFor = [pubObject.to_dbref()]
                            journalObject.save()

                        for authorDict in entity['authors']:
                            authorFirstName = authorDict.get('firstName','')
                            authorLastName = authorDict.get('lastName','')
                            personObjectList = Person.objects(__raw__={'$and':[
                                            {"firstName":{"$in":[authorFirstName]}},
                                            {"lastName":{"$in":[authorLastName]}}]})
                            personObj = personObjectList[0]

                            # Writing Authorship
                            authorshipURI = str(personObj.id)+'-'+str(pubObject.id)
                            authorshipObj = Authorship.objects(name = authorshipURI)
                            if authorshipObj:
                                authorshipObj = authorshipObj.get(name = authorshipURI)
                            else:
                                authorshipObj = Authorship(name = authorshipURI)
                            try:
                                authorshipObj.relates.append(personObj.to_dbref())
                                authorshipObj.relates.append(pubObject.to_dbref())
                            except:
                                authorshipObj.relates = [personObj.to_dbref(),pubObject.to_dbref()]
                            authorshipObj.save()
                            
                            # Connecting Person and Publication to the new Authorship
                            personObjectList = Person.objects(__raw__={'$and':[
                                            {"firstName":{"$in":[authorFirstName]}},
                                            {"lastName":{"$in":[authorLastName]}}]})
                            personObj = personObjectList[0]

                            try:
                                personObj.relatedBy.append(authorshipObj.to_dbref())
                            except:
                                personObj.relatedBy = [authorshipObj.to_dbref()]
                            personObj.save()

                            db = Publication.objects(__raw__={'$and':[
                                            {"name":{"$in":[name]}},
                                            {"year":{"$in":[year]}}]})
                            pubObject = db[0]
                            try:
                                pubObject.relatedBy.append(authorshipObj.to_dbref())
                            except:
                                pubObject.relatedBy = [authorshipObj.to_dbref()]

                            # Copy all other Key-Value Pairs
                            for k in newKeys:
                                setattr(pubObject,k,entity[k])
                            
                            # Saving Object
                            pubObject.save()
                ## --> Cluster
                    elif method == 'Cluster':
                        name = entity['name']
                        db = Cluster.objects(name = name)
                        ignoredKeys = ['name']
                        newKeys =  [x for x in entity.keys() if x not in ignoredKeys]
                        if db:
                            clusterObject = db[0]
                            for k in newKeys:
                                setattr(clusterObject,k,entity[k])
                ## --> Journal
                    elif method == 'Cluster':
                        name = entity['name']
                        db = Cluster.objects(name = name)
                        ignoredKeys = ['name']
                        newKeys =  [x for x in entity.keys() if x not in ignoredKeys]
                        if db:
                            clusterObject = db[0]
                            for k in newKeys:
                                setattr(clusterObject,k,entity[k])

                    
                            
                                    





