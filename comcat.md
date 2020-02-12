# ComCat
ComCat ist ein Softwareprojekt zur Bereitellung eine Smartphone-Anwendung zur Mieter-Vermieter Kommunikation mit Integrations in das bestehende DSCMS4 der HOMEINFO GmbH.

## Smartphone-App Backend

### Endpoints
Im Folgenden werden die Web-Application endpoints für die Smartphone-Anwenung beschrieben.

#### Meta-Dienste
* `/login`              Zur Anmeldung von Benutzern ("User").
* `/oauth/authorize`    Authorisierung von OAuth Clients durch den User.
* `/oauth/token`        Ausstellung von Bearer Tokens für die Clients.
* `/oauth/revoke`       Zurückziehen von Tokens.
* `/oauth/introspect`   Prüfung von Tokens.

#### Nutzdaten
* `/damage-report`    Abfragen und Senden von Schadensmeldungen.
* `/file`             Abfragen und Senden von Binärdateien.
* `/local-news`       Abfragen von lokalen Nachrichten.
* `/ltp`              Abfragen von ÖPNV Verbindungen.
* `/presentation`     Abfragen der Präsentationsdaten.

#### `/login`
Der Endpoint `/login` erwaret eine POST-Request mit JSON-Body, welcher folgenden Datensatz enthält:

    {
        "uuid": <uuid>,
        "passwd": <password>
    }

Dabei ist `uuid` die UUID des entsprechenden Users und `passwd` das Passwort des Users.

#### `/oauth/authorize`
Autorisierung von Zugriffen auf OAuth-geschützte Resources duch Clients.
TODO: Detailliert dokumentieren.

#### `/oauth/token`
Ausstellen von Bearer Tokens.
TODO: Detailliert dokumentieren.

#### `/oauth/revoke`
Zurückziehen von Bearer Tokens.
TODO: Detailliert dokumentieren.

#### `/oauth/introspect`
Prüfen / Einsehen von Tokens.
TODO: Detailliert dokumentieren.

#### `/damage-report`
Abfragen und Einsenden von Schadensmeldungen.

* `GET` Abfragen von Schadensmeldungen. Erzeugt eine JSON-Antwort nach dem Schema:

    [
      {
        "timestamp": "2020-02-12T14:21:35",
        "contact": "1234",
        "address": {
          "city": "Hanau",
          "id": 1225,
          "street": "Heinrich-Bott-Stra\u00dfe",
          "houseNumber": "1",
          "zipCode": "63450"
        },
        "message": "Testmail<br/>",
        "name": "Alex",
        "id": 2717,
        "damageType": "Heizung",
        "checked": false,
        "customer": 1063001
      },
      ...
    ]

* `POST` Einsenden einer Schadensmeldung. Erwartet ein JSON-Objekt der Form:

    {
      "contact": "1234",
      "message": "Testmail<br/>",
      "name": "Alex",
      "damageType": "Heizung"
    }
