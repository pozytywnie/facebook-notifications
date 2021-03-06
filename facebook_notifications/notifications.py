try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

import facepy


class FacebookNotificationsError(Exception):
    pass


class NotificationError(FacebookNotificationsError):
    pass


class SenderError(FacebookNotificationsError):
    def __init__(self, origin_exception):
        self.origin_exception = origin_exception
        return super(SenderError, self).__init__(origin_exception.message)


class Notification(object):
    def __init__(self, recipient, target, template):
        self.recipient = recipient
        self.target = target
        self.template = template

        self._clean_template()
        self._validate_if_recipient_is_not_empty()
        self._validate_if_target_is_relative_path()
        self._validate_template()

    def __repr__(self):
        arguments = 'recipient=%s, target=%s, template=%s' % (self.recipient,
                                                              self.target,
                                                              self.template)
        return "%s(%s)" % (type(self).__name__, arguments)

    def _clean_template(self):
        self.template = self.template.strip()

    def _validate_if_recipient_is_not_empty(self):
        if not self.recipient:
            raise NotificationError("Recipient could not be empty.")

    def _validate_if_target_is_relative_path(self):
        parsed_target = urlparse(self.target)
        if parsed_target.scheme or self.target.startswith('/'):
            raise NotificationError(
                "target is not valid relative path."
            )

    def _validate_template(self):
        self._validate_if_template_is_not_empty()
        self._validate_if_template_is_not_to_long()

    def _validate_if_template_is_not_empty(self):
        if not self.template:
            raise NotificationError("template should not be empty.")

    def _validate_if_template_is_not_to_long(self):
        # MAX_LENGHT is defined in Facebook docs:
        # https://developers.facebook.com/docs/app_notifications/
        MAX_LENGTH = 180
        if len(self.template) > MAX_LENGTH:
            raise NotificationError(
                "template is longer than %d characters" % MAX_LENGTH
            )


class NotificationSender(object):
    def __init__(self, graph_object_with_app_token):
        self.graph = graph_object_with_app_token

    def send(self, notification):
        try:
            self._try_to_send(notification)
        except facepy.FacepyError as e:
            code = getattr(e, 'code', None)
            low_priority_codes = self._low_priority_opengraph_errors().keys()
            if code not in low_priority_codes:
                raise SenderError(e)

    def _low_priority_opengraph_errors(self):
        return {
            1: 'An unknown error occurred',
            100: 'Invalid parameter / action not accepted',
            190: 'Invalid OAuth 2.0 Access Token',
            200: 'Permissions error'}

    def _try_to_send(self, notification):
        return self.graph.post(notification.recipient + '/notifications',
                               href=notification.target,
                               template=notification.template)
