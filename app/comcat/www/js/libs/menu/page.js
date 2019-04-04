/*
    Menu pages.
*/
'use strict';

var comcat = comcat || {};
comcat.menu = comcat.menu || {};


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
