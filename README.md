# lambda-calendar-integration

Lambda function to google calendar integration

## POST

Create a new Event.

Request Body:

```
{
    "StartUTC":  "2021-11-24T08:00:00Z",
    "EndUTC":  "2021-11-24T09:00:00Z",
    "Categories":  "Cat1; Cat2",
    "Subject":  "Walk through the CR22 R1893 timelines - updated",
    "IsRecurring":  false,
    "Organizer":  "Kettle, Mark",
    "RequiredAttendees":  "Kettle, Mark; Malik, Ashar; Karmanov, Igor; Woods, Mike; Geldrez, Valentina; Khazin, Vladimir; Dossani, Hiren; Wu, Bo",
    "OptionalAttendees":  ""
}
```

Response: Created Google Calendar event object

## PUT

Update a given EntryID event.


Request Body:

```
{
    "EntryID":  "d3dph21v3b59a97ohnn1p8mc58",
    "StartUTC":  "2021-11-24T08:00:00Z",
    "EndUTC":  "2021-11-24T09:00:00Z",
    "Categories":  "Cat1; Cat2",
    "Subject":  "Walk through the CR22 R1893 timelines - updated",
    "IsRecurring":  false,
    "Organizer":  "Kettle, Mark",
    "RequiredAttendees":  "Kettle, Mark; Malik, Ashar; Karmanov, Igor; Woods, Mike; Geldrez, Valentina; Khazin, Vladimir; Dossani, Hiren; Wu, Bo",
    "OptionalAttendees":  ""
}
```

Response: Updated Google Calendar event object


## DELETE /{id}

Delete the event with the given id 
