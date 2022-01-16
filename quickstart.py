from __future__ import print_function

import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

#! При изменении этих областей нужно удалить файл token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def main():
    """Показывает базовое использование API календаря. 
       Выводит на экран название и начало 10 будующих событий календаря.
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
            #! Необходимо указывать абсолютный путь к файлу credentials.json
            flow = InstalledAppFlow.from_client_secrets_file(
                'E:\Google_CalendarAPI\Ver_2\credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Сохранение учетных данных для следующего запуска
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)

        # Вызов Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        print('Getting the upcoming 10 events')
        events_result = service.events().list(calendarId='primary', timeMin=now,
                                              maxResults=10, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
            return

        # Отобаражает начало и название 10 будующих событий
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            # print(start, event['summary'])
            
            #! Отображение всех 10 будующих событий в календаре
            print(start, event)
    except HttpError as error:
        print('An error occurred: %s' % error)


if __name__ == '__main__':
    main()