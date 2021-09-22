# ComCat Marketplace

## Listing offers
 `GET` `/marketplace`
### Response
`Accept: application/json`

```JSON
[
	{
		"id": <int:id>,
		"user": <int:user_id>,
		"title": <str:title>,
		"description": <str:description>,
		"price": <int:price_in_EUR>,
		"email": <str|null:email_address>,
		"phone": <str|null:phone_number>,
		"images": [<int:image_id>, ...]
	},
	...
]
```

## Retrieving a single offer
 `GET` `/marketplace/<int:id>`
### Response
`Accept: application/json`

```JSON
{
	"id": <int:id>,
	"user": <int:user_id>,
	"title": <str:title>,
	"description": <str:description>,
	"price": <int:price_in_EUR>,
	"email": <str|null:email_address>,
	"phone": <str|null:phone_number>,
	"images": [<int:image_id>, ...]
}
```

## Adding an offer
 `POST` `/marketplace`
### Payload
`Content-Type: application/json`

```JSON
{
	"title": <str:title>,
	"description": <str:description>,
	"price": <int:price_in_EUR>,
	"email": <str|null:email_address>,
	"phone": <str|null:phone_number>
}
```
Of `email` and `phone` at least one has to be set.

### Response
`Accept: application/json`
#### Success
```JSON
{
	"message": <str:message>,
	"id": <int:offer_id>
}
```
#### Error
```JSON
{
	"message": <str:message>
}
```

## Deleting an offer
 `DELETE` `/marketplace/<int:id>`
### Response
`Accept: application/json`

```JSON
{
	"message": <str:message>
}
```

## Getting an image
 `GET` `/marketplace/image/<int:image_id>`
### Response
`Accept: <image/*>`

## Adding an image
 `POST` `/marketplace/<int:offer_id>/image/<int:image_sort_index>`
### Payload
`Content-Type: <*/*>`
### Response
`Accept: application/json`

```JSON
{
	"message": <str:message>,
	"id": <int:image_id>
}
```
There can be at most 4 images per offer.
The size of a single image is limited to 3 MiB

## Deleting an image
 `DELETE` `/marketplace/<image/<int:image_id>`
### Response
`Accept: application/json`

```JSON
{
	"message": <str:message>
}
```