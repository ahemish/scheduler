import os.path
import datetime
import pickle
import json
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


def gcal_auth(credentials_file):
  SCOPES = ['https://www.googleapis.com/auth/calendar']
  creds = None
  if os.path.exists('token.pickle'):
      with open('token.pickle', 'rb') as token:
          creds = pickle.load(token)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
      if creds and creds.expired and creds.refresh_token:
          creds.refresh(Request())
      else:
          flow = InstalledAppFlow.from_client_secrets_file(
              credentials_file, SCOPES)
          creds = flow.run_local_server()
      # Save the credentials for the next run
      with open('token.pickle', 'wb') as token:
          pickle.dump(creds, token)
  return creds



def gcal_events(credentials_file):
  gcal_creds = gcal_auth(credentials_file)
  service = build('calendar', 'v3', credentials=gcal_creds)
  events_result = service.events().list(calendarId='primary').execute()
  events = events_result.get('items', [])
  return events

def gcal_delete_event(event_id, credentials_file):
    gcal_creds = gcal_auth(credentials_file)
    service = build('calendar', 'v3', credentials=gcal_creds)
    events_result = service.events().delete(calendarId='primary',eventId=event_id).execute()
    return events_result

def gcal_add_event(title, start , end, credentials_file):
    gcal_creds = gcal_auth(credentials_file)
    service = build('calendar', 'v3', credentials=gcal_creds)
    new_event = {
    'summary': title,
    'start': {
        'dateTime': start,
        'timeZone' : 'Europe/London'
    },
    'end': {
        'dateTime': end,
        'timeZone' : 'Europe/London'

    }
    }
    events_result = service.events().insert(calendarId='primary',body=new_event).execute()
    return events_result['id']

    


if __name__ == "__main__":
    print(json.dumps(gcal_events('/Volumes/Disk 2/Users/arranhemish/Documents/git/credentials.json'),indent=4))

# now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
# print('Getting the upcoming 10 events')

# if not events:
#     print('No upcoming events found.')
# print(json.dumps(events,indent=4))

