
import urllib
from botocore.vendored import requests
import json
from html.parser import HTMLParser

BASE_API_URL = 'http://www.ebi.ac.uk/proteins/api/'

"""
The lambda_handler receives the request from the Alexa skill, identifies the type of intent and calls the appropriate function
"""

def lambda_handler(event, context):
    print(event['request'])
    if event['request']['type'] == "IntentRequest":
        return intent_scheme(event)
    if event['request']['type'] == "WebSearch":
        return intent_scheme(event)
    if event['request']['type'] == "LaunchRequest":
        return on_launch(event)
    elif event['request']['type'] == "IntentRequest":
        return intent_scheme(event)
    elif event['request']['type'] == "SessionEndedRequest":
        return on_end()

#start function basically logs to console to check if the request was received and the connection was made
def on_start(event):
   print("Session Started.")

#end function basically logs to console to know when the session has ended

def on_end():
    print("session end")

#this function dispatches the intent with appropriate parameters depending on the type of intent

def intent_scheme(event):

    intent_name = event['request']['intent']['name']
    if intent_name == "filterSearch":
        return getProteins(event)
    if intent_name == "WebSearch":
        return getProteins(event)
    elif intent_name in ["AMAZON.NoIntent", "AMAZON.StopIntent", "AMAZON.CancelIntent"]:
        return stop_the_skill(event)
    elif intent_name == "AMAZON.HelpIntent":
        return assistance(event)
    elif intent_name == "AMAZON.FallbackIntent":
        return fallback_call(event)

#This function sends a stop response to the alexa device when the user exits the skill
def stop_the_skill(event):
    stop_MSG = "Thank you. Bye!"
    reprompt_MSG = ""
    card_TEXT = "Bye."
    card_TITLE = "Bye Bye."
    return output_json_builder_with_reprompt_and_card(stop_MSG, card_TEXT, card_TITLE, reprompt_MSG, True)

#This function tells the user how to use the skill if they are not sure. This is triggered when the user says "Alexa, help" in an ongoing session
def assistance(event):
    assistance_MSG = "You can ask me to search a protein. For example, search cancer."
    reprompt_MSG = "Do you want to hear more about a particular protein?"
    card_TEXT = "You've asked for help."
    card_TITLE = "Help"
    return output_json_builder_with_reprompt_and_card(assistance_MSG, card_TEXT, card_TITLE, reprompt_MSG, False)

#If alexa does not undertsanf the request, this is what is triggered
def fallback_call(event):
    fallback_MSG = "I can't help you with that, try rephrasing the question or ask for help by saying HELP."
    reprompt_MSG = "Do you want to hear more about a particular protein?"
    card_TEXT = "You've asked a wrong question."
    card_TITLE = "Wrong question."
    return output_json_builder_with_reprompt_and_card(fallback_MSG, card_TEXT, card_TITLE, reprompt_MSG, False)

#This is triggered when the skill launches. It tells the user about the skill
def on_launch(event):
    print("launching")
    msg = "Hi, welcome to the Uniprot Protein Search Alexa Skill."
    reprompt_msg = "Do you want to hear more about a particular protein?"
    card_TEXT = "Protein Search"
    card_TITLE = "Choose a protein."
    return output_json_builder_with_reprompt_and_card(msg, card_TEXT, card_TITLE, reprompt_msg, False)
#Constructs the plaintext
def plain_text_builder(text_body):
    text_dict = {}
    text_dict['type'] = 'PlainText'
    text_dict['text'] = text_body
    return text_dict
#Builds reprompt message if the user does not say anything
def reprompt_builder(repr_text):
    reprompt_dict = {}
    reprompt_dict['outputSpeech'] = plain_text_builder(repr_text)
    return reprompt_dict
 #Constructs the card to be sent to the device
def card_builder(c_text, c_title):
    card_dict = {}
    card_dict['type'] = "Simple"
    card_dict['title'] = c_title
    card_dict['content'] = c_text
    return card_dict
#This function integrates other functions to create the card and response field for the output JSON
def response_field_builder_with_reprompt_and_card(outputSpeach_text, card_text, card_title, reprompt_text, value):
    speech_dict = {}
    speech_dict['outputSpeech'] = plain_text_builder(outputSpeach_text)
    speech_dict['card'] = card_builder(card_text, card_title)
    speech_dict['reprompt'] = reprompt_builder(reprompt_text)
    speech_dict['shouldEndSession'] = value
    return speech_dict

#Integrates other response functions to generate speecha nd card outputs
def output_json_builder_with_reprompt_and_card(outputSpeach_text, card_text, card_title, reprompt_text, value):
    print("outputting ", outputSpeach_text)
    response_dict = {}
    response_dict['version'] = '1.0'
    response_dict['response'] = response_field_builder_with_reprompt_and_card(outputSpeach_text, card_text, card_title, reprompt_text, value)
    return response_dict
################################################ Actual code for db search starts here###################################
#Class to parse HTML page. TODO: Replace with faster parsing library so that multiple results can be returned
#This class is a subclass of the built in HTMLParser. We use this class to extract the protein id's from the html page we get
#We faster method would be to use the bs4, but had problem since it was an external library and not built it
class LinksParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.recording = 0
        self.data = []

    def handle_starttag(self, tag, attributes):
        if tag != 'td':
            return
        if self.recording:
            self.recording += 1
            return
        for name, value in attributes:
            if name == 'class' and value == 'entryID':
                break
        else:
            return
        self.recording = 1

    def handle_endtag(self, tag):
        if tag == 'td' and self.recording:
            self.recording -= 1

    def handle_data(self, data):
        if self.recording:
            self.data.append(data)

#makes the API call and parses the output when given a list of terms to search for
#given a list of the protein ids, will call an api call for each id and extract the required data and accumlate it into a json object an return it

def proteinSearch(lis):
    data = {}
    data['proteins'] = []
    for keyword  in lis:
        parameters = {'offset': 0,'accession' : keyword}
        header = {'Accept': 'application/json'}
        #api call
        response = requests.get(BASE_API_URL + 'proteins', params = parameters, headers = header)
        #check if api call was successful
        if response.status_code != 200:
            print("NONE PROteINS")
            return None
        json_response = response.json()
        #go through each lsit in resposne
        for y in range(len(json_response)):
            protein = {}
            #get required information from the resposne
            protein['id'] = json_response[y]['accession']
            protein['protein_name'] = json_response[y]['protein']['recommendedName']['fullName']['value']
            protein['gene'] = json_response[y]['id']
            protein['function'] = json_response[y]['comments'][0]['text'][0]['value']
            go = []
            pdb_entry = []
            #used to get the go terms
            for x in range(len(json_response[y]['dbReferences'])):
                if json_response[y]['dbReferences'][x]['type'] == 'PDBsum':
                    pdb_entry.append([json_response[y]['dbReferences'][x]['id'], 'https://www.ebi.ac.uk/pdbe/entry/pdb/' + str(json_response[y]['dbReferences'][x]['id'])])
                if (json_response[y]['dbReferences'][x]['type'] == 'GO'):
                    go.append(json_response[y]['dbReferences'][x]['properties']['term'][2:].title())
            protein['pdb_entries'] = pdb_entry
            protein['gene_ontology'] = go
            #adding the protein to the json object
            data['proteins'].append(protein)
    return data

#keyword, protein name, location, discription, organism, proteinID
#pdb entry id, need to parse xml as well
#Returns protein ids from uniprot needed to search them through API
def get_protein_ids(query, entry_id = None, organism = None, protein_name = None, go_terms = None, keywords = None ):

    url  = 'https://www.uniprot.org/uniprot/?query='
    query = query.split()
    for q in range(len(query)):
        if q == 0:
            url+=  str(query[q])
        else:
            url+= '+' + str(query[q])
    url+= '+reviewed:yes&sort=score'
    #create object of custom parser class
    p = LinksParser()
    #api call righ there
    f = urllib.request.urlopen(url)
    mybytes = f.read()
    mystr = mybytes.decode("utf8")
    #read in the data and get the ids
    p.feed(mystr)
    p.close()
    return p.data


#This is the function called by the alexa intentt_scheme() that makes use of other functions to send a response back to the Alexa interface
#main function to interact with, right now only takes in query, and no filters.
#adding filters could be the next time to optimize this function
def getProteins (query,num=5, entry_id = None, organism = None, protein_name = None, go_terms = None, keywords = None):
    #fquery = query['request']['intent']['slots']['search']['value']
    protein_list  = get_protein_ids(query, entry_id, organism, protein_name, go_terms, keywords)
    print("getting proteins")
    print(protein_list)
    if len(protein_list) > num:
        protein_list = protein_list[:num]
    proteins =  proteinSearch(protein_list)
    print(proteins)
    msg = "YOOOOO"
    reprompt_msg = "Do you want to hear more about a particular protein?"
    card_TEXT = "Protein Search"
    card_TITLE = "Results for " + query
    print(msg)
    #return output_json_builder_with_reprompt_and_card(msg, card_TEXT, card_TITLE, reprompt_msg, False)

getProteins('cancer')
