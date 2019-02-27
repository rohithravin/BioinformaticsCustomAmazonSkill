import requests
import json
import simplejson
import sys

BASE_API_URL = 'http://www.ebi.ac.uk/proteins/api/'

def proteinSearch(keyword, size):

    parameters = {'offset': 0, 'size': size, 'keywords' : keyword}
    header = {'Accept': 'application/json'}

    response = requests.get(BASE_API_URL + 'proteins', params = parameters, headers = header)

    if response.status_code != 200:
        return None

    json_response = response.json()
    print(json_response)

    data = {}
    data['proteins'] = []
    for y in range(len(json_response)):
        protein = {}
        protein['id'] = json_response[y]['accession']
        protein['protein_name'] = json_response[y]['protein']['recommendedName']['fullName']['value']
        protein['gene'] = json_response[y]['id']
        protein['function'] = json_response[y]['comments'][0]['text'][0]['value']
        go = []
        for x in range(len(json_response[y]['dbReferences'])):
            if (json_response[y]['dbReferences'][x]['type'] == 'GO'):
                go.append(json_response[y]['dbReferences'][x]['properties']['term'][2:].title())
        protein['gene_ontology'] = go
        data['proteins'].append(protein)
    with open('proteins.json', 'w') as outfile:
        json.dump(data, outfile)

"""
args = []
for x in sys.argv:
     args.append(x)
proteinSearch(args[1], args[2])
"""

def test():
    print('hi')
    response = requests.get('https://www.uniprot.org/uniprot/?query=insulin')
    print(response)
test()
