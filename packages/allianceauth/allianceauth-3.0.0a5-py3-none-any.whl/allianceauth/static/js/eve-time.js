$(document).ready(function () {
    'use strict';

    /**
     * render a JS clock for Eve Time
     * @param element
     */
    const renderClock = function (element) {
        const datetimeNow = new Date();
        const h = String(datetimeNow.getUTCHours()).padStart(2, '0');
        const m = String(datetimeNow.getUTCMinutes()).padStart(2, '0');

        element.html(h + ':' + m);
    };

    // Start the Eve time clock in the top menu bar
    setInterval(function () {
        renderClock($('.eve-time-wrapper .eve-time-clock'));
    }, 500);
});
