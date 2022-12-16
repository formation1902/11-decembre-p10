import unittest
import aiounittest
from botbuilder.schema import Activity, ActivityTypes,Attachment
from botbuilder.dialogs import DialogSet, DialogTurnStatus
from botbuilder.core import TurnContext,ConversationState,MemoryStorage,MessageFactory

from botbuilder.core.adapters import TestAdapter
from opencensus.ext.azure.log_exporter import AzureLogHandler
import logging


from azure.cognitiveservices.language.luis.runtime import LUISRuntimeClient
from msrest.authentication import CognitiveServicesCredentials

import requests


# file_2.py
import sys
sys.path.append('/msaOpenClassrooms/p10/p10_bot')
import config
from Reserver_un_billet_d_avion_Recognizer import Reserver_un_billet_d_avion_Recognizer

# class TestP10(unittest.TestCase):
class TestP10(aiounittest.AsyncTestCase):    
    
    def setUp(self) -> None:
        self.CONFIG      = config.Bot_luis_app_and_insights_configuration()
        self.RECOGNIZER  = Reserver_un_billet_d_avion_Recognizer(self.CONFIG)
        
    
    def test_config_is_ok(self):
        self.assertEqual(self.CONFIG.PORT,3978)
        self.assertEqual(self.CONFIG.LUIS_API_HOST_NAME,"p10-luis-authoring.cognitiveservices.azure.com/")
        self.assertEqual(self.CONFIG.LUIS_API_KEY,"898a47800608435ea33ccde7f880abc5")
        
        
    def test_recognizer_is_configured(self):
        self.assertTrue(self.RECOGNIZER.is_configured)


    def test_AppInsights_connexion(self):
        try:
            logger = logging.getLogger(__name__)
            connect_str = "InstrumentationKey=d546dc50-469e-4f4b-abc6-2f30577a7572;IngestionEndpoint=https://centralus-0.in.applicationinsights.azure.com/;LiveEndpoint=https://centralus.livediagnostics.monitor.azure.com/"
            # logger.addHandler(AzureLogHandler(connection_string=self.CONFIG.APPINSIGHTS_INSTRUMENTATION_KEY))
            logger.addHandler(AzureLogHandler(connection_string=connect_str))
        except:
            self.assertIsNot(True, True)

    def test_luis(self):
        msaApiEndPoint = "https://msa-p10-luis-prediction.cognitiveservices.azure.com/luis/prediction/v3.0/apps/877689f4-e2c4-42ca-bfad-ef1b8f089840/slots/production/predict?verbose=true&show-all-intents=true&log=true&subscription-key=34f7bed36b224282b7a725375beabe6b&query="
        query ='From Paris to berlin leaving today, and coming back at Decembre 31 1999, for a maximum budget of 51 euros'
        
        try:
            response =  requests.get(msaApiEndPoint + query)
            intention_attendue = 'intention_reserver_un_billet_d_avion'
            luis_top_intent    =  response.json()['prediction']['topIntent']
            assert intention_attendue == luis_top_intent

            coffre_fort = response.json()['prediction']['entities']
            for key in coffre_fort.keys():
                if key == '$instance':
                    for ikey in coffre_fort[key]:
                        print('\t - ',ikey,' : ',coffre_fort[key][ikey])        
                else:
                    print('\t - ',key,' : ',coffre_fort[key])
            print("\n",)
            print("\n",)
        except:
            self.assertIsNot(True, True)
        
        
        
        
        
        
    def fx_test_luis_intent(self):
        clientRuntime = LUISRuntimeClient(
            'https://p10-luis-authoring.cognitiveservices.azure.com/', 
            # 'https://westeurope.api.cognitive.microsoft.com',
            CognitiveServicesCredentials(self.CONFIG.LUIS_API_KEY)
        )
    
        query ='From Paris to berlin leaving just right now coming back Decembre 31 1999, for a maximum budget of 51 euros'
    
        response = clientRuntime.prediction.resolve(self.CONFIG.LUIS_APP_ID, query=query)

        intention_attendue = 'intention_reserver_un_billet_d_avion'
        luis_top_intent = response.top_scoring_intent.intent
        
        print("Detected entities:")
        for entity in response.entities:
            print("\t-> Entity '{}' (type: {}, score:{:d}%)".format(
                entity.entity,
                entity.type,
                int(entity.additional_properties['score']*100)
            ))
        print("\nComplete result object as dictionnary")
        pprint(response.as_dict())
        
        assert intention_attendue == luis_top_intent
    
    
    
    
    # import json
    # import os.path
    # from pprint import pprint
    # SUBSCRIPTION_KEY_ENV_NAME = "LUIS_SUBSCRIPTION_KEY"
    # CWD = os.path.dirname(__file__)


    # def runtime(subscription_key):
    #     client = LUISRuntimeClient(
    #         'https://westus.api.cognitive.microsoft.com',
    #         CognitiveServicesCredentials(subscription_key),
    #     )

    #     try:
    #         query = "Look for hotels near LAX airport"
    #         print("Executing query: {}".format(query))
    #         result = client.prediction.resolve(
    #             "bce13896-4de3-4783-9696-737d8fde8cd1",  # LUIS Application ID
    #             query
    #         )

    #         print("\nDetected intent: {} (score: {:d}%)".format(
    #             result.top_scoring_intent.intent,
    #             int(result.top_scoring_intent.score*100)
    #         ))
    #         print("Detected entities:")
    #         for entity in result.entities:
    #             print("\t-> Entity '{}' (type: {}, score:{:d}%)".format(
    #                 entity.entity,
    #                 entity.type,
    #                 int(entity.additional_properties['score']*100)
    #             ))
    #         print("\nComplete result object as dictionnary")
    #         pprint(result.as_dict())

    #     except Exception as err:
    #         print("Encountered exception. {}".format(err))


    # if __name__ == "__main__":
    #     import sys
    #     import os.path
    #     sys.path.append(os.path.abspath(os.path.join(__file__, "..", "..")))
    #     from tools import execute_samples
    #     execute_samples(globals(), SUBSCRIPTION_KEY_ENV_NAME)