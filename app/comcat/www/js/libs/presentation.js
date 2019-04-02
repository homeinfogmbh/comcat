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
            return comcat.presentation.Presentation.from_json(response.json);
        }
    );
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
};


/*
    Factory method to create a presetation from a given JSON object.
*/
comcat.presentation.Presentation.from_json = function (json) {
    return new comcat.presentation.Presentation(json);
};


/*
    Renders the menus.
*/
comcat.presentation.renderMenus = function (json) {
    const menuItems = json.menuItems;
    let pages = comcat.menu.pages(menuItems);
    pages = Array.from(pages);
    const page = pages[0];
    const rows = comcat.menu.pageDOM(page);
    const menu = document.getElementById('menu');

    for (let row of rows) {
        menu.appendChild(row);
    }
};
