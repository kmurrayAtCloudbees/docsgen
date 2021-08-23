#!/usr/bin/env python3
from __future__ import print_function
import os.path, sys
from apiclient import errors
from googleapiclient.http import MediaFileUpload
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/documents', 'https://www.googleapis.com/auth/drive']

def main(argv):
    # The Name of the Client
    if len(sys.argv) <= 1:
        print('Invalid Argument')
        print('usage: addCoverPage.py <document_id>')
        sys.exit(2)
    else:
        DOC_ID = sys.argv[1]
    
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
    
    TITLE_PAGE_IMAGE = './templates/2020-cloudbees-whitepaper-lg.jpeg'

    file_metadata = {'name': TITLE_PAGE_IMAGE}
    media = MediaFileUpload(TITLE_PAGE_IMAGE, mimetype='image/jpeg')
    upload = driveService.files().create(body=file_metadata, media_body=media, fields='webContentLink, id, webViewLink').execute()
    IMAGE_ID = upload.get('id')
    IMAGE_URL = upload.get('webContentLink')

    driveService.permissions().create(fileId=IMAGE_ID, body={'type': 'anyone', 'role': 'reader'}).execute()

    BODY = {
        'requests': [
            { 
                'insertSectionBreak': { 
                    'sectionType': 'CONTINUOUS',
                    'location': {
                        'index': 1
                    }
                }
            },
            {
                'updateSectionStyle': {
                    'range': {
                        'startIndex': 1,
                        'endIndex': 2
                    },
                    'sectionStyle': {
                        'sectionType': 'CONTINUOUS',
                        'useFirstPageHeaderFooter': 'true',
                        'pageNumberStart': 2,
                        'columnProperties': [
                            {
                                "paddingEnd": {
                                    'magnitude': 0,
                                    'unit': 'PT'
                                }
                            }
                        ],
                        'columnSeparatorStyle': 'NONE',
                        'contentDirection': 'LEFT_TO_RIGHT',
                        'marginTop': {
                            'magnitude': 0,
                            'unit': 'PT'
                        },
                        'marginBottom': {
                            'magnitude': 0,
                            'unit': 'PT'
                        },
                        'marginRight': {
                            'magnitude': 0,
                            'unit': 'PT'
                        },
                        'marginLeft': {
                            'magnitude': 0,
                            'unit': 'PT'
                        },
                        'marginHeader': {
                            'magnitude': 0,
                            'unit': 'PT'
                        },
                        'marginFooter': {
                            'magnitude': 0,
                            'unit': 'PT'
                        },
                    },
                    'fields': '*'
                }
            },
            {
                'insertInlineImage': { 
                    'uri': IMAGE_URL,
                    'objectSize': {
                         'height': {
                            'magnitude': 792,
                            'unit': 'PT'
                        },
                        "width": {
                            "magnitude": 612,
                             "unit": 'PT'
                        }
                    },
                    'location': {
                        'index': 1
                    }
                }
            }
        ]
    }

    docUpdate = docsService.documents().batchUpdate(
        documentId=DOC_ID, body=BODY).execute()    

    driveService.permissions().delete(fileId=IMAGE_ID, 
        permissionId='anyoneWithLink').execute()

if __name__ == '__main__':
    main(sys.argv[1:])