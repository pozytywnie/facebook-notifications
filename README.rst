facebook-notifications
======================

Implements sending notifications to Facebook using Notifications API.

https://developers.facebook.com/docs/app_notifications/


Installation
------------

    $ pip install facebook-notifications


Usage
-----

    notification = notifications.Notification(recipient_id, target_url, message)

    token = facepy.get_application_access_token(settings.FACEBOOK_APP_ID,
                                                settings.FACEBOOK_APP_SECRET)
    graph = facepy.GraphAPI(token)

    sender = notifications.NotificationSender(graph)
    sender.send(notification)
