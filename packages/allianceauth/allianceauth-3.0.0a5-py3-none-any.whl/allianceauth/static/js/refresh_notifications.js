/* global notificationUPdateSettings */

/*
    This script refreshed the unread notification count in the top menu
    on a regular basis so to keep the user apprised about newly arrived
    notifications without having to reload the page.

    The refresh rate can be changes via the Django setting NOTIFICATIONS_REFRESH_TIME.
    See documentation for details.
*/
$(function () {
    'use strict';

    let notificationsListViewUrl = notificationUPdateSettings.notificationsListViewUrl;
    let notificationsRefreshTime = notificationUPdateSettings.notificationsRefreshTime;
    let userNotificationsCountViewUrl = notificationUPdateSettings.userNotificationsCountViewUrl;

    // update the notification unread count in the top menu
    let updateNotifications = function () {
        $.getJSON(userNotificationsCountViewUrl, function (data, status) {
            if (status === 'success') {
                let innerHtml = '';
                let unreadCount = data.unread_count;

                if (unreadCount > 0) {
                    innerHtml = (
                        `Notifications <span class="badge">${unreadCount}</span>`
                    );
                } else {
                    innerHtml = '<i class="far fa-bell"></i>';
                }

                $('#menu_item_notifications').html(
                    `<a href="${notificationsListViewUrl}">${innerHtml}</a>`
                );
            } else {
                console.error(
                    `Failed to load HTMl to render notifications item. Error: ${xhr.status}': '${xhr.statusText}`
                );
            }
        });
    };

    let myInterval;

    // activate automatic refreshing every x seconds
    let activateRefreshing = function () {
        if (notificationsRefreshTime > 0) {
            myInterval = setInterval(
                updateNotifications, notificationsRefreshTime * 1000
            );
        }
    };

    // deactivate automatic refreshing
    let deactivateRefreshing = function () {
        if ((notificationsRefreshTime > 0) && (typeof myInterval !== 'undefined')) {
            clearInterval(myInterval);
        }
    };

    // refreshing only happens on active browser tab
    $(document).on({
        'show': function () {
            activateRefreshing();
        },
        'hide': function () {
            deactivateRefreshing();
        }
    });

    // Initial start of refreshing on script loading
    activateRefreshing();
});
