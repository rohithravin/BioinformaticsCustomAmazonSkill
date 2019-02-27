import requests
import json
import simplejson
import sys
import urllib
from bs4 import BeautifulSoup

BASE_API_URL = 'http://www.ebi.ac.uk/proteins/api/'

def proteinSearch(lis):
    data = {}
    data['proteins'] = []
    for keyword  in lis:
        parameters = {'offset': 0,'accession' : keyword}
        header = {'Accept': 'application/json'}
        response = requests.get(BASE_API_URL + 'proteins', params = parameters, headers = header)
        if response.status_code != 200:
            return None
        json_response = response.json()
        for y in range(len(json_response)):
            protein = {}
            protein['id'] = json_response[y]['accession']
            print(protein['id'])
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


def get_protein_ids(keyword):
    url  = 'https://www.uniprot.org/uniprot/?query=' + keyword
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup( html ,'html.parser')
    entries = soup('td', {'class' : 'entryID'})
    protein_ids = []
    for entry in entries:
        protein_ids.append(entry.a.string)
    return protein_ids

args = []
for x in sys.argv:
     args.append(x)
protein_list  = get_protein_ids(args[1])
if len(protein_list) > int(args[2]):
    protein_list = protein_list[:int(args[2])]
proteinSearch(protein_list)
