/*
    Session management functions.
*/
var comcat = comcat || {};
comcat.session = comcat.session || {};


/*
    Performs a login.
*/
comcat.session.login = function (uuid, passwd) {
    const loginCredentials = {uuid: uuid, passwd: passwd};
    const postData = JSON.stringify(loginCredentials);
    const headers = {'Content-Type': 'application/json'};
    return comcat.makeRequest('POST', comcat.BASE_URL + '/login', postData, headers);
};


/*
    Checks whether we have a valid session.
*/
comcat.session.check = function () {
    return comcat.makeRequest('GET', comcat.BASE_URL + '/session');
};
