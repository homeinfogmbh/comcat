/*
    Login management.
*/
var comcat = comcat || {};
comcat.login = comcat.login || {};


/*
    Stores the login data in local storage.
*/
comcat.login.storeCredentials = function (userName, passwd) {
    localStorage.setItem('comcat.userName', userName);
    localStorage.setItem('comcat.passwd', passwd);
};


/*
    Retrieves the login data from local storage.
*/
comcat.login.loadCredentials = function () {
    return {
        userName: localStorage.getItem('comcat.userName'),
        passwd: localStorage.getItem('comcat.passwd')
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
