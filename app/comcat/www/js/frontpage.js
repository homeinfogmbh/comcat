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
var frontpage = {
    // Application Constructor
    initialize: function() {
        document.addEventListener('deviceready', this.onDeviceReady.bind(this), false);
    },

    // deviceready Event Handler
    //
    // Bind any cordova events here. Common events are:
    // 'pause', 'resume', etc.
    onDeviceReady: function() {
        comcat.presentation.get().then(function (json) {
            const menuItems = json.menuItems;
            let pages = comcat.menu.pages(menuItems);
            pages = Array.from(pages);
            console.log('Pages:');
            console.log(JSON.stringify(pages, null, 2));
            const page = pages[0];
            const rows = comcat.menu.pageDOM(page);
            console.log('Rows:');
            console.log(JSON.stringify(rows, null, 2));
            const menu = document.getElementById('menu');

            for (let row of rows) {
                console.log('Row: ' + row + ' ' + typeof row);
                console.log(JSON.stringify(row));
                menu.appendChild(row);
            }
        });
    }
};

frontpage.initialize();
