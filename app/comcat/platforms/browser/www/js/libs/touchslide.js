/*
    Handling of sliding events.
*/
var comcat = comcat || {};
comcat.touchslide = comcat.touchslide || {};


comcat.touchslide.Position = class {
    constructor (x, y) {
        this.x = x;
        this.y = y;
    }

    toString () {
        return this.x + 'x' + this.y;
    }
};


comcat.touchslide.SlideDelta = class extends comcat.touchslide.Position {
    get absX () {
        return Math.abs(this.x);
    }

    get absY () {
        return Math.abs(this.y);
    }

    get maxAbs () {
        return Math.max(this.absX, this.absY);
    }

    get moveX () {
        return this.absX >= this.absY;
    }

    get moveY () {
        return this.absY >= this.absX;
    }
};


comcat.touchslide.SlideHandler = class {
    constructor (onStart, onEnd) {
        this.onStart = onStart;
        this.onEnd = onEnd;
        this.startPosition = null;
        this.delta = null;
    }

    start (event) {
        const touchEvent = event.touches[0];
        this.startPosition = new comcat.touchslide.Position(touchEvent.pageX, touchEvent.pageY);
        return this.onStart(this.startPosition);
    }

    move (event) {
        if (event.touches.length > 1 || event.scale && event.scale !== 1) {
            return;
        }

        const touch = event.touches[0];
        const deltaX = touch.pageX - this.startPosition.x;
        const deltaY = touch.pageY - this.startPosition.y;
        this.delta = new comcat.touchslide.SlideDelta(deltaX, deltaY);
    }

    end (event) {
        return this.onEnd(this.delta);
    }

    bind (element) {
        element.addEventListener('touchstart', this.start.bind(this), false);
        element.addEventListener('touchmove', this.move.bind(this), false);
        element.addEventListener('touchend', this.end.bind(this), false);
    }
};
