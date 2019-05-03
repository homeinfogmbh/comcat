/*
    Menu rendering.
*/
'use strict';

comcat = comcat || {};
comcat.menu = comcat.menu || {};
comcat.menu._MENU = [];
comcat.menu.MAX_PAGE_SIZE = 6;
comcat.menu.HISTORY = [];


/*
    Sets the menu from the presentation.
*/
comcat.menu.set = function (menuItems) {
    comcat.menu._MENU = Array.from(comcat.menu.MenuItem.fromList(menuItems));
};


/*
    Goes one step back in the menu history.
*/
comcat.menu.pop = function () {
    const uuid = comcat.menu.HISTORY.pop();

    if (uuid != null) {
        const menuItem = comcat.menu.getMenuItem(uuid);
        const pages = menuItem.subMenu;
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
    Renders the menus.
*/
comcat.menu.render = function (pages) {
    if (pages == null) {
        pages = comcat.menu.Page.fromItems(comcat.menu._MENU);
    }

    const menu = document.getElementById('menu');
    menu.innerHTML = '';
    let visible = true;

    for (const page of pages) {
        menu.appendChild(page.toDOM(visible));
        visible = false;
    }
};


/*
    Initializes the menu.
*/
comcat.menu.init = function (presentation) {
    comcat.menu.set(presentation.menuItems);
    comcat.menu.render();
};
