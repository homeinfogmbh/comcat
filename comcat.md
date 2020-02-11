# ComCat
ComCat ist ein Softwareprojekt zur Bereitellung eine Smartphone-Anwendung zur Mieter-Vermieter Kommunikation mit Integrations in das bestehende DSCMS4 der HOMEINFO GmbH.

## Smartphone-App Backend

### Endpoints
Im Folgenden werden die Web-Application endpoints für die Smartphone-Anwenung beschrieben.

#### Meta-Dienste
* `/login`            Zur Anmeldung von Benutzern ("User").
* `/oauth/authorize`  Authorisierung von OAuth Clients durch den User.
* `/oauth/token`      Ausstellung von Bearer Tokens für die Clients.

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
Ausstellen und zurückziehen von Bearer Tokens.
TODO: Detailliert dokumentieren.

####
