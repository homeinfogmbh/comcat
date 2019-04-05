/*
    Menu item charts.
*/
'use strict';

var comcat = comcat || {};
comcat.menu = comcat.menu || {};


/*
    A menu item chart.
*/
comcat.menu.Chart = class {
    constructor (id, index, type, parentId) {
        this.id = id;
        this.index = index;
        this.type = type;
        this.parentId = parentId;
    }

    get chart () {
        try {
            return comcat.charts.Chart.get(this.id, this.type)
        } catch (error) {
            return {name: 'No such chart.'};
        }
    }

    get parent () {
        return comcat.menu.MenuItem.get(this.parentId);
    }

    toDOM () {
        const button = document.createElement('button');
        button.textContent = this.chart.name;
        button.style.backgroundColor = comcat.util.intToColor(this.parent.backgroundColor);
        button.style.color = comcat.util.intToColor(this.parent.textColor);
        button.setAttribute('class', 'w3-button w3-block');
        button.setAttribute('data-id', this.id);
        button.setAttribute('data-type', this.type);
        button.addEventListener('click', comcat.menu.Chart.onclick, false);
        return button;
    }
};


/*
    Creates a new chart from JSON.
*/
comcat.menu.Chart.fromJSON = function (json, parent) {
    return new comcat.menu.Chart(json.id, json.index, json.type, parent);
};


/*
    A menu item chart's onclick function.
*/
comcat.menu.Chart.onclick = function () {
    const id = this.getAttribute('data-id');
    const type = this.getAttribute('data-type');
    const chart = comcat.charts.Chart.get(id, type);
    chart.show();
};
