/*
    Menu rendering.
*/
'use strict';

var comcat = comcat || {};
comcat.menu = comcat.menu || {};
comcat.menu.MAX_PAGE_SIZE = 6;
comcat.menu.HISTORY = [];

comcat.menu.push = function (menuItem) {
    comcat.menu.HISTORY.push(menuItem);
};

/*
    Goes one step back in the menu history.
*/
comcat.menu.pop = function () {
    return comcat.menu.HISTORY.pop();
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
    Creates a button to go back.
*/
comcat.menu.backButton = function () {
    const button = document.createElement('button');
    button.textContent = '← back';
    button.setAttribute('class', 'comcat-button-submenu');
    return button;
};

/*
    Represents a menu item.
*/
comcat.menu.MenuItem = class {
    constructor (name, backgroundColor, textColor, menuItems, charts) {
        this.name = name;
        this.backgroundColor = backgroundColor;
        this.textColor = textColor;
        this.menuItems = menuItems;
        this.charts = charts;
    }

    toDOM () {
        console.log('DEBUG:\n' + JSON.stringify(this, null, 2));
        console.log('Text color: ' + comcat.util.intToColor(this.textColor));
        console.log('Background color: ' + comcat.util.intToColor(this.backgroundColor));
        const button = document.createElement('button');
        button.textContent = this.name;
        button.style.backgroundColor = comcat.util.intToColor(this.backgroundColor);
        button.style.color = comcat.util.intToColor(this.textColor);
        button.setAttribute('class', 'w3-button w3-block comcat-button-submenu');
        button.setAttribute('data-subtree', JSON.stringify(this.menuItems));
        button.setAttribute('data-charts', JSON.stringify(this.charts));
        return button;
    }
};

/*
    Returns a new MenuItem from JSON.
*/
comcat.menu.MenuItem.fromJSON = function (json) {
    const menuItems = [];

    for (let menuItem of json.menuItems) {
        menuItem = comcat.menu.MenuItem.fromJSON(menuItem);
        menuItems.push(menuItem);
    }

    return new comcat.menu.MenuItem(json.name, json.backgroundColor, json.textColor, menuItems, json.charts);
};

/*
    Returns new MenuItems from JSON.
*/
comcat.menu.MenuItem.fromItems = function* (items) {
    for (let item of items) {
        yield comcat.menu.MenuItem.fromJSON(item);
    }
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
    let root = true;

    for (let item of items) {
        if (!root && (page.length == comcat.menu.MAX_PAGE_SIZE - 1)) {
            let button = comcat.menu.backButton();
            page.push(button);
            yield page;
            root = false;
            page = new comcat.menu.Page();
        }

        item = item.toDOM();
        page.push(item);

        if (page.length == comcat.menu.MAX_PAGE_SIZE) {
            yield page;
            root = false;
            page = new comcat.menu.Page();
        }
    }

    if (page.length > 0) {
        yield page;
    }
};
