/*
    Handling of charts.
*/
'use strict';

var comcat = comcat || {};
comcat.charts = comcat.charts || {};
comcat.charts._CHARTS = [];
comcat.charts.TYPES = {};


/*
    Sets the charts.
*/
comcat.charts.set = function (charts) {
    comcat.charts._CHARTS = Array.from(comcat.charts.Chart.fromList(charts));
};


/*
    A base chart.
*/
comcat.charts.BaseChart = class {
    constructor (title, description, duration, displayFrom, displayUntil, transition, created, trashed, log, uuid) {
        this.title = title;
        this.description = description;
        this.duration = duration;
        this.displayFrom = displayFrom;
        this.displayUntil = displayUntil;
        this.transition = transition;
        this.created = created;
        this.trashed = trashed;
        this.log = log;
        this.uuid = uuid;
    }
};


/*
    Creates a BaseChart from the respective JSON object.
*/
comcat.charts.BaseChart.fromJSON = function (json) {
    return new comcat.charts.BaseChart(
        json.title, json.description, json.duration, json.displayFrom, json.displayUntil, json.transition,
        json.created, json.trashed, json.log, json.uuid);
};


/*
    An abstract chart.
*/
comcat.charts.Chart = class {
    constructor (base) {
        this.base = base;
    }

    toDOM () {
        const chart = document.createElement('div');
        chart.setAttribute('class', 'w3-container');
        const header = document.createElement('h1');
        header.innerHTML = this.base.title;
        chart.appendChild(header);
        return chart;
    }
};


/*
    Creates a chart from a JSON object.
*/
comcat.charts.Chart.fromJSON = function (json) {
    const chartClass = comcat.charts.TYPES[json.type];
    return chartClass.fromJSON(json);
};


/*
    Yields charts from list of JSON objects.
*/
comcat.charts.Chart.fromList = function* (list) {
    for (const json of list) {
        yield comcat.charts.Chart.fromJSON(json);
    }
};


/*
    Returns a chart by ID and type.
*/
comcat.charts.Chart.get = function (id, type) {
    for (const chart of comcat.charts.CHARTS) {
        if (chart.type == type && chart.id == id) {
            return chart;
        }
    }

    throw 'No such chart.';
};
