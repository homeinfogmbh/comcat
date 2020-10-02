# Client initialisierung:

1. Nonce abrufen (QR-Code).
2. Nonce per POST and Backend senden:  
   `POST /client {"nonce": "<uuid>"}`  
3. JSON Response verarbeiten.  
   Wichtig: `clientId`, `clientSecret`, `authorizationNonce`
4. Authorization mit authorizationNonce durchführen:  
   `POST /authorize {"nonce": "<uuid>"}`  
   Antwort: OAuth 2.0 Authorization Response.

Danach kann regulär OAuth 2.0 verwendet werden.
