/*
    ComCat comman API libarary.
*/
'use strict';

var comcat = comcat || {};
comcat.BASE_URL = 'https://wohninfo.homeinfo.de';


/*
    A JSON API requestor.
*/
comcat.JSONHttpRequest = class extends XMLHttpRequest {
    constructor (resolve, reject, withCredentials = true) {
        super();
        this.resolve = resolve;
        this.reject = reject;
        this.withCredentials = withCredentials;
    }

    get json () {
        const json = {
            response: this.response,
            status: this.status,
            statusText: this.statusText
        };

        try {
            json.json = JSON.parse(this.response);
        } catch (error) {
            return json;
        }

        return json;
    }

    setRequestHeaders (headers) {
        for (const header in headers) {
            this.setRequestHeader(header, headers[header]);
        }
    }
};


comcat.JSONHttpRequest.onload = function () {
    console.log('Onload.');
    if (this.status >= 200 && this.status < 300) {
        this.resolve(this.json);
    } else {
        this.reject(this.json);
    }
};


comcat.JSONHttpRequest.onerror = function () {
    console.log('Onerror.');
    this.reject(this.json);
};


/*
    Makes an asychronous JSON API reguest.
*/
comcat.request = function (method, url, data = null, headers = {}) {
    function executor (resolve, reject) {
        const jhr = new comcat.JSONHttpRequest(resolve, reject);
        jhr.open(method, url);
        jhr.setRequestHeaders(headers);

        /*
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
        */
        console.log('Onload is: ' + jhr.onload.toString());

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
comcat.get = function (url, headers = {}) {
    return comcat.request('GET', url, null, headers);
};


/*
    Makes an asychronous JSON API POST reguest.
*/
comcat.post = function (url, data = null, headers = {}) {
    return comcat.request('POST', url, data, headers);
};


/*
    Makes an asychronous JSON API PUT reguest.
*/
comcat.put = function (url, data = null, headers = {}) {
    return comcat.request('PUT', url, data, headers);
};


/*
    Makes an asychronous JSON API PATCH reguest.
*/
comcat.patch = function (url, data = null, headers = {}) {
    return comcat.request('PATCH', url, data, headers);
};


/*
    Makes an asychronous JSON API DELETE reguest.
*/
comcat.delete = function (url, headers = {}) {
    return comcat.request('DELETE', url, null, headers);
};
