/*
    Menu items.
*/
'use strict';

var comcat = comcat || {};
comcat.menu = comcat.menu || {};


/*
    Represents a menu item.
*/
comcat.menu.MenuItem = class {
    constructor (uuid, name, backgroundColor, textColor, menuItems, charts, parent) {
        this.uuid = uuid;
        this.name = name;
        this.backgroundColor = backgroundColor;
        this.textColor = textColor;
        this.menuItems = menuItems;
        this.charts = charts;
        this.parent = parent;
    }

    get subMenu () {
        let items = [];
        items = items.concat(this.menuItems);
        items = items.concat(this.charts);
        return comcat.menu.Page.fromItems(items);
    }

    toDOM () {
        const button = document.createElement('button');
        button.textContent = this.name;
        button.style.backgroundColor = comcat.util.intToColor(this.backgroundColor);
        button.style.color = comcat.util.intToColor(this.textColor);
        button.setAttribute('class', 'w3-button w3-block comcat-button-submenu');
        button.setAttribute('data-uuid', this.uuid);
        button.setAttribute('data-parent', this.parent);
        return button;
    }
};


/*
    Returns a new MenuItem from JSON.
*/
comcat.menu.MenuItem.fromJSON = function (json, parent = null) {
    const menuItems = [];
    const charts = [];

    for (let menuItem of json.menuItems) {
        menuItem = comcat.menu.MenuItem.fromJSON(menuItem, json.uuid);
        menuItems.push(menuItem);
    }

    for (let chart of json.charts) {
        chart = comcat.menu.Chart.fromJSON(chart, json.uuid);
        charts.push(chart);
    }

    return new comcat.menu.MenuItem(json.uuid, json.name, json.backgroundColor, json.textColor, menuItems, charts, parent);
};


/*
    Returns new MenuItems from JSON.
*/
comcat.menu.MenuItem.fromList = function* (list) {
    for (let json of list) {
        yield comcat.menu.MenuItem.fromJSON(json);
    }
};


/*
    Returns the respective menu.
*/
comcat.menu.MenuItem.get = function (uuid) {
    let menuItems = comcat.menu._MENU;

    while (menuItems.length > 0) {
        let nextMenuItems = [];

        for (let menuItem of menuItems) {
            if (menuItem.uuid == uuid) {
                return menuItem;
            }

            nextMenuItems = nextMenuItems.concat(menuItem.menuItems);
        }

        menuItems = nextMenuItems;
    }

    throw 'No such menu item.';
};


/*
    A menu item's onclick function.
*/
comcat.menu.MenuItem.onclick = function () {
    console.log('DEBUG: ' + this);
    const uuid = this.getAttribute('data-uuid');
    console.log('DEBUG: UUID =  ' + uuid);
    const menuItem = comcat.menu.MenuItem.get(uuid);
    console.log('DEBUG ITEM:\n' + JSON.stringify(menuItem));

    if (menuItem.menuItems.length == 0 && menuItem.charts.length == 1) {
        let chart = menuItem.charts[0];
        chart = comcat.charts.Chart.get(chart.id, chart.type);
        chart.show();
    } else {
        const pages = menuItem.subMenu;
        console.log('Pages:\n' + JSON.stringify(pages));
        comcat.menu.render(pages);
        comcat.menu.HISTORY.push(menuItem.parent);
    }
};
