# -*- coding: utf-8 -*-
import json
from mongoengine import *
from mongo.dbSchema import Cluster, ClusterVCard, Year, Person,  VCard, VCardName, Position, MembershipRole, Authorship, Project, Publication, Journal


class NeuroCure:
    def __init__(self):
        projects_info_file = './input/NC_PROJECTS.json'
        persons_info_file = './input/NC_CLUSTERPERSONS.json'
        employments_info_file = './input/NC_CLUSTEREMPLOYMENTS.json'
        publications_info_file = './input/NC_CLUSTERWORKS.json'
        short_publicationsfile = './input/NC_PUBLICATIONS.json'

        with open(projects_info_file) as f:
            self.projects_info = json.load(f)

        with open(employments_info_file) as f:
            self.employments_info = json.load(f)

        with open(persons_info_file) as f:
            self.persons_info = json.load(f)

        with open(publications_info_file) as f:
            self.publications_info = json.load(f)

        with open(short_publicationsfile) as f:
            self.short_publications_info = json.load(f)

        self.language = 'en'
        self.baseuri = 'http://vivo.berlin-university-alliance.de/ontology/core/v1/bua/'
        self.source = 'neurocure'
        self.membershipnames = []

    def __name__(self):
        return 'Neurocure'

    def Person(self):
        foundelements = []
        foundnames = []
        persons = []
        for _, val in enumerate(self.persons_info):
            if val not in foundelements and not self.hasname(val, foundnames):

                names = self.getnames(val['FirstName'] + ' ' + val['LastName'])
                foundnames.append(names['lastName'] + ' ' + names['firstName'])
                foundnames.append(names['firstName'] + ' ' + names['lastName'])
                foundelements.append(val)

                persondict = {'lastName': names['lastName'], 'firstName': names['firstName'], 'middleName': names['middleName'], 'familyName': names['lastName'], 'givenName': names['firstName'], 'label': names['firstName'] + " " + names['lastName']}
                if 'orcidid' in val:
                    persondict["orcidID"] = val['orcidid']
                if 'biography' in val:
                    persondict["overview"] = val['biography']
                if 'researcher_urls' in val:
                    researcher_urls = {'researcher_urls': val['researcher_urls']}
                    if 'addresses' in val:
                        researcher_urls['addresses'] = val['addresses']
                    if 'emails' in val:
                        researcher_urls['emails'] = val['emails']
                    if 'external-identifiers' in val:
                        researcher_urls['external-identifiers'] = val['external-identifiers']

                    persondict["ARG_2000029"] = researcher_urls

                    persondict['participatesIn'] = self.baseuri + self.source

                if persondict not in persons:
                    persons.append(persondict)

        for _, val in enumerate(self.publications_info):
                for contributor in val['contributors']:
                    if 'contributorname' in contributor:
                        names = self.getnames(contributor['contributorname'])
                        tempcontributor = {'lastName': names['lastName'], 'firstName': names['firstName'], 'middleName': names['middleName'], 'familyName': names['lastName'], 'givenName': names['firstName'], 'label': names['firstName'] + " " + names['lastName']}

                        if tempcontributor not in persons:
                            persons.append(tempcontributor)

        return persons

    def Project(self):
        foundelements = []
        projects = []

        for _, val in enumerate(self.projects_info['projects']):
            project = {}
            for name in val['names']:
                if name['label'] != '' and name['language'] == self.language:
                    if name['label'] not in foundelements:
                        project['name'] = name['label']
                        foundelements.append(name['label'])

            for description in val['descriptions']:
                if description['label'] != '' and description['language'] == self.language:
                    project['overview'] = description['label']

            project['members'] = []
            for member in val['members']:
                names = self.getnames(member['firstname'] + ' ' + member['lastname'])
                tempmember = {'lastName': names['lastName'], 'firstName': names['firstName'], 'middleName': names['middleName'], 'roles': member['roles']}

                for role in member['roles']:
                    if role not in self.membershipnames:
                        self.membershipnames.append(role)

                project['members'].append(tempmember)

                project['organization'] = self.source

            projects.append(project)

        return projects

    def Cluster(self):
        overview = """
        
Exploring the nervous system and developing new therapies

NeuroCure is a Cluster of Excellence in the neurosciences funded since 2007 by the German federal and state governments (Excellence Initiative), receiving further funding within the Excellence Strategy since 2019. The focus of the Cluster is on investigating neurological and psychiatric disorders. The aim of this interdisciplinary research network is to better understand disease mechanisms and to develop new therapies. Fostering local networks of scientists and their research activities lies at the heart of the Cluster’s efforts. In addition, NeuroCure has established a significant number of new research groups as well as several technological platforms.

By promoting close cooperation between basic science and clinical research, the Cluster aims to more rapidly transfer findings from basic research to clinical application. To facilitate this process, NeuroCure has established its own clinical research center (NCRC) within the Charité – Universitätsmedizin Berlin. The NCRC supports researchers in conducting clinical trials, and gives patients access to new therapies and diagnostic options through participation in clinical trials.
        """
        cluster = {'name': 'NeuroCure', 'overview': overview, 'uri': self.baseuri + self.source}

        return [cluster]

    def Publication(self):
        foundelements = []
        baseuri = "https://doi.org/"
        publications = []
        typedict = {
            'Edited Volume/Exhibition Catalogue': 'http://vivoweb.org/ontology/core/de/bua#EditedVolume',
            'BOOK_CHAPTER': 'http://vivoweb.org/ontology/core/de/bua#ContributionInEditedVolume',
            'JOURNAL_ARTICLE': 'http://purl.org/ontology/bibo/AcademicArticle',
            'journal-article': 'http://purl.org/ontology/bibo/AcademicArticle',
            'SUPERVISED_STUDENT_PUBLICATION': 'http://purl.org/ontology/bibo/AcademicArticle',
            'preprint': 'http://purl.org/ontology/bibo/AcademicArticle',
            'Review: Book/Exhibition': 'http://vivoweb.org/ontology/core#Review',
            'CONFERENCE_PAPER': 'http://vivoweb.org/ontology/core#ConferencePaper',
            'BOOK': 'http://purl.org/ontology/bibo/Book',
            'DATA_SET': 'http://vivoweb.org/ontology/core#Dataset',
            'Software publication': 'http://vivoweb.org/ontology/core/de/bua#SoftwarePublication',
            'OTHER': 'http://purl.org/ontology/bibo/Document'
        }
        for _, val in enumerate(self.publications_info):
            publication = {}
            if 'title' in val and val['title'] not in foundelements:

                publication['name'] = val['title']
                publication['year'] = val['publication-year']
                publication['@type'] = typedict[val['work-type']]
                tempdoi = self.fetchublicationdoi(val['external-identifiers'])
                if tempdoi is not None:
                    publication['doi'] = baseuri + tempdoi

                publication['journals'] = [{"name": val['journal-title']}]
                publication['authors'] = []
                for contributor in val['contributors']:
                    if 'contributorname' in contributor:
                        names = self.getnames(contributor['contributorname'])
                        tempcontributor = {'lastName': names['lastName'], 'firstName': names['firstName'], 'middleName': names['middleName']}
                        publication['authors'].append(tempcontributor)
                    else:
                        tempcontributor = {'lastName': "", 'firstName': "", 'middleName': ""}


                publications.append(publication)
                foundelements.append(val['title'])

        return publications

    def Journal(self):
        journals = []
        journalfoundelements = []
        for _, val in enumerate(self.publications_info):
            if 'journal-title' in val and val['journal-title'] not in journalfoundelements:
                journal = {'name': val['journal-title'], 'year': val['publication-year']}
                journalfoundelements.append(val['journal-title'])
                journals.append(journal)
        return journals

    def getnames(self, name):
        lastname_prefixes = ["le", "von", "van", "de"]
        names = {"firstName": "", "middleName": "", "lastName": ""}

        ns = name.split(" ")

        if len(ns) > 2:
            prefix_res = any(string in name.lower() for string in lastname_prefixes)
            if prefix_res:
                names['firstName'] = ns[0].strip().strip(",").strip(";").strip()
                names['middleName'] = " ".join(ns[1:-2]).strip().strip(",").strip(";").strip()
                names['lastName'] = " ".join(ns[-2:]).strip().strip(",").strip(";").strip()
            else:
                names['firstName'] = ns[0].strip().strip(",").strip(";").strip()
                names['middleName'] = " ".join(ns[1:-2]).strip().strip(",").strip(";").strip()
                names['lastName'] = ns[-1].strip().strip(",").strip(";").strip()

        else:
            names['firstName'] = ns[0].strip().strip(",").strip(";").strip()
            names['middleName'] = ""
            names['lastName'] = ns[-1].strip().strip(",").strip(";").strip()

        return names



    # Aux
    def hasname(self, val, foundnames):
        found = False
        if 'FirstName' in val and 'LastName' in val and len(val['LastName']) > 0 and len(val['FirstName']) > 0:
            if val['LastName'] + val['FirstName'] in foundnames or val['LastName'] + val['FirstName'][0] in foundnames or val['FirstName'] + val['LastName'][0] in foundnames:
                found = True
        elif 'firstname' in val and 'lastname' in val is not None and len(val['firstname']) > 0 and len(val['lastname']) > 0:
            if val['lastname'] + val['firstname'] in foundnames or val['firstname'] + val['lastname'] in foundnames:
                found = True
        return found

    def fetchublicationdoi(self, element):
        for external in element:
            if external['type'] == "doi" and external['external-id-value'] != "":
                return external['external-id-value']
