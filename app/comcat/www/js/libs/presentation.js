/*
    Retrieval and rendering of presentation data.

    Depends: libs/common.js
*/
'use strict';

var comcat = comcat || {};
comcat.presentation = comcat.presentation || {};


/*
    Retrieves presentation data from the backend.
*/
comcat.presentation.get = function () {
    return comcat.makeRequest('GET', comcat.BASE_URL + '/presentation').then(
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
    constructor (json) {
        for (const key in json) {
            this[key] = json[key];
        }

        this.initMenu();
    }

    initMenu () {
        return comcat.menu.setMenu(this.menuItems);
    }
};


/*
    Factory method to create a presetation from a given JSON object.
*/
comcat.presentation.Presentation.fromJSON = function (json) {
    return new comcat.presentation.Presentation(json);
};
