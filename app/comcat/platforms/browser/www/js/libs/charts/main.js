/*
    Handling of charts.
*/
'use strict';

var comcat = comcat || {};
comcat.charts = comcat.charts || {};


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
};
