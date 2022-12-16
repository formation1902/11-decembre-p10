from azure.cognitiveservices.language.luis.runtime import LUISRuntimeClient
from msrest.authentication import CognitiveServicesCredentials
from config import DefaultConfig

CONFIG = DefaultConfig()


def test_luis_intent():
    
    clientRuntime = LUISRuntimeClient(
        CONFIG.LUIS_API_HOST_NAME,
        CognitiveServicesCredentials(CONFIG.LUIS_API_KEY))
    
    request ='book a flight from Paris to London leaving April 15 2022 coming back May 15 2022, for a maximum budget of 500 euros'

    response = clientRuntime.prediction.resolve(CONFIG.LUIS_APP_ID, query=request)

    check_top_intent = 'book_flight'
    is_top_intent = response.top_scoring_intent.intent
    assert check_top_intent == is_top_intent


def test_luis_origin():

    clientRuntime = LUISRuntimeClient(
        CONFIG.LUIS_API_HOST_NAME,
        CognitiveServicesCredentials(CONFIG.LUIS_API_KEY))
    
    request ='book a flight from Paris to London leaving April 15 2022 coming back May 15 2022, for a maximum budget of 500 euros'

    response = clientRuntime.prediction.resolve(CONFIG.LUIS_APP_ID, query=request)
    
    check_origin = 'paris'
    all_entities = response.entities
    
    for i in range(0, len(all_entities)):
        if all_entities[i].type == 'from_city':
            is_origin = all_entities[i].entity
    
    assert check_origin == is_origin


def test_luis_destination():

    clientRuntime = LUISRuntimeClient(
        CONFIG.LUIS_API_HOST_NAME,
        CognitiveServicesCredentials(CONFIG.LUIS_API_KEY))
    
    request ='book a flight from Paris to London leaving April 15 2022 coming back May 15 2022, for a maximum budget of 500 euros'

    response = clientRuntime.prediction.resolve(CONFIG.LUIS_APP_ID, query=request)
    
    check_destination = 'london'
    all_entities = response.entities
    
    for i in range(0, len(all_entities)):
        if all_entities[i].type == 'to_city':
            is_destination = all_entities[i].entity
    
    assert check_destination == is_destination