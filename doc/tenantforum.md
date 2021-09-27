# ComCat Marketplace

## Listing visible topics
 `GET` `/tenantforum/topic`
### Response
`Accept: application/json`

```JSON
[
	{
		"id": <int:id>,
		"user": <int:user_id>,
		"title": <str:title>,
		"text": <str:text>,
		"visibility": <str:"tenement"|"customer">,
		"created": <str:datetime_iso_str>,
		"edited": <str|null:datetime_iso_str>
	},
	...
]
```

## Listing own topics
 `GET` `/tenantforum/topic/own`
### Response
`Accept: application/json`

```JSON
[
	{
		"id": <int:id>,
		"user": <int:user_id>,
		"title": <str:title>,
		"text": <str:text>,
		"visibility": <str:"tenement"|"customer">,
		"created": <str:datetime_iso_str>,
		"edited": <str|null:datetime_iso_str>
	},
	...
]
```

## Listing responses to a topic
 `GET` `/tenantforum/response/<int:topic_id>`
### Response
`Accept: application/json`

```JSON
[
	{
		"id": <int:id>,
		"user": <int:user_id>,
		"topic": <int:topic_id>,
		"text": <str:text>,	
		"created": <str:datetime_iso_str>,
		"edited": <str|null:datetime_iso_str>
	},
	...
]
```

## Listing own responses
 `GET` `/tenantforum/response/own`
### Response
`Accept: application/json`

```JSON
[
	{
		"id": <int:id>,
		"user": <int:user_id>,
		"topic": <int:topic_id>,
		"text": <str:text>,	
		"created": <str:datetime_iso_str>,
		"edited": <str|null:datetime_iso_str>
	},
	...
]
```

## Adding a topic
 `POST` `/tenantforum/topic`
### Payload
`Content-Type: application/json`

```JSON
{
	"title": <str:title>,
	"text": <str:text>,
	"visibility": <str:"tenement"|"customer">
}
```
#### Success
```JSON
{
	"message": <str:message>,
	"id": <int:topic_id>
}
```

## Adding a response
 `POST` `/tenantforum/response`
### Payload
`Content-Type: application/json`

```JSON
{
	"topic": <int:topic_id>,
	"text": <str|null:text>
}
```
#### Success
```JSON
{
	"message": <str:message>,
	"id": <int:reponse_id>
}
```

## Edit a topic
 `PATCH` `/tenantforum/topic/<int:topic_id>`
### Payload
`Content-Type: application/json`

```JSON
{
	"title": <str:text>,
	"text": <str:text>
}
```
#### Success
```JSON
{
	"message": <str:message>
}
```

## Edit a response
 `PATCH` `/tenantforum/response/<int:response_id>`
### Payload
`Content-Type: application/json`

```JSON
{
	"text": <str:text>
}
```
#### Success
```JSON
{
	"message": <str:message>
}
```

## Delete a topic
 `DELETE` `/tenantforum/topic/<int:topic_id>`
#### Success
```JSON
{
	"message": <str:message>
}
```

## Delete (empty) a response
 `DELETE` `/tenantforum/response/<int:response_id>`
#### Success
```JSON
{
	"message": <str:message>
}
```