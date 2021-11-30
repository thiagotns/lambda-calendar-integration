# lambda-calendar-integration

Lambda function to google calendar integration. 

Insert, update or delete events according to the payload. 

Receives events for one day at a time. 

Accept only POST requests.

## Payload

```
[
    {
        "EntryID":  "d3dph21v3b59a97ohnn1p8mc581",
        "StartUTC":  "2021-11-25T08:00:00Z",
        "EndUTC":  "2021-11-25T09:00:00Z",
        "Categories":  "Cat1; Cat2",
        "Subject":  "A WALK through the CR22 R1893 timelines - updated",
        "Organizer":  "Kettle, Mark",
        "RequiredAttendees":  "Kettle, Mark; Malik, Ashar; Karmanov, Igor; Woods, Mike; Geldrez, Valentina; Khazin, Vladimir; Dossani, Hiren; Wu, Bo",
        "OptionalAttendees":  ""
    },
    {
        "EntryID":  "d3dph21v3b59a97ohnn1p8mc582",
        "StartUTC":  "2021-11-25T08:00:00Z",
        "EndUTC":  "2021-11-25T09:00:00Z",
        "Categories":  "Cat1; Cat2",
        "Subject":  "B WALK through the CR22 R1893 timelines - updated",
        "Organizer":  "Kettle, Mark",
        "RequiredAttendees":  "Kettle, Mark; Malik, Ashar; Karmanov, Igor; Woods, Mike; Geldrez, Valentina; Khazin, Vladimir; Dossani, Hiren; Wu, Bo",
        "OptionalAttendees":  ""
    },
    {
        "EntryID":  "d3dph21v3b59a97ohnn1p8mc583",
        "StartUTC":  "2021-11-25T08:00:00Z",
        "EndUTC":  "2021-11-25T09:00:00Z",
        "Categories":  "Cat1; Cat2",
        "Subject":  "C WALK through the CR22 R1893 timelines - updated",
        "Organizer":  "Kettle, Mark",
        "RequiredAttendees":  "Kettle, Mark; Malik, Ashar; Karmanov, Igor; Woods, Mike; Geldrez, Valentina; Khazin, Vladimir; Dossani, Hiren; Wu, Bo",
        "OptionalAttendees":  ""
    }
]
```

## Install 

Create a AWS lambda function, create a layer with "layer.zip" and deploy "lambda_function.py".
Go to GCP console, create a app and enable a API https://developers.google.com/workspace/guides/create-project
Create a GCP Service Account and download the credentials https://developers.google.com/workspace/guides/create-credentials#create_a_service_account
Create this AWS lambda Environment variables and set them with GCP credentials :
```
type
project_id
private_key_id
private_key
client_email
client_id
auth_uri
token_uri
auth_provider_x509_cert_url
client_x509_cert_url
```

Create a lambda Environment to set the calendar id:
```
calendar_id = "teste..."
```

Create a API Gateway (REST), integrate with the lambda and create a POST resource.

Create a API key and a Usage Plan and configure the POST resource to require a API Key.

