#pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib bs4


#python -m venv my-venv
#my-venv/bin/pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib bs4
#my-venv/bin/python script.py


import os, pickle, time
from collections import OrderedDict

import google
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors


import json
import datetime
import re

request_delay = 1.0

def Create_Service(client_secret_file, picklename,picklepath='.', api_name='youtube', api_version='v3', scopes=['https://www.googleapis.com/auth/youtube']):
    # modified from:
    # https://learndataanalysis.org/copy-videos-from-any-youtube-playlist-to-your-own-playlist-with-python-and-youtube-api

    cred = None

    pickle_file = f'{picklepath}/{picklename}_token_{api_name}_{api_version}.pickle'
    print("'{}'".format(pickle_file))

    if os.path.exists(pickle_file):
        with open(pickle_file, 'rb') as token:
            cred = pickle.load(token)

    if not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(google.auth.transport.requests.Request())
        else:
            flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(client_secret_file, scopes)
            cred = flow.run_local_server()

        with open(pickle_file, 'wb') as token:
            pickle.dump(cred, token)

    try:
        service = googleapiclient.discovery.build(api_name, api_version, credentials=cred)
        print(api_name, 'service created successfully')
        return service
    except Exception as e:
        print(e)
        print(f'Failed to create service instance for {api_name}')
        os.remove(pickle_file)
        return None

def Create_Service2(n,dir='.'):
    your_id='YOURFILEID'
    return  Create_Service(f'{dir}/creds/client_secret_{your_id}.apps.googleusercontent.com.json', n, f'{dir}/creds')


def GetList(cmd,params,request_delay=1.0, maxResults=50):
    items=[]
    nextPageToken = None

    while True:
        time.sleep(request_delay)
        request = cmd.list(maxResults=maxResults, pageToken=nextPageToken, **params)
        response = request.execute()
        time.sleep(request_delay)
        nextPageToken = response.get('nextPageToken')
        items.extend(response['items'])

        if nextPageToken==None:
            break

    return items

def GetListBatch(cmd,params,batch_param_name,inputs,request_delay=1.0, maxResults=50):
    items=[]

    for i in range(0,(len(inputs)+maxResults-1)//maxResults):
        batch = ','.join(inputs[i*maxResults:i*maxResults+maxResults])
        time.sleep(request_delay)
        request = cmd.list(maxResults=maxResults, **(params|{batch_param_name : batch}))
        response = request.execute()
        items.extend(response['items'])

    return items







