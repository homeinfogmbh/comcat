/*
    Asynchronous JavaScript and JSON API.
*/

/*
  Makes a request returning a promise.
*/
var comcat = comcat || {};

comcat.parseJSON = function (text) {
    try {
        return JSON.parse(text);
    } catch (error) {
        return null;
    }
};

comcat.JSONHttpRequest = class extends XMLHttpRequest {
    constructor (resolve, reject, withCredentials = true) {
        super();
        this.withCredentials = withCredentials;
        this.resolve = resolve;
        this.reject = reject;
    }

    get json () {
        return {
            response: this.response,
            json: comcat.parseJSON(this.response),
            status: this.status,
            statusText: this.statusText
        };
    }

    onload () {
        if (this.status >= 200 && this.status < 300) {
            this.resolve(this.json);
        } else {
            this.reject(this.json);
        }
    }

    onerror () {
        this.reject(this.json);
    }
};

comcat.makeRequest = function (method, url, data=null, headers) {
    function executor (resolve, reject) {
        const jhr = new comcat.JSONHttpRequest(resolve, reject, false);
        jhr.open(method, url);

        for (let header in headers) {
            if (headers.hasOwnProperty(header)) {
                jhr.setRequestHeader(header, headers[header]);
            }
        }

        if (data == null) {
            jhr.send();
        } else {
            jhr.send(data);
        }
    }

    return new Promise(executor);
};
