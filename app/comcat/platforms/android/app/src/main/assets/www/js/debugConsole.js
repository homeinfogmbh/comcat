/*
    Console for debugging.
*/

var debugConsole = {
    /*
        Binds the debug console.
    */
    bind: function () {
        $(document).keydown(function(event) {
            switch(event.which) {
            case 73: // Lower case "i".
                $('#debugConsole').toggle();
                break;
            default:
                return; // exit this handler for other keys
            }
            event.preventDefault(); // prevent the default action (scroll / move caret)
        });
    },

    /*
        Prints text to the debug console.
    */
    print: function (text, newline = true) {
        $('#debugConsole').append(text);

        if (newline) {
            $('#debugConsole').append('\n');
        }
    }
};
