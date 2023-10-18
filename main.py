from __future__ import print_function

import datetime
import os
import time
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly','https://www.googleapis.com/auth/drive']
notag = "Shows basic usage of the Google Calendar API"

def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        parent_folder_id = 'dummy'
        calendar = build('calendar', 'v3', credentials=creds)
        drive = build('drive', 'v3', credentials=creds)
        query = f"'{parent_folder_id}' in parents and mimeType = 'application/vnd.google-apps.folder'"
        results = drive.files().list(q=query).execute()
        items = results.get('files', [])
        tempitems = []
        ids = []
        for item in items:
            tempitems.append(item['name'])
            ids.append(item['id'])
            #topfolder.append(drive.files().get(fileId=item['id'], fields='parents').execute().get('parents', []))
            #print(item['name'])
        #print(topfolder)
        items = tempitems
        def umbennen(name, newname):
            update = {
                'name': f'{newname}',
            }
            for item in range(len(items)):
                if items[item] == name:
                    updated_folder = drive.files().update(fileId=ids[item], body=update, fields='name').execute()
        def erstellen(name):
            file_metadata = {
                'name': f'{name}',
                'parents': [parent_folder_id],
                'mimeType': 'application/vnd.google-apps.folder'
            }
            file = drive.files().create(body=file_metadata, fields='id').execute()
        def existiert(name):
            #print(items)
            for item in items:
                if str(name) in item:
                    return True
            return False
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        events_result = calendar.events().list(calendarId='primary', timeMin=now, singleEvents=True, orderBy='startTime').execute()
        events = events_result.get('items', [])
        folders = os.listdir("events")
        folders = items
        if folders == []:
            folders = [notag]
        for folder in folders:
            if events == []:
                events = [{f'kind': 'calendar#event', 'etag': '"1"', 'id': '1', 'status': 'confirmed', 'htmlLink': 'https://www.google.com/calendar/', 'created': '2023-10-01T22:39:49.000Z', 'updated': '2023-10-01T22:39:49.595Z', 'summary': {notag}, 'creator': {'email': 'noway@no.de', 'self': True}, 'organizer': {'email': 'noway@no.de, 'self': True}, 'start': {'date': '2023-10-02'}, 'end': {'date': '2023-10-03'}, 'transparency': 'transparent', 'iCalUID': 'sasasm', 'sequence': 0, 'reminders': {'useDefault': False}, 'eventType': 'default'}]
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                if not existiert(f"{event['summary']} {start}") and str(str(event['summary'])) != "{'"+notag+"'}":
                    erstellen(f"{event['summary']} {start}")
                #print(start, event['summary'])
                if (not(str(folder) == str(f"{event['summary']} {start}")) and bool("[Veraltet]" not in folder and folder != notag)):
                    a = True
                    value = 2
                    while a:
                        if not existiert(f"{folder} [Veraltet]"):
                            umbennen(f"{folder}",f"{folder} [Veraltet]")
                            a = False
                        else:
                            if not existiert(f"{folder} [Veraltet][{value}]"):
                                umbennen(f"{folder}", f"{folder} [Veraltet][{value}]")
                                a = False
                            else:
                                value+=1
    except HttpError as error:
        print('An error occurred: %s' % error)


if __name__ == '__main__':
    while True:
        time.sleep(1)
        main()
