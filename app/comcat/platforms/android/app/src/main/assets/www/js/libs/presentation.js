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
        comcat.presentation.Presentation.from_json);
};


/*
    Represents presentation data with a function to render it.
*/
comcat.presentation.Presentation = class {
    constructor (json) {
        for (let key in json) {
            if (json.hasOwnProperty(key)) {
                this[key] = json[key];
            }
        }
    }

    render (element) {
        // TODO: implement.
    }
};


/*
    Factory method to create a presetation from a given JSON object.
*/
comcat.presentation.Presentation.from_json = function (json) {
    return new comcat.presentation.Presentation(json);
};
