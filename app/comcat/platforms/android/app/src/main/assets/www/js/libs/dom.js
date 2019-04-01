/*
    Dynamic DOM elements.
*/
'use strict';

var comcat = comcat || {};
comcat.dom = comcat.dom || {};


comcat.dom_resellerLogo = function (logo) {
    const col = document.createElement('div');
    col.setAttribute('class', 'w3-col s8');
    const h1 = document.createElement('h1');
    h1.textContent = caption;
    col.appendChild(h1);
    const padding = document.createElement('div');
    padding.setAttribute('class', 'w3-col s2');
    return [col, padding];
};


comcat.dom_resellerCaption = function (caption) {
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
    let elements;

    if (caption == null && logo == null) {
        return null;
    }

    if (logo != null) {
        return comcat.dom_resellerLogo(logo);
    } else if (caption != null) {
        return comcat.dom_resellerCaption(caption);
    }


};
