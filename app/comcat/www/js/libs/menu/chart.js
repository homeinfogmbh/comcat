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
    constructor (id, index, type, parent) {
        this.id = id;
        this.index = index;
        this.type = type;
        this.parent = parent;
    }

    toDOM () {
        const button = document.createElement('button');
        button.textContent = this.chart.name;
        button.style.backgroundColor = comcat.util.intToColor(this.backgroundColor);
        button.style.color = comcat.util.intToColor(this.textColor);
        button.setAttribute('class', 'w3-button w3-block comcat-button-chart');
        button.setAttribute('data-id', this.id);
        button.setAttribute('data-type', this.type);
        button.setAttribute('data-parent', this.parent);
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
