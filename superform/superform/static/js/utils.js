// Source : https://www.grafikart.fr/tutoriels/javascript/debounce-throttle-642

function debounce(callback, delay) {
    var timer;
    return function () {
        var args = arguments;
        var context = this;
        clearTimeout(timer);
        timer = setTimeout(function () {
            callback.apply(context, args);
        }, delay)
    }
}