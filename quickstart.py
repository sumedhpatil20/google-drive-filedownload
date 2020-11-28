'''
from __future__ import print_function
import pickle
import io
import requests
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaIoBaseDownload

SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']

def main():
    # def download_file(file_id, filename):
    #     request = service.files().get(fileId=file_id)
    #     fh = io.BytesIO()
    #     downloader = MediaIoBaseDownload(fh, request)
    #     done = False
    #     while done is False:
    #         status, done = downloader.next_chunk()
    #         print("Download %d%%." % int(status.progress() * 100))
    #     return fh.getvalue()
    # creds = None
    def download_file_from_google_drive(id, destination):
        URL = "https://docs.google.com/uc?export=download"
        session = requests.Session()
        response = session.get(URL, params = { 'id' : id }, stream = True)
        token = get_confirm_token(response)

        if token:
            params = { 'id' : id, 'confirm' : token }
            response = session.get(URL, params = params, stream = True)
        save_response_content(response, destination)    

    def get_confirm_token(response):
        for key, value in response.cookies.items():
            if key.startswith('download_warning'):
                return value
        return None

    def save_response_content(response, destination):
        CHUNK_SIZE = 32768
        with open(destination, "wb") as f:
            for chunk in response.iter_content(CHUNK_SIZE):
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)
    
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)

    
    results = service.files().list(
        pageSize=10, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])

    if not items:
        print('No files found.')
    else:
        print('Files:')
        #for item in items:
            #print(u'{0} ({1})'.format(item['name'], item['id']))
    
    for f in items:
        print( f['name'])
        print( f['id'])
        if f['id'] == "1gaNv4RK4NrKi5t3TOOmT6a5urYRmsIhs":
            # download_file(f['id'], f['name'])
            destination = 'D:\\download pc\\' + f['name']
            download_file_from_google_drive(f['id'], destination)

if __name__ == '__main__':
    main()
'''

from __future__ import print_function
import pickle
import io
import requests
import sys
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaIoBaseDownload

SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']

def main(file_id,tempdestination):

    def download_file_from_google_drive(id, destination):
        URL = "https://docs.google.com/uc?export=download"
        session = requests.Session()
        response = session.get(URL, params = { 'id' : id }, stream = True)
        token = get_confirm_token(response)

        if token:
            params = { 'id' : id, 'confirm' : token }
            response = session.get(URL, params = params, stream = True)
        save_response_content(response, destination)    

    def get_confirm_token(response):
        for key, value in response.cookies.items():
            if key.startswith('download_warning'):
                return value
        return None

    def save_response_content(response, destination):
        CHUNK_SIZE = 32768
        with open(destination, "wb") as f:
            for chunk in response.iter_content(CHUNK_SIZE):
                if chunk: 
                    f.write(chunk)
    
    
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)

    
    results = service.files().list(
        pageSize=10, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])

    if not items:
        print('No files found.')
    else:
        
        for f in items:
            # print( f['name'])
            # print( f['id'])
            if f['id'] == file_id:
                destination = tempdestination + '\\' +f['name']
                download_file_from_google_drive(f['id'], destination)
        print('Given file id not found')

if __name__ == '__main__':
    n = len(sys.argv)
    if n < 3 :
        print("Invalid Arguments passed")
        
    else:
        main(sys.argv[1],sys.argv[2])
