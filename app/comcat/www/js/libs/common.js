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
    Makes an asychronous JSON API reguest.
*/
comcat.makeRequest = function (method, url, data = null, headers = {}) {
    function executor (resolve, reject) {
        const xhr = new XMLHttpRequest();
        xhr.withCredentials = true;
        xhr.open(method, url);

        for (const header in headers) {
            xhr.setRequestHeader(header, headers[header]);
        }

        xhr.onload = function () {
            if (this.status >= 200 && this.status < 300) {
                resolve({
                    response: xhr.response,
                    json: comcat.parseJSON(xhr.response),
                    status: this.status,
                    statusText: xhr.statusText
                });
            } else {
                reject({
                    response: xhr.response,
                    json: comcat.parseJSON(xhr.response),
                    status: this.status,
                    statusText: xhr.statusText
                });
            }
        };
        xhr.onerror = function () {
            reject({
                response: xhr.response,
                json: comcat.parseJSON(xhr.response),
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
