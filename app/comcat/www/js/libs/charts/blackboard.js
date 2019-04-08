/*
    Blackboard charts and related models.
*/
'use strict';

var comcat = comcat || {};
comcat.charts = comcat.charts || {};


/*
    A Blackboard chart.
*/
comcat.charts.Blackboard = class extends comcat.charts.Chart {
    constructor (base, images) {
        super(base);
        this.images = Array.from(images);
    }

    toDOM () {
        const blackboard = super.toDOM();
        const imageGallery = document.createElement('div');
        imageGallery.setAttribute('w3-row');

        for (const image of this.images) {
            let frame = document.createElement('div');
            frame.setAttribute('class', 'w3-card-4');
            frame.appendChild(image.toDOM());
            imageGallery.append(frame);
        }

        blackboard.appendChild(imageGallery);
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

    toDOM () {
        const image = document.createElement('img');
        image.setAttribute('src', comcat.BASE_URL + '/file/' + this.image);
        return image;
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


// Register chart type.
comcat.charts.TYPES['Blackboard'] = comcat.charts.Blackboard;
