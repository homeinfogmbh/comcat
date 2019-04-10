/*
    Dynamic DOM elements.
*/
'use strict';

let comcat = comcat || {};
comcat.dom = comcat.dom || {};


comcat.dom.resellerLogo = function (logo) {
    const col = document.createElement('div');
    col.setAttribute('class', 'w3-col s8');
    const image = document.createElement('img');
    image.setAttribute('src', logo);
    col.appendChild(image);
    const padding = document.createElement('div');
    padding.setAttribute('class', 'w3-col s2');
    return [col, padding];
};


comcat.dom.resellerCaption = function (caption) {
    const col = document.createElement('div');
    col.setAttribute('class', 'w3-col s8');
    const h1 = document.createElement('h1');
    h1.textContent = caption;
    col.appendChild(h1);
    const padding = document.createElement('div');
    padding.setAttribute('class', 'w3-col s2');
    return [col, padding];
};


comcat.dom.resellerHeader = function (resellerConfig) {
    const caption = resellerConfig.caption || null;
    const logo = resellerConfig.logo || null;

    if (caption == null && logo == null) {
        return null;
    }

    if (logo != null) {
        return comcat.dom.resellerLogo(logo);
    } else if (caption != null) {
        return comcat.dom.resellerCaption(caption);
    }
};
