/*
    Blackboard chart stuff.
*/
'use strict';

var comcat = comcat || {};
comcat.charts = comcat.charts || {};


/*
    A Blackboard chart.
*/
comcat.charts.blackboard.Blackboard = class extends comcat.charts.Chart {
    constructor (base, images) {
        super(base);
        this.images = Array.from(images);
    }
};


/*
    Creates a blackboard chart from JSON.
*/
comcat.charts.Blackboard.fromJSON = function (json) {
    const base = comcat.charts.BaseChart.fromJSON(json.base);
    const images = comcat.charts.BlackboardImage.fromList(json.images);
    return new comcat.charts.Blackboard(base, images);
};


/*
    Images of a blackboard chart.
*/
comcat.charts.BlackboardImage = class {
    constructor (image, format, index) {
        this.image = image;
        this.format = format;
        this.index = index;
    }
};


/*
    Creates a blackboard chart image from a JSON object.
*/
comcat.charts.BlackboardImage.fromJSON = function (json) {
    return new comcat.charts.BlackboardImage(json.image, json.format, json.index);
};


/*
    Creates blackboard chart images from a JSON list.
*/
comcat.charts.BlackboardImage.fromList = function* (list) {
    for (const json of list) {
        yield comcat.charts.BlackboardImage.fromJSON(json);
    }
};
