#!/usr/bin/env PYTHONIOENCODING=UTF-8 /usr/local/bin/python3
# coding=utf-8


# https://developers.google.com/resources/api-libraries/documentation/tasks/v1/python/latest/tasks_v1.tasks.html

from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/tasks.readonly']

config_location = '/Users/yusup/.config/bitbar'


# tmp_dir = '/tmp'

def urgent_task():
    """Shows basic usage of the Tasks API.
    Prints the title and ID of the first 10 task lists.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(f'{config_location}/token.pickle'):
        with open(f'{config_location}/token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                f'{config_location}/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(f'{config_location}/token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('tasks', 'v1', credentials=creds)

    # Call the Tasks API
    results = service.tasklists().list(maxResults=10).execute()
    items = results.get('items', [])

    if not items:
        print('No task lists found.')
    else:
        for item in items:
            if item['title'] == 'Work':
                work = item
    r2 = service.tasks().list(tasklist=work['id'], showCompleted=False, maxResults=100).execute()
    tasks = r2.get('items', [])
    with_due = []
    without_due = []
    for t in tasks:
        if 'due' in t:
            with_due.append(t)
        else:
            without_due.append(t)
    with_due = sorted(with_due, key=lambda i: (i['due']))
    if len(with_due) > 0:
        return with_due[0]['title']

    if len(without_due) > 0:
        return without_due[0]['title']
    return 'No Task'


if __name__ == '__main__':
    print(urgent_task())
    print('---')
    print('Refresh | refresh=true')
