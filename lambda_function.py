from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime, timedelta
import json
import os

SCOPES = ['https://www.googleapis.com/auth/calendar']
CALENDAR_ID = os.environ['calendar_id']

def lambda_handler(event, context):
    
    #print("## event: " + json.dumps(event))
    
    try:
        payload = json.loads(event['body'])
    except Exception as e:
        print(e)
        return {
            'statusCode': 412,
            'body': "Invalid event body or url parameter"
        }
    
    try:
        for e in payload:
            update(e)
            
        delete(payload)
        
    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': str(e)
        }
    
    return {
        'statusCode': 200,
        'body': "Created"
    }
    
def create(event):
    try:
        
        print("Inserting: " + event["Subject"])
        
        entry_id = event["EntryID"]
        start_utc = event["StartUTC"]
        end_utc = event["EndUTC"]
        subject = event["Subject"]
        organizer = event["Organizer"]
        categories = event["Categories"]
        required_attendees = event["RequiredAttendees"] 
        optional_attendees = event["OptionalAttendees"]
        
        body = {
            "id": entry_id,
            "summary": subject, 
            "description": generate_description(subject, organizer, required_attendees, optional_attendees, categories),
            "start": {"dateTime": start_utc, "timeZone": 'UTC'}, 
            "end": {"dateTime": end_utc, "timeZone": 'UTC'}
        }
        
        service = create_service(get_service_account_credentials())
        event = service.events().insert(calendarId=CALENDAR_ID, body=body).execute()

    except Exception as e:
        print(e)
        raise ValueError('Error creating ' + event["Subject"])
        return False

    return True
    
    
    
def update(payload):
    try:
        print("Updating: " + payload["Subject"])
        
        entry_id = payload["EntryID"]
        start_utc = payload["StartUTC"]
        end_utc = payload["EndUTC"]
        subject = payload["Subject"]
        organizer = payload["Organizer"]
        categories = payload["Categories"]
        required_attendees = payload["RequiredAttendees"] 
        optional_attendees = payload["OptionalAttendees"]
        
        body = {
            "id": entry_id,
            "summary": subject, 
            "description": generate_description(subject, organizer, required_attendees, optional_attendees, categories),
            "start": {"dateTime": start_utc, "timeZone": 'UTC'}, 
            "end": {"dateTime": end_utc, "timeZone": 'UTC'}
        }
                
    except Exception as e:
        print(e)
        raise ValueError('Error updating ' + event["Subject"])
        return False

    try:
        service = create_service(get_service_account_credentials())
        event = service.events().update(calendarId=CALENDAR_ID, eventId=entry_id, body=body).execute()
    except Exception as e:
        
        status_code = json.loads(e.content)['error']['code']
        msg = json.loads(e.content)['error']['message']
        
        print(f"{status_code} - {msg}")
        
        if status_code == 404:
            return create(payload)
        
        print(e)
        raise ValueError('Error updating ' + event["Subject"])
        return False

    return True

def get_ids_from_day(day):
    
    start = day[0:day.find("T")] + 'T00:00:00Z'
    end = day[0:day.find("T")] + 'T23:59:59Z'
    
    service = create_service(get_service_account_credentials())
    events_result = service.events().list(calendarId=CALENDAR_ID, timeMin=start, timeMax=end).execute()
    events = events_result.get('items', [])
    
    l = []
    
    for e in events:
        l.append(e['id'])

    return l

def get_ids_from_payload(payload):
    
    l = []
    
    for e in payload:
        l.append(e["EntryID"])

    return l

def delete(payload):
    
    tmp = payload[0]["StartUTC"]
    
    ids_calendar = get_ids_from_day(tmp)
    ids_payload = get_ids_from_payload(payload)
    
    try:
        service = create_service(get_service_account_credentials())
        tmp = ''
        
        for i in ids_calendar:
            tmp = i
            if i not in ids_payload:
                print(f"Delete: {i}")
                event = service.events().delete(calendarId=CALENDAR_ID, eventId=i).execute()
    
    except Exception as e:
        print(e)
        raise ValueError('Error deleting ' + tmp)
        return False

    return True

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
        "httpMethod": "POST",
        "body": '''[
            {
                "EntryID":  "d3dph21v3b59a97ohnn1p8mc582",
                "LastModificationTime":  "2021-11-24T03:17:25Z",
                "StartUTC":  "2021-11-25T08:00:00Z",
                "Duration":  60,
                "EndUTC":  "2021-11-25T09:00:00Z",
                "Categories":  "Cat1; Cat2",
                "Subject":  "2. Walk through the CR22 R1893 timelines - updated",
                "IsRecurring":  false,
                "Organizer":  "Kettle, Mark",
                "RequiredAttendees":  "Kettle, Mark; Malik, Ashar; Karmanov, Igor; Woods, Mike; Geldrez, Valentina; Khazin, Vladimir; Dossani, Hiren; Wu, Bo",
                "OptionalAttendees":  ""
            }
        ]'''}
    
    print(lambda_handler(event, None))