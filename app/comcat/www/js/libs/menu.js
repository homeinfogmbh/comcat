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
    Converts a menu item into a button.
*/
comcat.menu.menuItemToDOM = function (item) {
    const button = document.createElement('button');
    button.textContent = item.name;
    button.style.backgroundColor = item.backgroundColor;
    button.style.color = item.textColor;
    button.setAttribute('class', 'comcat-button-submenu');
    button.setAttribute('data-subtree', JSON.stringify(item.menuItems));
    button.setAttribute('data-charts', JSON.stringify(item.charts));
    return button;
};

/*
    Returns a list of pages from the respective menu items.
*/
comcat.menu.pages = function* (menuItems, root = false) {
    menuItems.sort(comcat.menu.sortByIndex);
    let page = [];

    for (let index in menuItems) {
        let button;

        if (!root && (page.length == comcat.menu.MAX_PAGE_SIZE - 1)) {
            button = comcat.menu.backButton();
            page.push(button);
            yield page;
            page = [];
        }

        let menuItem = menuItems[index];
        button = comcat.menu.menuItemToDOM(menuItem);
        page.push(button);

        if (page.length == comcat.menu.MAX_PAGE_SIZE) {
            yield page;
            page = [];
        }
    }

    if (page.length > 0) {
        yield page;
    }
};

/*
    Converts a page into rows and columns.
*/
comcat.menu.pageDOM = function (items, visible = true) {
    if (items.length < 1 || items.length > 6) {
        throw 'Invalid page size: ' + items.length + '.';
    }

    const page = document.createElement('div');
    page.setAttribute('class', 'comcat-menu-page');

    if (!visible) {
        page.style.display = 'none';
    }

    // One row.
    if (items.length <= 3) {
        const row = document.createElement('div');
        row.setAttribute('class', 'w3-row');

        for (let item of items) {
            let column = document.createElement('div');
            let size = 12 / items.length;
            column.setAttribute('class', 'w3-col s' + size);
            column.appendChild(item);
            row.appendChild(column);
        }

        page.appendChild(row);
        return page;
    }

    // Two rows, 3 items and 2 items.
    if (items.length == 5) {
        let row = document.createElement('div');
        row.setAttribute('class', 'w3-row');

        for (let index = 0; index < 3; index++) {
            let item = items[index];
            let column = document.createElement('div');
            column.setAttribute('class', 'w3-col s' + 4);
            column.appendChild(item);
            row.appendChild(column);
        }

        page.appendChild(row);
        row = document.createElement('div');
        row.setAttribute('class', 'w3-row');

        for (let index = 3; index < 5; index++) {
            let item = items[index];
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

    for (let index = 0; index < items.length; index++) {
        let item = items[index];
        let column = document.createElement('div');
        let size = 12 / (items.length / 2);
        column.setAttribute('class', 'w3-col s' + size);
        column.appendChild(item);

        if (index == (items.length / 2)) {
            page.appendChild(row);
            row = document.createElement('div');
            row.setAttribute('class', 'w3-row');
        }

        row.appendChild(column);
    }

    page.appendChild(row);
    return page;
};
