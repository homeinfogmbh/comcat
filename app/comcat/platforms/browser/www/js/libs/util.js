/*
    ComCat utility functions.
*/
'use strict';

var comcat = comcat || {};
comcat.util = comcat.util || {};

comcat.util.intToColor = function (integer) {
    return '#' + integer.toString(16).padStart(6, '0');
};
