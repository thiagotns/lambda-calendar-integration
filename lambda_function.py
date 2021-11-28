from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime, timedelta
import json
import os

SCOPES = ['https://www.googleapis.com/auth/calendar']
CALENDAR_ID = os.environ['calendar_id']

def lambda_handler(event, context):
    
    print("## event: " + json.dumps(event))
    
    try:
        payload = json.loads(event['body'])
    except Exception as e:
        print(e)
        return {
            'statusCode': 412,
            'body': "Invalid event body"
        }
    
    if event['httpMethod'] == 'POST':
        return create(payload)
    elif event['httpMethod'] == 'PUT':
        return update(payload)
    elif event['httpMethod'] == 'DELETE':
        return {
            'statusCode': 501,
            'body': "Not Implemented"
        }
    else:
        return {
            'statusCode': 405,
            'body': "Method Not Allowed"
        }
    
def create(payload):
    try:
        
        start_utc = payload["StartUTC"]
        end_utc = payload["EndUTC"]
        subject = payload["Subject"]
        organizer = payload["Organizer"]
        categories = payload["Categories"]
        required_attendees = payload["RequiredAttendees"] 
        optional_attendees = payload["OptionalAttendees"]
        
        body = {
            "summary": subject, 
            "description": generate_description(subject, organizer, required_attendees, optional_attendees, categories),
            "start": {"dateTime": start_utc, "timeZone": 'UTC'}, 
            "end": {"dateTime": end_utc, "timeZone": 'UTC'}
        }
                
    except Exception as e:
        print(e)
        return {
            'statusCode': 412,
            'body': "Invalid Payload"
        }

    service = create_service(get_service_account_credentials())
    event = service.events().insert(calendarId=CALENDAR_ID, body=body).execute()

    return {
        'statusCode': 200,
        'body': json.dumps(event)
    }
    
    
    
def update(payload):
    try:
        
        entry_id = payload["EntryID"]
        start_utc = payload["StartUTC"]
        end_utc = payload["EndUTC"]
        subject = payload["Subject"]
        organizer = payload["Organizer"]
        categories = payload["Categories"]
        required_attendees = payload["RequiredAttendees"] 
        optional_attendees = payload["OptionalAttendees"]
        
        body = {
            "eventId": entry_id,
            "summary": subject, 
            "description": generate_description(subject, organizer, required_attendees, optional_attendees, categories),
            "start": {"dateTime": start_utc, "timeZone": 'UTC'}, 
            "end": {"dateTime": end_utc, "timeZone": 'UTC'}
        }
                
    except Exception as e:
        print(e)
        return {
            'statusCode': 412,
            'body': "Invalid Payload"
        }

    service = create_service(get_service_account_credentials())
    event = service.events().update(calendarId=CALENDAR_ID, eventId=entry_id, body=body).execute()

    return {
        'statusCode': 200,
        'body': json.dumps(event)
    }

def create_service(credentials):
    credentials = service_account.Credentials.from_service_account_info(credentials, scopes=SCOPES)
    service = build('calendar', 'v3', credentials=credentials)
    return service

#Get credentials from env 
def get_service_account_credentials():
    return {
        "type": os.environ['type'],
        "project_id": os.environ['project_id'],
        "private_key_id": os.environ['private_key_id'],
        "private_key": os.environ['private_key'].replace('\\n', '\n'),
        "client_email": os.environ['client_email'],
        "client_id": os.environ['client_id'],
        "auth_uri": os.environ['auth_uri'],
        "token_uri": os.environ['token_uri'],
        "auth_provider_x509_cert_url": os.environ['auth_provider_x509_cert_url'],
        "client_x509_cert_url": os.environ['client_x509_cert_url']
    }

def generate_description(subject, organizer, required_attendees, optional_attendees, categories):
    
    txt = f"<b>{subject}</b>\n<b>Organizer:</b> {organizer}\n"
    
    if len(categories.strip()) > 0:
        txt += f"\n<b>Categories:</b>\n"
    
    tmp = categories.split(";")
    for i in tmp:
        if len(i.strip()) == 0:
            continue
        txt += f"{i.strip()}\n"
    
    txt += "\n<b>RequiredAttendees:</b></n>"
    
    tmp = required_attendees.split(";")    
    for i in tmp:
        if len(i.strip()) == 0:
            continue
        txt += f"{i.strip()}\n"
    
    if len(optional_attendees.strip()) > 0:
        txt += f"\n<b>OptionalAttendees</b>: \n"
    
    tmp = optional_attendees.split(";")    
    for i in tmp:
        if len(i.strip()) == 0:
            continue
        txt += f"{i.strip()}\n"
    
    return txt

if __name__ == '__main__':
    
    event = {
        "httpMethod": "PUT",
        "body": '''{
        "EntryID":  "kevffela3sdhq95r79964j228g",
        "LastModificationTime":  "2021-11-24T03:17:25Z",
        "StartUTC":  "2021-11-24T08:00:00Z",
        "Duration":  60,
        "EndUTC":  "2021-11-24T09:00:00Z",
        "Categories":  "Cat1; Cat2",
        "Subject":  "Walk through the CR22 R1893 timelines - updated",
        "IsRecurring":  false,
        "Organizer":  "Kettle, Mark",
        "RequiredAttendees":  "Kettle, Mark; Malik, Ashar; Karmanov, Igor; Woods, Mike; Geldrez, Valentina; Khazin, Vladimir; Dossani, Hiren; Wu, Bo",
        "OptionalAttendees":  ""
    }'''}
    
    print(lambda_handler(event, None))