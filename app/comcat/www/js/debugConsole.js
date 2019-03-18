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
        const console = document.getElementById('debugConsole');

        function logEvent (event) {
            switch(event.which) {
            case 73: // Lower case "i".
                comcat.toggleVisibility(console);
                break;
            default:
                return; // Exit this handler for other keys.
            }
            event.preventDefault(); // Prevent the default action (scroll / move caret).
        }

        const input = document.querySelector('input');
        input.addEventListener('keydown', logEvent);
    },

    /*
        Prints text to the debug console.
    */
    print: function (text, newline = true) {
        const console = document.getElementById('debugConsole');
        console.innerHTML += text;

        if (newline) {
            console.innerHTML += '\n';
        }
    }
};
