# ComCat Local Public Transport (LPT) module

## Retrieve departures for the stops near the tenement.
`GET` `/lpt/home`
### Response
`Accept: application/json`

```JSON
{
    "source": <str:source_id>,
    "stops": [
        {
	        "id": <str:stop_id>,
            "name": <str:stop_name>,
            "geo": [<float:latitude>, <float:longitude>],
            "departures": [
                {
                    "type": <str:public_transport_type>,
                    "line": <str:line_name_or_number>,
                    "destination": <str:destination>,
                    "scheduled": <str:scheduled_departure>,
                    "estimated": <str|null:estimaed_departure>
                },
                ...
            ]
        },
        ...
    ]
}
```
The fields `scheduled` and `estimated` contain ISO datetimes if not `null`.

## Retrieve departures for the stops near given geo coordinates
`POST` `/lpt/current`
### Payload
`Content-Type: application/json`

```JSON
{
	"latitude": <float:latitude>,
	"longitude": <float:longitude>
}
```
### Response
See above.
