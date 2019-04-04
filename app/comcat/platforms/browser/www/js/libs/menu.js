/*
    Menu rendering.
*/
'use strict';

var comcat = comcat || {};
comcat.menu = comcat.menu || {};
comcat.menu.MENU = [];
comcat.menu.MAX_PAGE_SIZE = 6;
comcat.menu.HISTORY = [];


/*
    Sets the menu from the presentation.
*/
comcat.menu.setMenu = function (menuItems) {
    comcat.menu.MENU = Array.from(comcat.menu.MenuItem.fromList(menuItems));
};


/*
    Goes one step back in the menu history.
*/
comcat.menu.pop = function () {
    const uuid = comcat.menu.HISTORY.pop();

    if (uuid != null) {
        const menuItem = comcat.menu.getMenuItem(uuid);
        const pages = comcat.menu.getSubMenu(menuItem);
        comcat.menu.render(pages);
    }
};


/*
    Resets the current menu path history.
*/
comcat.menu.reset = function () {
    const history = comcat.menu.HISTORY;
    comcat.menu.HISTORY = [];
    return history;
};


/*
    Sorting function to sort menu items by index.
*/
comcat.menu.sortByIndex = function (alice, bob) {
    return alice.index - bob.index;
};


/*
    Returns the submenu of the specified menu.
*/
comcat.menu.getSubMenu = function (menuItem) {
    let items = [];
    items = items.concat(menuItem.menuItems);
    items = items.concat(menuItem.charts);
    return comcat.menu.Page.fromItems(items);
};


/*
    Onclick function.
*/
comcat.menu.onclick = function () {
    const uuid = this.getAttribute('data-uuid');
    const menuItem = comcat.menu.MenuItem.get(uuid);
    const pages = comcat.menu.getSubMenu(menuItem);
    comcat.menu.render(pages);
    comcat.menu.HISTORY.push(menuItem.parent);
};


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
        chart = comcat.menu.Chart.fromJSON(chart);
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
    let menuItems = comcat.menu.MENU;

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


comcat.menu.Page = class extends Array {
    toDOM (visible = true) {
        if (this.length < 1 || this.length > 6) {
            throw 'Invalid page size: ' + this.length + '.';
        }

        const page = document.createElement('div');
        page.setAttribute('class', 'comcat-menu-page');

        if (!visible) {
            page.style.display = 'none';
        }

        // One row.
        if (this.length <= 3) {
            const row = document.createElement('div');
            row.setAttribute('class', 'w3-row');

            for (let item of this) {
                let column = document.createElement('div');
                let size = 12 / this.length;
                column.setAttribute('class', 'w3-col s' + size);
                column.appendChild(item);
                row.appendChild(column);
            }

            page.appendChild(row);
            return page;
        }

        // Two rows, 3 items and 2 items.
        if (this.length == 5) {
            let row = document.createElement('div');
            row.setAttribute('class', 'w3-row');

            for (let index = 0; index < 3; index++) {
                let item = this[index];
                let column = document.createElement('div');
                column.setAttribute('class', 'w3-col s' + 4);
                column.appendChild(item);
                row.appendChild(column);
            }

            page.appendChild(row);
            row = document.createElement('div');
            row.setAttribute('class', 'w3-row');

            for (let index = 3; index < 5; index++) {
                let item = this[index];
                let column = document.createElement('div');
                column.setAttribute('class', 'w3-col s' + 6);
                column.appendChild(item);
                row.appendChild(column);
            }

            page.appendChild(row);
            return page;
        }

        // Four or six items in two rows.
        let row = document.createElement('div');
        row.setAttribute('class', 'w3-row');

        for (let index = 0; index < this.length; index++) {
            let item = this[index];
            let column = document.createElement('div');
            let size = 12 / (this.length / 2);
            column.setAttribute('class', 'w3-col s' + size);
            column.appendChild(item);

            if (index == (this.length / 2)) {
                page.appendChild(row);
                row = document.createElement('div');
                row.setAttribute('class', 'w3-row');
            }

            row.appendChild(column);
        }

        page.appendChild(row);
        return page;
    }
};


/*
    Returns a list of pages from the respective menu items.
*/
comcat.menu.Page.fromItems = function* (items) {
    items = Array.from(items);
    items.sort(comcat.menu.sortByIndex);
    let page = new comcat.menu.Page();

    for (let item of items) {
        item = item.toDOM();
        page.push(item);

        if (page.length == comcat.menu.MAX_PAGE_SIZE) {
            yield page;
            page = new comcat.menu.Page();
        }
    }

    if (page.length > 0) {
        yield page;
    }
};


/*
    Renders the menus.
*/
comcat.menu.render = function (pages) {
    if (pages == null) {
        pages = comcat.menu.Page.fromItems(comcat.menu.MENU);
    }

    const menu = document.getElementById('menu');
    let visible = true;

    for (let page of pages) {
        menu.appendChild(page.toDOM(visible));
        visible = false;
    }
};
