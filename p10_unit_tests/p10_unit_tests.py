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

class TestP10(unittest.TestCase): 
    
    def setUp(self) -> None:
        self.CONFIG      = config.Bot_luis_app_and_insights_configuration()
    
    def test_config_is_ok(self):
        self.assertEqual(self.CONFIG.PORT,3978)
        self.assertEqual(self.CONFIG.LUIS_API_HOST_NAME,"p10-luis-authoring.cognitiveservices.azure.com/")
        self.assertEqual(self.CONFIG.LUIS_API_KEY,"898a47800608435ea33ccde7f880abc5")
        
        
    def test_recognizer_is_configured(self):
        self.assertTrue(Reserver_un_billet_d_avion_Recognizer(self.CONFIG).is_configured)


    def test_AppInsights_connexion(self):
        try:
            logger = logging.getLogger(__name__)
            connect_str = "InstrumentationKey=d546dc50-469e-4f4b-abc6-2f30577a7572;IngestionEndpoint=https://centralus-0.in.applicationinsights.azure.com/;LiveEndpoint=https://centralus.livediagnostics.monitor.azure.com/"
            logger.addHandler(AzureLogHandler(connection_string=connect_str))
            logger.info('\n\n------------------------------------- local chatbot application started\n\n')
        except:
            self.assertIsNot(True, True)

    def test_luis(self):
        msaApiEndPoint = "https://msa-p10-luis-prediction.cognitiveservices.azure.com/luis/prediction/v3.0/apps/877689f4-e2c4-42ca-bfad-ef1b8f089840/slots/production/predict?verbose=true&show-all-intents=true&log=true&subscription-key=34f7bed36b224282b7a725375beabe6b&query="
        msaApiEndPoint = "https://msa-p10-luis-prediction.cognitiveservices.azure.com/luis/prediction/v3.0/apps/9159a5e0-246d-4723-9fd1-865fdd18d709/slots/production/predict?verbose=true&show-all-intents=true&log=true&subscription-key=34f7bed36b224282b7a725375beabe6b&query="
        query ='I would like a vacation for one. Depart from Paris to London between August 17 to September 7 and it should cost less than $3000 '
        
        try:
            #
            # L'intention
            #
            response =  requests.get(msaApiEndPoint + query)
            intention_attendue = 'intention_reserver_un_billet_d_avion'
            luis_top_intent    =  response.json()['prediction']['topIntent']
            
            assert intention_attendue == luis_top_intent

            #
            # Les entites
            #
            resultats_attendues = dict()
            resultats_attendues['ville_depart']      = 'paris'
            resultats_attendues['ville_destination'] = 'london'
            resultats_attendues['date_depart']       = 'august 17'
            resultats_attendues['date_retour']       = 'september 7'
            resultats_attendues['budget']           = '$3000'

            coffre_fort = response.json()['prediction']['entities']
            for key in coffre_fort.keys():
                # if key == '$instance':
                #     for ikey in coffre_fort[key]:
                #         print('\t - ',ikey,' : ',coffre_fort[key][ikey])        
                # else:
                if key != '$instance':
                    print('\t - ',key,' : ',coffre_fort[key])
                    error = "Pb with predicted value for ",key," : attendue==",resultats_attendues[key]," predicted==",coffre_fort[key][0].lower()
                    self.assertEqual(resultats_attendues[key],coffre_fort[key][0].lower(),error)
        except:
            self.assertIsNot(True, True)
        
        
        
# {"activityId":"340268f0-7cc8-11ed-88a8-31f87dfbab1f","activityType":"message","channelId":"emulator","fromId":"08bbd904-df4c-43ad-904e-e8ba0880109b","fromName":"User","locale":"en-US","recipientId":"1a98d340-7cc8-11ed-b01f-8519a79807a5","recipientName":"Bot","text":"No"}