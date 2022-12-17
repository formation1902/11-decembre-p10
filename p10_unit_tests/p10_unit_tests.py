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

from botbuilder.core    import TelemetryLoggerMiddleware
from botbuilder.applicationinsights                     import ApplicationInsightsTelemetryClient
from botbuilder.integration.applicationinsights.aiohttp import AiohttpTelemetryProcessor

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
        
    def test_recognizer_is_configured(self):
        self.assertTrue(Reserver_un_billet_d_avion_Recognizer(self.CONFIG).is_configured)

    def test_luis(self):
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
        
        
    def test_telemetry(self):
        print("Testing telemetry")
        try:
            INSTRUMENTATION_KEY = self.CONFIG.APPINSIGHTS_INSTRUMENTATION_KEY


            TELEMETRY_CLIENT = ApplicationInsightsTelemetryClient(
                INSTRUMENTATION_KEY, 
                telemetry_processor=AiohttpTelemetryProcessor(), 
                client_queue_size=10
            )

            # ---> Logging :  Code for enabling activity and personal information logging.
            TELEMETRY_CLIENT.track_trace("TELEMETRY_CLIENT - test before build - activated by git actions")
            TELEMETRY_CLIENT.flush()
        except:
            self.assertIsNot(True, True)
        
        
