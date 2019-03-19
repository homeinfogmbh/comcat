/*
    Console for debugging.
*/
var comcat = comcat || {};

comcat.toggleVisibility = function (element) {
    if (element.style.display === 'none') {
        element.style.display = 'block';
    } else {
        element.style.display = 'none';
    }
};

comcat.debugConsole = {
    /*
        Binds the debug console.
    */
    bind: function () {
        const debugConsole = document.getElementById('debugConsole');

        document.onkeydown = function (event) {
            switch(event.which) {
            case 73: // Lower case "i".
                comcat.toggleVisibility(debugConsole);
                break;
            default:
                return; // Exit this handler for other keys.
            }
            event.preventDefault(); // Prevent the default action (scroll / move caret).
        };
    },

    /*
        Prints text to the debug console.
    */
    log: function (text, newline = true) {
        const debugConsole = document.getElementById('debugConsole');
        debugConsole.innerHTML += text;

        if (newline) {
            debugConsole.innerHTML += '\n';
        }
    }
};
