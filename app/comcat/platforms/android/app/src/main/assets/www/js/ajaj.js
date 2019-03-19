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

comcat.makeRequest = function (method, url, data=null, headers) {
    function executor (resolve, reject) {
        const xhr = new XMLHttpRequest();
        //xhr.withCredentials = true;
        xhr.open(method, url);

        for (let header in headers) {
            if (headers.hasOwnProperty(header)) {
                xhr.setRequestHeader(header, headers[header]);
            }
        }

        xhr.onload = function () {
            if (this.status >= 200 && this.status < 300) {
                resolve({
                    response: xhr.response,
                    json: comcat.parseJSON (xhr.response),
                    status: this.status,
                    statusText: xhr.statusText
                });
            } else {
                reject({
                    response: xhr.response,
                    json: comcat.parseJSON (xhr.response),
                    status: this.status,
                    statusText: xhr.statusText
                });
            }
        };
        xhr.onerror = function () {
            reject({
                response: xhr.response,
                json: comcat.parseJSON (xhr.response),
                status: this.status,
                statusText: xhr.statusText
            });
        };

        if (data == null) {
            xhr.send();
        } else {
            xhr.send(data);
        }
    }

    return new Promise(executor);
};
