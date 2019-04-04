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
comcat.presentation.Presentation.fromJSON = function (json) {
    return new comcat.presentation.Presentation(json);
};


/*
    Renders the menus.
*/
comcat.presentation.renderMenus = function (json) {
    const menuItems = comcat.menu.MenuItem.fromItems(json.menuItems);
    const pages = comcat.menu.Page.fromItems(menuItems);
    const menu = document.getElementById('menu');
    let visible = true;

    for (let page of pages) {
        menu.appendChild(page.toDOM(visible));
        visible = false;
    }
};
