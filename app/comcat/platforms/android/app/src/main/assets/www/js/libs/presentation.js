/*
    Retrieval and rendering of presentation data.

    Depends:
        * libs/common.js
        * libs/menu/main.js
        * libs/menu/item.js
        * libs/charts/main.js
        * libs/configuration.js
        * libs/playlist.js
*/
'use strict';

var comcat = comcat || {};
comcat.presentation = comcat.presentation || {};


/*
    Retrieves presentation data from the backend.
*/
comcat.presentation.get = function () {
    return comcat.get(comcat.BASE_URL + '/presentation').then(
        function (response) {
            return comcat.presentation.Presentation.fromJSON(response.json);
        }
    );
};


/*
    Represents presentation data with a function to render it.
*/
comcat.presentation.Presentation = class {
    // TODO: Migrated to fromJSON() static factory method.
    constructor (account, customer, configuration, charts, playlist, menuItems) {
        this.account = account;
        this.customer = customer;
        this.configuration = configuration;
        this.charts = Array.from(charts);
        this.playlist = Array.from(playlist);
        this.menuItems = Array.from(menuItems);
    }
};


/*
    Factory method to create a presetation from a given JSON object.
*/
comcat.presentation.Presentation.fromJSON = function (json) {
    //const configuration = comcat.configuration.Configuration.fromJSON(json.configuration);
    const configuration = json.configuration;
    //const charts = comcat.charts.Chart.fromList(json.charts);
    const charts = json.charts;
    //const playlist = comcat.playlist.Playlist.fromList(json.playlist);
    const playlist = json.playlist;
    const menuItems = comcat.menu.MenuItem.fromList(json.menuItems);
    return new comcat.presentation.Presentation(
        json.account, json.customer, configuration, charts, playlist, menuItems);
};


/*
    Initializes the presentation.
*/
comcat.presentation.init = function (presentation) {
    comcat.charts.set(presentation.charts);
    comcat.menu.init(presentation);
};
