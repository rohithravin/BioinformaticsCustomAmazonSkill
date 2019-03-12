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
            protein['protein_name'] = json_response[y]['protein']['recommendedName']['fullName']['value']
            protein['gene'] = json_response[y]['id']
            protein['function'] = json_response[y]['comments'][0]['text'][0]['value']
            go = []
            pdb_entry = []
            for x in range(len(json_response[y]['dbReferences'])):
                if json_response[y]['dbReferences'][x]['type'] == 'PDBsum':
                    pdb_entry.append([json_response[y]['dbReferences'][x]['id'], 'https://www.ebi.ac.uk/pdbe/entry/pdb/' + str(json_response[y]['dbReferences'][x]['id'])])
                if (json_response[y]['dbReferences'][x]['type'] == 'GO'):
                    go.append(json_response[y]['dbReferences'][x]['properties']['term'][2:].title())
            protein['pdb_entries'] = pdb_entry
            protein['gene_ontology'] = go
            data['proteins'].append(protein)
    with open('proteins.json', 'w') as outfile:
        json.dump(data, outfile)
    return data

#keyword, protein name, location, discription, organism, proteinID
#pdb entry id, need to parse xml as well
def get_protein_ids(query, entry_id = None, organism = None, protein_name = None, go_terms = None, keywords = None ):
    url  = 'https://www.uniprot.org/uniprot/?query='
    query = query.split()
    for q in range(len(query)):
        if q == 0:
            url+=  str(query[q])
        else:
            url+= '+' + str(query[q])
    if entry_id is not None:
        for x in range(len(entry_id)):
            if x == 0:
                url += '+mnemonic:' + str(entry_id[x])
            else:
                url += '+OR+mnemonic:' + str(entry_id[x])
    if organism is not None:
        for x in range(len(organism)):
            if x == 0:
                url += '+organism:' + str(organism[x])
            else:
                url += '+OR+organism:' + str(organism[x])
    if protein_name is not None:
        for x in range(len(protein_name)):
            if x == 0:
                url += '+name:' + str(protein_name[x])
            else:
                url += '+OR+name:' + str(protein_name[x])
    if go_terms is not None:
        for x in range(len(go_terms)):
            if x == 0:
                url += '+goa:' + str(go_terms[x])
            else:
                url += '+OR+goa:' + str(go_terms[x])
    if keywords is not None:
        for x in range(len(keywords)):
            if x == 0:
                url += '+keyword:' + str(keywords[x])
            else:
                url += '+OR+keyword:' + str(keywords[x])
    url+= '+reviewed:yes&sort=score'
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup( html ,'html.parser')
    entries = soup('td', {'class' : 'entryID'})
    protein_ids = []
    for entry in entries:
        protein_ids.append(entry.a.string)
    return protein_ids


def get_proteins (num, query, entry_id = None, organism = None, protein_name = None, go_terms = None, keywords = None):
    if not isinstance(num, int):
        return -1
    if not isinstance(query, str):
        return -1
    if entry_id is not None and not  isinstance(entry_id, list):
        return -1
    if organism is not None and not  isinstance(organism, list):
        return -1
    if protein_name is not None and not  isinstance(protein_name, list):
        return -1
    if go_terms is not None and not  isinstance(go_terms, list):
        return -1
    if keywords is not None and not  isinstance(keywords, list):
        return -1
    protein_list  = get_protein_ids(query, entry_id, organism, protein_name, go_terms, keywords)
    if len(protein_list) > num:
        protein_list = protein_list[:num]
    return proteinSearch(protein_list)

#EXPAMPLES
#print(get_proteins (10, 'insulin', organism = ['human']))
#print(get_proteins (10, 'lung cancer', organism = ['mouse']))
