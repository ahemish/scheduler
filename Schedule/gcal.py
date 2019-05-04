import os.path
import datetime
import pickle
import json
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


def gcal_auth(credentails_file):
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
              credentails_file, SCOPES)
          creds = flow.run_local_server()
      # Save the credentials for the next run
      with open('token.pickle', 'wb') as token:
          pickle.dump(creds, token)
  return creds



def gcal_events(credentails_file):
  gcal_creds = gcal_auth(credentails_file)
  service = build('calendar', 'v3', credentials=gcal_creds)
  events_result = service.events().list(calendarId='primary').execute()
  events = events_result.get('items', [])
  return events

if __name__ == "__main__":
    print(json.dumps(gcal_events('/Volumes/Disk 2/Users/arranhemish/Downloads/credentials.json'),indent=4))

# now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
# print('Getting the upcoming 10 events')

# if not events:
#     print('No upcoming events found.')
# print(json.dumps(events,indent=4))

# new_event = {
#   'summary': 'Python',
#   'description': 'A chance to hear more about Google\'s developer products.',
#   'start': {
#     'dateTime': '2019-05-03T09:00:00',
#     'timeZone' : 'Europe/London'
#   },
#   'end': {
#     'dateTime': '2019-05-03T17:00:00',
#     'timeZone' : 'Europe/London'

#   }
# }

# events_result = service.events().insert(calendarId='primary',body=new_event).execute()
