#!/usr/bin/env python

import os


class Bot_luis_app_and_insights_configuration:
    #
    # Elements pour la configuration de l'application chatbot : 
    #   - ___________________________PORT: port du service pour le bot emulator
    #   - _________________________APP_ID: 
    #   - ___________________APP_PASSWORD: 
    #   - ____________________LUIS_APP_ID: 
    #   - ___________________LUIS_API_KEY: 
    #   - _____________LUIS_API_HOST_NAME: 
    #   - APPINSIGHTS_INSTRUMENTATION_KEY: app-insight
    #
    
    PORT = 3978
    
    APP_ID = os.environ.get("MicrosoftAppId", "msa-p10-manually-set-id")
    
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "msaSecret1902")
    
    LUIS_APP_ID = os.environ.get("LuisAppId","fa851bde-e539-4c83-b9ef-2f36ca8e1b44")
    
    LUIS_API_KEY = os.environ.get("LuisAPIKey","898a47800608435ea33ccde7f880abc5")
    
    LUIS_API_HOST_NAME = os.environ.get("LuisAPIHostName","p10-luis-authoring.cognitiveservices.azure.com/")
    # 
    # LUIS_API_HOST_NAME = os.environ.get("LuisAPIHostName","westeurope.api.cognitive.microsoft.com")

    # LUIS_API_HOST_NAME = os.environ.get("LuisAPIHostName","p10-luis.cognitiveservices.azure.com")
    
    APPINSIGHTS_INSTRUMENTATION_KEY = os.environ.get(
        "AppInsightsInstrumentationKey", "a8995314-2a9d-4720-b3ad-cba0cbd2258c"
    )
    
    
# https://p10-luis.cognitiveservices.azure.com/luis/prediction/v3.0/apps/cf2d6334-8bf9-459a-8a52-573d90fa218c/slots/staging/predict?verbose=true&show-all-intents=true&log=true&subscription-key=a328ef4940ad427db28faf097810819c&query=YOUR_QUERY_HERE    