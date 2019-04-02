/*
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 * KIND, either express or implied.  See the License for the
 * specific language governing permissions and limitations
 * under the License.
 */
var login = {
    // Application Constructor
    initialize: function() {
        document.addEventListener('deviceready', this.onDeviceReady.bind(this), false);
    },

    // Bind any cordova events here. Common events are:
    // 'pause', 'resume', etc.
    onDeviceReady: function() {
        document.getElementById('login').addEventListener('click', this.login.bind(this), false);
        document.getElementById('closeInvalidCredentials').addEventListener('click', this.closeInvalidCredentails.bind(this), false);
    },

    // Performs the login.
    login: function (event) {
        event.preventDefault();
        const userNameElement = document.getElementById('userName');
        const passwdElement = document.getElementById('password');
        const userName = userNameElement.value;
        const passwd = passwdElement.value;
        const storeCredentials = document.getElementById('storeCredentials').checked;
        comcat.session.login(userName, passwd).then(
            function () {
                if (storeCredentials) {
                    comcat.login.storeCredentials(userName, passwd);
                }

                window.location = 'frontpage.html';
            },
            function () {
                userNameElement.value = '';
                passwdElement.value = '';
                document.getElementById('invalidCredentialsModal').style.display = 'block';
            }
        );
    },

    // Closes the invalid Credentials dialog.
    closeInvalidCredentails: function (event) {
        event.preventDefault();
        document.getElementById('invalidCredentialsModal').style.display = 'none';
    }
};

login.initialize();
