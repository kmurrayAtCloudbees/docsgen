#!/usr/bin/env python3
from __future__ import print_function
import os.path, sys
from apiclient.http import MediaFileUpload
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive','https://www.googleapis.com/auth/documents' ]

def main(argv):
    # The Name of the Client
    if len(sys.argv) <= 2:
        print('Invalid Argument')
        print('usage: uploadDoc.py <folder_id> <document_path>')
        sys.exit(2)
    else:
        FOLDER_ID = sys.argv[1]
        DOC_PATH = sys.argv[2]
    
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('./gdocs/token.json'):
        creds = Credentials.from_authorized_user_file('./gdocs/token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                './gdocs/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('./gdocs/token.json', 'w') as token:
            token.write(creds.to_json())

    docsService = build('docs', 'v1', credentials=creds)
    driveService = build('drive', 'v3', credentials=creds)

    file_metadata = {
        'name': DOC_PATH,
        'parents': [FOLDER_ID],
        'mimeType': 'application/vnd.google-apps.document'
        }
    
    media = MediaFileUpload(DOC_PATH,
                        mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                        resumable=True)

    new_doc = driveService.files().create(body=file_metadata,
        media_body=media, fields='id').execute()
    
    print(str(new_doc['id']))

if __name__ == '__main__':
    main(sys.argv[1:])