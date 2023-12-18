# -*- coding: utf-8 -*-

import pandas as pd
from mongoengine import *


class SCIoI:
    def __init__(self):
        #register_connection(db=databasename, host='127.0.0.1', port=27017, alias=DEFAULT_CONNECTION_NAME)
        self.scioiPublicationsXLSX = 'scioiPUBLICATIONS.xlsx'
        self.scioiMembersXLSX = 'scioiLIST.xlsx'
        self.scioiResearchProjectsXLSX = 'scioiRESEARCHPROJECTS.xlsx'

        df_publ_raw = pd.read_excel('./input/'+self.scioiPublicationsXLSX)
        self.df_publ = df_publ_raw.fillna('None').reset_index(drop=True)

        df_projectmember_raw = pd.read_excel('./input/'+self.scioiMembersXLSX)
        self.df_project_mem = df_projectmember_raw.fillna('None').reset_index(drop=True)

        df_project_raw = pd.read_excel('./input/'+self.scioiResearchProjectsXLSX)
        self.df_project = df_project_raw.fillna('None').reset_index(drop=True)

        self.uri ='http://vivo.berlin-university-alliance.de/ontology/core/v1/bua/SCIoI'

        self.language = 'en'
        self.baseuri = 'http://vivo.berlin-university-alliance.de/ontology/core/v1/bua/'
        self.source = 'SCIoI'

    def __name__(self):
        return 'Science of Intelligence'

    def Cluster(self):
        overviewObj = '''
            What are the principles of intelligence, shared by all forms of intelligence, no matter whether artificial or biological, whether robot, computer program, human, or animal? And how can we apply these principles to create intelligent technology? Answering these questions - in an ethically responsible way - is the central scientific objective of the Cluster Science of Intelligence (SCIoI).            
            '''

        clusterDict = {}
        clusterDict.setdefault('name', self.__name__())
        clusterDict.setdefault('overview', overviewObj)
        clusterDict.setdefault('uri', self.uri)

        return [clusterDict]


    def Person(self):

        rawoutput = []
        output = []
        ace = list(self.df_publ['Author'])
        cm = list(self.df_project['Cluster members'])

        for multiNameString in ace:
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
                    nameDict.setdefault('firstName', firstName)
                    nameDict.setdefault('middleName', middleName)
                    nameDict.setdefault('lastName', lastName)
                    nameDict.setdefault('givenName', givenName)
                    nameDict.setdefault('familyName', lastName)
                    nameDict.setdefault('label', label)


                    rawoutput.append(nameDict)

        [output.append(x) for x in rawoutput if x not in output]

        for multiNameString in cm:
            multiNameList = multiNameString.split(',')
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
                    nameDict.setdefault('firstName', firstName)
                    nameDict.setdefault('middleName', middleName)
                    nameDict.setdefault('lastName', lastName)
                    nameDict.setdefault('givenName', givenName)
                    nameDict.setdefault('familyName', lastName)
                    nameDict.setdefault('label', label)
                    nameDict.setdefault('participatesIn', self.uri)
                    output.append(nameDict)

        return output

    def Project(self):
        output = []

        for projectLine in range(len(self.df_project)):
            projectDict = {}
            projectDict.setdefault('members', [])
            projectDict.setdefault('name', self.df_project['Name'][projectLine])
            projectDict.setdefault('organization', self.__name__())
            pis = self.df_project['Principal Investigators'][projectLine]
            pis_multiNameList = pis.split(',')
            if pis_multiNameList != ['None']:
                projectDict['members'] = self.parseNames(pis_multiNameList, 'Principal Investigator', projectDict['members'])
            tms = self.df_project['Team Members'][projectLine]
            tms_multiNameList = tms.split(',')
            if tms_multiNameList != ['None']:
                projectDict['members'] = self.parseNames(tms_multiNameList, 'Team Member', projectDict['members'])
            ems = self.df_project['External members'][projectLine]
            ems_multiNameList = ems.split(',')
            if ems_multiNameList != ['None']:
                projectDict['members'] = self.parseNames(ems_multiNameList, 'External member', projectDict['members'])

            output.append(projectDict)

        return output


    def Publication(self):
        output = []

        typedict = {
            'journalArticle': 'http://purl.org/ontology/bibo/AcademicArticle',
            'conferencePaper': 'http://vivoweb.org/ontology/core#ConferencePaper',
        }


        for row in range(len(self.df_publ)):
            pubDict = {}

            pubDict.setdefault('name', self.df_publ['Title'][row])
            pubDict.setdefault('year', self.df_publ['Publication Year'][row])
            if self.df_publ['Abstract Note'][row] != 'None':
                pubDict.setdefault('abstract', self.df_publ['Abstract Note'][row])
            if self.df_publ['Volume'][row] != 'None':
                pubDict.setdefault('volume', self.df_publ['Volume'][row])
            if self.df_publ['DOI'][row] != 'None':
                pubDict.setdefault('doi', self.df_publ['DOI'][row])
            if self.df_publ['Publication Title'][row] != 'None':
                pubDict.setdefault('hasPublicationVenue', self.df_publ['Publication Title'][row])
            else:
                if self.df_publ['Conference Name'][row] != 'None':
                    pubDict.setdefault('hasPublicationVenue', self.df_publ['Publication Title'][row])

            if self.df_publ['Item Type'][row] != 'None':
                pubDict.setdefault('@type', typedict[self.df_publ['Item Type'][row]])

            pages = self.df_publ['Pages'][row]

            if pages != 'None':
                if isinstance(pages, int) or isinstance(pages, float):
                    pages = str(pages)

                pageList = pages.split('-')
                if len(pageList) == 1:
                    if pageList[0] not in ['None', 'np', 'Forthcoming']:
                        pubDict.setdefault('startPage', pageList[0])
                elif len(pageList) == 2:
                    pubDict.setdefault('startPage', pageList[0])
                    pubDict.setdefault('endPage', pageList[1])
                else:
                    pass

            pubDict.setdefault('authors', [])
            authors = self.df_publ['Author'][row]
            cm = list(self.df_project['Cluster members'])
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

                    nameDict.setdefault('firstName', firstName)
                    nameDict.setdefault('middleName', middleName)
                    nameDict.setdefault('lastName', lastName)
                    pubDict['authors'].append(nameDict)

            for multiNameString in cm:
                multiNameList = multiNameString.split(',')
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
        journalList = list(set(list(self.df_publ['Publication Title'])))
        [output.append({'name': x}) for x in journalList]

        return output


    def parseNames(self, multiNameList, role, output):
        #multiNameList = [x for x in multiNameList if x != 'None']
        for nameString in multiNameList:
            if nameString is not None:
                nameString = nameString.strip()
                nameList = nameString.split(' ')

                firstName = ''
                middleName = ''
                lastName = ''
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
                    if len(nameList) > 3:
                        firstName = nameList[0]+' '+nameList[1]
                        middleName = ''
                        lastName = nameList[2]+' '+nameList[3]

                personDict = {}
                if firstName != '':
                    personDict['firstname'] = firstName
                if middleName != '':
                    personDict['middleName'] = middleName
                if lastName != '':
                    personDict['lastName'] = lastName

                if firstName != '' and lastName != '':
                    personDict['role'] = [role]

                output.append(personDict)


        return output
