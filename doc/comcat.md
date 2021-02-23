# Authorization Server

## Boundaries

* Token endpoint auth method: `client_secret_post`
* Allowed redirect URLs:
  - `https://comcat.homeinfo.de/oauth/authorize`
  - `https://comcat.homeinfo.de/oauth/token`
  - `de.homeinfo.comcat://auth`
  - `de.homeinfo.comcat://token`
* Allowed grant types:
  - `authorization_code`
  - `refresh_token`
* Allowed response types:
  - `code`
  - `token`
* Allowed scopes: `comcat`

## Client registrieren

`POST` `https://comcat.homeinfo.de/client`

### Beispieldatensatz
Accept: `application/json`

    {
      "id": <int:user_id>,
      "passwd": <str:user_password>
    }

### Beispielantwort
Content-Type: `application/json`

    {
      "id": <int:client_database_id>,
      "client_id": <str:client_oauth_id>,
      ...
      "clientSecret": <str:client_secret>,
      "authorizationNonce": <str:authorization_nonce>
    }

## Access Token beziehen

`POST` `https://comcat.homeinfo.de/authorize`

### Zu sendende Daten
Accept: `application/x-www-form-urlencoded`

Gem. OAuth 2.0 Protokoll zzgl. `nonce` aus o.g. Anfrage.

## Weitere OAuth Endpoints

Gemäß [rfc6749](https://tools.ietf.org/html/rfc6749) und [rfc8252](https://tools.ietf.org/html/rfc8252).

* `POST` https://comcat.homeinfo.de/oauth/token
* `POST` https://comcat.homeinfo.de/oauth/revoke
* `POST` https://comcat.homeinfo.de/oauth/introspect

# Resource Providers

## Charts
Über die Charts-Schnittstelle werden die sog. *Charts* abgefragt.
Dabei handelt es sich um Darstellungseinheiten analog zu Folien einer Präsentation.

### Abfragen
`GET` `https://comcat.homeinfo.de/charts`


#### Beispielantwort
Content-Type: `application/json`

	[
	  {
		"titleColor": 0,
		"fontSize": 24,
		"kenBurns": false,
		"title": "Abdunkelung Digitale Bretter",
		"id": 71,
		"randomImage": false,
		"base": {
		  "transition": "fade-in",
		  "duration": 10,
		  "id": 95,
		  "created": "2018-06-22T13:18:05",
		  "uuid": "5fad5a8baace458095ad2ddbc2dbf7fb",
		  "customer": 1030020,
		  "trashed": true,
		  "log": false,
		  "title": "Abdunkelung Digi-Bretter",
		  "pins": [],
		  "menus": []
		},
		"type": "ImageText",
		"texts": [
		  {
		    "id": 33,
		    "chart": 71,
		    "text": "Sehr geehrte Mieter,<br>\n<br>\ndie Digitalen Bretter erhalten einen \u201eBildschirmschoner\u201c, d. h. nach f\u00fcnf Minuten Inaktivit\u00e4t dunkelt der Bildschirm leicht ab.<br>\nTrotz der Abdunkelung sind alle Informationen und Touch-Felder zu sehen und zu lesen.<br>\n<br>\nSobald der Bildschirm ber\u00fchrt wird, hellt dieser wieder auf.<br>\nDie Helligkeit wird im Zuge der Umstellung zus\u00e4tzlich von 100 % auf 90 % reduziert.<br>\n<br>\nWir w\u00fcnschen Ihnen weiterhin gute Informationen.<br>\n<br>\nWohnungsgenossenschaft<br>\nKleefeld-Buchholz eG"
		  }
		],
		"images": [
		  {
		    "id": 112,
		    "mimetype": "image/jpeg",
		    "sha256sum": "d5238686e861ffd24eb5a7889a261abed1c9e2bb9da9741ca86e45c66931bd35",
		    "size": 20394,
		    "created": "2018-05-29T16:26:26",
		    "lastAccess": "2019-11-20T01:37:34",
		    "accessed": 627860,
		    "name": "news_default.jpg",
		    "index": 0
		  }
		]
	  }
	]

## Schadensmeldungen
Über diese Schnittstelle können Schadensmeldungen abgefragt und eingestellt werden.

### Liste abfragen
`GET` `https://comcat.homeinfo.de/damage-report`

#### Beispielantwort
Content-Type: `application/json`

	[
	  {
		"contact": "2356529",
		"id": 4,
		"name": "leidenheimer",
		"timestamp": "2017-09-05T15:10:20",
		"customer": 1030020,
		"message": "fernseh HD empfang gest\u00f6rt.",
		"address": {
		  "zipCode": "30625",
		  "city": "Hannover",
		  "street": "Berckhusenstr.",
		  "houseNumber": "57",
		  "id": 482
		},
		"damageType": "Sonstiges",
		"checked": true,
		"attachments": []
	  }
	]

### Einzelne Schadensmeldung abfragen
`GET` `https://comcat.homeinfo.de/damage_report/<int:report_id>`

#### Beispielantwort
Content-Type: `application/json`

	{
	  "contact": "2356529",
	  "id": 4,
	  "name": "leidenheimer",
	  "timestamp": "2017-09-05T15:10:20",
	  "customer": 1030020,
	  "message": "fernseh HD empfang gest\u00f6rt.",
	  "address": {
		"zipCode": "30625",
		"city": "Hannover",
		"street": "Berckhusenstr.",
		"houseNumber": "57",
		"id": 482
	  },
	  "damageType": "Sonstiges",
	  "checked": true,
	  "attachments": [
        1,
        2,
        3
      ]
	}

### Schadensmeldung übermitteln
`POST` `https://comcat.homeinfo.de/damage_report`

#### Beispieldatensatz
Accept: `application/json`

	{
	  "message": <str:nachrichtentext>,
	  "name": <str:name>,
	  "contact": <str,optional:e_mail_addresse>,
	  "damage_type": <str:typ_des_schadens>
	}

#### Beispielantwort
Content-Type: `application/json`

	{
	  "message": "Damage report submitted."
	}

### Schadensmeldung löschen
`DELETE` `https://comcat.homeinfo.de/damage_report/<int:report_id>`

### Anhang zur Schadensmeldung hinzufügen
`POST` `https://comcat.homeinfo.de/damage_report/attachment`

#### Beispieldatensatz
Accept: `application/json`

{
  "userDamageReport": <int:user_damage_report_id>,
  "file": <int:user_file_id>
}

#### Beispielantwort
Content-Type: `application/json`

	{
	  "message": "Attachment added.",
	  "id": <int:attachment_id>
	}

### Anhang von Schadensmeldung entfernen
`DELETE` `https://comcat.homeinfo.de/damage_report/attachment/<int:attachment_id>`

## Lokalnachrichten
Mit dieser Schnittstelle können Lokalnachrichten abgerufen werden.

### Liste von Lokalnachrichten abfragen
`GET` `https://comcat.homeinfo.de/local-news`

#### Beispielantwort
Content-Type: `application/json`

	[
	  {
		"created": "2018-02-06T12:23:00",
		"text": "Um gr\u00f6\u00dferen Problemen mit eingefrorenen Wasser- und Heizungsleitungen entgegenzuwirken, gibt es einige Ratschl\u00e4ge. Von Vorteil ist es, Au\u00dfent\u00fcren und Fenster bei Frost geschlossen zu lassen und die Zimmertemperatur durch Heizen konstant zu halten.<br />\nGrunds\u00e4tzlich gilt, wenn eine Wasserleitung eingefroren ist, nur vom Fachmann auftauen lassen. Die Bereitschaftsdienste sind rund um die Uhr zu erreichen.",
		"source": "http://www.nw.de/lokal/bielefeld/mitte/22051187_Auf-Bielefeld-kommt-Dauerfrost-zu-Stadtwerke-geben-Tipps.html",
		"title": "Der richtige Frostschutz vor dem Dauerfrost ",
		"id": 71,
		"activeFrom": "2018-02-06",
		"activeUntil": "2018-02-14",
		"images": [
		  {
		    "uploaded": "2018-02-06T12:23:01",
		    "id": 92,
		    "source": "https://pixabay.com/de/eis-winter-frost-winterlich-2435657/",
		    "mimetype": "image/jpeg"
		  }
		],
		"tags": [
		  "Aktuelles",
		  "Bielefeld",
		  "Deutschland",
		  "Hannover",
		  "Winter",
		  "Wohnen"
		]
	  }
	]

### Einzelne Lokalnachricht abfragen
`GET` `https://comcat.homeinfo.de/local-news/<int:article_id>`

#### Beispielantwort
Content-Type: `application/json`

	{
	  "created": "2018-02-06T12:23:00",
	  "text": "Um gr\u00f6\u00dferen Problemen mit eingefrorenen Wasser- und Heizungsleitungen entgegenzuwirken, gibt es einige Ratschl\u00e4ge. Von Vorteil ist es, Au\u00dfent\u00fcren und Fenster bei Frost geschlossen zu lassen und die Zimmertemperatur durch Heizen konstant zu halten.<br />\nGrunds\u00e4tzlich gilt, wenn eine Wasserleitung eingefroren ist, nur vom Fachmann auftauen lassen. Die Bereitschaftsdienste sind rund um die Uhr zu erreichen.",
	  "source": "http://www.nw.de/lokal/bielefeld/mitte/22051187_Auf-Bielefeld-kommt-Dauerfrost-zu-Stadtwerke-geben-Tipps.html",
	  "title": "Der richtige Frostschutz vor dem Dauerfrost ",
	  "id": 71,
	  "activeFrom": "2018-02-06",
	  "activeUntil": "2018-02-14",
	  "images": [
		{
		  "uploaded": "2018-02-06T12:23:01",
		  "id": 92,
		  "source": "https://pixabay.com/de/eis-winter-frost-winterlich-2435657/",
		  "mimetype": "image/jpeg"
		}
	  ],
	  "tags": [
		"Aktuelles",
		"Bielefeld",
		"Deutschland",
		"Hannover",
		"Winter",
		"Wohnen"
	  ]
	}

### Artikelbild abfragen
`GET` `https://comcat.homeinfo.de/local-news/image/<int:image_id>`

Content-Type: Abhängig vom Bild-Typ. Z.B.: `image/png`

## ÖPNV
Die *ÖPNV* Schnittstelle dient der Abfrage von Fahrplaninformationen für öffentliche Verkehrsmittel.

### Abfragen von Fahrplaninformationen
`GET` `https://comcat.homeinfo.de/lpt`

#### Beispielantwort
Content-Type: `application/json`

	{
	  "source": "EFA",
	  "stops": [
		{
		  "id": "de:03241:211",
		  "name": "Hannover Christuskirche",
		  "latitude": 52.38176,
		  "longitude": 9.72591,
		  "departures": [
		    {
		      "type": "Stadtbahn",
		      "line": "6",
		      "destination": "Messe/Ost(EXPO-Plaza)",
		      "scheduled": "2021-02-04T14:00:00",
		      "estimated": null
		    },
		    {
		      "type": "Stadtbahn",
		      "line": "11",
		      "destination": "Hannover/Haltenhoffstra\u00dfe",
		      "scheduled": "2021-02-04T14:02:00",
		      "estimated": null
		    },
		    {
		      "type": "Stadtbahn",
		      "line": "11",
		      "destination": "Hannover/Zoo",
		      "scheduled": "2021-02-04T14:05:00",
		      "estimated": null
		    },
		    {
		      "type": "Stadtbahn",
		      "line": "6",
		      "destination": "Hannover/Nordhafen",
		      "scheduled": "2021-02-04T14:07:00",
		      "estimated": null
		    },
		    {
		      "type": "Bus",
		      "line": "200",
		      "destination": "Hannover August-Holweg-Platz",
		      "scheduled": "2021-02-04T14:09:00",
		      "estimated": null
		    },
		    {
		      "type": "Bus",
		      "line": "100",
		      "destination": "Hannover August-Holweg-Platz",
		      "scheduled": "2021-02-04T14:09:00",
		      "estimated": null
		    },
		    {
		      "type": "Stadtbahn",
		      "line": "6",
		      "destination": "Messe/Ost(EXPO-Plaza)",
		      "scheduled": "2021-02-04T14:10:00",
		      "estimated": null
		    },
		    {
		      "type": "Stadtbahn",
		      "line": "11",
		      "destination": "Hannover/Haltenhoffstra\u00dfe",
		      "scheduled": "2021-02-04T14:12:00",
		      "estimated": null
		    },
		    {
		      "type": "Stadtbahn",
		      "line": "11",
		      "destination": "Hannover/Zoo",
		      "scheduled": "2021-02-04T14:15:00",
		      "estimated": null
		    },
		    {
		      "type": "Stadtbahn",
		      "line": "6",
		      "destination": "Hannover/Nordhafen",
		      "scheduled": "2021-02-04T14:17:00",
		      "estimated": null
		    }
		  ]
		},
		{
		  "id": "de:03241:219",
		  "name": "Hannover Lilienstra\u00dfe",
		  "latitude": 52.38475,
		  "longitude": 9.72478,
		  "departures": [
		    {
		      "type": "Bus",
		      "line": "100",
		      "destination": "Hannover August-Holweg-Platz",
		      "scheduled": "2021-02-04T14:00:00",
		      "estimated": null
		    },
		    {
		      "type": "Bus",
		      "line": "200",
		      "destination": "Hannover August-Holweg-Platz",
		      "scheduled": "2021-02-04T14:07:00",
		      "estimated": null
		    },
		    {
		      "type": "Bus",
		      "line": "100",
		      "destination": "Hannover August-Holweg-Platz",
		      "scheduled": "2021-02-04T14:10:00",
		      "estimated": null
		    },
		    {
		      "type": "Bus",
		      "line": "200",
		      "destination": "Hannover August-Holweg-Platz",
		      "scheduled": "2021-02-04T14:17:00",
		      "estimated": null
		    },
		    {
		      "type": "Bus",
		      "line": "100",
		      "destination": "Hannover August-Holweg-Platz",
		      "scheduled": "2021-02-04T14:20:00",
		      "estimated": null
		    },
		    {
		      "type": "Bus",
		      "line": "200",
		      "destination": "Hannover August-Holweg-Platz",
		      "scheduled": "2021-02-04T14:27:00",
		      "estimated": null
		    },
		    {
		      "type": "Bus",
		      "line": "100",
		      "destination": "Hannover August-Holweg-Platz",
		      "scheduled": "2021-02-04T14:30:00",
		      "estimated": null
		    },
		    {
		      "type": "Bus",
		      "line": "200",
		      "destination": "Hannover August-Holweg-Platz",
		      "scheduled": "2021-02-04T14:37:00",
		      "estimated": null
		    },
		    {
		      "type": "Bus",
		      "line": "100",
		      "destination": "Hannover August-Holweg-Platz",
		      "scheduled": "2021-02-04T14:40:00",
		      "estimated": null
		    },
		    {
		      "type": "Bus",
		      "line": "200",
		      "destination": "Hannover August-Holweg-Platz",
		      "scheduled": "2021-02-04T14:47:00",
		      "estimated": null
		    }
		  ]
		},
		{
		  "id": "de:03241:161",
		  "name": "Hannover K\u00f6nigsworther Platz",
		  "latitude": 52.37825,
		  "longitude": 9.72274,
		  "departures": [
		    {
		      "type": "Stadtbahn",
		      "line": "4",
		      "destination": "Garbsen",
		      "scheduled": "2021-02-04T14:00:00",
		      "estimated": null
		    },
		    {
		      "type": "Bus",
		      "line": "200",
		      "destination": "Hannover August-Holweg-Platz",
		      "scheduled": "2021-02-04T14:01:00",
		      "estimated": null
		    },
		    {
		      "type": "Stadtbahn",
		      "line": "4",
		      "destination": "Hannover/Roderbruch",
		      "scheduled": "2021-02-04T14:03:00",
		      "estimated": null
		    },
		    {
		      "type": "Stadtbahn",
		      "line": "5",
		      "destination": "St\u00f6cken",
		      "scheduled": "2021-02-04T14:04:00",
		      "estimated": null
		    },
		    {
		      "type": "Stadtbahn",
		      "line": "5",
		      "destination": "Anderten",
		      "scheduled": "2021-02-04T14:07:00",
		      "estimated": null
		    },
		    {
		      "type": "Bus",
		      "line": "100",
		      "destination": "Hannover August-Holweg-Platz",
		      "scheduled": "2021-02-04T14:07:00",
		      "estimated": null
		    },
		    {
		      "type": "Stadtbahn",
		      "line": "4",
		      "destination": "Garbsen",
		      "scheduled": "2021-02-04T14:10:00",
		      "estimated": null
		    },
		    {
		      "type": "Bus",
		      "line": "200",
		      "destination": "Hannover August-Holweg-Platz",
		      "scheduled": "2021-02-04T14:11:00",
		      "estimated": null
		    },
		    {
		      "type": "Stadtbahn",
		      "line": "4",
		      "destination": "Hannover/Roderbruch",
		      "scheduled": "2021-02-04T14:13:00",
		      "estimated": null
		    },
		    {
		      "type": "Stadtbahn",
		      "line": "5",
		      "destination": "St\u00f6cken",
		      "scheduled": "2021-02-04T14:14:00",
		      "estimated": null
		    }
		  ]
		}
	  ]
	}

## QR Code generieren
Diese Schnittstelle dient dem Generieren von QR Codes für Mobilgeräte.

**VORSICHT**: Das Generieren eines neuen QR Codes generiert auch ein neues Passwort für den entsprechenden Benutzer!

### QR Code generieren
`GET` `https://comcat.homeinfo.de/init/qrcode`

Content-Type: Vom angefragten Bildformat abhängig. Standardmäßig `image/png`

## Assoziierte Dateien
Diese Schnittstelle dient dazu, assoziierte Dateien, z.B. für die Charts abzufragen.

### Dateien abfragen
`GET` `https://comcat.homeinfo.de/related-file/<int:ident>`

Content-Type: Vom Typ der angefragten Datei abhängig.

## Mieter-zu-Mieter Forum
Diese Schnittstelle dient dem Abfragen und Versenden von Mieter-zu-Mieter Nachrichten, ähnlich einem Forum oder Messenger Dienst.

### Liste von Nachrichten abfragen
`GET` `https://comcat.homeinfo.de/tenant2tenant`

#### Beispielantwort
Content-Type: `application/json`

	[
	  {
		"released": true,
		"startDate": "2018-01-01",
		"visibility": "tenement",
		"id": 77,
		"endDate": "2018-01-08",
		"message": "<b>Information f\u00fcr die Nachbarn</b><br><br>Liebe Nachbarn,<br><br><b>Frohes neues Jahr!<br><br>Familie Stechemesser</b><br><br>Vielen Dank!<br>",
		"address": {
		  "zipCode": "30625",
		  "houseNumber": "97",
		  "city": "Hannover",
		  "id": 278,
		  "street": "Misburger Str."
		},
		"created": "2018-01-01T12:09:57",
		"customer": 1030020
	  }
	]

### Nachricht hochladen
`POST` `https://comcat.homeinfo.de/tenant2tenant`

Mit der Einstellung `visibility` kann angegeben werden, ob die Nachricht nur für Mieter desselben Wohnhauses (`"tenement"`) oder des gesamten Wohnungsunternehmens (`"customer"`) sichtbar sein soll.

#### Beispieldatensatz
Accept: `application/json`

	{
	  "subject": <str:betreff>,
	  "message": <str:nachricht>,
	  "visibility": <enum:{"tenement"|"customer"}>
	}

### Nachricht löschen
`DELETE` `https://comcat.homeinfo.de/tenant2tenant/<int:ident>`

## Benutzerdateien
Mit dieser Schnittstelle kann der App-Benutzer eigene Dateien hoch- und herunterladen, sowie löschen.

### Dateien hochladen
`POST` `https://comcat.homeinfo.de/user-file`

Accept: `application/octet-stream`

### Dateien abfragen
`GET` `https://comcat.homeinfo.de/user-file/<int:ident>`

Content-Type: Anhängig vom Typ der angefragten Datei.

### Dateien löschen
`DELETE` `https://comcat.homeinfo.de/user-file/<int:ident>`

## Abmelden
Diese Schnittstelle dient dazu, den aktuellen Benutzer abzumelden.
`DELETE` `https://comcat.homeinfo.de/logout`
