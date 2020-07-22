# ComCat
ComCat ist ein Softwareprojekt zur Bereitellung eine Smartphone-Anwendung zur Mieter-Vermieter Kommunikation mit Integration in das bestehende DSCMS4 der HOMEINFO GmbH.

## Smartphone-App Backend

### Endpoints
Im Folgenden werden die Web-Application endpoints für die Smartphone-Anwenung beschrieben.

#### Meta-Dienste
* `/client`             Client Registrierung.
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
* `/charts`           Abfragen von zugeordneten Charts.

#### `/login`
Der Endpoint `/login` erwaret eine POST-Request mit Form-Body, welcher folgenden Datensatz enthält:

* "uuid": <uuid>
* "passwd": <password>

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

* `GET /` Abfragen von Schadensmeldungen. Erzeugt eine JSON-Antwort nach dem Schema:

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

* `POST /` Einsenden einer Schadensmeldung. Erwartet ein JSON-Objekt der Form:

      {
          "contact": "1234",
          "message": "Testmail<br/>",
          "name": "Alex",
          "damageType": "Heizung"
      }

#### /file
Herunter- und hochladen von Dateien.

* `GET /<int:id>` Herunterladen der Datei mit der angegebenen ID.

* `POST /` Hochladen einer Datei. **Aktuell nicht implementiert!**

#### /local-news
Abfragen von Lokalnachrichten.

* `GET /` Abfragen der Nachrichtenartikel. Ergibt ein JSON-Objekt nach dem Schema:

      [
          {
              "title": "Winterzeit ist Zeit der Feuerzangenbowle",
              "id": 386,
              "created": "2018-11-13T11:36:04",
              "activeUntil": "2018-11-23",
              "activeFrom": "2018-11-16",
              "source": "https://www.t-online.de/ratgeber/id_84546504/feuerzangenbowle-set-und-rezept-fuer-den-film-klassiker.html",
              "text": "Das Rezept der Feuerzangenbowle ist bereits sehr alt, wurde aber erst 1944 durch den gleichnamigen Film mit Heinz R\u00fchmann Kult. F\u00fcr die Zubereitung ben\u00f6tigt man lediglich 2 Flaschen trockenen Rotwein, einen halben Liter Rum, Orangen- und Zitronensaft, einen Zuckerhut und weihnachtliche Gew\u00fcrze, wie Nelken und Zimtstangen. Im Internet finden sich verschiedene Sets von 25 bis 100 Euro, mit denen das Anz\u00fcnden und Heruntertropfen des in Rum getr\u00e4nkten Zuckers besonders gut funktioniert. Um Stichflammen zu verhindern, sollte man den Rum langsam mit einer Sch\u00f6pfkelle nachsch\u00fctten. \u00dcblicherweise wird das Getr\u00e4nk bei 70 Grad Celsius getrunken.&nbsp;",
              "images": [
                  {
                      "source": "https://pixabay.com/de/gl%C3%BChwein-weihnachtsmarkt-1075689/",
                      "uploaded": "2018-11-13T11:36:04",
                      "id": 460,
                      "mimetype": "image/jpeg"
                  }
              ],
              "tags": [
                  "Aktuelles",
                  "Hannover",
                  "Winter",
                  "Wohnen",
                  "CMS"
              ]
          },
          ...
      ]

* `GET /<int:article_id>/<int:image_id>` Abfrage von Bildern eines Artikels.
