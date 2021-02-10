#more info here: https://developers.google.com/identity/protocols/oauth2
#quickstart here: https://developers.google.com/gmail/api/quickstart/python
import os.path
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from config import *


def get_token(filename='token.pickle', 
                credentials="credentials.json", 
                scopes=DEFAULT_SCOPES):
    
    creds = None
    if os.path.exists(filename):
        with open(filename, 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials, scopes)
            creds = flow.run_local_server(port=0)
        
        # Save the credentials for the next run
        with open(filename, 'wb') as token:
            pickle.dump(creds, token)

    return creds

def get_service(token):
    service = build('gmail', 'v1', credentials=token)
    return service
