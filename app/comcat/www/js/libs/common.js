/*
    ComCat comman API libarary.
*/
'use strict';

var comcat = comcat || {};
comcat.BASE_URL = 'https://wohninfo.homeinfo.de';


comcat.parseJSON = function (text) {
    try {
        return JSON.parse(text);
    } catch (error) {
        return null;
    }
};


/*
    A JSON API requestor.
*/
comcat.JSONHttpRequest = class extends XMLHttpRequest {
    constructor () {
        super();
        this.withCredentials = true;
    }

    get json () {
        return {
            response: this.response,
            json: comcat.parseJSON(this.response),
            status: this.status,
            statusText: this.statusText
        };
    }

    set headers (headers) {
        for (const header in headers) {
            this.setRequestHeader(header, headers[header]);
        }
    }
};


/*
    Makes an asychronous JSON API reguest.
*/
comcat.JSONHttpRequest.request = function (method, url, data = null, headers = {}) {
    function executor (resolve, reject) {
        const jhr = new comcat.JSONHttpRequest(resolve, reject);
        jhr.open(method, url);
        jhr.headers = headers;

        jhr.onload = function () {
            if (this.status >= 200 && this.status < 300) {
                resolve(this.json);
            } else {
                reject(this.json);
            }
        };

        jhr.onerror = function () {
            reject(this.json);
        };

        if (data == null) {
            jhr.send();
        } else {
            jhr.send(data);
        }
    }

    return new Promise(executor);
};


/*
    Makes an asychronous JSON API GET reguest.
*/
comcat.JSONHttpRequest.get = function (url, data = null, headers = {}) {
    return comcat.JSONHttpRequest.request('GET', url, data, headers);
};


/*
    Makes an asychronous JSON API POST reguest.
*/
comcat.JSONHttpRequest.post = function (url, data = null, headers = {}) {
    return comcat.JSONHttpRequest.request('POST', url, data, headers);
};


/*
    Makes an asychronous JSON API PUT reguest.
*/
comcat.JSONHttpRequest.put = function (url, data = null, headers = {}) {
    return comcat.JSONHttpRequest.request('PUT', url, data, headers);
};


/*
    Makes an asychronous JSON API PATCH reguest.
*/
comcat.JSONHttpRequest.patch = function (url, data = null, headers = {}) {
    return comcat.JSONHttpRequest.request('PATCH', url, data, headers);
};


/*
    Makes an asychronous JSON API DELETE reguest.
*/
comcat.JSONHttpRequest.delete = function (url, data = null, headers = {}) {
    return comcat.JSONHttpRequest.request('DELETE', url, data, headers);
};
