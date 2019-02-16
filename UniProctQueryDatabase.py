import requests
import json
import pandas as pd
import numpy as np

BASE_API_URL = 'http://www.ebi.ac.uk/proteins/api/'

def proteinSearch():

    parameters = {'offset': 0, 'size': 1, 'keywords' : 'cancer'}
    header = {'Accept': 'application/json'}

    response = requests.get(BASE_API_URL + 'proteins', params = parameters, headers = header)

    #get response code from the request
    print('RESPONSE CODE: ' + str(response.status_code))

    #json_response = response.json()

    print(response.json())


proteinSearch()


#EXAMPLE OF HOW TO USE REST API WITH OpenNotify API'S
def dummy_test_api():
    #dummy base url
    base_api_url = 'http://api.open-notify.org/'

    #how to set up the parameters for the api request
    parameters = {"lat": 37.78, "lon": -122.41}

    #how to call the REST API
    response = requests.get(base_api_url + 'iss-pass.json', params = parameters)

    #get response code from the request
    print('RESPONSE CODE: ' + str(response.status_code))

    # Headers is a dictionary
    print('RESPONSE HEADERS: ' + str(response.headers))

    # Get the content-type from the dictionary.
    print('CONTENT-TYPE: ' + str(response.headers["content-type"]))

    #convert response to json NOTE THE STATUS CODE DISSAPEARS IN THIS CONVERSION
    json_response = response.json()

    #print the response
    print(json_response['response'])

#dummy_test_api()
