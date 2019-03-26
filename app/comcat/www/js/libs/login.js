/*
    Login management.
*/
var comcat = comcat || {};
comcat.login = comcat.login || {};
comcat.login.USER_NAME = 'comcat.userName';
comcat.login.PASSWD = 'comcat.passwd';


/*
    Stores the login data in local storage.
*/
comcat.login.storeCredentials = function (userName, passwd) {
    localStorage.setItem(comcat.login.USER_NAME, userName);
    localStorage.setItem(comcat.login.PASSWD, passwd);
};


/*
    Retrieves the login data from local storage.
*/
comcat.login.loadCredentials = function () {
    return {
        userName: localStorage.getItem(comcat.login.USER_NAME),
        passwd: localStorage.getItem(comcat.login.PASSWD)
    };
};


/*
    Removes the login data from local storage.
*/
comcat.login.clearCredentials = function () {
    return {
        userName: localStorage.removeItem(comcat.login.USER_NAME),
        passwd: localStorage.removeItem(comcat.login.PASSWD)
    };
};


/*
    Performs an autologin.
*/
comcat.login.autologin = function () {
    const credentials = comcat.login.loadCredentials();

    if (credentials.userName != null && credentials.passwd != null) {
        comcat.session.login(credentials.userName, credentials.passwd).then(
            function () {
                window.location = 'frontpage.html';
            },
            function () {
                window.location = 'index.html';
            }
        );
    } else {
        window.location = 'login.html';
    }
};
