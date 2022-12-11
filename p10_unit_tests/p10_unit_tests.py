import unittest
import aiounittest
from botbuilder.schema import Activity, ActivityTypes,Attachment
from botbuilder.dialogs import DialogSet, DialogTurnStatus
from botbuilder.core import TurnContext,ConversationState,MemoryStorage,MessageFactory
from email_prompt import EmailPrompt

from botbuilder.core.adapters import TestAdapter


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

