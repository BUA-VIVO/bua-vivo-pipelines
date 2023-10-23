import faulthandler; faulthandler.enable()
import getopt
import json
import sys
import orcid
from requests import RequestException


def orcidmemberconnect():
    try:
        api = orcid.MemberAPI("APP-KEY-NAME-HERE", sandbox=True)
        search_token = api.get_search_token_from_orcid()
        return {"api": api, "token": search_token}
    except RequestException as e:
    # Here the error should be handled. As the exception message might be
    # too generic, additional info can be obtained by:
        print(e.response.text)
    # The response is a requests Response instance.


def orcidconnect():
    try:
        api = orcid.PublicAPI("APP-KEY-NAME-HERE", "APP-KEY-HERE", sandbox=False)
        search_token = api.get_search_token_from_orcid()
        return {"api": api, "token": search_token}
    except RequestException as e:
    # Here the error should be handled. As the eception message might be
    # too generic, additional info can be obtained by:
        print(e.response.text)
    # The response is a requests Response instance.


def searchperson(token, orcidid, api, section):
    try:
        data = api.read_record_public(orcidid, section, token)
        return data

    except RequestException as e:
        # Here the error should be handled. As the exception message might be
        # too generic, additional info can be obtained by:
        print("The ORCID identificator " + orcidid + " does not exist, please correct your input file" )
        exit(1)
        # The response is a requests Response instance.


def getkeywords(inputlist, api, token):
    for item in inputlist:
        print(item['firstName'] + " " + item['lastName'] + " / " + item['orcid'])
        endpointdata = searchperson(token, item['orcid'], api, "keywords")
    return endpointdata


def processlist(inputlist, api, token, endpoint, personmapping):
    output = {}
    if endpoint == "record" and len(personmapping) == 0:
        output["persondata"] = []
        output["personmap"] = []
    elif endpoint == "works" and len(personmapping) > 0:
        output["workdata"] = []
        output["personmap"] = []

    for item in inputlist:
        endpointdata = searchperson(token, item['orcid'], api, endpoint)

        if endpoint == "record" and len(personmapping) == 0:
            tempperson = mapperson(endpointdata)
            output["persondata"].append(tempperson['persondata'])
            output["personmap"].append(tempperson['personmap'])
        elif endpoint == "keywords" and len(personmapping) > 0:
            print(json.dumps(endpointdata))
        elif endpoint == "works" and len(personmapping) > 0:
            tempwork = mappersonworks(endpointdata, api, token, item['orcid'], endpoint, {'firstName': item['firstName'], 'lastName': item['lastName'], 'orcid': item['orcid']}, personmapping)
            output["workdata"] = [*output["workdata"], *tempwork['workdata']]
            output["personmap"] = tempwork['personmap']

    return output


def processputcode(api, token, orcidid, endpoint, putcode):
    try:
        endpointdata = searchperson(token, orcidid, api, endpoint + "/" + putcode)
        return endpointdata
    except RequestException as e:
    # Here the error should be handled. As the exception message might be
    # too generic, additional info can be obtained by:
        print(e.response.text)
    # The response is a requests Response instance.


def existsinmapping(clustermember, contributor):
    exists = False
    if 'contributor-firstname' not in contributor:
        contributor['contributor-firstname'] = ''

    if 'contributor-lastname' not in contributor:
        contributor['contributor-lastname'] = ''

    if contributor['contributor-firstname'] == clustermember['firstName'] and contributor['contributor-lastname'] == clustermember['lastName']:
        exists = True
    return exists


def mappersonworks(workdata, api, token, orcidid, endpoint, authordata, personmapping):
    works = {}
    works['personmap'] = []
    works['workdata'] = []

    for workitem in workdata['group']:
        for workitemsummary in workitem['work-summary']:
            additionalworkdata = processputcode(api, token, orcidid, endpoint, str(workitemsummary['put-code']))
            workdict = {}
            workdict['clustermember'] = {}
            workdict['clustermember']['firstName'] = authordata['firstName']
            workdict['clustermember']['lastName'] = authordata['lastName']
            workdict['clustermember']['orcid'] = authordata['orcid']
            for putworkitem in additionalworkdata['bulk']:
                workdict['title'] = putworkitem['work']['title']['title']['value'] if putworkitem['work']['title']['title'] and putworkitem['work']['title']['title']['value'] else ""
                workdict['subtitle'] = putworkitem['work']['title']['subtitle']['value'] if putworkitem['work']['title']['subtitle'] and putworkitem['work']['title']['subtitle']['value'] else ""
                workdict['journal-title'] = putworkitem['work']['journal-title']['value'] if putworkitem['work']['journal-title'] and putworkitem['work']['journal-title']['value'] else ""
                workdict['short-description'] = putworkitem['work']['short-description'] if putworkitem['work']['short-description'] else ""
                workdict['citation-type'] = putworkitem['work']['citation']['citation-type'] if putworkitem['work']['citation'] and putworkitem['work']['citation']['citation-type'] else ""
                workdict['citation-value'] = putworkitem['work']['citation']['citation-value'] if putworkitem['work']['citation'] and putworkitem['work']['citation']['citation-value'] else ""
                workdict['work-type'] = putworkitem['work']['type'] if putworkitem['work']['type'] else ""
                workdict['publication-year'] = putworkitem['work']['publication-date']['year']['value'] if putworkitem['work']['publication-date'] and putworkitem['work']['publication-date']['year'] else ""
                workdict['publication-month'] = putworkitem['work']['publication-date']['month']['value'] if putworkitem['work']['publication-date'] and putworkitem['work']['publication-date']['month'] else ""
                workdict['publication-day'] = putworkitem['work']['publication-date']['day']['value'] if putworkitem['work']['publication-date'] and putworkitem['work']['publication-date']['day'] else ""
                workdict['external-identifiers'] = []
                if putworkitem['work']['external-ids']['external-id'] is not None:
                    for externalidentifier in putworkitem['work']['external-ids']['external-id']:
                        extemp = {'type': externalidentifier['external-id-type'] if externalidentifier['external-id-type'] else "",
                                  'external-id-type': externalidentifier['external-id-type'] if externalidentifier['external-id-type'] else "",
                                  'external-id-value': externalidentifier['external-id-value'] if externalidentifier['external-id-value'] else "",
                                  'external-id-url': externalidentifier['external-id-url']['value'] if externalidentifier['external-id-url'] and externalidentifier['external-id-url']['value'] else ""}
                        workdict['external-identifiers'].append(extemp)

                workdict['contributors'] = []
                if putworkitem['work']['contributors'] is not None and putworkitem['work']['contributors']['contributor'] is not None:
                    for contributor in putworkitem['work']['contributors']['contributor']:
                        ctemp = {'contributor-orcid': contributor['contributor-orcid']['path'] if contributor['contributor-orcid'] and contributor['contributor-orcid']['path'] else "",
                                 'contributor-role': contributor['contributor-attributes']['contributor-role'] if contributor['contributor-attributes'] and contributor['contributor-attributes']['contributor-role'] else ""}
                        mapdict = {}

                        if contributor['credit-name'] and contributor['credit-name']['value']:
                            contributorname = contributor['credit-name']['value']

                            namelist = str(contributorname).split()

                            ctemp['contributor-firstname'] = ""
                            ctemp['contributor-lastname'] = ""

                            if len(namelist) > 2:
                                ctemp['contributor-firstname'] = namelist[0] + " " + namelist[1]
                            else:
                                ctemp['contributor-firstname'] = namelist[0]

                            last_index = len(namelist) - 1
                            ctemp['contributor-lastname'] = namelist[last_index]

                        if not existsinmapping(workdict['clustermember'], ctemp):
                            mapdict['FirstName'] = ctemp['contributor-firstname'].replace(",", "") if ctemp['contributor-firstname'] else ""
                            mapdict['LastName'] = ctemp['contributor-lastname'].replace(",", "") if ctemp['contributor-lastname'] else ""
                            mapdict['cluster'] = "None"
                            personmapping.append(mapdict)

                        workdict['contributors'].append(ctemp)

        works['workdata'].append(workdict)
        works['personmap'] = personmapping

    return works




def mapperson(persondata):
    persondict = {}
    persondict['personmap'] = []
    persondict['persondata'] = []

    mapdict = {}
    persontemp = {}

    persontemp['FirstName'] = persondata['person']['name']['given-names']['value'] if persondata['person']['name']['given-names']['value'] else ""
    persontemp['LastName'] = persondata['person']['name']['family-name']['value'] if persondata['person']['name']['family-name']['value'] else ""

    mapdict['FirstName'] = persondata['person']['name']['given-names']['value'] if persondata['person']['name']['given-names']['value'] else ""
    mapdict['LastName'] = persondata['person']['name']['family-name']['value'] if persondata['person']['name']['family-name']['value'] else ""
    mapdict['cluster'] = "NC"

    persontemp['orcidid'] = persondata['person']['name']['path'] if persondata['person']['name']['path'] else ""
    if persondata['person']['biography']:
        persontemp['biography'] = persondata['person']['biography']['content'] if persondata['person']['biography']['content'] else ""
    persontemp['researcher_urls'] = []
    for researcherref in persondata['person']['researcher-urls']['researcher-url']:
        rtemp = {'url-name': researcherref['url-name'] if researcherref['url-name'] else "",
                 'url': researcherref['url']['value'] if researcherref['url']['value'] else ""}
        persontemp['researcher_urls'].append(rtemp)

    persontemp['addresses'] = []
    for address in persondata['person']['addresses']['address']:
        atemp = {'country': address['country']['value'] if address['country']['value'] else ""}
        persontemp['addresses'].append(atemp)

    persontemp['emails'] = []
    for email in persondata['person']['emails']['email']:
        etemp = {'email': email['email'] if email['email'] else ""}
        persontemp['emails'].append(etemp)

    persontemp['keywords'] = []
    for keyword in persondata['person']['keywords']['keyword']:
        ktemp = {'keyword': keyword['content'] if keyword['content'] else ""}
        persontemp['keywords'].append(ktemp)

    persontemp['external-identifiers'] = []
    for externalidentifier in persondata['person']['external-identifiers']['external-identifier']:
        extemp = {'name': externalidentifier['source']['source-name']['value'] if externalidentifier['source']['source-name']['value'] else "",
                  'external-id-type': externalidentifier['external-id-type'] if externalidentifier['external-id-type'] else "",
                  'external-id-value': externalidentifier['external-id-value'] if externalidentifier['external-id-value'] else "",
                  'external-id-url': externalidentifier['external-id-url']['value'] if externalidentifier['external-id-url']['value'] else ""}
        persontemp['external-identifiers'].append(extemp)

    persondict['persondata'] = persontemp
    persondict['personmap'] = mapdict

    return persondict


def main(*kwargs):
    """
          main
       """
    try:
        opts, args = getopt.getopt(sys.argv[1:], "j:p:w:m:h", ["jsonfile=", "personoutfile=", "worksoutfile=", "personmap=", "help"])
    except getopt.GetoptError as e:
        print('publications2vivo.py -j <jsonfile> -p <personoutfile> -w <worksoutfile> -m <personmap>')
        sys.exit(2)

    if not opts:
        print('publications2vivo.py -j <jsonfile> -p <personoutfile> -w <worksoutfile> -m <personmap>')
        sys.exit(2)

    arguments = {}

    for opt, arg in opts:
        if opt == '-h':
            print('publications2vivo.py -j <jsoninputfile> -p <personoutfile> -w <worksoutfile> -m <personmap>')
            sys.exit()
        elif opt in ("-j", "--jsoninputfile"):
            arguments['jsoninputfile'] = arg
        elif opt in ("-p", "--outputfile"):
            arguments['personoutfile'] = arg
        elif opt in ("-w", "--worksoutfile"):
            arguments['worksoutfile'] = arg
        elif opt in ("-m", "--personmap"):
            arguments['personmap'] = arg

    if 'personoutfile' not in arguments:
        print('You need to specify a output file : -o <personoutfile>')
        sys.exit()
    elif 'worksoutfile' not in arguments:
        print('You need to specify a json works outfile : -w <worksoutfile>')
        sys.exit()
    elif 'personmap' not in arguments:
        print('You need to specify a json person map outfile : -m <personmap>')
        sys.exit()
    elif 'jsoninputfile' not in arguments:
        print('You need to specify a json input file : -j <jsoninputfile>')
        sys.exit()
    else:
        with open(arguments['jsoninputfile']) as f:
            jsondata = json.load(f)

        orciddata = orcidconnect()
        print("Connected to ORCID")

        print("Looking up person data")
        personlist = processlist(jsondata, orciddata['api'], orciddata['token'], 'record', [])

        print("Writing person data")
        with open(arguments['personoutfile'], "w") as file_object:
            file_object.write(json.dumps(personlist['persondata']))

        
        print("Looking up publications")
        publicationlist = processlist(jsondata, orciddata['api'], orciddata['token'], 'works', personlist['personmap'])


        with open(arguments['worksoutfile'], "w") as file_object:
            file_object.write(json.dumps(publicationlist['workdata']))

        with open(arguments['personmap'], "w") as file_object:
            file_object.write(json.dumps(publicationlist['personmap']))

        print("DONE")



if __name__ == '__main__':
    main()