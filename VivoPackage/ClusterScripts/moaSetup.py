# -*- coding: utf-8 -*-

import pandas as pd
import json

class MattersOfActivity():

    def __init__(self):
        self.publicationXLSX = 'MOA_PUBLICATION.xlsx'
        self.projectsJSON = 'MOA_PROJECTS.json'


        df_raw = pd.read_excel('./input/'+self.publicationXLSX)
        self.df = df_raw.fillna('None').reset_index(drop=True)
        self.uri ='http://vivo.berlin-university-alliance.de/ontology/core/v1/bua/matters-activity'
    
    def __name__(self):
        return 'Matters of Activity'

    def Cluster(self):
        overviewObj = '''
            The Cluster Matters of Activity. 
            Image Space Material aims to create a basis for a new culture of materials. 
            The central vision of the Cluster is to rediscover the analog in the activity of images, 
            spaces and materials in the age of the digital. Biology and technology, mind and material, 
            nature and culture intertwine in a new way. In this context, the interdisciplinary research 
            and development of sustainable practices and structures is a central concern in areas such 
            as architecture and soft robotics, textiles, materials and digital filters, and surgical 
            cutting techniques.

            In six projects, more than 40 disciplines systematically investigate design strategies for 
            active materials and structures that adapt to specific requirements and environments. The 
            Cluster focuses on a new role of design, which is emerging in the context of growing diversity 
            and the continuous development of materials and visualization forms in all disciplines.            
            '''

        clusterDict = {}
        clusterDict.setdefault('name','Matters of Activity')
        clusterDict.setdefault('overview',overviewObj)
        clusterDict.setdefault('uri',self.uri)

        return [clusterDict]


    def Person(self):
        rawoutput = []
        output = []
        ace = list(self.df['Authors/Contributors/Editors'])
        eds = list(self.df['Editors'])
        cm = list(self.df['Cluster members'])

        for multiNameString in ace+eds: 
            multiNameList = multiNameString.split(';')
            for nameString in multiNameList:
                nameDict = {}
                if nameString != 'None':
                    nameList = nameString.split(',')
                    lastName = nameList[0].strip()
                    restName = nameList[1].strip()
                    restNameList = restName.split(' ')
                    firstName = restNameList[0]
                    if len(restNameList) > 1:
                        middleName = restNameList[1]
                    else:
                        middleName = ''
                    
                    if middleName == '':
                        givenName = firstName
                        label = firstName+' '+lastName
                    else:
                        givenName = firstName+' '+middleName
                        label = firstName+' '+middleName+' '+lastName
                    nameDict.setdefault('firstName',firstName)
                    nameDict.setdefault('middleName',middleName)
                    nameDict.setdefault('lastName',lastName)
                    nameDict.setdefault('givenName',givenName)
                    nameDict.setdefault('familyName',lastName)
                    nameDict.setdefault('label',label)


                    rawoutput.append(nameDict)

        [output.append(x) for x in rawoutput if x not in output]
        
        for multiNameString in cm:
            multiNameList = multiNameString.split('//')
            for nameString in multiNameList:
                nameString = nameString.strip()
                nameList = nameString.split(' ')
                if len(nameList) == 2:
                    firstName, lastName = nameList
                    middleName = ''
                elif len(nameList) == 3:
                    if '.' in nameList[1]:
                        firstName, middleName, lastName = nameList
                    else:
                        firstName = nameList[0]
                        middleName = ''
                        lastName = nameList[1]+' '+nameList[2]
                else:
                    firstName = nameList[0]+' '+nameList[1]
                    middleName = ''
                    lastName = nameList[2]+' '+nameList[3]

                if middleName == '':
                        givenName = firstName
                        label = firstName+' '+lastName
                else:
                    givenName = firstName+' '+middleName
                    label = firstName+' '+middleName+' '+lastName

                for x in output:
                    if x['lastName'] == lastName and x['firstName'][0] == firstName[0]:
                        x['lastName'] = lastName
                        x['firstName'] = firstName
                        x['givenName'] = givenName
                        x['label'] = label
                        x['participatesIn'] = self.uri
                        break
                else:
                    nameDict = {}
                    nameDict.setdefault('firstName',firstName)
                    nameDict.setdefault('middleName',middleName)
                    nameDict.setdefault('lastName',lastName)
                    nameDict.setdefault('givenName',givenName)
                    nameDict.setdefault('familyName',lastName)
                    nameDict.setdefault('label',label)
                    nameDict.setdefault('participatesIn',self.uri)
                    output.append(nameDict)

        return output

    def Project(self):
        output = []
        projectList = []
        with open('./input/'+self.projectsJSON, encoding='UTF-8') as fp:
            json.load(fp)

        projects = list(self.df['Achievement within the following projects'])
        for projectLine in projects:
            projectLineList = projectLine.split('//')
            for project in projectLineList:
                project = project.strip()
                if project != 'None':
                    if project != 'No project context':
                        projectList.append(project)
            
        projectList = list(set(projectList))

        for pro in projectList:
            projectDict = {}
            projectDict.setdefault('name',pro)
            projectDict.setdefault('organization','Matters of Activity')
            projectDict.setdefault('members',[])
            for row in range(len(self.df)):
                if pro in self.df['Achievement within the following projects'][row]:
                    persons = self.df['Cluster members'][row]
                    multiNameList = persons.split('//')
                    for nameString in multiNameList:
                        nameString = nameString.strip()
                        nameList = nameString.split(' ')
                        if len(nameList) == 2:
                            firstName, lastName = nameList
                            middleName = ''
                        elif len(nameList) == 3:
                            if '.' in nameList[1]:
                                firstName, middleName, lastName = nameList
                            else:
                                firstName = nameList[0]
                                middleName = ''
                                lastName = nameList[1]+' '+nameList[2]
                        else:
                            firstName = nameList[0]+' '+nameList[1]
                            middleName = ''
                            lastName = nameList[2]+' '+nameList[3]
                        personDict= {'firstName':firstName,
                                     'middleName':middleName,
                                     'lastName':lastName,
                                     'role': ['member'] }

                        projectDict['members'].append(personDict)
            output.append(projectDict)
        return output

    def Publication(self):
        output = []

        typedict = {
            'Edited Volume/Exhibition Catalogue': 'http://vivoweb.org/ontology/core/de/bua#EditedVolume',
            'Contribution in Edited Volume/Exhibition Catalogue': 'http://vivoweb.org/ontology/core/de/bua#ContributionInEditedVolume',
            'Article': 'http://purl.org/ontology/bibo/AcademicArticle',
            'Review: Book/Exhibition': 'http://vivoweb.org/ontology/core#Review',
            'Conference proceeding': 'http://vivoweb.org/ontology/core#ConferencePaper',
            'Monograph/Book': 'http://purl.org/ontology/bibo/Book',
            'Software publication': 'http://vivoweb.org/ontology/core/de/bua#SoftwarePublication',
            'Other': 'http://purl.org/ontology/bibo/Document'
            }

        for row in range(len(self.df)):
            pubDict = {}
            pubDict.setdefault('name',self.df['Title of publication'][row])
            pubDict.setdefault('year', self.df['Year of publication'][row])
            if self.df['Abstract'][row] != 'None':
                pubDict.setdefault('abstract', self.df['Abstract'][row])
            if self.df['Volume'][row] != 'None':
                pubDict.setdefault('volume', self.df['Volume'][row])
            if self.df['Digital Object Identifier (DOI)'][row] != 'None':
                pubDict.setdefault('doi', self.df['Digital Object Identifier (DOI)'][row])
            if self.df['Title of journal/archive/magazine'][row] != 'None':
                pubDict.setdefault('hasPublicationVenue',self.df['Title of journal/archive/magazine'][row])
            if self.df['Type of publication'][row] != 'None':
                pubDict.setdefault('@type',typedict[self.df['Type of publication'][row]])
            
            pages = self.df['Pages (from - to)'][row]
            pageList = pages.split('-')
            if len(pageList) == 1:
                if pageList[0] not in ['None','np','Forthcoming']:
                    pubDict.setdefault('startPage',pageList[0])
            elif len(pageList) == 2:
                pubDict.setdefault('startPage',pageList[0])
                pubDict.setdefault('endPage',pageList[1])
            else:
                pass

            pubDict.setdefault('authors',[])
            authors = self.df['Authors/Contributors/Editors'][row]
            cm = self.df['Cluster members'][row]
  
            multiNameList = authors.split(';')
            for nameString in multiNameList:
                nameDict = {}
                if nameString != 'None':
                    nameList = nameString.split(',')
                    lastName = nameList[0].strip()
                    restName = nameList[1].strip()
                    restNameList = restName.split(' ')
                    firstName = restNameList[0]
                    if len(restNameList) > 1:
                        middleName = restNameList[1]
                    else:
                        middleName = ''
                        
                    nameDict.setdefault('firstName',firstName)
                    nameDict.setdefault('middleName',middleName)
                    nameDict.setdefault('lastName',lastName)
                    pubDict['authors'].append(nameDict)

            multiNameList = cm.split('//')
            for nameString in multiNameList:
                nameString = nameString.strip()
                nameList = nameString.split(' ')
                if len(nameList) == 2:
                    firstName, lastName = nameList
                    middleName = ''
                elif len(nameList) == 3:
                    if '.' in nameList[1]:
                        firstName, middleName, lastName = nameList
                    else:
                        firstName = nameList[0]
                        middleName = ''
                        lastName = nameList[1]+' '+nameList[2]
                else:
                    firstName = nameList[0]+' '+nameList[1]
                    middleName = ''
                    lastName = nameList[2]+' '+nameList[3]

                for x in pubDict['authors']:
                    if x['lastName'] == lastName and x['firstName'][0] == firstName[0]:
                        x['lastName'] = lastName
                        x['firstName'] = firstName
            output.append(pubDict)
        return output

    def Journal(self):
        output = []
        journalList = list(set(list(self.df['Title of journal/archive/magazine'])))
        [output.append({'name':x}) for x in journalList]
        
        return output
