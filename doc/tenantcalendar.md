# tenantcalendar
A tenant-oriented calendar for ComCat

## List events
`GET` `/tenantcalendar`
### Response
`Accept: application/json`

```JSON
[
	{
		"id": <int:event_id>,
		"user": <int:user_id>,
		"title": <str[30]:event_title>,
		"email": <str[64]|null:email_address>,
		"phone": <str[64]|null:phone_number>,
		"start": <str(ISO 8601):start_of_event>,
		"end": <str(ISO 8601):end_of_event>,
		"text": <str:event_text>
	},
	...
]
```

## Add an event
`GET` `/tenantcalendar`
### Payload
`Content-Type: application/json`

```JSON
{
	"title": <str[30]:event_title>,
	"email": <str[64]|null:email_address>,
	"phone": <str[64]|null:phone_number>,
	"start": <str(ISO 8601):start_of_event>,
	"end": <str(ISO 8601):end_of_event>,
	"text": <str:event_text>
}
```
Of `email` and `phone`, at least one has to be not-`null`.
### Response
`Accept: application/json`

```JSON
{
	"message": <str:message>
	"id": <int:event_id>
}
```

## Modify an event
`PATCH` `/tenantcalendar/<int:id>`
### Payload
`Content-Type: application/json`

```JSON
{
	"title": <str[30]:event_title>,
	"email": <str[64]|null:email_address>,
	"phone": <str[64]|null:phone_number>,
	"start": <str(ISO 8601):start_of_event>,
	"end": <str(ISO 8601):end_of_event>,
	"text": <str:event_text>
}
```
All fields are optional here.
Missing fields will not be changed.

### Response
`Accept: application/json`

```JSON
{
	"message": <str:message>
}
```

## Delete an event
`DELETE` `/tenantcalendar/<int:id>`

### Response
`Accept: application/json`

```JSON
{
	"message": <str:message>
}
```